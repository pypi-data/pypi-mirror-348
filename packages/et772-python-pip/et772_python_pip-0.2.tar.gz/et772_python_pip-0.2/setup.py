from setuptools import setup, find_packages

setup(
    name='et772_python_pip',
    version='0.2',
    packages=find_packages(),
    install_requires=[
    ],
    entry_points={
        "console_scripts": [
            "piphelp = commands:help",
        ]
    }
)