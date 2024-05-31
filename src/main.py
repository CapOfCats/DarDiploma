# Press the green button in the gutter to run the script.
import re
import Utils
import Validator
import customtkinter
from tkinter import ttk
from tkinter import *
from tkinter import messagebox
import asyncio

customtkinter.set_appearance_mode("dark")
customtkinter.set_default_color_theme("dark-blue")
isES = False
ck = 0
window = customtkinter.CTk()
window.title('Круиз DB')
window.geometry('700x300')
frame = customtkinter.CTkFrame(
    master=window,
    width=500,
    height=200,
    border_width=2,
    border_color=("aquamarine"),
    fg_color="darkgrey"
)
frame.pack(expand=True)
validator = Validator.Validator()
utils = Utils.Utils()
window.resizable(False, False)
connection = utils.create_connection("D:\Drova&Utilyty\MSVS\Diploma1.db")


def on_closing():
    if messagebox.askokcancel("Quit", "Do you want to quit?"):
        window.destroy()


async def asyncStart():
    while True:
        windowtask = asyncio.create_task(utils.asyncMLoop(window))
        timetask = asyncio.create_task(utils.timetick(timer_lb))
        await windowtask
        await timetask
        command = f"""
                                    UPDATE Doors SET
                                    System_time = (datetime('now','localtime')) ;
                                """
        utils.execute_silent(connection, command)


def updateAccesses():
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


def list_table(direction, table):
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


def configure_list(direction, table, combinedControls, currentLb):
    cortage = list_table(direction, table)
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


def validate_whole(tfS, which):
    checkDig = (window.register(validator.validation_digits), '%P')
    checkText = (window.register(validator.validation_text), "%P")
    checkChar = (window.register(validator.validation_char), "%P")
    checkCharD = (window.register(validator.validation_charD), "%P")
    checkTime = (window.register(validator.validation_time), "%P")
    checkChar2 = (window.register(validator.validation_char2), "%P")
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


def TreeRefresh(tree, table, tableWin):
    cursor = connection.cursor()
    cursor.execute(f''' SELECT * FROM {table} ''')  # запрос данных из таблицы
    [tree.delete(i) for i in
     tree.get_children()]  # получаем строки из treeview и удаляем, дабы исключить повторения содержимого
    [tree.insert('', 'end', values=row) for row in cursor.fetchall()]  # добавляем строки в виджет treeview
    # '', 'end' - новое значение будет добавляться после предыдущего
    # values=row - переменная, хранящая в себе данные извлеченные из бд
    # fetchall - метод,    который забирает список с кортажами значений


def TreeCreate(tree, table, tableWin):
    if tree != None:
        tree.destroy()
        tree = None
    colnames = []
    colnamesTranslated = []
    match table:
        case "Passengers":
            colnames = ["ID", "Name", "Surname", "Age", "Rate", "Sex", "Room", "Judgements", "Medical_restrictions",
                        "Education", "Qualification"]
            colnamesTranslated = ["Идентификатор", "Имя", "Фамилия", "Возраст", "Тариф", "Пол", "Комната", "Судимости",
                                  "Мед.Ограничения",
                                  "Образование", "Квалификация"]
        case "Doors":
            colnames = ["ID", "Name", "Room_it_belongs_to", "System_Time", "Number", "Status", "Opening_Speed",
                        "Max_Amount"]
            colnamesTranslated = ["Идентификатор", "Наименование", "Принадлежность", "Системное время", "Номер",
                                  "Статус", "Скорость открытия", "Вместимость"]
        case "Rooms":
            colnames = ["ID", "Name", "Door_Amount", "Type", "Time_Restrictions", "Sex_Restrictions",
                        "Med_Restrictions",
                        "Judge_Restrictions", "Penalty_Restrictions", "Age_Restrictions"]
            colnamesTranslated = ["Идентификатор", "Наименование", "Кол-во дверей", "Тип", "Огр.Время", "Огр.Пол",
                                  "Огр.Здоровья",
                                  "Огр.Судимости", "Огр.Штраф", "Огр.Возраст"]
        case "Penalties":
            colnames = ["ID", "Is_active", "Is_removable", "Remove_wage", "Type", "Belongness", "Time_Created"]
            colnamesTranslated = ["Идентификатор", "Активность", "Возможность снять", "Сумма выкупа", "Тип",
                                  "Принадлежность", "Время создания"]
        case "Passengers_Underage":
            colnames = ["ID", "Name", "Surname", "Age", "Rate", "Sex", "Room", "Judgements", "Medical_restrictions",
                        "Sattelite"]
            colnamesTranslated = ["Идентификатор", "Имя", "Фамилия", "Возраст", "Тариф", "Пол", "Комната", "Судимости",
                                  "Мед.Ограничения",
                                  "Сопровождающий"]
    command = f"""
                    SELECT * FROM {table}
                    """
    cortage = utils.execute_read_query(connection, command)
    tree = ttk.Treeview(tableWin, columns=colnames, show="headings")
    tree.pack(fill=BOTH, expand=1)
    for i in range(0, len(colnames)):
        tree.heading(colnames[i], text=colnamesTranslated[i])
        tree.column(f"#{i + 1}", stretch=YES, width=50)
    for element in cortage:
        tree.insert("", END, values=element)
    scrollbar = ttk.Scrollbar(tableWin, orient=VERTICAL, command=tree.yview)
    tree.configure(yscroll=scrollbar.set)
    scrollbar.pack(side=RIGHT, fill=Y)
    return tree


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


