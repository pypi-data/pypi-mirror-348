from setuptools import setup, find_packages
                    
setup(
name="RaynFn",
version="0.1.2",
author="myname",
author_email="mxtsouko@gmail.com",
description="Fortnite Interact with api",
long_description=open("README.md", encoding="utf-8").read(),
long_description_content_type="text/markdown",
url="https://github.com/Mxtsouko-off/RaynFn",
packages=find_packages("src"),
package_dir={"": "src"},
classifiers=[
    "Programming Language :: Python :: 3",
    "License :: OSI Approved :: MIT License",
    "Operating System :: OS Independent",
],
python_requires=">=3.10",
install_requires=[
    "aiohttp",
    "asyncio",
],
)