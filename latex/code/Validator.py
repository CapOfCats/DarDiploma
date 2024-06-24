import re
from tkinter import messagebox

import Utils


class Validator:
    utils = Utils.Utils()
    connection = utils.create_connection("Diploma1.db")

    @staticmethod
    def validation_digits(stringVal):
        return re.match(r"^\d{0,3}$", stringVal) is not None

    @staticmethod
    def validation_text(stringVal):
        return re.match(r"^[А-я]{0,}$", stringVal) is not None

    @staticmethod
    def validation_char(stringVal):
        return re.match(r'^[МЖ]?$', stringVal) is not None

    @staticmethod
    def validation_time(stringVal):
        return re.fullmatch(r'^\d{0,6}$', stringVal) is not None

    @staticmethod
    def FKValid(number, tableName):
        element = None
        if tableName == "Doors":
            command = f"""
            SELECT * FROM ({tableName}) WHERE Number = {number}
            """
            element = Validator.utils.execute_read_query(Validator.connection, command)
        else:
            element = Validator.utils.read_single_row(number, Validator.connection, tableName)
        if element is not None:
            if (len(element)!=0):
                return True
        else:
            return False

    @staticmethod
    def validate_single(element, window, type):
        checkDig = (window.register(Validator.validation_digits), '%P')
        checkText = (window.register(Validator.validation_text), "%P")
        checkTime = (window.register(Validator.validation_time), "%P")
        if type == "Number":
            element.configure (validate="key", validatecommand = checkDig)
        elif type == "Time":
            element.configure(validate="key", validatecommand=checkTime)
        else:
            element.configure(validate="key", validatecommand=checkText)
        return element


    @staticmethod
    def validate_whole(tfS, which, window):
        checkDig = (window.register(Validator.validation_digits), '%P')
        checkText = (window.register(Validator.validation_text), "%P")
        checkTime = (window.register(Validator.validation_time), "%P")
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

