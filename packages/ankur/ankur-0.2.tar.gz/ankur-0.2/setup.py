from setuptools import setup, find_packages

setup(
    name="ankur",
    version="0.2",  # Updated version
    packages=find_packages(),
    description="Ankur's package with CLI support",
    author="Ankur",
    author_email="ankurkumar7753@gmail.com",
    url="https://github.com/7007259Ankur",
    entry_points={
        'console_scripts': [
            'ankur-cli=ankur.cli:main',  # Creates CLI command
        ],
    },
    install_requires=[],  # Add dependencies if needed
)