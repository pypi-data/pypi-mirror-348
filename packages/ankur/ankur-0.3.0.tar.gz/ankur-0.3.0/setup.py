from setuptools import setup, find_packages

setup(
    name="ankur",
    version="0.3.0",  # Updated version
    packages=find_packages(),
    description="Ankur's package with CLI support",
    author="Ankur",
    author_email="ankurkumar7753@gmail.com",
    url="https://github.com/7007259Ankur",
    entry_points={
        'console_scripts': [
            'ankur-cli=ankur.cli:main', 
             'ankur=ankur.cli:main' # Creates CLI command
        ],
    },
    install_requires=['colorama>=0.4.6'],  # Add dependencies if needed
)