from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="pipfixer",
    version="1.0.2",  # versiyonu artır
    description="Auto-installs missing Python imports from a script",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="PozStudio",
    author_email="you@example.com",
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'pipfixer=pipfixer.cli:main',
        ],
    },
    python_requires='>=3.6',
)
