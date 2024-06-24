from tkinter import END, messagebox
import re
import Controller
import Utils
import Validator
import time
class Tables:
    def __init__(self, uti, val, con):
        self.utils = uti
        self.validator = val
        self.controller = con
    def add_element(self, table, combinedControls, currentLb, tree, tableWin, connection, window):
        colnames = []
        foreign = None
        FColumn = None
        FColumn1 = None
        baseInsertT = []
        baseInsertC = []
        boundTable = ""
        finallen = 0
        match table:
            case "Passengers":
                colnames = ["Name", "Surname", "Age", "Rate", "Sex", "", "Judgements", "Medical_restrictions",
                            "Education", "Qualification", "Room"]
                baseInsertT = [0, 1, 2, 5]
                baseInsertC = [3, 4, 6, 7, 8, 9]
                foreign = 3
                FColumn = "Number"
                boundTable = "Doors"
            case "Doors":
                colnames = ["Name", "", "Number", "Status", "Opening_Speed", "Max_Amount", "Room_it_belongs_to"]
                baseInsertT = [0, 1, 2, 5]
                baseInsertC = [3, 4]
                foreign = 1
                FColumn = "ID"
                boundTable = "Rooms"
            case "Rooms":
                colnames = ["Name", "Door_Amount", "Type", "Time_Restrictions", "Sex_Restrictions", "Med_Restrictions",
                            "Judge_Restrictions", "Penalty_Restrictions", "Age_Restrictions"]
                baseInsertT = [0, 3]
                baseInsertC = [1, 2, 4, 5, 6, 7, 8]
                finallen = 1
            case "Penalties":
                baseInsertT = [2, 4]
                baseInsertC = [0, 1, 3]
                colnames = ["Is_active", "Is_removable", "Remove_wage", "Type", "Belongness"]
                foreign = 1
                FColumn = "ID"
                boundTable = "Passengers"
            case "Passengers_Underage":
                colnames = ["Name", "Surname", "Age", "Rate", "Sex", "Room", "Judgements", "Medical_restrictions",
                            "Sattelite"]
                baseInsertT = [0, 1, 2, 5, 8]
                baseInsertC = [3, 4, 6, 7]
                foreign = 4
                FColumn = "Number"
                FColumn1 = "ID"
                boundTable = "Passengers"
        resultcolls = ''
        tfValues = ''
        t = 0
        c = 0
        if self.validator.overvalidation(table, combinedControls):
            finallen += len(colnames)
            for i in range(0, finallen):
                if i in baseInsertT:
                    if (t != foreign): #combinedControls[0][t].get() != "") and
                        resultcolls += colnames[i] + ','
                        if (re.match(r"^[А-я]+$", combinedControls[0][t].get())) or (combinedControls[0][t].get() == ""):
                            tfValues += "'" + combinedControls[0][t].get() + "'" + ','
                        elif ((table == "Rooms") & (i == 3) & (combinedControls[0][1].get() != "")):
                            tfValues += "'" + self.timeAppend(combinedControls[0][t].get()) + "'" + ','
                        else:
                            tfValues += combinedControls[0][t].get() + ','
                    t += 1
                elif i in baseInsertC:
                    resultcolls += colnames[i] + ','
                    if (re.match(r"^[А-я]+$", combinedControls[1][c].get())) or (combinedControls[1][c].get() == ""):
                        tfValues += "'" + combinedControls[1][c].get() + "'" + ','
                    else:
                        tfValues += combinedControls[1][c].get() + ','
                    c += 1
                else:
                    pass

            if (foreign != None):
                if FColumn1 != None:
                    tfValues += f"(SELECT {FColumn1} FROM {boundTable} WHERE {FColumn1}={combinedControls[0][foreign].get()})" + ','
                else:
                    tfValues += f"(SELECT {FColumn} FROM {boundTable} WHERE {FColumn} = {combinedControls[0][foreign].get()})" + ','  ## Вот тут можно сломать
                resultcolls += colnames[len(colnames) - 1] + ','
            command = f"""
                                SELECT COUNT(*) FROM ({table})
                                """
            newId = self.utils.execute_read_query(connection, command)[0][0] + 1
            resultcolls += "ID"
            tfValues += f"{newId}"
            command = f"""
                    INSERT INTO {table} ({resultcolls}) VALUES ({tfValues})
                    """
            print(command)
            if (self.utils.execute_silent(connection, command)):
                command = f"""
                    SELECT COUNT(*) FROM ({table})
                    """
                self.controller.MoveTo(self.utils.execute_read_query(connection, command)[0][0], table, combinedControls, currentLb, window, connection)
                tree = self.controller.TreeRefresh(tree, table, connection)
                messagebox.showinfo("Успех", "Элемент успешно добавлен")
                self.utils.writeLog(f"В таблицу {Tables.self_definition_reverse(table)} был добавлен новый элемент:")
                self.utils.writeLog('[' + tfValues + ']')

    def delete_element(self, table, key, currentLb, combinedControls, tree, connection, window):
        command = ""
        if key == 0:
            messagebox.showinfo("ОЙ!", "Выберите элемент, который нужно удалить")
        else:
            command = command = f"""
                DELETE FROM {table} Where ID ={key}
                """
            if (self.utils.execute_silent(connection, command)):
                self.controller.clear(currentLb, combinedControls, window)
                command = f"""
                            UPDATE {table} SET ID =ID-1 where ID>{key}
                            """
                self.utils.execute_silent(connection, command)
                messagebox.showinfo('Готово', "Элемент успешно удалён")
                tree = self.controller.TreeRefresh(tree, table, connection)
                self.utils.writeLog(f"Из таблицы {Tables.self_definition_reverse(table)} был удалён элемент №{key}")

    def update_element(self, table, combinedControls, key, tree, connection):
        colnames = []
        foreign = None
        FColumn = None
        FColumn1 = None
        baseInsertT = []
        baseInsertC = []
        boundTable = ""
        finalLen = 0
        match table:
            case "Passengers":
                colnames = ["Name", "Surname", "Age", "Rate", "Sex", "", "Judgements", "Medical_restrictions",
                            "Education", "Qualification", "Room"]
                baseInsertT = [0, 1, 2, 5]
                baseInsertC = [3, 4, 6, 7, 8, 9]
                foreign = 3
                FColumn = "Number"
                boundTable = "Doors"
            case "Doors":
                colnames = ["Name", "", "Number", "Status", "Opening_Speed", "Max_Amount", "Room_it_belongs_to"]
                baseInsertT = [0, 1, 2, 5]
                baseInsertC = [3, 4]
                foreign = 1
                FColumn = "ID"
                boundTable = "Rooms"  # "Наименование", "Принадлежность", "Номер", "Статус", "Скорость открытия", "Вместимость"
            case "Rooms":
                colnames = ["Name", "Door_Amount", "Type", "Time_Restrictions", "Sex_Restrictions", "Med_Restrictions",
                            "Judge_Restrictions", "Penalty_Restrictions", "Age_Restrictions"]
                baseInsertT = [0, 3]
                baseInsertC = [1, 2, 4, 5, 6, 7, 8]
                finalLen = 1
            case "Penalties":
                baseInsertT = [2, 4]
                baseInsertC = [0, 1, 3]
                colnames = ["Is_active", "Is_removable", "Remove_wage", "Type", "Belongness"]
                foreign = 1
                FColumn = "ID"
                boundTable = "Passengers"
            case "Passengers_Underage":
                colnames = ["Name", "Surname", "Age", "Rate", "Sex", "Room", "Judgements", "Medical_restrictions",
                            "Sattelite"]  # "Имя", "Фамилия", "Возраст", "Тариф", "Пол", "Комната", "Судимости", "Мед.Ограничения","Сопровождающий"
                baseInsertT = [0, 1, 2, 5, 8]
                baseInsertC = [3, 4, 6, 7]
                foreign = 4
                FColumn = "Number"
                FColumn1 = "ID"
                boundTable = "Passengers"
        resultcolls = []
        tfValues = []
        t = 0
        c = 0
        if self.validator.overvalidation(table, combinedControls):
            finalLen += len(colnames)
            for i in range(0, finalLen):
                if i in baseInsertT:
                    if  (t != foreign):#(combinedControls[0][t].get() != "") and
                        resultcolls.append(colnames[i])  # ,
                        if (re.match(r"^[А-я]+$", combinedControls[0][t].get())) or  (combinedControls[0][t].get() == ""):
                            tfValues.append("'" + combinedControls[0][t].get() + "'" + ',')
                        elif ((table == "Rooms") & (i == 3) & (combinedControls[0][1].get() != "")):
                            tfValues.append("'" + self.timeAppend(combinedControls[0][t].get()) + "'" + ',')
                        else:
                            tfValues.append(combinedControls[0][t].get() + ',')
                    t += 1
                elif i in baseInsertC:
                    print(combinedControls[1][c].get())
                    #if combinedControls[1][c].get() != "":
                    resultcolls.append(colnames[i])
                    if (re.match(r"^[А-я]+$", combinedControls[1][c].get())) or  (combinedControls[1][c].get() == ""):
                        tfValues.append("'" + combinedControls[1][c].get() + "'" + ',')
                    else:
                        tfValues.append(combinedControls[1][c].get() + ',')
                    c += 1
                else:
                    pass

            if (foreign != None):
                if FColumn1 != None:
                    tfValues.append(
                        f"(SELECT {FColumn1} FROM {boundTable} WHERE {FColumn1}={combinedControls[0][foreign].get()})")
                else:
                    tfValues.append(
                        f"(SELECT {FColumn} FROM {boundTable} WHERE {FColumn} = {combinedControls[0][foreign].get()})")
                resultcolls.append(colnames[len(colnames) - 1])
            lastElementRc = resultcolls[len(resultcolls) - 1]
            lastElementTf = tfValues[len(tfValues) - 1]
            if (lastElementRc[len(lastElementRc) - 1] == ','):
                resultcolls[len(resultcolls) - 1] = lastElementRc[:-1]
            if (lastElementTf[len(lastElementTf) - 1] == ','):
                tfValues[len(tfValues) - 1] = lastElementTf[:-1]
            preCommand = ''
            for i in range(0, len(resultcolls)):
                preCommand += resultcolls[i] + "=" + tfValues[i] + "\n"
            preCommand = preCommand[:-1]
            command = f"""
                        UPDATE {table} SET
                        {preCommand} WHERE ID={key} ;
                    """
            if (self.utils.execute_silent(connection, command)):
                messagebox.showinfo("Успех", "Элемент успешно отредактирован!")
                tree = self.controller.TreeRefresh(tree, table, connection)
                self.utils.writeLog(f"В таблице {self.self_definition_reverse(table)} были изменены данные элемента №{key}. Теперь они выглядят так:")
                self.utils.writeLog('[' + ''.join(tfValues) + ']')