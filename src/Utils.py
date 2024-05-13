import asyncio
import sqlite3
from sqlite3 import Error
import time

class Utils:
    @staticmethod
    def create_connection(path):
        connection = None
        try:
            connection = sqlite3.connect(path)
            print("Connection to SQLite DB successful")
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

