from Tables import *
import unittest

class TablesTest(unittest.TestCase):
    def test_self_definition(self):
        self.assertEqual(Tables.self_definition("Пассажиры"), "Passengers")
        self.assertEqual(Tables.self_definition("Двери"), "Doors")
        self.assertEqual(Tables.self_definition("Комнаты"), "Rooms")
        self.assertEqual(Tables.self_definition("Штрафы"), "Penalties")
        self.assertEqual(Tables.self_definition("Дети"), "Passengers_Underage")
        self.assertEqual(Tables.self_definition("Доступы"), "Accesses")
        self.assertEqual(Tables.self_definition("ДоступыЧС"), "Accesses_ES")

    def test_invalid_definition(self):
        self.assertEqual(Tables.self_definition("ААААААААААААА"), "Unknown_table")
        self.assertEqual(Tables.self_definition([]), "Invalid table name type")
        self.assertEqual(Tables.self_definition(3), "Invalid table name type")
        self.assertEqual(Tables.self_definition(None), "Invalid table name type")

    def test_timeAppend(self):
        self.assertEqual(Tables.timeAppend("200000"), "20:00:00")
        self.assertEqual(Tables.timeAppend("032914"), "03:29:14")

    def test_invalid_time(self):
        self.assertEqual(Tables.timeAppend(([2], ['a'])), "Invalid time type")
        self.assertEqual(Tables.timeAppend("14"), "Time format error")
        self.assertEqual(Tables.timeAppend("320000"), "Invalid hours")
        self.assertEqual(Tables.timeAppend("238911"), "Invalid minutes")
        self.assertEqual(Tables.timeAppend("232399"), "Invalid seconds")
        self.assertRaises(ValueError, Tables.timeAppend, "*2****")

if __name__ == '__main__':
    unittest.main()