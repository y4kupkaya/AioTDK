import os
import setuptools

classifiers = [
    "Programming Language :: Python :: 3",
    "Programming Language :: Python :: 3.8",
    "Programming Language :: Python :: 3.9",
    "Programming Language :: Python :: 3.10",
    "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
    "Operating System :: OS Independent",
]

setuptools.setup(
    name="aiotdk",
    version="0.0.1",
    author="Yakup Kaya",
    author_email="support@yakupkaya.net.tr",
    description=(
        "A Python package to interact with TDK (Türkiye Dil Kurumu) API."
        "This package works asynchronously unlike others."
        "TDK'nın API'si ile etkileşim kurmak için bir Python paketi."
        "Bu paket diğerlerinden farklı olarak asenkron çalışır."
    ),
    license="GNU AFFERO GENERAL PUBLIC LICENSE (v3)",
    keywords="example documentation tutorial",
    url="http://github.com/aylak-github/aiotdk",
    package_dir={
        "": "src",
    },
    packages=setuptools.find_packages(where="src"),
    long_description="http://github.com/aylak-github/aiotdk/blob/main/README.md",
    classifiers=classifiers,
    long_description_content_type="text/markdown",
)
