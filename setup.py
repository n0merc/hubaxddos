from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="hubaxddos",
    version="2.0.0",
    author="n0merc",
    author_email="anujin696969@gmail.com",
    description="Advanced Network Stress Testing Tool",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/hubaxddos",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Development Status :: 4 - Beta",
        "Intended Audience :: Information Technology",
        "Topic :: Security",
        "Topic :: System :: Networking",
    ],
    python_requires=">=3.6",
    install_requires=[
        "requests>=2.28.0",
        "colorama>=0.4.6",
    ],
    entry_points={
        "console_scripts": [
            "hubaxddos=hubaxddos:main",
        ],
    },
)
