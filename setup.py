import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="handwrite",
    version="0.3.1",
    author="Yash Lamba, Saksham Arora, Aryan Gupta",
    author_email="yashlamba2000@gmail.com, sakshamarora1001@gmail.com, aryangupta973@gmail.com",
    description="Convert text to custom handwriting",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/builtree/handwrite",
    packages=setuptools.find_packages(),
    install_requires=["opencv-python", "Pillow", "flask"],
    extras_require={
        "dev": [
            "pre-commit",
            "black",
            "mkdocs==1.2.2",
            "mkdocs-material==6.1.0",
            "pymdown-extensions==8.2",
            "mkdocstrings>=0.16.1",
            "pytkdocs[numpy-style]",
        ],
        "webapp": [
            "gunicorn>=20.1.0",
        ],
    },
    entry_points={
        "console_scripts": ["handwrite = handwrite.cli:main"],
    },
    include_package_data=True,
    package_data={
        "handwrite": ["default.json"],
        "webapp": ["templates/*", "static/*"],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
)
