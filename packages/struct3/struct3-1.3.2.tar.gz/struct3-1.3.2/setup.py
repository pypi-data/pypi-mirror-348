from setuptools import setup, find_packages

setup(
    name='struct3',
    version='1.3.2',
    author='Loic M.Herry',
    author_email='priv@octagonax.com',
    description='Replacement for the standard struct lib',
    packages=find_packages(),
    classifiers=[
        'Operating System :: OS Independent',
    ],
    python_requires='>=2.7',
)