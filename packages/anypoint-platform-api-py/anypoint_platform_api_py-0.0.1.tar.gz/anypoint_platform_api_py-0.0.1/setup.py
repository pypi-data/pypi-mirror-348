import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="anypoint-platform-api-py",
    version="0.0.1",
    author="Aminul Haque",
    author_email="aminul1983@Gmail.com",
    description="MuleSoft Anypoint Platform Python Library",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Neo-Integrations/anypoint-platform-api-py",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
