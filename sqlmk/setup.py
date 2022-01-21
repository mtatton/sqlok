from setuptools import setup

setup(
    name="sqlm_kernel",
    version="0.1.3",
    description="MySQL Kernel for Jupyter Notebook",
    long_description=open("README.txt").read(),
    long_description_content_type="text/plain",
    url="https://github.com/mtatton/sqlok",
    author="Michael Tatton",
    license="",
    packages=["sqlm_kernel"],
    install_requires=[
        "tabulate",
        "mysql-connector-python",
    ],
    scripts={"sqlm_kernel/sqlmk_install"},
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Science/Research",
        "Operating System :: POSIX :: Linux",
        "Programming Language :: Python :: 3.7",
    ],
)
