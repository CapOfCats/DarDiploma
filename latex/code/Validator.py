import re
from tkinter import messagebox

import Utils


class Validator:
    def __init__(self, uti):
        self.utils = uti
        self.connection = self.utils.create_connection("Diploma1.db")

    def validation_digits(self,stringVal):
        return re.match(r"^\d{0,3}$", stringVal) is not None

    def validation_text(self, stringVal):
        return re.match(r"^[А-я]{0,}$", stringVal) is not None

    def validation_char(self, stringVal):
        return re.match(r'^[МЖ]?$', stringVal) is not None

    def validation_time(self, stringVal):
        return re.fullmatch(r'^\d{0,6}$', stringVal) is not None

    def FKValid(self, number, tableName):
        element = None
        if tableName == "Doors":
            command = f"""
            SELECT * FROM ({tableName}) WHERE Number = {number}
            """
            element = self.utils.execute_read_query(self.connection, command)
        else:
            element = self.utils.read_single_row(number, self.connection, tableName)
        if element is not None:
            if (len(element)!=0):
                return True
        else:
            return False

    def validate_single(self, element, window, type):
        checkDig = (window.register(self.validation_digits), '%P')
        checkText = (window.register(self.validation_text), "%P")
        checkTime = (window.register(self.validation_time), "%P")
        if type == "Number":
            element.configure (validate="key", validatecommand = checkDig)
        elif type == "Time":
            element.configure(validate="key", validatecommand=checkTime)
        else:
            element.configure(validate="key", validatecommand=checkText)
        return element


    def validate_whole(self, tfS, which, window):
        checkDig = (window.register(self.validation_digits), '%P')
        checkText = (window.register(self.validation_text), "%P")
        checkTime = (window.register(self.validation_time), "%P")
        vcomms = []
        match which:
            case "Пассажиры":
                vcomms = [checkText, checkText, checkDig, checkDig]  # Имя, Фамилия, возраст, комната
            case "Двери":
                vcomms = [checkText, checkDig, checkDig, checkDig]  # Наименование, принадлежность, номер, вместимость
            case "Комнаты":
                vcomms = [checkText, checkTime]  # Наименование, огр. время
            case "Штрафы":
                vcomms = [checkDig, checkDig]  # Сумма выкупа, принадлежность
            case "Дети":
                vcomms = [checkText, checkText, checkDig, checkDig,
                          checkDig]  # имя, фамилия, возраст, комната, сопровождающий
        for i in range(0, len(tfS)):
            tfS[i].configure(validate="key", validatecommand=vcomms[i])
        return tfS

