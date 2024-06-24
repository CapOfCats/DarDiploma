import asyncio
import sqlite3
from sqlite3 import Error
import time
import os

#connstring = None

class Utils:

    def create_connection(self, path):
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

    def read_single_row(self, id, connection, table):
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

    def execute_query(self, connection, query):
        if (type(query) is not str):
            return "Invalid query given"
        cursor = connection.cursor()
        try:
            cursor.execute(query)
            connection.commit()
            print("Query executed successfully")
            return True
        except Error as e:
            print(f"The error '{e}' occurred")
            raise SyntaxError

    def execute_silent(self, connection, query):
        cursor = connection.cursor()
        try:
            cursor.execute(query)
            connection.commit()
            return True
        except Error as e:
            print(f"The error '{e}' occurred")
            return False

    def execute_read_query(self, connection, query):
        cursor = connection.cursor()
        result = None
        try:
            cursor.execute(query)
            result = cursor.fetchall()
            return result
        except Error as e:
            print(f"The error '{e}' occurred")

    async def timetick(self, timerLb):
        t = time.localtime()
        current_time = time.strftime("%H:%M:%S", t)
        timerLb.configure(text= "Системное время:   " + current_time)
        await asyncio.sleep(0.03)

    async def asyncMLoop(self, wndw):
        wndw.update()
        await asyncio.sleep(0.01)
    async def asyncStart(self, window, timer_lb, connection):
        while True:
            windowtask = asyncio.create_task(self.asyncMLoop(window))
            timetask = asyncio.create_task(self.timetick(timer_lb))
            await windowtask
            await timetask
            command = f"""
                                        UPDATE Doors SET
                                        System_time = (datetime('now','localtime')) ;
                                    """
            self.execute_silent(connection, command)

    def writeLog(self, text):
        text = '[' + time.strftime("%H:%M:%S", time.localtime()) + ']' + text + '\n'
        if not os.path.exists("ASLog.txt"):
            stream = open("ASLog.txt", "x")
            stream.close()
        stream = open("ASLog.txt", "a")
        stream.write(text)
        stream.close()
