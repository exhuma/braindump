from setuptools import setup

setup(
    name="wpclassifier",
    version="1.0",
    author="Michel Albert",
    author_email="michel@albert.lu",
    description="Tiny tool to automatically classify wallpapers by their dimensions",
    long_description=open("README.rst").read(),
    license="BSD",
    include_package_data=True,
    install_requires=[
        "pillow"
    ],
    entry_points = {
        'console_scripts': [
                'wpclassifier = wpclassifier.cli:main'
            ]
        },
    packages=["wpclassifier"],
)
