from setuptools import setup

setup(
    name="sqli_kernel",
    version="0.1.3",
    description="SQLite Kernel for Jupyter Notebook",
    long_description=open("README.txt").read(),
    long_description_content_type="text/plain",
    url="https://github.com/mtatton/sqlok",
    author="Michael Tatton",
    license="",
    packages=["sqli_kernel"],
    install_requires=[
        "tabulate",
    ],
    scripts={"sqli_kernel/sqlik_install"},
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Science/Research",
        "Operating System :: POSIX :: Linux",
        "Programming Language :: Python :: 3.7",
    ],
)
