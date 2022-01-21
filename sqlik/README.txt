SQLite Kernel for Jupyter Notebook

to install:

pip install sqli-kernel
sqlik_install

optionally install terminal jupyter notebooks:

pip install nbtermix

CHANGELOG:

v0.1.3
+ added error message return

v0.1.2
+ text/html fix (--% ohtml)

v0.1.1
+ otext and ohtml magics for output mode

v0.1.0
+ bugfixing in cload, csave
+ added dsave to save last query res to csv

v0.0.9
+ fixed bug preventing error display

v0.0.8
+ added on_shutdown to kernel class
+ added disconnect to db connection class
+ upon kernel create connect to db
+ upon kernel delete disconnect from db
+ try to load connection file on startup