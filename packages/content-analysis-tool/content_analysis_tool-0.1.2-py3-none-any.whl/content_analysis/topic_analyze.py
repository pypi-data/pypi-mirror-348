from collections import Counter
import pickle
import re
import statistics
import time
import copy
from importlib.resources import files as pkg_files
import content_analysis.data as data_dir
load_start = time.time()
VERSION = "1.2.0"


# Thay thế các đoạn đọc tệp
data_path = pkg_files(data_dir)
with open(data_path / "branded_hashtag.pickle", "rb") as f:
    BRAND_NAME_MAPPING = pickle.load(f)

with open(data_path / "topic_hashtag.pickle", "rb") as f:
    TOPICS_HASHTAGS_SOCIAL = pickle.load(f)

with open(data_path / "bio2topic.pickle", "rb") as f:
    BIO_TOPIC_KEYWORD = pickle.load(f)

with open(data_path / "product_type2topic.pickle", "rb") as f:
    PRODUCT_TYPE_TO_TOPIC = pickle.load(f)

with open(data_path / "kwtree_brandname.pickle", "rb") as f:
    KWTREE_BRANDNAME = pickle.load(f)

with open(data_path / "kwtree_product.pickle", "rb") as f:
    KWTREE_PRODUCT = pickle.load(f)

BRANDNAME_TO_TOPIC = dict()

KID_KEYWORDS = """cho trẻ mẫu giáo
cho các bé
cho trẻ nhỏ
cho em bé
cho bé
cho trẻ
cho trẻ nhỏ mới sinh
cho bé sơ sinh
cho trẻ sơ sinh
cho sơ sinh
bé sơ sinh
bé trai
bé gái
sơ sinh
trẻ sơ sinh
mẹ và bé
em bé""".split(
    "\n"
)


for hashtag, brand_name in BRAND_NAME_MAPPING.items():
    for topic in TOPICS_HASHTAGS_SOCIAL.keys():
        if hashtag in TOPICS_HASHTAGS_SOCIAL[topic] and len(brand_name) > 4:
            BRANDNAME_TO_TOPIC[brand_name] = topic


