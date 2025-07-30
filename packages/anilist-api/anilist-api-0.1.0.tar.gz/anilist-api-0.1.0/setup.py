from setuptools import setup, find_packages
import pathlib

here = pathlib.Path(__file__).parent
long_description = (here / "README.md").read_text(encoding="utf-8")

setup(
    name="anilist-api",
    version="0.1.0",
    author="Mohammad Alamin",
    author_email="anbuinfosec@gmail.com",
    description="A complete Python wrapper for AniList GraphQL API",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/anbuinfosec/anilist-api",
    packages=find_packages(),
    install_requires=["requests"],
    license="MIT",
    keywords=["anilist", "graphql", "api", "wrapper", "python", "anime", "manga", "anbuinfosec"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Intended Audience :: Developers"
    ],
    python_requires=">=3.7",
    project_urls={
        "Bug Tracker": "https://github.com/anbuinfosec/anilist-api/issues",
        "Documentation": "https://github.com/anbuinfosec/anilist-api#readme",
        "Source": "https://github.com/anbuinfosec/anilist-api",
        "Homepage": "https://github.com/anbuinfosec/anilist-api"
    },
)