from setuptools import setup, find_packages

setup(
    name="ghswitch",
    version="0.1.0",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "click>=8.0.0",
        "pyyaml>=6.0",
        "gitpython>=3.1.0",
    ],
    entry_points={
        "console_scripts": [
            "ghswitch=ghswitch.cli:cli",
        ],
    },
    author="GitHub Account Manager",
    author_email="example@example.com",
    description="A tool for managing multiple GitHub accounts on a single device",
    keywords="github, git, account, management",
    python_requires=">=3.6",
)
