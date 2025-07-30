from setuptools import setup, find_packages

setup(
    name="winmemory",
    version="0.1.0",
    author="ph_thienphu1006",
    author_email="phualan1006@gmail.com",
    description="Memory manipulation using python and ctypes",
    long_description=open("README.md", "r").read(),
    long_description_content_type="text/markdown",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: Microsoft :: Windows",
    ]
)