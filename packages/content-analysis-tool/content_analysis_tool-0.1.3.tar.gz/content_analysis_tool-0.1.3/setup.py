from setuptools import setup, find_packages

setup(
    name="content-analysis-tool",
    version="0.1.3",
    packages=find_packages(),
    package_data={"content_analysis": ["data/*.pickle"]},
    install_requires=[
        "ahocorapy",
        "regex",
        "statistics",
        "pathlib",
    ],
    author="DongHoang",
    author_email="hvdong1990@gmail.com",
    description="Phân tích nội dung và nhận diện thương hiệu, chủ đề",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/username/content-analysis-tool",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
