from setuptools import setup, find_packages

setup(
    name="clipdump",
    version="1.0.2",
    author="Backspace Studios",
    description="A simple CLI tool to save and append clipboard contents.",
    long_description=open("README.md", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/clipdump",  # replace with your actual repo
    packages=find_packages(),
    install_requires=[
        "pyperclip"
    ],
    entry_points={
        "console_scripts": [
            "clipdump=clipdump.main:cli"
        ]
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
        "Environment :: Console",
        "Intended Audience :: End Users/Desktop",
        "License :: OSI Approved :: MIT License",  # update if you use another
        "Topic :: Utilities"
    ],
    python_requires=">=3.6",
    include_package_data=True,
    zip_safe=False,
)