def MoveTo(id, table, combinedControls, currentLb):
    window.ck = id
    cortage = utils.read_single_row(id, connection, table)
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
    else:
        messagebox.showinfo('Ой!', "Таблица пуста. Для пролистывания нужно её заполнить.")


def add_element(table, combinedControls, currentLb, tree, tableWin):
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
            boundTable = "Rooms"  # "Наименование", "Принадлежность", "Номер", "Статус", "Скорость открытия", "Вместимость"
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
                        "Sattelite"]  # "Имя", "Фамилия", "Возраст", "Тариф", "Пол", "Комната", "Судимости", "Мед.Ограничения","Сопровождающий"
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
                        tfValues += "'" + timeAppend(combinedControls[0][t].get()) + "'" + ','
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
                print("Пробоина")

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
        print(resultcolls)
        print(tfValues)
        command = f"""
                INSERT INTO {table} ({resultcolls}) VALUES ({tfValues})
                """
        if (utils.execute_query(connection, command)):
            command = f"""
                SELECT COUNT(*) FROM ({table})
                """
            MoveTo(utils.execute_read_query(connection, command)[0][0], table, combinedControls, currentLb)
            tree = TreeRefresh(tree, table, tableWin)


def timeAppend(timeString):
    return timeString[0] + timeString[1] + ":" + timeString[2] + timeString[3] + ":" + timeString[4] + timeString[5]


