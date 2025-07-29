import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="colorizator",
    version="2.1.2",
    author="Rick",
    author_email="me@rickgrimes.org",
    description="Simple way to add color to your terminal text output",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/",
    project_urls={
        "Bug Tracker": "https://github.com/",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.6",
    install_requires=[
        "colorama",
    ]
)
