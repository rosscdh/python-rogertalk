from setuptools import setup

setup(
    name="python-rogertalk",
    packages=['rogertalk'],
    version='0.0.1',
    author="Ross Crawford-d'Heureuse",
    license="MIT",
    author_email="sendrossemail@gmail.com",
    url="https://github.com/rosscdh/python-rogertalk",
    description="A python module for using the rogertalk api",
    zip_safe=False,
    include_package_data=True,
    install_requires=[
        'requests',
        'requests-oauth2',
        'pytest',
        'coverage',
        'httpretty',
    ]
)
