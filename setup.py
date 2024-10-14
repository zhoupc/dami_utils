from setuptools import setup, find_packages

setup(
    name="dami_utils",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "latex2svg",
        # Add other dependencies here
    ],
    author="Pengcheng Zhou",
    author_email="zhoupc19@gmail.com",
    description="A utility package for DAMI lab",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/zhoupc/dami-utils",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
