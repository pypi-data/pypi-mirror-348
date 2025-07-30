from setuptools import setup, find_packages

setup(
    name="spec2chat",
    version="0.1.5",
    author="María Jesús Rodríguez Sánchez",
    author_email="mjesusrodriguez@ugr.es",
    description="A Python library for generating task-oriented dialogue systems from service specifications (PPTalk).",
    long_description=open("README.md", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/mjesusrodriguez/spec2chat",  # Replace with your real GitHub URL
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "openai>=0.27.0",
        "pymongo>=4.0.0,<5.0.0",
        "spacy==3.7.2",
        "nltk>=3.7",
        "python-dotenv>=0.21.0",
        "dnspython",
        "setuptools>=65.0.0"
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
        "License :: OSI Approved :: Apache Software License",
        "Intended Audience :: Developers",
        "Topic :: Scientific/Engineering :: Artificial Intelligence"
    ],
    license="Apache-2.0",
    python_requires='>=3.8',
)