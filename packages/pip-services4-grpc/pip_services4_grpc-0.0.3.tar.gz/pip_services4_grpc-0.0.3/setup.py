"""
Pip.Services gRRPC
------------------

Pip.Services is an open-source library of basic microservices.
pip_services4_grpc provides grpc clients and controllers components.

Links
`````

* `website <http://github.com/pip-services/pip-services>`_
* `development version <http://github.com/pip-services4/pip-services4-python/tree/main/tree/main//pip-services4-grpc-python>`

"""

from setuptools import setup
from setuptools import find_packages

try:
    readme = open('readme.md').read()
except:
    readme = __doc__

setup(
    name='pip_services4_grpc',
    version='0.0.3',
    url='http://github.com/pip-services4/pip-services4-python/tree/main/tree/main//pip-services4-grpc-python',
    license='MIT',
    author='Conceptual Vision Consulting LLC',
    author_email='seroukhov@gmail.com',
    description='gRPC clients and controllers for Pip.Services in Python',
    long_description=readme,
    long_description_content_type="text/markdown",
    packages=find_packages(exclude=['config', 'data', 'test']),
    include_package_data=True,
    zip_safe=True,
    platforms='any',
    install_requires=[
        'grpcio >= 1.43.0, < 2.0.0',
        'grpcio-tools >= 1.43.0, < 2.0.0',
        'protobuf >= 3.19.3, < 6.0.0',

        'pip_services4_commons >= 0.0.1, < 1.0',
        'pip_services4_rpc >= 0.0.1, < 1.0',
        'pip_services4_components >= 0.0.1, < 1.0'
    ],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ]    
)
