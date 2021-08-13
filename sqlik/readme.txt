Jupyter SQL Kernel for SQLite

Howto Install:

git clone https://github.com/mtatton/sqlok
cd ./sqlok/sqlik/sqli_kernel
python install
python3 -c "import site; print(site.getsitepackages())"
cp -R ../sqli_kernel <to one of the site packages location>
test using: python -m sqli_kernel 
then use: nbterm --kernel sqlik
