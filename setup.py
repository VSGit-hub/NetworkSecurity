from setuptools import find_packages, setup
from typing import List

def get_requiments() -> List:
    """
        This function will return list of requiments
    """

    reqirement_list: List[str] = []
    try:
        with open("requirements.txt", 'r') as file:
            # Read lines from file
            lines=file.readlines()
            for line in lines:
                reqirement = line.strip()
                # Ignore empty line and -e .
                if reqirement and reqirement != '-e .':
                    reqirement_list.append(reqirement)
    except FileNotFoundError:
        print("requiment.txt not found")

    return reqirement_list


setup(
    name="NetworkSecurity",
    version="0.0.1",
    author="Vaibhav Shinde",
    author_email="vbs.codestuff@gmail.com",
    packages=find_packages(),
    install_requires=get_requiments()
)