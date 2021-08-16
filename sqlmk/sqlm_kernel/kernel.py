#
# (c) 2021 Michael Tatton
#
# CHANGELOG:
#
# 20210814 | Michael Tatton | Initial version
#
# pip install mysql-connector-python
#
# TODO:
#
#
#

__version__ = "0.0.6"

import os
import json
import mysql.connector
from tabulate import tabulate
from ipykernel.kernelbase import Kernel
from ipykernel.kernelapp import IPKernelApp

DEBUG = 0

con = None


def qry2df(qry, constr=None):
    try:
        df = []
        hdr = []

        log(str(type(constr)))
        con = mysql.connector.connect(**constr)
        cur = con.cursor()
        cur.execute(qry)
        rows = cur.fetchall()
        if rows:
            for cn in cur.description:
                hdr.append(cn[0])
        con.commit()
        con.close()
        if rows:
            df.append(hdr)
            for r in rows:
                df.append(list(r))
        else:
            df = [("OK")]
        return ("OK", df)
    except Exception as e:
        retval = "ERROR"
        rows = [(str(e))]
        log(str(e))
        return (retval, rows)


def log(str):
    if DEBUG == 1:
        f = open("/tmp/sqlk.log", "a")
        f.write(str + "\n")
        f.close()


class SQLmKernel(Kernel):

    implementation = "sql_kernel"
    implementation_version = __version__
    dbcon = None
    constr = {
        "host": "127.0.0.1",
        "port": "3306",
        "user": "root",
        "password": "",
        "database": "mysql",
    }

    @property
    def language_version(self):
        return ""

    @property
    def banner(self):
        return ""

    language_info = {
        "name": "sqlmk",
        "mimetype": "text/plain",
        "file_extension": ".sql",
    }

    def __init__(self, **kwargs):
        Kernel.__init__(self, **kwargs)
        self.dbcon = self.constr
        log("__init__")

    def do_execute(
        self, code, silent, store_history=True, user_expressions=None, allow_stdin=False
    ):
        log("__init__")
        try:
            if code[-1] == ";":
                code = code[:-1]
            if not silent:
                magics = self._filter_magics(code)
                if magics:
                    if magics["dbcon"]:
                        self.dbcon = str(magics["dbcon"])
                        log(self.dbcon)
                        self.constr = json.loads(magics["dbcon"])
                        log(str(type(json.loads(magics["dbcon"]))))
                    else:
                        status, res = qry2df(code, self.constr)

                log(status)
                log(str(res))

                if len(res) > 1:
                    ret = tabulate(res, headers="firstrow")
                else:
                    ret = str(res[0])
                log("OK")
                message = {"name": "stdout", "text": ret + "\n"}
                self.send_response(self.iopub_socket, "stream", message)
                return {
                    "status": "ok",
                    "execution_count": self.execution_count,
                    "payload": [],
                    "user_expressions": {},
                }
        except Exception as e:
            log("ERROR IN DO_EXECUTE: " + str(e))

    def _filter_magics(self, code):

        try:
            magics = {"dbcon": []}

            for line in code.splitlines():
                if line.startswith("--%"):
                    dbconln = line[4:]
                    # log(dbconln[0:6])
                    if dbconln[0:6] == "dbcon:":
                        magics["dbcon"] = dbconln[7:]
                    elif dbconln[0:5] == "csave":
                        f = open("sqlmk_conn.json", "w")
                        f.write(str(self.dbcon).replace("'", '"'))
                        f.close()
                        log("save")
                        magics["dbcon"] = self.dbcon
                    elif dbconln[0:5] == "cload":
                        f = open("sqlmk_conn.json")
                        dbcontmp = f.read()
                        f.close()
                        self.dbcon = json.loads(dbcontmp)
                        self.constr = json.loads(dbcontmp)
                        log("load" + str(json.dumps(self.dbcon)))
                        magics["dbcon"] = self.dbcon
                    log(str(magics["dbcon"]))
        except Exception as e:
            log(str(e))
        return magics

    def do_shutdown(self, restart):
        """Remove all the temporary files created by the kernel"""
        for file in self.files:
            os.remove(file)
        os.remove(self.master_path)
        log("SHUTDOWN")


IPKernelApp.launch_instance(kernel_class=SQLmKernel)
