from setuptools import setup, find_packages

setup(
    name="startic",
    version="1.1.4",
    packages=find_packages(),
    install_requires=[
        "clight",
        
    ],
    entry_points={
        "console_scripts": [
            "startic=startic.main:main",  # Entry point of the app
        ],
    },
    package_data={
        "startic": [
            "main.py",
            "__init__.py",
            ".system/imports.py",
            ".system/index.py",
            ".system/modules/-placeholder",
            ".system/sources/clight.json",
            ".system/sources/logo.ico",
            ".system/sources/sitemap.xml",
            "frame/.gitignore",
            "frame/index.html",
            "frame/pages.yml",
            "frame/robots.txt",
            "frame/assets/logo.png",
            "frame/assets/sitemap.xml",
            "frame/assets/startic.json",
            "frame/parts/.html",
            "frame/parts/author.html",
            "frame/parts/details.html",
            "frame/parts/intro.html",
            "frame/parts/links.html",
            "frame/social/linkedin.html",
            "frame/social/mail.html",
            "frame/social/x.html"
        ],
    },
    include_package_data=True,
    author="Irakli Gzirishvili",
    author_email="gziraklirex@gmail.com",
    description="Startic is a Python CLI tool for quickly building static webpages, allowing you to start publishing lightweight templates with ease",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/IG-onGit/Startic",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
