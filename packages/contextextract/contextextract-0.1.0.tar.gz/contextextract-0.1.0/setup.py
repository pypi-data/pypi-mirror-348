from setuptools import setup, find_namespace_packages

setup(
    name="contextextract",
    version="0.1.0",
    author="SSJ",
    author_email="ssj@gmail.com",
    description="Extract contextual key-value pairs from URLs, PDFs, or text using Groq API",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/contextextract",
    package_dir={"": "src"},
    packages=find_namespace_packages(where="src"),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
    install_requires=[
        "requests>=2.25.0",
        "beautifulsoup4>=4.9.0",
        "PyPDF2>=2.0.0",
        "tqdm>=4.60.0",
        "groq>=0.4.0",
    ],
)
