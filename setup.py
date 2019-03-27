from setuptools import find_packages, setup


setup(
    name='girder-dkc',
    version='0.1.0',
    author='Kitware, Inc.',
    author_email='kitware@kitware.com',
    packages=find_packages(include=['girder_dkc', 'girder_dkc.*']),
    include_package_data=True,
    install_requires=[
        'click',
        'flask',
        'flask-sqlalchemy',
        'fs>=2',
        'marshmallow>=3.0.0rc4',
        'python-dotenv',
        'sqlalchemy-utils'
    ],
    license='Apache Software License 2.0',
    entry_points={
        'console_scripts': [
            'dkc-create-tables=girder_dkc.cli:create_tables'
        ]
    }
)
