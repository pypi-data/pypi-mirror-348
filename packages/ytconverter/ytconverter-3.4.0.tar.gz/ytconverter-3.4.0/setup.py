from setuptools import setup, find_packages

setup(
    name="ytconverter",  # required
    version="3.4.0",     # required
    author="KAIF_CODEC",
    author_email="kaifcodec@gmail.com",
    description="A tool for converting YouTube videos into various formats.",
    long_description=open("README.md", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/kaifcodec/ytconverter",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "requests",
        "yt-dlp",
        "fontstyle",
        "colored",
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
    entry_points={
        "console_scripts": [
            "ytconverter=ytconverter.core:main"
        ]
    }
)
