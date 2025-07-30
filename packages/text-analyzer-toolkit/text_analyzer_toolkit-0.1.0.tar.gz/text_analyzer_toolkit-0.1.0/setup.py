from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="text-analyzer-toolkit", 
    version="0.1.0",
    author="Zoe Duan",  
    author_email="zoe_dyh@hotmail.com",  
    description="A simple text analysis toolkit for basic text processing tasks",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/ZoeDuan/text-analyzer-toolkit",  
    packages=find_packages(),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Text Processing :: Linguistic",
    ],
    python_requires=">=3.7",
    install_requires=[
        # No external dependencies for basic version
    ],
    extras_require={
        "dev": [
            "pytest>=6.0",
            "black",
            "flake8",
            "mypy",
        ],
    },
)