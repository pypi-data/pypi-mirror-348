from setuptools import setup, find_packages

setup(
    name="nuggetry",
    version="0.1",
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'nuggetry = runner:main',
        ],
    },
    install_requires=['lark'],
    author="Your Name",
    description="Nuggetry Programming Language",
    long_description="A fun Lua-like scripting language!",
    long_description_content_type="text/markdown",
)
