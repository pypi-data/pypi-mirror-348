from setuptools import setup, find_packages

setup(
    name='ip-to-country',
    version='1.0.0',
    description='Convert IP addresses to countries using delegated registry data',
    long_description=open('README.md').read(),  # Loads the content of the README.md for long description
    long_description_content_type='text/markdown',  # Specifies the format of the long description (Markdown)
    author='Pieter-Jan Coenen',
    author_email='pieterjan.coenen@gmail.com',
    packages=find_packages(),
    include_package_data=True,
    package_data={'ip_to_country': ['../data/country_info.pkl', '../data/ipv4_ranges.pkl', '../data/ipv6_ranges.pkl']},  # Include your CSV
    install_requires=[],
    python_requires='>=3.6',
)