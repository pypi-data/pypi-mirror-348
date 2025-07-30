from setuptools import find_packages, setup

setup(
    name='gendia',
    version='1.6.2',
    packages=find_packages(include=["src", "src.*"]),
    install_requires=[
        # List your dependencies here
    ],
    entry_points={
        'console_scripts': [
            'gendia=src.main:main',  # Adjust this to your CLI entry point
        ],
    },
    author='Silicon27',
    author_email='yangsilicon@gmail.com',
    description='A Python CLI to generate a tree structured diagram for any directory',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/Silicon27/gendia',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
