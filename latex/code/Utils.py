import asyncio
import sqlite3
from sqlite3 import Error
import time
import os

connstring = None

class Utils:
    @staticmethod
    def create_connection(path):
        if (type(path) is not str):
            return "Wrong path format given"
        #     return "Wrong database for this project"
        connection = None
        if os.path.exists(f"{path}"):
            connection = sqlite3.connect(path)
            print("Connection to SQLite DB successful")
            connstring = connection
        else:
            raise FileNotFoundError
        return connection

    @staticmethod
    def read_single_row(id, connection, table):
        tables = ["Passengers", "Passengers_Underage", "Doors", "Rooms", "Penalties", "Accesses", "Accesses_ES"]
        if (type(id) is not int) or (id < 1):
            return "ID should be int natural value"
        elif (type(table) is not str) or (table not in tables):
            return "Wrong table name given"
        cursor = connection.cursor()
        result = None
        try:
            sqlite_select_query = f"""SELECT * from {table} where ID =:ID"""
            cursor.execute(sqlite_select_query, {"ID": id})
            connection.commit()
            result = cursor.fetchone()
            # if result == None:
            #     raise KeyError
            return result
        except sqlite3.Error as e:
            print(f"The error '{e}' occurred")

    @staticmethod
    async def timetick(timerLb):
        t = time.localtime()
        current_time = time.strftime("%H:%M:%S", t)
        timerLb.configure(text= "Системное время:   " + current_time)
        await asyncio.sleep(0.03)

    @staticmethod
    async def asyncMLoop(wndw):
        wndw.update()
        await asyncio.sleep(0.01)

    @staticmethod
    def writeLog(text):
        text = '[' + time.strftime("%H:%M:%S", time.localtime()) + ']' + text + '\n'
        if not os.path.exists("ASLog.txt"):
            stream = open("ASLog.txt", "x")
            stream.close()
        stream = open("ASLog.txt", "a")
        stream.write(text)
        stream.close()
