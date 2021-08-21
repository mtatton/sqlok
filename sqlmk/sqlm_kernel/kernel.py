#
# (c) 2021 Michael Tatton
#
# CHANGELOG:
#
# 20210815 | Michael Tatton | Initial version
# 20210820 | Michael Tatton | v0.0.8
# 20210821 | Michael Tatton | v0.0.9
# 20210822 | Michael Tatton | v0.1.0
#

import os
import json
import csv
from tabulate import tabulate
import traceback
from ipykernel.kernelbase import Kernel
from ipykernel.kernelapp import IPKernelApp
import mysql.connector

# import signal

str_kernel = "sqlmk"
__version__ = "0.1.0"

DEBUG = 0


def log(str):
    if DEBUG == 1:
        f = open("/tmp/sqlok.log", "a")
        f.write(str_kernel + " " + str + "\n")
        f.close()


class DBConnection:

    con = None
    connected = False
    dbcon = None
    dns = None
    cols = None
    rows = None

    def __init__(self, constr):
        self.connected = True
        try:
            if os.path.exists(str_kernel + "_conn.json"):
                f = open(str_kernel + "_conn.json", "r")
                dbcontmp = f.read()
                f.close()
                self.dbcon = json.loads(dbcontmp)
            self.constr = self.dbcon
            self.con = mysql.connector.connect(**self.constr)
            log("-- CONNECTED TO: " + str(json.dumps(self.dbcon)))
            self.connected = True
        except Exception as e:
            self.connected = False
            log("-- INIT CONNECTION ERROR : " + str(e))
            log(traceback.format_exc())

    def connect(self, constr):
        try:
            self.constr = constr
            self.con = mysql.connector.connect(**self.constr)
            log("-- CONNECTED TO DATABASE")
            self.connected = True
            return "CONNECTED"
        except Exception as e:
            self.connected = False
            log("-- CONNECT PROBLEM: " + str(e))
            log(traceback.format_exc())
            return str(e)

    def qry2df(self, qry):
        try:
            df = []
            hdr = []
            rows = None
            retres = "OK"
            error_ind = False
            data_ind = False
            rows = None
            if self.connected:
                # CREATE CURSOR
                cur = self.con.cursor()
                try:
                    cur.execute(qry)
                except Exception as e:
                    self.con.rollback()
                    rows = [[str(e)]]
                    log("-- QUERY EXECUTION ERROR: " + str(e))
                    error_ind = True
                # TRY TO FETCH DATA
                try:
                    if not error_ind:
                        rows = cur.fetchall()
                        data_ind = True
                except Exception as e:
                    log("-- NO FETCH : " + str(e))
                # COMMIT WHEN NO ERROR IS PRESENT
                if error_ind is False and data_ind is False:
                    self.con.commit()
                    rows = [["OK"]]
                # IF DATA AND NO ERROR GET HEADER
                if data_ind is True and cur.description:
                    # log(str(rows))
                    for cn in cur.description:
                        hdr.append(cn[0])
                    df.append(hdr)
                # con.close()
                if rows:
                    if rows:
                        for r in rows:
                            df.append(list(r))
                        self.rows = rows
                        self.cols = hdr
                else:
                    df = [["OK"]]
            else:
                df = [("NOT CONNECTED")]
                retres = "ERROR"
            return (retres, df)
        except Exception as e:
            retval = "ERROR"
            rows = [(str(e))]
            log("QUERY ERROR: " + str(e))
            log(traceback.format_exc())
            return (retval, rows)

    def disconnect(self):
        self.connected = False
        self.con.close()
        log("-- DISCONNECTED")

    def __del__(self):
        self.disconnect()


