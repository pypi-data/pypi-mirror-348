from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()
    
setup(
    name='two_pcepd',
    version='0.1.3',    
    description='The official implementation of the 2pCePd-Net model. pBPf Fusion block coming soon...',
    long_description=long_description,
    long_description_content_type="text/markdown",
    author='Supratim Ghosh, Sourav Pramanik, Anoop Kumar Tiwari, Kottakkaran Sooppy Nisar, Mahantapas Kundu, Mita Nasipuri',
    author_email='supratimghosh2772@gmail.com',
    license='GNU General Public License v3.0',
    packages=['two_pcepd'],
    install_requires=['numpy', 'torch'],

    classifiers=[
        'Programming Language :: Python :: 3.9',
    ],
)