from setuptools import setup, find_packages

setup(
    name='ecocrop',
    version='0.2.0',
    description='Ecological crop suitability model matching Recocrop (R) in Python',
    author='Troy Wiipongwii, PhD, MPP',
    author_email='ttwiipongwii@wm.edu',
    url='https://github.com/ttwiipongwii/ecocrop',
    packages=find_packages(),
    install_requires=[
        'numpy',
        'pandas',
        'rasterio',
        'matplotlib',
        'scipy'
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent'
    ],
    python_requires='>=3.7',
)
