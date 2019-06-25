import setuptools


with open("README.md", "r") as f:
    long_descr = f.read()


setuptools.setup(
    name='onem-py',
    version='1.0',
    author='Marius Vigariu',
    author_email='marius.vigariu@onem.com',
    description='Client which defines the JSON structure accepted by ONEm '
                'platform.',
    long_description=long_descr,
    long_description_content_type='text/markdown',
    url='https://github.com/mvnm/onem-py',
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
    ]
)