class TopicAnalysis:

    @staticmethod
    def merge(x, y):
        return list(set(list(x) + list(y)))

    @classmethod
    def basic_content_analysis(cls, content, *args, **kwargs):
        """
        input:
            content: string
            is_use_hashtag_extra: bool (default: False)
        output:
            topic: set of string
            brands: set of string
            topic_hashtags: dict(hashtag, topic)
            branded_hashtags: dict(hashtag, brand_name)
            branded_hashtags_extra: dict(hashtag, brand_name)
            topic_hashtags_extra: dict(hashtag, topic)
        """
        topic, topic_hashtags = cls.detect_topic_by_hashtags(str(content))
        brands, branded_hashtags, not_found_hashtags = cls.detect_brand_name(
            str(content), BRAND_NAME_MAPPING
        )

        content_analysis = {
            "topic": list(topic),
            "brands": list(brands),
            "topic_hashtags": topic_hashtags,
            "branded_hashtags": branded_hashtags,
            "content_analysis_version": VERSION,
        }

        return content_analysis

    @classmethod
    def basic_categorize(
        cls, topics, count_branded_topic, bio_topics, med_metric, total_post
    ):
        """
        input:
            contents: list of string
            views: list of float
            country_code: string ['vi', 'my', 'id', 'sg', 'ph', 'th']
            social_network: string
            count_branded_topic: dict mapping topic --> count num branded topic posts
                Ex: "beauty": 10 --> 10 posts chứa branded hashtag hoặc brand keyword về beauty
            bio_topics: list bio topic
        output:
            main_categories: list of string
            ranking_point: list of float
        """

        if med_metric is list:
            med_metric = statistics.median(med_metric)
        if med_metric is None:
            med_metric = 0

        count_topics = {}
        for topic in topics:
            if topic == "others":
                continue
            count_topics[topic] = count_topics.get(topic, 0) + 1

        categories = []
        for topic, count in count_topics.items():
            count_branded = (
                count_branded_topic[topic] if topic in count_branded_topic else 0
            )
            percent = ContentAnalysis.calculate_ratio(
                total=total_post, quantity=count * 100, round_up=2
            )
            percent_branded = ContentAnalysis.calculate_ratio(
                total=total_post, quantity=count_branded * 100, round_up=2
            )
            have_bio_topic = topic in bio_topics
            category = {
                "name": topic,
                "count": count,
                "count_branded": count_branded,
                "percent": percent,
                "percent_branded": percent_branded,
                "ranking_point": ContentAnalysis.calculate_ratio(
                    total=total_post,
                    quantity=percent * med_metric * (1 + percent_branded)
                    + 10e9 * have_bio_topic,
                    round_up=2,
                ),
            }
            categories.append(category)
        categories = sorted(categories, key=lambda x: x["percent"], reverse=True)

        main_categories = list(filter(lambda x: x["percent"] >= 50, categories))
        main_category = None
        if len(main_categories) == 1:
            main_category = main_categories[0]["name"]

        return categories, main_category

    @staticmethod
    def calculate_ratio(quantity, total, round_up=4):
        if total is None or total == 0:
            return 0

        return round(quantity / total, round_up)

    @staticmethod
    def hashtag_detect(content):
        punctation = """[,./?;:'"|\\!-$%^&*@]="""
        hashtags = [x.lower() for x in re.findall(r"#\S+", content)]
        hashtags = [x[1:] for x in hashtags]
        result = []
        for hashtag in hashtags:
            if "#" in hashtag:
                for h in hashtag.split("#"):
                    if len(h) > 0:
                        result.append(h)
            else:
                result.append(hashtag)
        hashtags = []
        for hashtag in result:
            hashtag_ = hashtag
            for p in punctation:
                if p in hashtag_:
                    hashtag_ = hashtag_.split(p)[0]
            if len(hashtag_) > 0:
                hashtags.append(hashtag_)
        return hashtags

    @staticmethod
    def check_brand_name(x, topic_final):
        topics = set()
        brand_names = set()
        result_brandnames = list(KWTREE_BRANDNAME.search_all(x))
        for brand_name in result_brandnames:
            if brand_name[0] in BRANDNAME_TO_TOPIC:
                topic = BRANDNAME_TO_TOPIC[brand_name[0]]

                topics.add(topic)
                brand_names.add(brand_name[0])

                if not topic_final.get(topic, {}).get("brands"):
                    topic_final[topic] = {"brands": set()}
                topic_final[topic]["brands"].add(brand_name[0])

        if len(topics) == 0:
            return [], []
        return list(brand_names), list(topics)

    @staticmethod
    def check_product(x, topic_final):
        topics = set()
        product_categories = set()
        x = x.lower()

        result_products = list(KWTREE_PRODUCT.search_all(x))
        result_products_ = set(result_products)
        for product in result_products:
            for product_ in result_products:
                if product in result_products_:
                    if (
                        product[0] != product_[0]
                        and product[0] in product_[0]
                        and product_[1] == product[1]
                    ):
                        result_products_.remove(product)

        is_family_kids = False
        for kid_keyword in KID_KEYWORDS:
            if kid_keyword in x:
                is_family_kids = True
                break

        for product in list(result_products_):
            if " " in product[0]:
                topic = PRODUCT_TYPE_TO_TOPIC[product[0]]
                topics.add(topic)
                if is_family_kids:
                    topics.add("family_kids")
                product_categories.add(product[0])

                if not topic_final.get(topic, {}).get("products"):
                    topic_final[topic] = {"products": set()}
                topic_final[topic]["products"].add(product[0])
                if not topic_final.get("family_kids", {}).get("products"):
                    topic_final["family_kids"] = {"products": set()}
                topic_final["family_kids"]["products"].add(product[0])

            else:
                if (
                    product[1] - 1 < 0
                    or x[product[1] - 1] in [" ", "\n", ",", ";", "-"]
                ) and (
                    product[1] + len(product[0]) >= len(x)
                    or x[product[1] + len(product[0])]
                    in [" ", "\n", ",", ";", ".", "?", "-"]
                ):  # noqa: E501
                    topic = PRODUCT_TYPE_TO_TOPIC[product[0]]
                    topics.add(topic)
                    if is_family_kids:
                        topics.add("family_kids")
                    product_categories.add(product[0])

                    if not topic_final.get(topic, {}).get("products"):
                        topic_final[topic] = {"products": set()}
                    topic_final[topic]["products"].add(product[0])
                    if not topic_final.get("family_kids", {}).get("products"):
                        topic_final["family_kids"] = {"products": set()}
                    topic_final["family_kids"]["products"].add(product[0])

        return list(product_categories), list(topics)

    @classmethod
    def detect_topic_by_hashtag(
        cls,
        text,
        topics_hashtags_all=TOPICS_HASHTAGS_SOCIAL,
        brand_name_mapping=BRAND_NAME_MAPPING,
    ):
        topics_hashtags = topics_hashtags_all

        hashtags = cls.hashtag_detect(str(text))
        topics = set()
        brand_topics = set()
        for hashtag in hashtags:
            for topic in topics_hashtags.keys():
                if hashtag in topics_hashtags[topic]:
                    if hashtag in brand_name_mapping:
                        brand_topics.add(topic)

                    else:
                        topics.add(topic)
        return list(topics), list(brand_topics)

    @classmethod
    def detect_brand_name(cls, text, brand_name_mapping=BRAND_NAME_MAPPING):
        brand_name_mapping = brand_name_mapping  # [country_code]

        hashtags = cls.hashtag_detect(str(text))
        brands = set()
        for hashtag in hashtags:
            if (
                hashtag in brand_name_mapping.keys()
                and brand_name_mapping[hashtag] is not None
            ):
                brands.add(brand_name_mapping[hashtag])
        return list(brands)

    @classmethod
    def detect_hashtag_topic(cls, content):
        topic_hashtags, topic_brands = cls.detect_topic_by_hashtag(str(content))
        brand_names = cls.detect_brand_name(str(content), BRAND_NAME_MAPPING)
        return topic_hashtags, brand_names, topic_brands

    @classmethod
    def detect_content_topic(cls, content, topic_final={}):
        brand_names, topic_brands = cls.check_brand_name(content, topic_final)
        product_categories, topic_products = cls.check_product(content, topic_final)
        return brand_names, topic_brands, product_categories, topic_products

    @classmethod
    def detect_live_event_topic(cls, content):
        live_topics = {}
        brand_names, topic_brands, product_categories, topic_products = (
            cls.detect_content_topic(content)
        )
        topics = topic_brands + topic_products
        for topic in topics:
            cls.add_topic(topic, live_topics, brand_names, product_categories)
        return live_topics

    @classmethod
    def detect_topic_by_hashtags(cls, text, topics_hashtags=TOPICS_HASHTAGS_SOCIAL):
        # OLD
        hashtags = set(cls.hashtag_detect(str(text)))
        topics = set()
        topic_hashtags = {}
        for hashtag in hashtags:
            topic_target = None
            for topic in topics_hashtags.keys():
                if hashtag in topics_hashtags[topic]:
                    topic_target = topic
                    break
            if topic_target is not None:
                topics.add(topic_target)
                topic_hashtags[hashtag] = topic_target
        return topics, topic_hashtags

    # @classmethod
    # def detect_brand_name(cls, text, brand_name_mapping=BRAND_NAME_MAPPING):

    #     hashtags = cls.hashtag_detect(str(text))
    #     brands = set()
    #     branded_hashtags = {}
    #     not_found_hashtags = set()
    #     for hashtag in hashtags:
    #         if brand_name_mapping.get(hashtag) is not None:
    #             brands.add(brand_name_mapping[hashtag])
    #             branded_hashtags[hashtag] = brand_name_mapping[hashtag]
    #         else:
    #             not_found_hashtags.add(hashtag)

    #     return brands

    @staticmethod
    def _get_user_brand_names(post_data):
        list_brands = []
        for post in post_data:
            list_brands += post.get("brands", [])
        if not list_brands:
            return []
        brand_counter = Counter(list_brands)
        brand_names = [
            {"name": brand, "count": count} for brand, count in brand_counter.items()
        ]
        brand_names = sorted(brand_names, key=lambda i: i.get("count", 0), reverse=True)
        return brand_names

    @staticmethod
    def detect_bio_topic(bio, country_code):
        # https://docs.google.com/spreadsheets/d/1-BZdEe5yq30f8pKA7PSAOZOI81OTpHX1GgbhnfvTe5M/edit#gid=2065748147
        bio_topic = set()
        for keyword in BIO_TOPIC_KEYWORD["all"].keys():
            if keyword.lower() in bio.lower():
                bio_topic.add(BIO_TOPIC_KEYWORD["all"][keyword])

        if country_code in BIO_TOPIC_KEYWORD:
            for keyword in BIO_TOPIC_KEYWORD[country_code].keys():
                if keyword.lower() in bio.lower():
                    bio_topic.add(BIO_TOPIC_KEYWORD[country_code][keyword])
        return list(bio_topic)

    @staticmethod
    def add_topic(topic, post_topics, brand_names, product_categories):
        if not post_topics.get(topic):
            post_topics[topic] = {"brands": set(), "products": set()}
        for brand_name in brand_names:
            if (
                brand_name not in BRANDNAME_TO_TOPIC
                or BRANDNAME_TO_TOPIC[brand_name] == topic
            ):
                post_topics[topic]["brands"].add(brand_name)
        for product_cate in product_categories:
            if (
                product_cate not in PRODUCT_TYPE_TO_TOPIC
                or PRODUCT_TYPE_TO_TOPIC[product_cate] == topic
            ):
                post_topics[topic]["products"].add(product_cate)

    @classmethod
    def detect_post_topic_from_content_and_product_list(
        cls, content, product_name, bio_topics, topic_final=None, topic_dict=None
    ):
        """
        * input:
            - user_id
            - post_id
            - bio_topics
            - content
            - product_list
            - image_link

        * output:
                - is_crawl_transcript: bool
                - post_topics: list topics
                - post_brand_names: list brand_names
                - post_product_categories: list product category
        """
        if topic_final is None:
            topic_final = {}
        if topic_dict is None:
            topic_dict = {}

        post_topics = topic_dict.get("post_topics") or {}

        # detect topic_content & brand_name_content
        (
            brand_name_content,
            topic_brand_content,
            product_categories_content,
            topic_product_content,
        ) = cls.detect_content_topic(content, topic_final)
        topic_hashtag, brand_name_hashtag, topic_brand_hashtag = (
            cls.detect_hashtag_topic(content)
        )
        topic_content = topic_hashtag
        topic_brand_content = cls.merge(topic_brand_content, topic_brand_hashtag)
        brand_name_content = cls.merge(brand_name_content, brand_name_hashtag)

        (
            brand_name_product_list,
            topic_brand_product_list,
            product_categories_product_list,
            topic_product_product_list,
        ) = cls.detect_content_topic(product_name, topic_final)

        brand_names = brand_name_content + brand_name_product_list
        product_categories = (
            product_categories_content + product_categories_product_list
        )

        topic_dict = {
            "post_topics": post_topics,
            "topic_final": topic_final,
            "topic_content": topic_content,
            "topic_brand_content": topic_brand_content,
            "topic_product_content": topic_product_content,
            "topic_brand_product_list": topic_brand_product_list,
            "topic_product_product_list": topic_product_product_list,
            "brand_name_content": brand_name_content,
            "brand_name_product_list": brand_name_product_list,
            "product_categories_content": product_categories_content,
            "product_categories_product_list": product_categories_product_list,
        }

        num_existed_term = 0
        num_existed_term = sum(
            map(
                bool,
                [
                    topic_content,
                    topic_brand_content,
                    topic_product_content,
                    topic_brand_product_list,
                    topic_product_product_list,
                ],
            )
        )

        if (
            num_existed_term == 0
        ):  # không detect được topic --> không crawl transcript, không có topic
            return False, topic_dict

        if num_existed_term == 1:  # chỉ detect được 1 term có topics
            topics = list(
                set(
                    topic_content
                    + topic_brand_content
                    + topic_product_content
                    + topic_brand_product_list
                    + topic_product_product_list
                )
            )

            if (
                len(topics) == 1
            ):  # chỉ detect được 1 topic trong term --> crawl transcript, trả về topic
                topic = topics[0]
                cls.add_topic(topic, post_topics, brand_names, product_categories)
                return True, topic_dict

            num_post_topic = 0
            for topic in topics:
                if topic in topics and topic in bio_topics:
                    num_post_topic += 1
                    cls.add_topic(topic, post_topics, brand_names, product_categories)
            if (
                num_post_topic == 1
            ):  # chỉ có 1 post topic -->  crawl transcript, trả về topic
                return True, topic_dict
            else:  # nhiều post topic --> không crawl transcript, trả về topic
                return False, topic_dict

        topics = list(
            set(
                topic_content
                + topic_brand_content
                + topic_product_content
                + topic_brand_product_list
                + topic_product_product_list
            )
        )

        num_post_topic = 0
        for topic in topics:  # nhiều term
            count = sum(
                map(
                    lambda x: int(topic in x),
                    [
                        topic_content,
                        topic_brand_content,
                        topic_product_content,
                        topic_brand_product_list,
                        topic_product_product_list,
                    ],
                )
            )

            if count / num_existed_term > 0.5:
                num_post_topic += 1
                cls.add_topic(topic, post_topics, brand_names, product_categories)

            elif count / num_existed_term == 0.5 and topic in bio_topics:
                num_post_topic += 1
                cls.add_topic(topic, post_topics, brand_names, product_categories)

        if (
            num_post_topic == 1
        ):  # chỉ có 1 post topic -->  crawl transcript, trả về topic
            return True, topic_dict
        else:  # nhiều post topic --> không crawl transcript, trả về topic
            return False, topic_dict

    @classmethod
    def detect_post_topic_from_transcript(
        cls, content, product_content, transcript, bio_topics, topic_dict=None
    ):
        """
        Detects the topic, brand names, and product categories of a post from its transcript.

        Args:
            content (str): The content of the post.
            product_list (List[str]): A list of product names.
            transcript (str): The transcript of the post.
            bio_topics (List[str]): A list of topics related to the user's bio.
            topic_dict (Optional[Dict[str, Any]]): A dictionary containing precomputed topic-related information.
                Defaults to None.

        Returns:
            Tuple[bool, List[str], List[str], List[str], Dict[str, Any]]: A tuple containing the following:
                - A boolean indicating whether the post has any relevant topics.
                - A list of topics related to the post.
                - A list of brand names related to the post.
                - A list of product categories related to the post.
                - A dictionary containing the following precomputed topic-related information:
                    - 'topic_content': A list of topics related to the post content.
                    - 'topic_brand_content': A list of topics related to the post brand names.
                    - 'topic_product_content': A list of topics related to the post product categories.
                    - 'topic_brand_product_list': A list of topics related to the post brand names and product names.
                    - 'topic_product_product_list': A list of topics related to the post product names.
                    - 'topic_brand_transcript': A list of topics related to the post brand names in the transcript.
        """
        if topic_dict is None:
            topic_dict = {}

        post_topics = topic_dict.get("post_topics") or {}

        topic_final = topic_dict.get("topic_final") or {}
        topic_content = topic_dict.get("topic_content")
        topic_brand_content = topic_dict.get("topic_brand_content")
        topic_product_content = topic_dict.get("topic_product_content")
        topic_brand_product_list = topic_dict.get("topic_brand_product_list")
        topic_product_product_list = topic_dict.get("topic_product_product_list")
        brand_name_content = topic_dict.get("brand_name_content")
        brand_name_product_list = topic_dict.get("brand_name_product_list")
        product_categories_content = topic_dict.get("product_categories_content")
        product_categories_product_list = topic_dict.get(
            "product_categories_product_list"
        )

        if any(
            map(
                lambda x: x is None,
                [
                    topic_content,
                    topic_brand_content,
                    topic_product_content,
                    topic_brand_product_list,
                    topic_product_product_list,
                ],
            )
        ):

            # detect topic_content & brand_name_content
            (
                brand_name_content,
                topic_brand_content,
                product_categories_content,
                topic_product_content,
            ) = cls.detect_content_topic(content, topic_final)
            topic_hashtag, brand_name_hashtag, topic_brand_hashtag = (
                cls.detect_hashtag_topic(content)
            )
            topic_content = topic_hashtag
            topic_brand_content = cls.merge(topic_brand_content, topic_brand_hashtag)
            brand_name_content = cls.merge(brand_name_content, brand_name_hashtag)

            (
                brand_name_product_list,
                topic_brand_product_list,
                product_categories_product_list,
                topic_product_product_list,
            ) = cls.detect_content_topic(product_content, topic_final)

        (
            brand_name_transcript,
            topic_brand_transcript,
            product_categories_transcript,
            topic_product_transcript,
        ) = cls.detect_content_topic(transcript, topic_final)

        # num_existed_term = 0
        # num_existed_term = sum(map(bool, [topic_content, topic_brand_content,
        #                                   topic_product_content, topic_brand_product_list,
        #                                   topic_product_product_list, topic_brand_transcript,
        #                                   topic_product_transcript]))

        brand_names = (
            brand_name_content + brand_name_product_list + brand_name_transcript
        )
        product_categories = (
            product_categories_content
            + product_categories_product_list
            + product_categories_transcript
        )

        topic_dict = {
            "post_topics": post_topics,
            "topic_final": topic_final,
            "topic_content": topic_content,
            "topic_brand_content": topic_brand_content,
            "topic_product_content": topic_product_content,
            "topic_brand_product_list": topic_brand_product_list,
            "topic_product_product_list": topic_product_product_list,
            "brand_name_content": brand_name_content,
            "brand_name_product_list": brand_name_product_list,
            "product_categories_content": product_categories_content,
            "product_categories_product_list": product_categories_product_list,
            "topic_brand_transcript": topic_brand_transcript,
            "brand_name_transcript": brand_name_transcript,
            "topic_product_transcript": topic_product_transcript,
            "product_categories_transcript": product_categories_transcript,
        }

        # topics = list(set(topic_content + topic_brand_content + topic_product_content + topic_brand_product_list +
        #                       topic_product_product_list + topic_brand_transcript + topic_product_transcript))
        post_topics_ = copy.deepcopy(post_topics)
        for topic in post_topics_:
            cls.add_topic(topic, post_topics, brand_names, product_categories)
        return False, topic_dict

    @classmethod
    def detect_post_topic_from_image(
        cls,
        content,
        product_content,
        transcript,
        bio_topics,
        topic_image,
        topic_dict=None,
    ):
        """
        input:
            user_id
            post_id
            bio_topics
            content
            product_list
            transcript
            image_link

        output:
            post_topics, post_brand_names, post_product_categories:
                - post_topics: list topics
                - post_brand_names: list brand_names
                - post_product_categories: list product category
        """
        post_topics = set()

        if topic_dict is None:
            topic_dict = {}

        post_topics = topic_dict.get("post_topics") or {}

        topic_final = topic_dict.get("topic_final") or {}
        topic_content = topic_dict.get("topic_content")
        topic_brand_content = topic_dict.get("topic_brand_content")
        topic_product_content = topic_dict.get("topic_product_content")
        topic_brand_product_list = topic_dict.get("topic_brand_product_list")
        topic_product_product_list = topic_dict.get("topic_product_product_list")
        topic_brand_transcript = topic_dict.get("topic_brand_transcript")
        topic_product_transcript = topic_dict.get("topic_product_transcript")
        brand_name_content = topic_dict.get("brand_name_content")
        brand_name_product_list = topic_dict.get("brand_name_product_list")
        brand_name_transcript = topic_dict.get("brand_name_transcript")
        product_categories_content = topic_dict.get("product_categories_content")
        product_categories_product_list = topic_dict.get(
            "product_categories_product_list"
        )
        product_categories_transcript = topic_dict.get("product_categories_transcript")

        if any(
            map(
                lambda x: x is None,
                [
                    topic_content,
                    topic_brand_content,
                    topic_product_content,
                    topic_brand_product_list,
                    topic_product_product_list,
                    topic_brand_transcript,
                    topic_product_transcript,
                ],
            )
        ):

            # detect topic_content & brand_name_content
            (
                brand_name_content,
                topic_brand_content,
                product_categories_content,
                topic_product_content,
            ) = cls.detect_content_topic(content, topic_final)
            topic_hashtag, brand_name_hashtag, topic_brand_hashtag = (
                cls.detect_hashtag_topic(content)
            )
            topic_content = topic_hashtag
            topic_brand_content = cls.merge(topic_brand_content, topic_brand_hashtag)
            brand_name_content = cls.merge(brand_name_content, brand_name_hashtag)

            (
                brand_name_product_list,
                topic_brand_product_list,
                product_categories_product_list,
                topic_product_product_list,
            ) = cls.detect_content_topic(product_content, topic_final)

            (
                brand_name_transcript,
                topic_brand_transcript,
                product_categories_transcript,
                topic_product_transcript,
            ) = cls.detect_content_topic(transcript, topic_final)

        brand_names = (
            brand_name_content + brand_name_product_list + brand_name_transcript
        )
        product_categories = (
            product_categories_content
            + product_categories_product_list
            + product_categories_transcript
        )

        num_existed_term = 0
        num_existed_term = sum(
            map(
                bool,
                [
                    topic_content,
                    topic_brand_content,
                    topic_product_content,
                    topic_brand_product_list,
                    topic_product_product_list,
                    topic_brand_transcript,
                    topic_product_transcript,
                    topic_image,
                ],
            )
        )

        topic_dict = {"topic_image": topic_image}

        if num_existed_term == 0:
            return [], [], []

        if num_existed_term == 1:
            if len(topic_image) > 0:
                return topic_image, [], []

            else:
                topics = list(
                    set(
                        topic_content
                        + topic_brand_content
                        + topic_product_content
                        + topic_brand_product_list
                        + topic_product_product_list
                        + topic_brand_transcript
                        + topic_product_transcript
                    )
                )
                if len(topics) > 1:
                    return [], [], []
                topic = topics[0]
                cls.add_topic(topic, post_topics, brand_names, product_categories)
                return topic_dict

        topics = list(
            set(
                topic_content
                + topic_brand_content
                + topic_product_content
                + topic_brand_product_list
                + topic_product_product_list
                + topic_brand_transcript
                + topic_product_transcript
                + topic_image
            )
        )
        for topic in topics:
            count = sum(
                map(
                    lambda x: int(topic in x),
                    [
                        topic_content,
                        topic_brand_content,
                        topic_product_content,
                        topic_brand_product_list,
                        topic_product_product_list,
                        topic_brand_transcript,
                        topic_product_transcript,
                        topic_image,
                    ],
                )
            )

            if count / num_existed_term > 0.5:
                cls.add_topic(topic, post_topics, brand_names, product_categories)

            elif count / num_existed_term == 0.5:
                if topic in bio_topics and topic in topic_image:
                    cls.add_topic(topic, post_topics, brand_names, product_categories)

        return topic_dict
