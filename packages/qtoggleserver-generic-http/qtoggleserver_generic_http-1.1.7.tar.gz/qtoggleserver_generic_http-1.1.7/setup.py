from setuptools import setup, find_namespace_packages


setup(
    name='qtoggleserver-generic-http',
    version='1.1.7',
    description='qToggleServer ports backed by configurable HTTP requests',
    author='Calin Crisan',
    author_email='ccrisan@gmail.com',
    license='Apache 2.0',

    packages=find_namespace_packages(),

    install_requires=[
        'aiohttp',
        'jinja2',
        'jsonpointer'
    ]
)
