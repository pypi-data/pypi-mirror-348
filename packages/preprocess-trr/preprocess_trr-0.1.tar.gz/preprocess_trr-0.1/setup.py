import setuptools

with open('Readme.md') as fp:
    long_description = fp.read()

with open('requirements.txt') as fp:
    requirements = fp.read()

setuptools.setup(
    name='preprocess_trr',
    include_package_data=True,
    version='0.1',
    author='Vladyslav Borsh',
    author_email='test@udemy.com',
    description='This is a text preprocessing package',
    long_description=long_description,
    long_description_content_type='text/markdown',
    packages=setuptools.find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent'
    ],
    python_requires='>=3.7',
    # install_requires=requirements
)
