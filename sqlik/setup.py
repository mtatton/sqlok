from setuptools import setup

setup(
    name="sqli_kernel",
    version="0.0.8",
    description="SQLite Kernel for Jupyter Notebook",
    url="https://github.com/mtatton/sqlok",
    author="Michael Tatton",
    author_email="nocon@null.net",
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
        "Programming Language :: Python :: 3.8",
    ],
)
