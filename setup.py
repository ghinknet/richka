import os
import sys

from setuptools import setup, find_packages

about = {}
here = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(here, "richka", "__version__.py"), "r") as f:
    exec(f.read(), about)

with open("README.md", "r", encoding="utf-8") as f:
    readme = f.read()

if sys.argv[-1] == "publish":
    os.system("python setup.py sdist bdist_wheel")
    os.system("twine upload dist/*")
    sys.exit()

setup(
    name=about["__title__"],
    version=about["__version__"],
    description=about["__description__"],
    packages=find_packages(),
    install_requires=[
        "aiohttp",
    ],
    url=about["__url__"],
    license=about["__license__"],
    author=about["__author__"],
    author_email=about["__author_email__"],
    long_description_content_type="text/markdown",
    long_description=readme,
    python_requires='>=3.9',
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12',
        'Programming Language :: Python :: 3 :: Only',
    ],
    entry_points={
        'console_scripts': ['richka=richka.__main__:main'],
    },
    package_data={'': ['README.md']},
    include_package_data=True,
    zip_safe=False)
