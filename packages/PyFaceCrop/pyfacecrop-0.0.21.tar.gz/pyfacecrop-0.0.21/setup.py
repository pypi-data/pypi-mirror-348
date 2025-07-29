from setuptools import setup, find_packages

with open("README.md", "r") as f:
    description = f.read()

setup(
    name='PyFaceCrop',
    version='0.0.21',
    packages=find_packages(),
    install_requires=['opencv-python'],
    long_description=description,
    include_package_data=True, 
    package_data={
        'PyFaceCrop': ['haarcascades/*.xml']
    },
    long_description_content_type="text/markdown"
)
