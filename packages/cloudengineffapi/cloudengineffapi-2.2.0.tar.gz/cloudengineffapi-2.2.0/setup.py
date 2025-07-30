from setuptools import setup, find_packages

setup(
    name="cloudengineffapi",
    version="2.2.0",  # Updated version for the advanced SDK
    packages=find_packages(),
    install_requires=["requests>=2.25.1"],
    description="Advanced Client for CloudEngineFF APIs with distributed rate limiting",
    author="BIJOY",  # Replace with your name
    author_email="hackf1283@gmail.com",  # Optional, replace as needed
    url="https://github.com/ashikurggd/cloudengineffapi",  # Optional, replace as needed
    python_requires=">=3.6",
    long_description="An advanced Python SDK for interacting with CloudEngineFF APIs, featuring distributed rate limiting across a pool of API keys.",
    long_description_content_type="text/plain",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",  # Adjust license as needed
        "Operating System :: OS Independent",
    ],
)