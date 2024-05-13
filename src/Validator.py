import re
from tkinter import messagebox

import Utils


class Validator:
    utils = Utils.Utils()
    connection = utils.create_connection("D:\Drova&Utilyty\MSVS\Diploma1.db")
    @staticmethod
    def setMask(self,mask,strValue):
        return re.match(mask, strValue)

    @staticmethod
    def validation_digits(stringVal):
        return re.match(r"^\d{0,2}$", stringVal) is not None

    @staticmethod
    def validation_text(stringVal):
        return re.match(r"^[А-я]{0,}$", stringVal) is not None

    @staticmethod
    def validation_char(stringVal):
        return re.match(r'^[МЖ]?$', stringVal) is not None

    @staticmethod
    def validation_char2(stringVal):
        return re.match(r'^[ОЗ]?$', stringVal) is not None

    @staticmethod
    def validation_charD(stringVal):
        return re.match(r'^[0-9]?$', stringVal) is not None

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
        if (element is not None):
            return True
        else:
            return False

    @staticmethod
    def overvalidation(table, tfS):
        flag = True
        FKs = [6, 2, 5, 9]
        match table:
            case "Passengers":
                warnlist = ["Имени", "Фамилии", "Возраста", "Тарифа", "Пола", "Комнаты"]
                for i in range(0, 6):
                    if (tfS[i].get() == ""):
                        messagebox.showinfo("ОШИБКА", f"Поле {warnlist[i]} не должно быть пустым")
                        flag = False
                if(flag):
                    if (Validator.FKValid(tfS[5].get(),"Doors")==False):
                        messagebox.showerror("Ошибка", "Введите корректную ссылку на дверь в комнату")
                        flag=False
                    elif (int(tfS[2].get()) < 18):
                        messagebox.showerror("Ошибка", "Введите корректный возраст(больше 17)")
                        flag = False
            case "Doors":
                indexes = [0, 3, 4]
                warnlist = ["Имени", "Статуса", "Скорости открытия"]
                for i in range(0, 3):
                    if (tfS[indexes[i]].get() == ""):
                        messagebox.showinfo("ОШИБКА", f"Поле {warnlist[i]} не должно быть пустым")
                        flag = False
                if(flag):
                    if (Validator.FKValid(tfS[1].get(),"Rooms")==False):
                        messagebox.showerror("Ошибка", "Введите корректную ссылку на комнату")
                        flag=False

                # if (tfS[3].get()[0] != 0 & tfS[3].get()[0] != 1 & tfS[3].get()[0] != 2):
                #  messagebox.showwarning("Ошибка", "Введите корректное значение времени ЧЧММСС")
                #  return
                # elif (tfS[3].get()[1] != 0 & tfS[3].get()[1] != 1 & tfS[3].get()[1] != 2 & tfS[3].get()[1] != 3):
                #     messagebox.showwarning("Ошибка", "Введите корректное значение времени ЧЧММСС")
                #     return
                # elif (tfS[3].get()[2] != 0 & tfS[3].get()[2] != 1 & tfS[3].get()[2] != 2 & tfS[3].get()[2] != 3 &
                #       tfS[3].get()[2] != 4 & tfS[3].get()[2] != 5):
                #     messagebox.showwarning("Ошибка", "Введите корректное значение времени ЧЧММСС")
                #     return
                # elif (tfS[3].get()[4] != 0 & tfS[3].get()[4] != 1 & tfS[3].get()[4] != 2 & tfS[3].get()[4] != 3 &
                #       tfS[3].get()[4] != 4 & tfS[3].get()[4] != 5):
                #     messagebox.showwarning("Ошибка", "Введите корректное значение времени ЧЧММСС")
                #     return
                # else:
                #     resultcolls += colnames[len(colnames) - 1]
                #    tfValues += timeAppend(tfS[3].get())
            case "Rooms":
                warnlist = ["Имени", "Количества дверей", "Типа"]
                for i in range(0, 3):
                    if (tfS[i].get() == ""):
                        messagebox.showinfo("ОШИБКА", f"Поле {warnlist[i]} не должно быть пустым")
                        flag = False
                    if (flag & (tfS[3].get() != "")):
                        if (len(tfS[3].get()) < 6):
                            messagebox.showwarning("Ошибка", "Введите корректное значение времени ЧЧММСС")
                            flag = False
                        elif (int(tfS[3].get()[0] + tfS[3].get()[1]) > 23):
                            messagebox.showwarning("Ошибка", "Некорректно введены часы")
                            flag = False
                        elif (int(tfS[3].get()[2] + tfS[3].get()[3]) > 59):
                            messagebox.showwarning("Ошибка", "Некорректно введены минуты")
                            flag = False
                        elif (int(tfS[3].get()[4] + tfS[3].get()[5]) > 59):
                            messagebox.showwarning("Ошибка", "Некорректно введены секунды")
                            flag = False
            case "Penalties":
                indexes = [0, 1, 3, 4]
                warnlist = ["Активности", "Возможности снятия", "Типа", "Принадлежности"]
                for i in range(0, 4):
                    if (tfS[indexes[i]].get() == ""):
                        messagebox.showinfo("ОШИБКА", f"Поле {warnlist[i]} не должно быть пустым")
                        flag = False
                if(flag):
                    if (Validator.FKValid(tfS[4].get(), "Passengers") == False):
                        messagebox.showerror("Ошибка", "Введите корректную ссылку на нарушителя")
                        flag = False
            case "Passengers_Underage":
                warnlist = ["Имени", "Фамилии", "Возраста", "Тарифа", "Пола", "Комнаты", "Сопровождающего"]
                if (tfS[8].get() == ""):
                    messagebox.showinfo("ОШИБКА", "Поле Сопровождающего не должно быть пустым")
                    flag = False
                elif((int(tfS[2].get())>17) | (tfS[2].get() =="")):
                    messagebox.showerror("Ошибка", "Введите корректный возраст(от 0 до 17)")
                    flag = False
                elif (Validator.FKValid(tfS[5].get(), "Doors") == False):
                    messagebox.showerror("Ошибка", "Введите корректную ссылку на дверь в комнату")
                    flag = False
                elif (Validator.FKValid(tfS[8].get(), "Passengers") == False):
                    messagebox.showerror("Ошибка", "Введите корректную ссылку на Сопровождающего")
                    flag = False
                for i in range(0, 6):
                    if (tfS[i].get() == ""):
                        messagebox.showinfo("ОШИБКА", f"Поле {warnlist[i]} не должно быть пустым")
                        flag = False
        return flag