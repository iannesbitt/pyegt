import setuptools
from pyegt import _version

with open('README.md', 'r') as fh:
    long_description = fh.read()

setuptools.setup(
    author='Ian Nesbitt',
    author_email='nesbitt@nceas.ucsb.edu',
    name='pyegt',
    version=_version.__version__,
    description='Look up geoid and tidal model heights relative to the ellipsoid',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://iannesbitt.github.io/pyegt',
    packages=setuptools.find_packages(),
    include_package_data=True,
    install_requires=[
        'pyproj>=3.1.0',
        'requests'
    ],
    entry_points = {
        'console_scripts': [
            'pyegt-test=pyegt.test:test'
        ],
    },
    python_requires='>=3.9, <4.0',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Education',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: Apache Software License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Topic :: Scientific/Engineering :: GIS',
    ],
    license='Apache Software License 2.0',
)