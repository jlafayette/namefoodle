from setuptools import setup, find_packages

setup(
    name='namefoodle',
    version='0.1.0',
    description='Gnomish name generation',
    url='https://github.com/jlafayette/namefoodle',
    classifiers=[
        'Programming Language :: Python :: 3.6',
    ],
    packages=find_packages(exclude=['bin']),
    install_requires=['beautifulsoup4', 'click'],
)
