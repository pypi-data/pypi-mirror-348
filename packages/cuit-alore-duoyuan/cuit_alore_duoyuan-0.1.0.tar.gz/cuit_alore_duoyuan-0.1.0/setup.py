from setuptools import setup, find_packages

setup(
    name="cuit_alore_duoyuan",
    version="0.1.0",
    packages=find_packages(),
    include_package_data=True,
    package_data={
        "cuit_alore_duoyuan": ["data/*.txt"]
    },
    entry_points={
        "console_scripts": [
            "cuit_alore_duoyuan = cuit_alore_duoyuan.__main__:main"
        ]
    },
    author="Alore",
    description="CUIT课堂代码库",
    long_description=open("README.md", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
