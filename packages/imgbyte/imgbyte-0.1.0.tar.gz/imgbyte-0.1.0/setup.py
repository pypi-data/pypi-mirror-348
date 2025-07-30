from setuptools import setup, find_packages

setup(
    name='imgbyte',
    version='0.1.0',
    author='32-Bit',
    description='Automation library for interacting with Imgflip using Selenium and Requests',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/CreeperKing77/imgbyte',
    packages=find_packages(),
    install_requires=[
        'selenium',
        'requests'
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.11',
)
