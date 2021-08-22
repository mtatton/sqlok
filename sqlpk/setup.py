from setuptools import setup

setup(
    name="sqlp_kernel",
    version="0.1.1",
    description="PostgreSQL Kernel for Jupyter Notebook",
    url="https://github.com/mtatton/sqlok",
    author="Michael Tatton",
    license="",
    packages=["sqlp_kernel"],
    install_requires=[
        "tabulate",
        "psycopg2",
    ],
    scripts={"sqlp_kernel/sqlpk_install"},
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Science/Research",
        "Operating System :: POSIX :: Linux",
        "Programming Language :: Python :: 3.8",
    ],
)
