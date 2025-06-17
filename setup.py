# this file defines how the proj shld be installed and distributed

from setuptools import find_packages,setup

setup(
    name="mcqgenerator",
    version = '0.0.1',
    author = 'aakrisht narang',
    author_email ='aakrishtnarang@gmail.com',
    install_requires=["openai","langchain","streamlit","python-dotenv","PyPDF2"],
    packages=find_packages()
)


 