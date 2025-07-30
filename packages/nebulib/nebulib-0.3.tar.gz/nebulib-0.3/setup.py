from setuptools import setup, find_packages

setup(
    name='nebulib',
    version='0.3',
    packages=find_packages(),
    install_requires=['psutil'],
    author='XZRDev',
    description='A performance-focused system monitor library.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    license='MIT',
)
