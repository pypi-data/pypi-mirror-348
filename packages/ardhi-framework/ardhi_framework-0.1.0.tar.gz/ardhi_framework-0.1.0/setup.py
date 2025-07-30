from setuptools import setup, find_packages

setup(
    name='ardhi_framework',
    version='0.1.0',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'Django>=3.2',
        'djangorestframework>=3.12',
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'Framework :: Django',
    ],
    entry_points={
        'console_scripts': [
            # optional CLI tool
        ]
    },
)
