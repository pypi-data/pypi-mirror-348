from setuptools import setup, find_packages

__name__ = 'cpjson'
__version__ = '4.7.5'

long_description = """
cpjson provides tools for deeply comparing JSON objects to identify structural 
or value-based differences. It supports recursive comparison of nested dictionaries, 
lists, and primitive types, highlighting added, removed, or modified fields. 
Designed for configuration validation, API response testing, and data auditing, 
the library offers a clear and consistent way to analyze changes between JSON 
documents.
"""

setup(
    name=__name__,
    version=__version__,
    packages=find_packages(),
    description=__name__,
    long_description_content_type='text/plain',
    long_description=long_description,
    url='https://github.com/monsur/jsoncompare',
    download_url='https://github.com/monsur/jsoncompare',
    project_urls={
        'Documentation': 'https://github.com/monsur/jsoncompare'},
    author='Monsur Hossain',
    author_email='monsur.hossain@zssolutionsllc.net',
    setup_requires=[
        'nix-utils'
    ],
)

try:
    from cpjson.version._version import __name__, __version__
except Exception as e:
    pass
