from setuptools import setup, find_packages

setup(
    name="correlation_stats_analyzer",
    version="0.1.0",
    author="Md. Ismiel Hossen Abir",
    author_email="ismielabir1971@gmail.com",
    description="A simple tool to compute and interpret Pearson correlation coefficients.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Topic :: Scientific/Engineering :: Information Analysis",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)