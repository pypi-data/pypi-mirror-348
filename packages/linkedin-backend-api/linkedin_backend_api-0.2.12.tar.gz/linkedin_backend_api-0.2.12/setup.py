from setuptools import setup, find_packages

setup(
    name="linkedin-backend-api",
    version="0.2.1",
    packages=find_packages(),
    install_requires=[
        "aiohttp>=3.8.0",
        "pydantic>=1.10.0",
    ],
    python_requires=">=3.8",
    description="",
    author="",
    author_email="example@example.com",
    url="https://github.com/0x216/linkedin-backend-api",
) 