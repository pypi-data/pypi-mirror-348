from setuptools import setup, find_packages

with open("README.md", "r", encoding='utf-8') as f:
    long_description = f.read()

install_requires = [
    'ase',
    'networkx',
    'spglib',
    'pandas',
    'tqdm',
    'scikit-learn',
    'scikit-image'
]

setup(
    name='surface_construct',
    version='0.9.3',
    packages=find_packages(),
    url='https://gitee.com/pjren/surface_construct/',
    license='GPL',
    author='ren',
    author_email='0403114076@163.com',
    description='Surface termination construction especially for complex model, such as oxides or carbides.',
    long_description=long_description,
    long_description_content_type="text/markdown",
    install_requires=install_requires,
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
)
