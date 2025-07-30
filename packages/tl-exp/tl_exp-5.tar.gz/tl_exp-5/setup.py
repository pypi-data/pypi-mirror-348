from setuptools import setup, find_packages

setup(
    name="tl_exp",
    version="5",  # Increment if re-uploading
    author="Your Name",
    author_email="you@example.com",
    description="A package for running transfer learning experiments",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/tl_exp",  # optional
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
