from tkinter import END, messagebox
import re
import Controller
import Utils
import Validator
utils = Utils.Utils()
validator = Validator.Validator()
controller = Controller.Controller()
class Tables:
    @staticmethod
    def self_definition(which):
        if which == "Пассажиры":
            return "Passengers"
        elif which == "Двери":
            return "Doors"
        elif which == "Комнаты":
            return "Rooms"
        elif which == "Штрафы":
            return "Penalties"
        else:
            return "Passengers_Underage"
    @staticmethod
    def timeAppend(timeString):
        return timeString[0] + timeString[1] + ":" + timeString[2] + timeString[3] + ":" + timeString[4] + timeString[5]

    @staticmethod
    def add_element(table, combinedControls, currentLb, tree, tableWin, connection, window):
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
        if validator.overvalidation(table, combinedControls):
            finallen += len(colnames)
            for i in range(0, finallen):
                if i in baseInsertT:
                    if (combinedControls[0][t].get() != "") and (t != foreign):
                        resultcolls += colnames[i] + ','
                        if (re.match(r"^[А-я]+$", combinedControls[0][t].get())):
                            tfValues += "'" + combinedControls[0][t].get() + "'" + ','
                        elif ((table == "Rooms") & (i == 3) & (combinedControls[0][1].get() != "")):
                            tfValues += "'" + Tables.timeAppend(combinedControls[0][t].get()) + "'" + ','
                        else:
                            tfValues += combinedControls[0][t].get() + ','
                    t += 1
                elif i in baseInsertC:
                    if combinedControls[1][c].get() != "":
                        resultcolls += colnames[i] + ','
                        if (re.match(r"^[А-я]+$", combinedControls[1][c].get())):
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
            newId = utils.execute_read_query(connection, command)[0][0] + 1
            resultcolls += "ID"
            tfValues += f"{newId}"
            command = f"""
                    INSERT INTO {table} ({resultcolls}) VALUES ({tfValues})
                    """
            if (utils.execute_silent(connection, command)):
                command = f"""
                    SELECT COUNT(*) FROM ({table})
                    """
                controller.MoveTo(utils.execute_read_query(connection, command)[0][0], table, combinedControls, currentLb, window, connection)
                tree = controller.TreeRefresh(tree, table, connection)
                messagebox.showinfo("Успех", "Элемент успешно добавлен")
    @staticmethod
    def delete_element(table, key, currentLb, combinedControls, tree, connection, window):
        command = ""
        if key == 0:
            messagebox.showinfo("ОЙ!", "Выберите элемент, который нужно удалить")
        else:
            command = command = f"""
                DELETE FROM {table} Where ID ={key}
                """
            if (utils.execute_silent(connection, command)):
                controller.clear(currentLb, combinedControls, window)
                command = f"""
                            UPDATE {table} SET ID =ID-1 where ID>{key}
                            """
                utils.execute_silent(connection, command)
                messagebox.showinfo('Готово', "Элемент успешно удалён")
                tree = controller.TreeRefresh(tree, table, connection)
    @staticmethod
    def update_element(table, combinedControls, key, tree, connection):
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
        if validator.overvalidation(table, combinedControls):
            finalLen += len(colnames)
            for i in range(0, finalLen):
                if i in baseInsertT:
                    if (combinedControls[0][t].get() != "") and (t != foreign):
                        resultcolls.append(colnames[i])  # ,
                        if (re.match(r"^[А-я]+$", combinedControls[0][t].get())):
                            tfValues.append("'" + combinedControls[0][t].get() + "'" + ',')
                        elif ((table == "Rooms") & (i == 3) & (combinedControls[0][1].get() != "")):
                            tfValues.append("'" + Tables.timeAppend(combinedControls[0][t].get()) + "'" + ',')
                        else:
                            tfValues.append(combinedControls[0][t].get() + ',')
                    t += 1
                elif i in baseInsertC:
                    if combinedControls[1][c].get() != "":
                        resultcolls.append(colnames[i])
                        if (re.match(r"^[А-я]+$", combinedControls[1][c].get())):
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
            if (utils.execute_silent(connection, command)):
                messagebox.showinfo("Успех", "Элемент успешно отредактирован!")
                tree = controller.TreeRefresh(tree, table, connection)
    @staticmethod
    def search_element(combinedControls, table, tf, currentLb, connection, window):
        cortage = utils.read_single_row(int(tf.get()), connection, table)
        if cortage == None:
            messagebox.showwarning("Ошибка", "Элемента с таким id не существует")
        else:
            controller.MoveTo(int(tf.get()), table, combinedControls, currentLb, window, connection)
            messagebox.showinfo("Успех", "Элемент найден")

    @staticmethod
    def updateAccesses(connection, isES):
        command = f"""
                    DELETE FROM Accesses
                    """
        utils.execute_read_query(connection, command)
        command = f"""
                    DELETE FROM Accesses_ES
                    """
        utils.execute_read_query(connection, command)
        tableName = ""
        command = f"""
                SELECT COUNT(*) FROM Passengers
                """
        psrAmount = utils.execute_read_query(connection, command)[0][0]
        command = f"""
                    SELECT COUNT(*) FROM Doors
                    """
        doorsAmount = utils.execute_read_query(connection, command)[0][0]
        command = f"""
                        SELECT * FROM Passengers
                        """
        passengers = utils.execute_read_query(connection, command)
        command = f"""
                            SELECT * FROM Doors
                            """
        doors = utils.execute_read_query(connection, command)
        room = None
        # matches = ["Age","Sex","Judge","Penalty","Health","Number"]
        if not isES:
            tableName = "Accesses"
            for i in range(0, psrAmount):
                for j in range(0, doorsAmount):
                    if doors[j][2] != "":
                        room = utils.read_single_row(int(doors[j][2], connection, "Rooms"))

                        # if(room[9]!=None):
                        # h=0
        else:
            tableName = "Accesses_ES"
    @staticmethod
    def list_table(direction, table, connection, window):
        command = f"""
            SELECT COUNT(*) FROM ({table})
            """
        tableLength = utils.execute_read_query(connection, command)
        if (direction):
            if (window.ck < int(tableLength[0][0])):
                window.ck = window.ck + 1
            else:
                window.ck = 1
        else:
            if (window.ck > 1):
                window.ck = window.ck - 1
            else:
                window.ck = int(tableLength[0][0])
        return utils.read_single_row(window.ck, connection, table)

    @staticmethod
    def configure_list(direction, table, combinedControls, currentLb, connection, window):
        cortage = Tables.list_table(direction, table, connection, window)
        for i in range(0, len(combinedControls[0])):
            combinedControls[0][i].delete(0, END)
        tIndexes = []
        c = 0
        t = 0
        f = None
        valueToIns = ""
        match table:
            case "Rooms":
                roomnum = [1, 2, 3, 4, 5, 6, 7, 8, 9]
                tIndexes = [0, 3]
                if cortage != None:
                    for i in range(0, len(roomnum)):
                        if i != 3:
                            valueToIns = cortage[roomnum[i]]
                            if type(cortage[roomnum[i]]) == type(f):
                                valueToIns = ""
                            if i in tIndexes:
                                combinedControls[0][t].insert(0, valueToIns)
                                t += 1
                            else:
                                combinedControls[1][c].set(valueToIns)
                                c += 1
                    if type(cortage[4]) != type(f):
                        convTime = cortage[4][:2] + cortage[4][3:]
                        convTime = convTime[:4] + convTime[5:]
                        combinedControls[0][1].insert(0, str(convTime))
                    else:
                        combinedControls[0][1].insert(0, "")
            case "Passengers":
                tIndexes = [0, 1, 2, 5]
                if cortage != None:
                    for i in range(0, len(cortage) - 1):
                        valueToIns = cortage[i + 1]
                        if type(cortage[i + 1]) == type(f):
                            valueToIns = ""
                        if i in tIndexes:
                            combinedControls[0][t].insert(0, valueToIns)
                            t += 1
                        else:
                            combinedControls[1][c].set(valueToIns)
                            c += 1
            case "Passengers_Underage":
                tIndexes = [0, 1, 2, 5, 8]
                if cortage != None:
                    for i in range(0, len(cortage) - 1):
                        valueToIns = cortage[i + 1]
                        if type(cortage[i + 1]) == type(f):
                            valueToIns = ""
                        if i in tIndexes:
                            combinedControls[0][t].insert(0, valueToIns)
                            t += 1
                        else:
                            combinedControls[1][c].set(valueToIns)
                            c += 1
            case "Doors":
                doornum = [1, 2, 4, 5, 6, 7]
                tIndexes = [0, 1, 2, 5]
                if cortage != None:
                    for i in range(0, len(doornum)):
                        valueToIns = cortage[doornum[i]]
                        if type(cortage[doornum[i]]) == type(f):
                            valueToIns = ""
                        if i in tIndexes:
                            combinedControls[0][t].insert(0, valueToIns)
                            t += 1
                        else:
                            combinedControls[1][c].set(valueToIns)
                            c += 1
            case "Penalties":
                tIndexes = [2, 4]
                if cortage != None:
                    for i in range(0, len(cortage) - 2):
                        valueToIns = cortage[i + 1]
                        if type(cortage[i + 1]) == type(f):
                            valueToIns = ""
                        if i in tIndexes:
                            combinedControls[0][t].insert(0, valueToIns)
                            t += 1
                        else:
                            combinedControls[1][c].set(valueToIns)
                            c += 1
        if cortage != None:
            currentLb.configure(text=f"{cortage[0]}")
            window.ck = cortage[0]
        else:
            messagebox.showinfo('Ой!', "Таблица пуста. Для пролистывания нужно её заполнить.")

