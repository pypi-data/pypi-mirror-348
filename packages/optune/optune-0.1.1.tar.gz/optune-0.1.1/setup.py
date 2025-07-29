from setuptools import setup, find_packages

setup(
    name="optune",
    version="0.1.1",
    packages=find_packages() + find_packages(where="src"),
    package_dir={"": "src", "examples": "examples"},
    install_requires=[
        "requests",
        "openai",
        "pydantic",
    ],
    extras_require={
        "dev": [
            "pytest",
            "pandas",
        ],
    },
    author="optune.ai team",
    author_email="support@optune.ai",
    description="optune.ai python sdk",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://optune.ai/",
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
)
