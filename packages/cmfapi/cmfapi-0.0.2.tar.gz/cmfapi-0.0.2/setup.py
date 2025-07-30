from setuptools import setup, find_packages

setup(
    name="cmfapi",
    version="0.0.2",
    description="A client library for interacting with the CMF API",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="Aalap Tripathy",
    author_email="atripathy.bulk@gmail.com",
    url="https://github.com/atripathy86/cmfapi",
    packages=find_packages(),
    install_requires=[
        "requests",
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)