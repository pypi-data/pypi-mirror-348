import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

classifiers = [
    "Programming Language :: Python :: 3",
    "License :: OSI Approved :: MIT License",
    "Operating System :: OS Independent",
]

requires = [
    "requests>=2.32.3",
    "python-dateutil>=2.8.2",
    "jsonpickle>=0.9.6",
    "urllib3>=1.26.20",
    "six>=1.16.0",
]

setuptools.setup(
    name="tabadul",
    version="1.0.1",
    description="Tabadul API client",
    author="Abdullah Alaidrous",
    author_email="abd.alaidrous@gmail.com",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://gitlab.com/abdroos/tabadul",
    package_dir={"tabadul": "tabadul"},
    packages=setuptools.find_packages(),
    python_requires=">=3.6",
    install_requires=requires,
    classifiers=classifiers,
)
