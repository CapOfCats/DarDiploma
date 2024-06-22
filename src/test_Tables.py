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

    def test_penalty_check(self):
        self.assertEqual(Tables.penalty_check([(1, 'Да', 'Да', 3, 'Загрязнение', 2, '2024-05-15 22:22:09')],"Хулиганство"), True)
        self.assertEqual(Tables.penalty_check([(1, 'Да', 'Нет', 3, 'Загрязнение', 1, '2024-02-15 11:03:12')], "Загрязнение"), False)

    def test_wrong_penalty_check(self):
        self.assertEqual(Tables.penalty_check([(1, 2, 3)],"Хулиганство"), "Not a penalty tuple given")
        self.assertEqual(Tables.penalty_check([(1, 'Да', 'Нет', 3, 'Загрязнение', 1, '2024-02-15 11:03:12')], ""), "Wrong penalty type")
        self.assertEqual(Tables.penalty_check([(1, 'Да', 'Нет', 3, 'Загрязнение', 1, '2024-02-15 11:03:12')], "Поведение - неуд"),"Wrong penalty type")

if __name__ == '__main__':
    unittest.main()