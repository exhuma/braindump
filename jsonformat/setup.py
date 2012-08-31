from setuptools import setup

setup(
    name="jsonf",
    version="1.0",
    author="Michel Albert",
    author_email="michel@albert.lu",
    description="Tiny tool to pretty print JSON documents on the console.",
    long_description=open("README.rst").read(),
    license="BSD",
    include_package_data=True,
    install_requires=[
        "pygments"
    ],
    entry_points={
        'console_scripts': [
                'jsonf = jsonf.cli:main'
            ]
        },
    packages=["jsonf"],
)
