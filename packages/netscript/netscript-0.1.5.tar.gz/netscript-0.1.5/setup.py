from setuptools import setup, find_packages

setup(
    name='netscript',
    version='0.1.5',
    description='Flask server wrapper for running Python scripts',
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author='Grey Liedtke',
    author_email='grey.liedtke@gmail.com',
    packages=find_packages(),
    install_requires=[
        'flask',
    ],
    entry_points={
        'console_scripts': [
            'netscript=netscript.cli:main',  # optional CLI support
        ],
    },
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
    ],
    include_package_data=True,
)
