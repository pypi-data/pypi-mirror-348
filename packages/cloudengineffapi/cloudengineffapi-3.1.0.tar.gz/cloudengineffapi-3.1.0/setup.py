from setuptools import setup, find_packages

setup(
    name="cloudengineffapi",
    version="3.1.0",
    packages=find_packages(),
    install_requires=["requests>=2.28.0"],
    description="Advanced SDK for CloudEngineFF APIs with thread-safe rate limiting",
    author="Bijoy",
    author_email="hackf1283@gmail.com",  # Replace with your email
    python_requires=">=3.6",
    long_description="An advanced Python SDK for interacting with CloudEngineFF APIs, featuring thread-safe rate limiting, internal API key management, and efficient request handling.",
    long_description_content_type="text/plain",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)