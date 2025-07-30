from setuptools import setup, find_packages
import re

with open("requirements.txt", encoding="utf-8") as mano:
  requires = [z.strip() for z in mano]
    
with open("Nexgram/__init__.py", encoding="utf-8") as fk:
  version = re.findall(r"__version__ = \"(.+)\"", fk.read())[0]

setup( 
  name="Nexgram.py",
  version=version,
  packages=find_packages(),
  install_requires=requires,
  author="Otazuki",
  author_email="otazuki004@gmail.com",
  description="just a try",
  long_description=open("README.md").read(),
  long_description_content_type="text/markdown",
  url="https://github.com/Otazuki004/Nexgram.py",
  classifiers=[
    "Programming Language :: Python :: 3",
    "License :: OSI Approved :: MIT License",
    "Operating System :: OS Independent",
  ],
  python_requires='>=3.12',
)