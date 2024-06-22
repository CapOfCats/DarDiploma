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

    @staticmethod
    def overvalidation(table, combinedControls):
        flag = True
        FKs = [6, 2, 5, 9]
        match table:
            case "Passengers":
                warnlistT = ["Имени", "Фамилии", "Возраста",  "Комнаты"]
                warnlistC = ["Тарифа", "Пола"]
                for i in range(0, len(warnlistT)):
                    if (combinedControls[0][i].get() == ""):
                        messagebox.showinfo("ОШИБКА", f"Поле {warnlistT[i]} не должно быть пустым")
                        flag = False
                for i in range(0, len(warnlistC)):
                    if (combinedControls[1][i].get() == ""):
                        messagebox.showinfo("ОШИБКА", f"Поле {warnlistC[i]} не должно быть пустым")
                        flag = False
                if(flag):
                    #print(bool(Validator.FKValid(combinedControls[0][3].get(),"Doors")))
                    #print(combinedControls[0][3].get())
                    if (Validator.FKValid(combinedControls[0][3].get(),"Doors")==False):
                        messagebox.showerror("Ошибка", "Введите корректную ссылку на дверь в комнату")
                        flag=False
                    elif (int(combinedControls[0][2].get()) < 18):
                        messagebox.showerror("Ошибка", "Введите корректный возраст(больше 17)")
                        flag = False
            case "Doors":
                #indexes = [3, 4]
                warnlistT = ["Имени"]
                warnlistC = ["Статуса", "Скорости открытия"]
                for i in range(0, len(warnlistT)):
                    if (combinedControls[0][i].get() == ""):
                        messagebox.showinfo("ОШИБКА", f"Поле {warnlistT[i]} не должно быть пустым")
                        flag = False
                for i in range(0, len(warnlistC)):
                    if (combinedControls[1][i].get() == ""):
                        messagebox.showinfo("ОШИБКА", f"Поле {warnlistC[i]} не должно быть пустым")
                        flag = False
                if(flag):
                    if (Validator.FKValid(combinedControls[0][1].get(),"Rooms")==False):
                        messagebox.showerror("Ошибка", "Введите корректную ссылку на комнату")
                        flag=False
            case "Rooms":
                warnlistT = ["Имени"]
                warnlistC = ["Количества дверей", "Типа"]
                for i in range(0, len(warnlistT)):
                    if (combinedControls[0][i].get() == ""):
                        messagebox.showinfo("ОШИБКА", f"Поле {warnlistT[i]} не должно быть пустым")
                        flag = False
                for i in range(0, len(warnlistC)):
                    if (combinedControls[1][i].get() == ""):
                        messagebox.showinfo("ОШИБКА", f"Поле {warnlistC[i]} не должно быть пустым")
                        flag = False
                if (flag & (combinedControls[0][1].get() != "")):
                    if (len(combinedControls[0][1].get()) < 6):
                        messagebox.showwarning("Ошибка", "Введите корректное значение времени ЧЧММСС")
                        flag = False
                    elif (int(combinedControls[0][1].get()[0] + combinedControls[0][1].get()[1]) > 23):
                        messagebox.showwarning("Ошибка", "Некорректно введены часы")
                        flag = False
                    elif (int(combinedControls[0][1].get()[2] + combinedControls[0][1].get()[3]) > 59):
                        messagebox.showwarning("Ошибка", "Некорректно введены минуты")
                        flag = False
                    elif (int(combinedControls[0][1].get()[4] + combinedControls[0][1].get()[5]) > 59):
                        messagebox.showwarning("Ошибка", "Некорректно введены секунды")
                        flag = False
            case "Penalties":
                indexes = [0, 1, 3, 4]
                warnlistC = ["Активности", "Возможности снятия", "Типа"]
                #warnlistT = ["Принадлежности"] #Вот тут внимание, не подряд индекс идёт
                if (combinedControls[0][1].get() == ""):
                    messagebox.showinfo("ОШИБКА", f"Поле Принадлежности не должно быть пустым")
                    flag = False
                for i in range(0, len(warnlistC)):
                    if (combinedControls[1][i].get() == ""):
                        messagebox.showinfo("ОШИБКА", f"Поле {warnlistC[i]} не должно быть пустым")
                        flag = False
                if(flag):
                    if (Validator.FKValid(combinedControls[0][1].get(), "Passengers") == False):
                        messagebox.showerror("Ошибка", "Введите корректную ссылку на нарушителя")
                        flag = False
            case "Passengers_Underage":
                warnlistT = ["Имени", "Фамилии", "Возраста", "Комнаты", "Сопровождающего"]
                warnlistC = ["Тарифа", "Пола"]
                if (combinedControls[0][4].get() == ""):
                    messagebox.showinfo("ОШИБКА", "Поле Сопровождающего не должно быть пустым")
                    flag = False
                elif((int(combinedControls[0][2].get())>17) | (combinedControls[0][2].get() =="")):
                    messagebox.showerror("Ошибка", "Введите корректный возраст(от 0 до 17)")
                    flag = False
                elif (Validator.FKValid(combinedControls[0][3].get(), "Doors") == False):
                    messagebox.showerror("Ошибка", "Введите корректную ссылку на дверь в комнату")
                    flag = False
                elif (Validator.FKValid(combinedControls[0][4].get(), "Passengers") == False):
                    messagebox.showerror("Ошибка", "Введите корректную ссылку на Сопровождающего")
                    flag = False
                for i in range(0, len(warnlistT)):
                    if (combinedControls[0][i].get() == ""):
                        messagebox.showinfo("ОШИБКА", f"Поле {warnlistT[i]} не должно быть пустым")
                        flag = False
                for i in range(0, len(warnlistC)):
                    if (combinedControls[1][i].get() == ""):
                        messagebox.showinfo("ОШИБКА", f"Поле {warnlistC[i]} не должно быть пустым")
                        flag = False
        return flag
        #Оптимизировать с elif