class SQLmKernel(Kernel):

    implementation = str_kernel
    implementation_version = __version__
    dbcon = None

    con = None
    constr = {
        "host": "localhost",
        "port": "3306",
        "database": "mysql",
        "user": "user",
        "password": "",
    }

    @property
    def language_version(self):
        return ""

    @property
    def banner(self):
        return ""

    language_info = {
        "name": str_kernel,
        "mimetype": "text/plain",
        "file_extension": ".sql",
    }

    # def handler(signum, frame):
    #    log("- - - - - - - - - - - - - SIGINT || SIGTERM")

    def __init__(self, **kwargs):
        try:
            Kernel.__init__(self, **kwargs)
            self.dbcon = self.constr
            self.con = DBConnection(self.dbcon)
            log("__init__")
        except Exception as e:
            log("-- KERNEL INIT PROBLEM: " + str(e))
            log(traceback.format_exc())
        # signal.signal(signal.SIGINT, self.handler)
        # signal.signal(signal.SIGTERM, self.handler)

    def send_message(self, msg):
        try:
            message = {"name": "stdout", "text": msg + "\n"}
            self.send_response(self.iopub_socket, "stream", message)
            return {
                "status": "ok",
                "execution_count": self.execution_count,
                "payload": [],
                "user_expressions": {},
            }
        except Exception as e:
            log("-- SEND MESAGE ERROR: " + str(e))
            log(traceback.format_exc())

    def save_data_to_csv(self, file_name):
        msg = None
        if self.con.cols and self.con.rows:
            try:
                with open(file_name + ".csv", "w") as out:
                    csv_out = csv.writer(out)
                    csv_out.writerow(self.con.cols)
                    for row in self.con.rows:
                        csv_out.writerow(row)
                    msg = "Written " + file_name + ".csv"
            except Exception as e:
                msg = "Error during csv export " + str(e)
        else:
            msg = "No data to save"
        self.send_message(msg)

    def do_execute(
        self, code, silent, store_history=True, user_expressions=None, allow_stdin=False
    ):
        try:
            if len(code) > 0 and code[-1] == ";":
                code = code[:-1]
            log("-- EXECUTE CONNECTED: " + str(self.con.connected))
            magics = self._filter_magics(code)
            status = None
            res = None
            ret = None
            if magics["noexec"]:
                return
            if self.con.connected is True and not silent:
                if magics:
                    if magics["dbcon"]:
                        self.dbcon = str(magics["dbcon"])
                        self.constr = self.dbcon
                        # log(str(self.dbcon))
                    else:
                        # status, res = self.con.qry2df(code, self.constr)
                        status, res = self.con.qry2df(code)
                log("-- EXECUTE STATUS: " + str(status))
                log("-- EXECUTE RES: " + str(res))

                if res:
                    if len(res) > 1:
                        ret = tabulate(res, headers="firstrow")
                    else:
                        ret = str(res[0][0])
            else:
                ret = "NOT CONNECTED"
            if ret:
                self.send_message(ret)
        except Exception as e:
            log("-- ERROR IN DO_EXECUTE: " + str(e))
            log(traceback.format_exc())

    def _filter_magics(self, code):

        try:
            magics = {"dbcon": [], "noexec": False}

            for line in code.splitlines():
                if line.startswith("--%"):
                    dbconln = line[4:]
                    # log("-- dbconln magics: " + dbconln[0:5])
                    if dbconln[0:5] == "dbcon":
                        if len(dbconln) > 6:
                            magics["dbcon"] = dbconln[6:]
                            self.dbcon = json.loads(magics["dbcon"])
                            self.constr = self.dbcon
                            log("-- TYRING TO CONNECT WITH: " + str(self.constr))
                            conret = self.con.connect(self.constr)
                            log("-- MAGICS DBCON CONNECTED: " + str(self.con.connected))
                            self.send_message(conret)
                    elif dbconln[0:5] == "dsave":
                        fname = "tmp"
                        if len(dbconln) > 6:
                            fname = dbconln[6:]
                        log("-- SAVING DATA TO FILE")
                        self.save_data_to_csv(fname)
                        magics["noexec"] = True
                    elif dbconln[0:5] == "csave":
                        f = open(str_kernel + "_conn.json", "w")
                        f.write(str(self.dbcon).replace("'", '"'))
                        f.close()
                        magics["dbcon"] = self.dbcon
                        conret = "CONNECTION INFO SAVED"
                        self.send_message(conret)
                        log("-- MAGICS CONNECTION INFO SAVED")
                    elif dbconln[0:5] == "cload":
                        if os.path.exists(str_kernel + "_conn.json"):
                            f = open(str_kernel + "_conn.json", "r")
                            dbcontmp = f.read()
                            f.close()
                            log(dbcontmp)
                            self.dbcon = json.loads(dbcontmp)
                            self.constr = self.dbcon
                            magics["dbcon"] = self.dbcon
                            conret = self.con.connect(self.constr)
                            log("-- MAGICS DBCON CONNECTED: " + str(self.con.connected))
                            self.send_message(conret)
                            log(
                                "-- CONNECTION INFO LOADED "
                                + str(json.dumps(self.dbcon))
                            )
                    log(str(magics["dbcon"]))
        except Exception as e:
            log("-- ERROR IN MAGICS: " + str(e))
            log(traceback.format_exc())
        return magics

    def do_shutdown(self, restart):
        self.con.disconnect()
        log("-- KERNEL SHUTDOWN DO SHUTDOWN")
        for file in self.files:
            os.remove(file)
        os.remove(self.master_path)


IPKernelApp.launch_instance(kernel_class=SQLmKernel)
