from setuptools import setup, find_packages
with open("requirements.txt") as f:
    install_requires = f.read().splitlines()

setup(
    name='SpatioloJI',
    version='0.1.2',
    packages=find_packages(),
    install_requires=install_requires,
    include_package_data=True,
    author='Ji Wang',
    author_email='gynecoloji@gmail.com',
    description='A spatial transcriptomics toolkit',
    url='https://github.com/gynecoloji/SpatioloJI',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.12',
)
