from setuptools import setup, find_packages

setup(
    name="freelabs",
    version="1.1.5",
    description="Creating a quick backup",
    author="Areerr",
    author_email="a.le.xd.a.m.ayok@gmail.com",
    packages=find_packages(),
    install_requires=[
        "pyzipper",
        "python-telegram-bot",
        "requests"
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent"
    ],
    python_requires=">=3.6",
)