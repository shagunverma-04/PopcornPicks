from setuptools import setup 
with open("README.md","r", encoding="utf-8") as fh:
    long_description = fh.read() 


AUTHOR_NAME="SHAGUN VERMA"
SRC_REPO="src"
LIST_OF_REQUIREMENTS= ['streamlit']


setup(
    name='PopcornPicks',
    version='0.0.1',
    author=AUTHOR_NAME,
    author_email='shagunverma.2004@gmail.com',
    description='A movie recommender system using the content-based filtering logic. (DATASET USED: TMDB 5000)',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/shagunverma-04/PopcornPicks',
    package=[SRC_REPO],
    python_requires='>=3.7',
    install_requires=LIST_OF_REQUIREMENTS
    )