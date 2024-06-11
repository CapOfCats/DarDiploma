from tkinter import END, messagebox
import re
import Controller
import Utils
import Validator
import time
utils = Utils.Utils()
validator = Validator.Validator()
controller = Controller.Controller()
class Tables:
    @staticmethod
    def self_definition(which):
        if type(which) is not str:
            return "Invalid table name type"
        if which == "Пассажиры":
            return "Passengers"
        elif which == "Двери":
            return "Doors"
        elif which == "Комнаты":
            return "Rooms"
        elif which == "Штрафы":
            return "Penalties"
        elif which == "Доступы":
            return "Accesses"
        elif which == "ДоступыЧС":
            return "Accesses_ES"
        elif which == "Дети":
            return "Passengers_Underage"
        else:
            return "Unknown_table"
    @staticmethod
    def timeAppend(timeString):
        if type(timeString) is not str:
            return "Invalid time type"
        if type(int(timeString)) is not int:
            raise ValueError
        elif (len(timeString)!=6):
            return  "Time format error"
        elif (int(timeString[0]+timeString[1])>23):
            return "Invalid hours"
        elif (int(timeString[2] + timeString[3]) > 59):
            return "Invalid minutes"
        elif (int(timeString[4] + timeString[5]) > 59):
            return "Invalid seconds"
        return timeString[0] + timeString[1] + ":" + timeString[2] + timeString[3] + ":" + timeString[4] + timeString[5]
    @staticmethod
    def penalty_check(pennies, type):
        allow = True
        if (pennies!=None):
            for penny in pennies:
                if (penny[4] == type):
                    allow = False
        return allow

    @staticmethod
    def check_access(psr_Tf, dor_Tf, switch, connection):
        if (switch.get() == "Пассажир"):
            pastable ="Passengers"
        else:
            pastable ="Passengers_Underage"

        pasFindCommand = f"""
                            SELECT ID FROM {pastable} WHERE ID = {psr_Tf.get()}
                            """
        dorFindCommand = f"""
                                    SELECT ID FROM Doors WHERE ID = {dor_Tf.get()}
                                    """
        if psr_Tf.get() == "":
            messagebox.showwarning(title="Предупреждение", message= "Для проверки доступа пассажира укажите его идентификатор")
        elif dor_Tf.get() == "":
            messagebox.showwarning(title="Предупреждение", message="Для проверки доступа к двери укажите идентификатор двери")
        else:
            if(len(utils.execute_read_query(connection,pasFindCommand)) == 0):
                messagebox.showerror(title="Ошибка", message="Пассажира с таким идентификатором не существует")
            elif(len(utils.execute_read_query(connection,dorFindCommand)) == 0):
                messagebox.showerror(title="Ошибка", message="Двери с таким идентификатором не существует")
            else:
                acccomand = f"""
                            SELECT * FROM Accesses WHERE (Psr_ID = {psr_Tf.get()}) AND (Dor_ID = {dor_Tf.get()}) 
                            """
                access = utils.execute_read_query(connection,acccomand)
                if (len(access[0]) != 0):
                    giveaccess = True
                    for i in range (2,len(access[0])-1):
                        if (access[0][i] == "Нет"):
                            giveaccess = False
                    if giveaccess:
                        messagebox.showinfo(title="Контакт", message= "Доступ разрешён")
                    else:
                        messagebox.showerror(title="Контакт", message="Доступ запрещён")



    @staticmethod
    def start_accesses(connection, psr_switch):
        command = f"""
                      DELETE FROM Accesses
                      """
        utils.execute_silent(connection, command)
        command = f"""
                     DELETE FROM Accesses_ES
                     """
        utils.execute_silent(connection, command)
        pastable = ""
        if (psr_switch.get() == "Пассажир"):
            pastable = "Passengers"
        else:
            pastable = "Passengers_Underage"
        command = f"""
                        SELECT * FROM {pastable}
                        """
        passengers = utils.execute_read_query(connection, command)
        command = f"""
                        SELECT * FROM Doors
                        """
        doors = utils.execute_read_query(connection, command)
        colnames = "Psr_ID" + ',' + "Dor_ID" + ',' +  "Access_age" + ',' + "Access_sex" + ',' + "Access_judge" + ',' + "Access_penalty" + ',' "Access_health" + ',' + "Access_number" + ',' + "Access_time" + ',' + "Access_rate"
        giveaccess = True
        for door in doors:

            if (door[2]!=""):
                room = utils.read_single_row(door[2],connection,"Rooms")
                for passenger in passengers:
                    resultcolls = f"(SELECT ID FROM {pastable} WHERE ID={passenger[0]})" + ',' + f"(SELECT ID FROM Doors WHERE ID={door[0]})" + ','
                    if (room[9] == None):
                        resultcolls+='"' + "Да" + '"' + ','
                    else:
                        if (passenger[3]>=room[9]):
                            resultcolls+='"' + "Да" + '"' + ','
                        else:
                            resultcolls += "Нет" + ',' # на возраст
                            giveaccess = False
                    if (room[5] == None ) or (room[5]==""):
                        resultcolls+='"' + "Да" + '"' + ','
                    else:
                        if (room[5]!=passenger[5]):
                            resultcolls += '"' +"Нет" + '"'+ ','
                            giveaccess = False
                        else:
                            resultcolls+='"' + "Да" + '"' + ',' # на пол
                    if (room[7] == None ) or (room[7]==""):
                        resultcolls+='"' + "Да" + '"' + ','
                    else:
                        if (room[7] ==passenger[7]):
                            resultcolls += '"' +"Нет" + '"'+ ','
                            giveaccess = False
                        else:
                            resultcolls+='"' + "Да" + '"' + ',' # на судимости
                    if (room[8]== None) or (room[8] ==""):
                        resultcolls+='"' + "Да" + '"' + ','
                    else:
                        command = f"""
                                    SELECT * FROM Penalties WHERE Belongness = {passenger[0]}
                                    """
                        if Tables.penalty_check(utils.execute_read_query(connection,command),room[8]):
                            resultcolls+='"' + "Да" + '"' + ','
                        else:
                            resultcolls += '"' +"Нет" + '"'+ ','
                            giveaccess = False# на штрафы
                    if (room[6]== None) or (room[6] ==""):
                        resultcolls+='"' + "Да" + '"' + ','
                    else:
                        if (room[6] == passenger[6]):
                            resultcolls += '"' +"Нет" + '"'+ ','
                            giveaccess = False
                        else:
                            resultcolls+='"' + "Да" + '"' + ',' # на здоровье
                    if (door[4] == "") or (door[4] == None):
                        resultcolls+='"' + "Да" + '"' + ','
                    else:
                        if (door[4]!=passenger[6]):
                            resultcolls += '"' +"Нет" + '"'+ ','
                            giveaccess = False
                        else:
                            resultcolls+='"' + "Да" + '"' + ',' # на номер
                    if (room[4]== None) or (room[4] ==""):
                        resultcolls+='"' + "Да" + '"' + ','
                    else:
                        convTimeR = room[4][:2] + room[4][3:]
                        convTimeR = convTimeR[:4] + convTimeR[5:]
                        t = time.localtime()
                        current_time = time.strftime("%H%M%S", t)
                        if (current_time<convTimeR):
                            resultcolls += '"' +"Нет" + '"'+ ','
                            giveaccess= False
                        else:
                            resultcolls+='"' + "Да" + '"' + ',' # на время
                    if (room[3]=="Служебная"):
                        if (passenger[4]!= "Персонал"):
                            resultcolls += '"' +"Нет" + '"'+ ','
                            giveaccess = False
                    else:
                        resultcolls += '"' + "Да" + '"' + ','

                    lastElementRc = resultcolls[len(resultcolls) - 1]
                    if (lastElementRc == ','):
                        resultcolls = resultcolls[:len(resultcolls)-1]
                    command = f"""
                                        INSERT INTO Accesses ({colnames}) VALUES ({resultcolls})
                                        """

                    utils.execute_silent(connection,command)
            else:
                for passenger in passengers:
                    resultcolls = f"(SELECT ID FROM {pastable} WHERE ID={passenger[0]})" + ',' + f"(SELECT ID FROM Doors WHERE ID={door[0]})" + ','
                    resultcolls += "Да" + ',' + "Да" + ',' + "Да" + ',' + "Да" + ',' + "Да" + ',' + "Да" + ',' + "Да" + ',' + "Да"
                    command = f"""
                                                            INSERT INTO Accesses ({colnames}) VALUES ({resultcolls})
                                                            """

                    utils.execute_silent(connection, command)


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

