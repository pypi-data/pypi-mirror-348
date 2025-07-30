from setuptools import setup, find_packages

setup(
    name="ani-title",
    version="0.1.1",
    description="Get official anime titles from Kitsu API by name",
    long_description=open("README.md", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    author="Arise",
    author_email="AriseAgatsuma@gmail.com",
    url="https://github.com/wxxoxo/ani-title",
    packages=find_packages(),
    install_requires=["requests"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
        "License :: OSI Approved :: MIT License",
        "Topic :: Utilities",
    ],
    python_requires='>=3.6',
)
