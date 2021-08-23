from setuptools import setup

setup(
    name="sqlo_kernel",
    version="0.1.2",
    description="Oracle Kernel for Jupyter Notebook",
    long_description=open("readme.txt").read(),
    long_description_content_type="text/plain",
    url="https://github.com/mtatton/sqlok",
    author="Michael Tatton",
    license="",
    packages=["sqlo_kernel"],
    install_requires=[
        "tabulate",
        "cx_Oracle",
    ],
    scripts={"sqlo_kernel/sqlok_install"},
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Science/Research",
        "Operating System :: POSIX :: Linux",
        "Programming Language :: Python :: 3.7",
    ],
)
