from setuptools import setup, find_packages

setup(
    name="manga_reader",
    version="0.1.0",
    description="A Streamlit-based manga reader application using MangaDex API",
    author="Your Name",
    author_email="your.email@example.com",
    packages=find_packages(),
    install_requires=[
        "streamlit>=1.37.0",
        "requests>=2.31.0",
        "beautifulsoup4>=4.12.3",
    ],
    entry_points={
        "console_scripts": [
            "manga-reader = manga_reader:main"
        ]
    },
    scripts=["run.py"],
    include_package_data=True,
    license="MIT",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
)