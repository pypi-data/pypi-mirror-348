from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="ufm-config-diff",
    version="0.1.0",
    author="Ariel Weiser ",
    author_email="arielwe@nvidia.com",
    description="A tool to compare UFM configurations between two servers",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/ufm-config-diff",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
    install_requires=[
        "paramiko",
        "beautifulsoup4",
    ],
    entry_points={
        "console_scripts": [
            "ufm-config-diff=ufm_config_diff.config_diff:main",
        ],
    },
) 