from setuptools import setup, find_packages

install_requires = [
    'click>=7.0,<8.0'
]

setup(
    name='hadopy',
    description="Easy parallel map-reduce command line tool",
    version='0.1.3',
    packages=find_packages(),
    install_requires=install_requires,
    python_requires='>=3.6',
    author='Lucas van der Horst',
    author_email='Lucas.vanderhorst@student.hu.nl',
    keyword="mapreduce, map, parallel, hadoop",
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    license='GPL3',
    url='https://github.com/MariaDukmak/Hadopy',
    entry_points='''
        [console_scripts]
        hadopy=hadopy.main:cli
    '''
)
