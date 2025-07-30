from setuptools import setup, find_packages
import os

# Read the requirements.txt file
def read_requirements():
    with open(os.path.join(os.path.dirname(__file__), 'requirements.txt')) as f:
        return f.read().splitlines()

setup(
    name="redis_worker_API",
    version="0.5.8",
    packages=find_packages(),
    description="Library to exchange messages between workers using Redis Streams",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",  # Use "text/markdown" for a markdown README
    author="GCP",
    author_email="gonzalo.h.cordova@gmail.com",
    # url="https://github.com/yourusername/my_library",
    license="MIT",
    install_requires=read_requirements(),
   
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
