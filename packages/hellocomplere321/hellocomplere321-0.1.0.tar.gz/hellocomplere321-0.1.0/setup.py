from setuptools import setup, find_packages 

setup(
    name='hellocomplere321',
    version='0.1',
    author='AshutoshSemwal',
    packages=find_packages(),
    install_requires=[
        #'numpy'
    ],
    entry_points={
        'console_scripts': [
            'hellocomplere321 = hello_complere.main:say_hello',
        ],
    },
)