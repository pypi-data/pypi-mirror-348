# streamlit-math-keyboard/setup.py
from setuptools import setup, find_packages
import os
import re # Import regular expressions

# Function to extract version from __init__.py
def get_version():
    init_py_path = os.path.join("streamlit_math_keyboard", "__init__.py")
    with open(init_py_path, "r") as f:
        for line in f:
            match = re.search(r"^__version__\s*=\s*['\"]([^'\"]*)['\"]", line)
            if match:
                return match.group(1)
    raise RuntimeError("Unable to find version string.")

# Read the contents of your README file
this_directory = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name="streamlit-math-keyboard",
    version=get_version(), # Use the new function here
    author="Nuttibase Charupeng",
    author_email="basedevbackend@gmail.com",
    description="A custom Streamlit component for a math input keyboard.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/streamlit-math-keyboard",
    packages=find_packages(include=["streamlit_math_keyboard", "streamlit_math_keyboard.*"], exclude=["tests", "*.tests", "*.tests.*", "tests.*"]),
    include_package_data=True,
    package_data={
        "streamlit_math_keyboard": [
            "frontend/build/index.html",
            "frontend/build/assets/*"
        ],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Scientific/Engineering :: Mathematics",
    ],
    python_requires='>=3.7',
    install_requires=[
        "streamlit >= 1.0",
    ],
    zip_safe=False,
)