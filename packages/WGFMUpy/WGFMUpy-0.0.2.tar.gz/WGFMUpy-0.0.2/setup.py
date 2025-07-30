from setuptools import setup, find_packages

setup(
    name='WGFMUpy',
    version='0.0.2',
    packages=find_packages(),
    include_package_data=True,
    package_data={
        'WGFMUpy': ['libs/wgfmu.dll'],
    },
    author='Davide Florini',
    author_email='davideflorini92@gmail.com',
    description = 'A Python wrapper for the WGFMU library',
    url='https://github.com/DavideFlorini/WGFMUpy',
    install_requires=[
        # List any dependencies your package needs
        'numpy>=1.20',
    ],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: Microsoft :: Windows',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Scientific/Engineering :: Interface Engine/Protocol Translator'
    ],
)
