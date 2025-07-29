import setuptools

with open('Readme.md') as fp:
    long_description = fp.read()

with open('requirements.txt') as fp:
    requirements = fp.read()

setuptools.setup(
    name='preprocess_tr',
    include_package_data=True,
    version='0.1.1',
    author='noname',
    author_email='test@test.com',
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
