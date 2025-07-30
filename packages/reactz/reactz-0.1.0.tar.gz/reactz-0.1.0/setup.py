from setuptools import setup, find_packages

setup(
    name="reactz",
    version="0.1.0",
    author="katarymba",
    author_email="your.email@example.com",
    description="PHP project packaged as Python library with CLI tool",
    packages=["n"],  # Используем "n" вместо "test"
    include_package_data=True,
    package_data={
        'n': [
            'admin/*.php',
            'assets/css/*.css',
            'config/*.php',
            'config/*.sql',
            'includes/*.php',
            '*.php',
        ],
    },
    entry_points={
        'console_scripts': [
            'reactz=n.cli:main',  # Используем "n.cli" вместо "test.cli"
        ],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)