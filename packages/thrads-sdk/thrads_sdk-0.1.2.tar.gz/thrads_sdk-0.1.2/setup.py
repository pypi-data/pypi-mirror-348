from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="thrads_sdk",
    version="0.1.2",
    author="Your Name",
    author_email="your.email@example.com",
    description="Python SDK for the Thrads Ad Platform API",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/thrads-sdk",
    packages=find_packages(exclude=["tests", "tests.*"]),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
    install_requires=[
        "requests>=2.25.0",
        "Pillow>=8.0.0",  # If you're using PIL for image processing
    ],
    license="MIT",  # Use this instead of license-file
    # Remove or fix the license-file field
)
