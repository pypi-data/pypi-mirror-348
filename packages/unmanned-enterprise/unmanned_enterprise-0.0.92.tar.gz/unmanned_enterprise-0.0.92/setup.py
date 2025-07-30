from setuptools import setup, find_packages

setup(
    name="unmanned_enterprise",
    version="0.0.92",
    packages=find_packages(),
    install_requires=[],
    author="Jie Xiong",
    author_email="yuanjiexiong@gmail.com",
    description="Package for unmanned_enterprise only!",
    long_description=open('README.md', encoding="utf-8").read(),
    long_description_content_type='text/markdown',
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.9',
    package_data={
        'unmanned_enterprise.member': ['prompt.jinja'],
    },
)
