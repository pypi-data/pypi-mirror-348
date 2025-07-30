from setuptools import setup, find_packages

setup(
    name="appwrite-sync",
    version="0.3",
    packages=find_packages(),
    include_package_data=True,
    package_data={
        "appwrite_sync": ["templates/*.json", "templates/*.example"],
    },
    install_requires=["appwrite"],
    entry_points={
        "console_scripts": [
            "appwrite-sync=appwrite_sync.cli:main"
        ]
    },
)
