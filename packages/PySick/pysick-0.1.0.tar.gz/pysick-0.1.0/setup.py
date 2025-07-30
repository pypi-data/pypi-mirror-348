from setuptools import setup, find_packages

setup(
    name='pysick',
    version='0.1.0',
    description='A minimal 2D game module built on top of Pygame',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='PySick',
    author_email='name@gmail.com',
    url='https://github.com/name/pysick',
    packages=find_packages(),
    install_requires=[
        'pygame>=2.0.0'
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
