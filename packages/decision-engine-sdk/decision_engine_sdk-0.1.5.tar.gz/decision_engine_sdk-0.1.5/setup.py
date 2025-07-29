from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="decision_engine_sdk",
    version="0.1.5",
    author="Your Name",
    author_email="your.email@example.com",
    description="A Python SDK for interacting with the Decision Engine REST APIs",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/decision_engine_sdk",  # Replace with your GitHub repository URL
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    install_requires=[
        "requests",
    ],
)
