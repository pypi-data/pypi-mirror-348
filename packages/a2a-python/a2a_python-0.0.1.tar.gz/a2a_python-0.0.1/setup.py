from setuptools import setup, find_packages

setup(
    name='a2a-python',
    version='0.0.1',
    author='Luke Hinds',
    author_email='lukehinds@gmail.com',
    description='Python A2A Implementation',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/lukehinds/a2a-python',
    packages=find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.11',
) 