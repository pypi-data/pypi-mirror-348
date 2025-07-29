from setuptools import setup, find_packages

setup(
    name='authorization_module',
    version='0.1.0',
    description='A description of your module',
    author='Hoang',
    author_email='you@example.com',
    packages=find_packages(),
    install_requires=[
        'jose','PyJWT'
    ],
    python_requires='>=3.11',
)
