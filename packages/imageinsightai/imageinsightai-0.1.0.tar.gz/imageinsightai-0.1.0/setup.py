from setuptools import setup, find_packages

setup(
    name='imageinsightai',
    version='0.1.0',
    author='Asad khan',
    author_email='asakha@ktu.lt',
    description='ImageInsightAI: An image captioning package using BLIP model',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/kham123123/imageinsightai',  # Optional, can be empty or your repo
    packages=find_packages(),
    install_requires=[
        'torch',
        'transformers',
        'Pillow'
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.7',
)
