from setuptools import setup, find_packages

setup(
    name='stackoverflow',
    version='1.0',
    description='StackOverflow-lite platform API where people can ask questions and provide answers.',
    url='https://github.com/asheuh/StackOverflow-lite',
    author='Brian Mboya',

    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: All',
        'Topic :: Software Development :: Libraries :: Application Frameworks',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],
    packages=find_packages()
)
