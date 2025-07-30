from setuptools import setup, find_packages

setup(
    name="pipfixer",
    version="1.0.0",
    description="Auto-installs missing Python imports from a script",
    author="PozStudio",
    author_email="you@example.com",
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'pipfixer=cli:main',
        ],
    },
    python_requires='>=3.6',
)
