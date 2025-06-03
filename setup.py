from setuptools import setup, find_packages
from pathlib import Path

here = Path(__file__).parent

setup(
    name='memify',
    version='0.1.0',
    package_dir={'': 'src'},
    packages=find_packages(where='src'),
    install_requires=[ 'rich>=14.0.0', 'simple-term-menu>=1.6.6', ],
    entry_points={
        'console_scripts': [
            'memify=memify.main:main',
        ],
    },
    python_requires='>=3.8',
    description='A simple CLI flashcard tool.',
    long_description=(here / 'README.md').read_text(encoding='utf-8'),
    long_description_content_type='text/markdown',
    author='clamsfeel2',
    url='https://github.com/clamsfeel2/memify',
    license='MIT',
)
