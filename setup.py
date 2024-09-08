from setuptools import setup, find_packages

setup(
    name='memify',
    version='0.1.0',
    packages=find_packages(where='src'),
    package_dir={'': 'src'},
    install_requires=[ 'rich', 'simple_term_menu' ],
    entry_points={ 'console_scripts': [ 'memify=main:main', ], },
    python_requires='>=3.6',
    description='A brief description of my package',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='clamsfeel2',
    url='https://github.com/clamsfeel2/memify',
    license='GPL 3.0',
)
