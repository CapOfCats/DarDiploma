import asyncio
import sqlite3
from sqlite3 import Error
import time
import os

connstring = None

class Utils:
    @staticmethod
    def create_connection(path):
        connection = None
        try:
            connection = sqlite3.connect(path)
            print("Connection to SQLite DB successful")
            connstring = connection
        except Error as e:
            print(f"The error '{e}' occurred")
        return connection

    @staticmethod
    def read_single_row(id, connection, table):
        cursor = connection.cursor()
        result = None
        try:
            sqlite_select_query = f"""SELECT * from {table} where ID =:ID"""
            cursor.execute(sqlite_select_query, {"ID": id})
            connection.commit()
            result = cursor.fetchone()
            return result
        except sqlite3.Error as e:
            print(f"The error '{e}' occurred")

    @staticmethod
    def execute_query(connection, query):
        cursor = connection.cursor()
        try:
            cursor.execute(query)
            connection.commit()
            print("Query executed successfully")
            return True
        except Error as e:
            print(f"The error '{e}' occurred")
            return False

    @staticmethod
    def execute_silent(connection, query):
        cursor = connection.cursor()
        try:
            cursor.execute(query)
            connection.commit()
            return True
        except Error as e:
            print(f"The error '{e}' occurred")
            return False

    @staticmethod
    def execute_read_query(connection, query):
        cursor = connection.cursor()
        result = None
        try:
            cursor.execute(query)
            result = cursor.fetchall()
            return result
        except Error as e:
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
    async def asyncStart(window, timer_lb, connection):
        while True:
            windowtask = asyncio.create_task(Utils.asyncMLoop(window))
            timetask = asyncio.create_task(Utils.timetick(timer_lb))
            await windowtask
            await timetask
            command = f"""
                                        UPDATE Doors SET
                                        System_time = (datetime('now','localtime')) ;
                                    """
            Utils.execute_silent(connection, command)

    @staticmethod
    def writeLog(text):
        text = '[' + time.strftime("%H:%M:%S", time.localtime()) + ']' + text + '\n'
        if not os.path.exists("ASLog.txt"):
            stream = open("ASLog.txt", "x")
            stream.close()
        stream = open("ASLog.txt", "a")
        stream.write(text)
        stream.close()
