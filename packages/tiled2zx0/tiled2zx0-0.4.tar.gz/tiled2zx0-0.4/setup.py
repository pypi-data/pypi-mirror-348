from setuptools import setup, find_packages
import pathlib

HERE = pathlib.Path(__file__).parent
README = (HERE / "README.md").read_text()

setup(
    name='tiled2zx0',
    version='0.4',
    author='Raül Torralba',
    description='Convert tmx Tiled map to ZX0 compressed file',
    long_description=README,
    long_description_content_type='text/markdown',
    packages=find_packages(),
    include_package_data=True,
    entry_points='''
        [console_scripts]
        tiled2zx0=tiled2zx0.cli:main
    ''',
    url = 'https://github.com/rtorralba/tiled2zx0',
    install_requires=[
    ],
)