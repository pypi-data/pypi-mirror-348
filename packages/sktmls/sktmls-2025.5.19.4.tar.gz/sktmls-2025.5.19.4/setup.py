import setuptools


def load_long_description():
    with open("README.md", "r") as f:
        long_description = f.read()
    return long_description


def get_version():
    with open("sktmls/__init__.py", "r") as f:
        for line in f.readlines():
            if line.startswith("__version__"):
                return line.split('"')[1]
        else:
            raise TypeError("NO SKTMLS_VERSION")


setuptools.setup(
    name="sktmls",
    version=get_version(),
    author="SKTMLS",
    author_email="mls@sktai.io",
    description="MLS SDK",
    long_description=load_long_description(),
    long_description_content_type="text/markdown",
    url="https://github.com/sktaiflow/mls-sdk",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
    install_requires=[
        "aiohttp[speedups]",
        "autogluon.tabular",
        "boto3",
        "catboost",
        "haversine",
        "joblib",
        "lightgbm",
        "numpy",
        "pandas",
        "pytz",
        "requests",
        "scikit-learn",
        "simplejson",
        "torch",
        "xgboost",
        "ipyparallel",
    ],
)
