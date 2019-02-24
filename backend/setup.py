from setuptools import find_packages, setup

setup(
    name="src",
    packages=find_packages(),
    version="0.1.0",
    description="Flask server",
    author="John Murray",
    include_package_data=True,
    install_requires=["flask"],
)
