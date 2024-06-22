import sqlite3

from Utils import *
import unittest

class UtilsTest(unittest.TestCase):
    def test_create_connection_fail(self):
        self.assertRaises(FileNotFoundError, Utils.create_connection, "")
        self.assertEqual(Utils.create_connection(2),"Wrong path format given")
        self.assertEqual(Utils.create_connection([(1,3), ("Diploma1.db", "someDb.db")]), "Wrong path format given")

    def test_execute_read_query(self):
        self.assertEqual(Utils.read_single_row("","",""), "ID should be int natural value")
        self.assertEqual(Utils.read_single_row(1, "", ""), "Wrong table name given")
        self.assertEqual(Utils.read_single_row(1, "", [2]), "Wrong table name given")
        self.assertEqual(Utils.read_single_row(-2, "", ""), "ID should be int natural value")
        #self.assertRaises(KeyError, Utils.read_single_row, -1, sqlite3.connect("Diploma1.db"),"Doors")

    def test_execute_invalid_query(self):
        self.assertRaises(SyntaxError,Utils.execute_query,sqlite3.connect("Diploma1.db"), f""" I AM COMMAND""")
        self.assertEqual(Utils.execute_query(sqlite3.connect("Diploma1.db"), ...), "Invalid query given")

    def test_execute_right_query(self):
        self.assertEqual(Utils.execute_query(sqlite3.connect("Diploma1.db"), f""" SELECT * FROM Doors"""), True)
        self.assertEqual(Utils.execute_query(sqlite3.connect("Diploma1.db"), f""" SELECT * FROM Rooms WHERE ID>0"""), True)

if __name__ == '__main__':
    unittest.main()