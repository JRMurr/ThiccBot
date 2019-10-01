from setuptools import find_packages, setup

setup(
    name="thiccBot",
    packages=find_packages(),
    version="0.1.0",
    description="Flask Graphene server",
    author="John Murray",
    include_package_data=True,
    install_requires=["flask"],
)
