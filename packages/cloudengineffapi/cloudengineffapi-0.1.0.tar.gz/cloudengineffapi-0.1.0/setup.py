from setuptools import setup, find_packages

setup(
    name="cloudengineffapi",
    version="0.1.0",
    packages=find_packages(),
    install_requires=["requests"],  # Dependency for API calls
    description="Client for CloudEngineFF APIs with rate limiting",
    author="Bijoy",  # Replace with your name
    python_requires=">=3.6",
)