from setuptools import setup, find_packages

setup(
    name="chromades",
    version="0.1.0",
    author="Cipherix",
    author_email="",
    description="A cool terminal graphics module with progress bars and colors",
    long_description=open("README.md", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7',
    entry_points={
        'console_scripts': [
            'chromades=chromades.cli:main',
        ],
    },
)