def update_element(table, combinedControls, key, tree, tableWin):
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
                        tfValues.append("'" + timeAppend(combinedControls[0][t].get()) + "'" + ',')
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
                print("Пробоина")

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
                    {preCommand} WHERE ID={window.ck} ;
                """
        print("Привет, это апдейт. Вот мои значения:")
        print(resultcolls)
        print(tfValues)
        if (utils.execute_query(connection, command)):
            messagebox.showinfo("Успех", "Элемент успешно отредактирован!")
            tree = TreeRefresh(tree, table, tableWin)


def search_element(combinedControls, table, tf, currentLb):
    cortage = utils.read_single_row(int(tf.get()), connection, table)
    if cortage == None:
        messagebox.showwarning("Ошибка", "Элемента с таким id не существует")
    else:
        MoveTo(int(tf.get()), table, combinedControls, currentLb)
        messagebox.showinfo("Успех", "Элемент найден")


def clear(keyLabel, combinedControls):
    keyLabel.config(text="?????")
    for i in range(0, len(combinedControls[0])):
        combinedControls[0][i].delete(0, END)
    for i in range(0, len(combinedControls[1])):
        combinedControls[1][i].set("")
    window.ck = 0


def delete_element(table, key, currentLb, combinedControls, tree, tableWin):
    command = ""
    if key == 0:
        messagebox.showinfo("ОЙ!", "Выберите элемент, который нужно удалить")
    else:
        command = command = f"""
            DELETE FROM {table} Where ID ={key}
            """
        if (utils.execute_query(connection, command)):
            clear(currentLb, combinedControls)
            command = f"""
                        UPDATE {table} SET ID =ID-1 where ID>{key}
                        """
            utils.execute_query(connection, command)
            messagebox.showinfo('Готово', "Элемент успешно удалён")
            tree = TreeRefresh(tree, table, tableWin)


def fields_creation(which, frameEx):
    lblist = []
    tflist = []
    lbnames = []
    lenlist = []
    combolist = []
    combodict = []
    combonumbers = []
    match which:
        case "Пассажиры":
            lbnames = ["Имя", "Фамилия", "Возраст", "Тариф", "Пол", "Комната", "Судимости", "Мед.Ограничения",
                       "Образование", "Квалификация"]
            lenlist = [15, 15, 6, 12, 3, 11, 11, 11, 11,
                       3]  # Тариф 3, пол 4,судимости 6, мед 7, образование 8,  квалификация 9
            combonumbers = [3, 4, 6, 7, 8, 9]
            combodict = {
                3: ["Эконом", "Средний", "Бизнес", "Персонал"],
                4: ["М", "Ж"],
                6: ["Убийство", "Домогательства", "Кража", "Хулиганство", "Мошенничество"],
                7: ["Сердце", "Печень", "Легкие", "Моторные", "Желудок"],
                8: ["Инженер", "Медик", "Штурман", "Пловец", "Радист"],
                9: ["1", "2", "3", "4", "5"]
            }
        case "Двери":
            lbnames = ["Наименование", "Принадлежность", "Номер", "Статус", "Скорость открытия", "Вместимость"]
            lenlist = [15, 11, 10, 16, 8, 10]  # Статус 3, скорость открытия 4
            combonumbers = [3, 4]
            combodict = {
                3: ["Открыта", "Закрыта"],
                4: ["1", "2", "3", "4", "5"]
            }
        case "Комнаты":
            lbnames = ["Наименование", "Кол-во дверей", "Тип", "Огр.время", "Огр.пол", "Огр.здоровье", "Огр.судимости",
                       "Огр.штраф", "Огр.возраст"]
            combonumbers = [1, 2, 4, 5, 6, 7, 8]
            lenlist = [10, 10, 10, 10, 10, 10, 10, 10,
                       10]  # Кол-во дверей 1, тип 2, пол 4, здоровье 5, судимости 6, штраф 7, возраст 8
            combodict = {
                1: ["1", "2", "3", "4", "5"],
                2: ['Служебная', "Развлекательная", "Жилая", "Провизионная", "Первоочередная"],
                4: ["М", "Ж"],
                5: ["Сердце", "Печень", "Легкие", "Моторные", "Желудок"],
                6: ["Убийство", "Домогательства", "Кража", "Хулиганство", "Мошенничество"],
                7: ["Загрязнение", "Хулиганство", "ОбманСистемы", "Грубость"],
                8: ["16", "18"]
            }
        case "Штрафы":
            lbnames = ["Активность", "Возможность снять", "Сумма выкупа", "Тип", "Принадлежность"]
            combonumbers = [0, 1, 3]
            lenlist = [5, 5, 8, 20, 14]  # Активность 0, возможность 1, тип 3
            combodict = {
                0: ["Да", "Нет"],
                1: ["Да", "Нет"],
                3: ["Загрязнение", "Хулиганство", "ОбманСистемы", "Грубость"]
            }
        case "Дети":
            lbnames = ["Имя", "Фамилия", "Возраст", "Тариф", "Пол", "Комната", "Судимости", "Мед.Ограничения",
                       "Сопровождающий"]  # Тариф 3, пол 4, судимости 6, мед 7
            combonumbers = [3, 4, 6, 7]
            combodict = {
                3: ["Эконом", "Средний", "Бизнес", "Персонал"],
                4: ["М", "Ж"],
                6: ["Убийство", "Домогательства", "Кража", "Хулиганство", "Мошенничество"],
                7: ["Сердце", "Печень", "Легкие", "Моторные", "Желудок"],
            }
            lenlist = [15, 15, 8, 16, 3, 11, 13, 13, 13]
    for i in range(0, len(lbnames)):
        lblist.append(Label(
            frameEx,
            text=lbnames[i],
        ))
        lblist[i].grid(row=2, column=i + 1, pady=15, padx=7)
        if i in combonumbers:
            combolist.append(ttk.Combobox(
                frameEx,
                textvariable=StringVar(value=""),
                values=combodict[i],
                width=lenlist[i]
            ))
            combolist[-1].grid(row=3, column=i + 1, pady=5, padx=5)
        else:
            tflist.append(Entry(
                frameEx,
                width=lenlist[i],
            ))
            tflist[-1].grid(row=3, column=i + 1, pady=5, padx=5)

    validatedTFs = validate_whole(tflist, which)
    return (validatedTFs, combolist)


def show_table(which):
    window.ck = 0
    tableWin = Toplevel()
    tableWin.title(which)
    tableWin.geometry('1200x600')

    frameWin = Frame(
        tableWin,
        padx=10,
        pady=10
    )
    frameWin.pack(anchor=N, expand=True)
    tableWin.resizable(False, False)
    tableWin.grab_set()
    combinedControls = (fields_creation(which, frameWin))
    tree = None
    tree = TreeCreate(tree, self_definition(which), tableWin)
    current_lb = Label(
        frameWin,
        width=20,
        height=2,
        text="???????",
    )

    prev_btn = Button(
        frameWin,
        width=2,
        height=2,
        text="←",
        command=lambda: configure_list(False, self_definition(which), combinedControls, current_lb)
    )

    next_btn = Button(
        frameWin,
        width=2,
        height=2,
        text="→",
        command=lambda: configure_list(True, self_definition(which), combinedControls, current_lb)
    )

    delete_btn = Button(
        frameWin,
        width=15,
        height=3,
        text="УДАЛИТЬ",
        command=lambda: delete_element(self_definition(which), window.ck, current_lb, combinedControls, tree, tableWin)
    )

    add_btn = Button(
        frameWin,
        width=15,
        height=3,
        text="ДОБАВИТЬ",
        command=lambda: add_element(self_definition(which), combinedControls, current_lb, tree, tableWin)
    )

    update_btn = Button(
        frameWin,
        width=15,
        height=3,
        text="ИЗМЕНИТЬ",
        command=lambda: update_element(self_definition(which), combinedControls, window.ck, tree, tableWin)
    )
    searchLb = Label(
        frameWin,
        width=20,
        height=2,
        text="Введите номер для поиска",
    )

    searchTf = Entry(
        frameWin,
        width=10,
    )

    search_btn = Button(
        frameWin,
        width=15,
        height=3,
        text="НАЙТИ",
        command=lambda: search_element(combinedControls, self_definition(which), searchTf, current_lb)
    )
    grid_coef = round((len(combinedControls[0]) + len(combinedControls[1])) / 2)
    prev_btn.grid(row=1, column=grid_coef, pady=10)
    next_btn.grid(row=1, column=grid_coef + 2, pady=10)
    current_lb.grid(row=1, column=grid_coef + 1, pady=10)
    delete_btn.grid(row=4, column=grid_coef - 1, pady=10, padx=10)
    add_btn.grid(row=4, column=grid_coef, pady=10)
    update_btn.grid(row=4, column=grid_coef + 1, pady=10)
    search_btn.grid(row=4, column=grid_coef + 2, pady=10)
    searchLb.grid(row=5, column=grid_coef, pady=5, padx=5)
    searchTf.grid(row=6, column=grid_coef, pady=5, padx=5)


ask_lb = Label(
    frame,
    text="Выберите таблицу:",
)

psr_btn = Button(
    frame,
    width=18,
    height=2,
    text="Пассажиры",
    command=lambda: show_table("Пассажиры")
)

psr_ua_btn = Button(
    frame,
    text="Дети",
    width=8,
    height=2,
    command=lambda: show_table("Дети")
)

drs_btn = Button(
    frame,
    width=10,
    height=2,
    text="Двери",
    command=lambda: show_table("Двери")
)

rms_btn = Button(
    frame,
    width=14,
    height=2,
    text="Комнаты",
    command=lambda: show_table("Комнаты")
)

pns_btn = Button(
    frame,
    width=12,
    height=2,
    text="Штрафы",
    command=lambda: show_table("Штрафы")
)
timer_lb = Label(
    frame,
    text="Системное время:",
)

ask_lb.pack(side=TOP, pady=15)
timer_lb.pack(side=BOTTOM, pady=2)
psr_btn.pack(side=LEFT, padx=10, pady=2)
psr_ua_btn.pack(side=LEFT, padx=10, pady=2)
drs_btn.pack(side=LEFT, padx=10, pady=2)
rms_btn.pack(side=LEFT, padx=10, pady=2)
pns_btn.pack(side=LEFT, padx=10, pady=2)
window.protocol("WM_DELETE_WINDOW", on_closing)
asyncio.run(asyncStart())
