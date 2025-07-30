from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="thrads_sdk",
    version="0.1.3",
    author="Thrads Team",
    author_email="contact@thrads.ai",
    description="Python SDK for the Thrads Ad Platform API",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/thrads/thrads-sdk",
    packages=find_packages(exclude=["tests", "tests.*"]),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
    install_requires=[
        "requests>=2.25.0",
        "Pillow>=8.0.0",
        "aiohttp>=3.8.0",
        "certifi>=2023.5.7"
    ],
    license="MIT",  # Use this instead of license-file
    # Remove or fix the license-file field
)
