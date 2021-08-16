#
# (c) 2021 Michael Tatton
#
# CHANGELOG:
#
# 20210812 | Michael Tatton | Initial version
#
# TODO:
#
# think about class for database access
# read only mode
# better db funcs debugging
# dump to csv, load from csv
# show where the error is in the code editor
# autocomplete
#

__version__ = "0.0.6"

import os
import sqlite3
from tabulate import tabulate
from ipykernel.kernelbase import Kernel
from ipykernel.kernelapp import IPKernelApp

DEBUG = 0


def log(str):
    if DEBUG == 1:
        f = open("/tmp/sqlk.log", "a")
        f.write(str + "\n")
        f.close()


con = None


def qry2df(qry, dbfile="tmp.db"):
    try:
        df = []
        hdr = []

        con = sqlite3.connect(dbfile)
        con.row_factory = sqlite3.Row
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
        return (retval, rows)


class SQLiKernel(Kernel):

    implementation = "sql_kernel"
    implementation_version = __version__
    dbfile = "tmp.db"

    @property
    def language_version(self):
        return ""

    @property
    def banner(self):
        return ""

    language_info = {
        "name": "sqlik",
        "mimetype": "text/plain",
        "file_extension": ".sql",
    }

    def __init__(self, **kwargs):
        Kernel.__init__(self, **kwargs)
        log("__init__")

    def do_execute(
        self, code, silent, store_history=True, user_expressions=None, allow_stdin=False
    ):
        if code[-1] == ";":
            code = code[:-1]
        if not silent:
            magics = self._filter_magics(code)
            if magics:
                if magics["dbfile"]:
                    log(str(magics))
                    self.dbfile = str(magics["dbfile"][0])
            # log(self.dbfile)
            status, res = qry2df(code, self.dbfile)
            log(status)
            log(str(res))

            # if status == "OK":
            if len(res) > 1:
                ret = tabulate(res, headers="firstrow")
            else:
                ret = str(res[0])
            message = {"name": "stdout", "text": ret + "\n"}
            self.send_response(self.iopub_socket, "stream", message)
            return {
                "status": "ok",
                "execution_count": self.execution_count,
                "payload": [],
                "user_expressions": {},
            }
            # else:
            #    error_content = {
            #        'ename': '',
            #        'evalue': str(res),
            #        'traceback': []
            #    }
            #    self.send_response(self.iopub_socket, 'error', error_content)
            #    error_content['execution_count'] = self.execution_count
            #    error_content['status'] = 'error'
            #    return(error_content)

    def _filter_magics(self, code):

        magics = {"dbfile": []}

        for line in code.splitlines():
            if line.startswith("--%"):
                key, value = line[3:].split(":", 2)
                key = key.strip().lower()

                if key in ["dbfile"]:
                    for flag in value.split():
                        magics[key] += [flag]

        return magics

    def do_shutdown(self, restart):
        """Remove all the temporary files created by the kernel"""
        for file in self.files:
            os.remove(file)
        os.remove(self.master_path)
        log("SHUTDOWN")


IPKernelApp.launch_instance(kernel_class=SQLiKernel)
