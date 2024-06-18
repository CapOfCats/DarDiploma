from tkinter import *
from tkinter import ttk, messagebox
import Validator
import customtkinter

import Utils

utils = Utils.Utils()
validator = Validator.Validator()

class Controller:
    @staticmethod
    def show_acc(connection, isES, tables, window):
        tableWin = customtkinter.CTkToplevel()
        tableWin.title("Праверка доступа")
        tableWin.geometry('1200x600')

        frameWin = customtkinter.CTkFrame(
            master=tableWin,
            width=600,
            height=200,
            border_width=1,
            border_color=("cyan"),
            fg_color="black"
        )
        frameWin.pack(anchor=N, expand=True, fill=BOTH)
        tableWin.resizable(False, False)
        tableWin.grab_set()

        title_lb = customtkinter.CTkLabel(
            master=frameWin,
            width=20,
            height=5,
            text="Проверить доступ:",
            text_color="Cyan",
            font=customtkinter.CTkFont(family="Courier New", size=18)
        )
        title_lb.place(relx=0.4, rely=0.05)

        psr_lb = customtkinter.CTkLabel(
            master=frameWin,
            width=20,
            height=5,
            text="Ребёнок:",
            text_color="Cyan",
            font=customtkinter.CTkFont(family="Consolas", size=17)
        )
        psr_lb.place(relx=0.25, rely=0.35)

        dor_lb = customtkinter.CTkLabel(
            master=frameWin,
            width=20,
            height=5,
            text="Дверь:",
            text_color="Cyan",
            font=customtkinter.CTkFont(family="Consolas", size=17)
        )
        dor_lb.place(relx=0.65, rely=0.35)

        psr_switch = customtkinter.CTkSwitch(
            master=frameWin,
            width= 20,
            height = 8,
            switch_height= 24,
            switch_width= 60,
            border_width= 1,
            fg_color= "green",
            border_color= "cyan",
            button_color= "grey",
            button_hover_color = "aquamarine",
            text_color= "cyan",
            onvalue= "Пассажир",
            offvalue= "Ребёнок",
            text = "Ребёнок",
            font=customtkinter.CTkFont(family="Consolas", size=15),
            command= lambda : Controller.toggle_switch(psr_switch, psr_lb, tables, connection, tree, isES)
        )
        psr_switch.place(relx=0.43, rely=0.2)

        psr_tf = customtkinter.CTkEntry(
            master = frameWin,
            width=100,
            corner_radius=7,
            fg_color="black",
            border_color="cyan",
            border_width=1,
            text_color="cyan",
            font=customtkinter.CTkFont(family="Consolas", size=15)
        )
        psr_tf.place(relx = 0.235, rely =0.45)


        dor_tf = customtkinter.CTkEntry(
            master=frameWin,
            width=100,
            corner_radius=7,
            fg_color="black",
            border_color="cyan",
            border_width=1,
            text_color="cyan",
            font=customtkinter.CTkFont(family="Consolas", size=15)
        )
        dor_tf.place(relx=0.625, rely=0.45)


        acc_btn = customtkinter.CTkButton(
            frameWin,
            width=100,
            text="Проверить доступ",
            corner_radius=15,
            border_width=1,
            border_color="cyan",
            hover_color="green",
            bg_color="black",
            text_color="cyan",
            fg_color="black",
            font=customtkinter.CTkFont(family="Consolas", size=15),
            command=lambda: tables.check_access(validator.validate_single(psr_tf,window,"Number"),  validator.validate_single(dor_tf, window, "Number"), psr_switch, connection, isES)
        )
        acc_btn.place(relx=0.415, rely=0.45)

        tables.start_accesses(connection, psr_switch, isES)
        tree = None
        which = "Доступы"
        if isES:
            which = "ДоступыЧС"
        tree = Controller.TreeCreate(tree, tables.self_definition(which), tableWin, connection)

    @staticmethod
    def toggle_switch(switch, psrlb, tables,connection, tree, isES):
        switch.configure(text=switch.get())
        psrlb.configure(text=switch.get() + ":")
        which = "Доступы"
        if isES:
            which = "ДоступыЧС"
        tables.start_accesses(connection,switch,isES)
        tree = Controller.TreeRefresh(tree, tables.self_definition(which), connection)

    @staticmethod
    def styles_init(st):
        if (not ("Custom.Treeheading.border" in st.element_names())):
            st.element_create("Custom.Treeheading.border", "from", "clam")
        st.layout("Custom.Treeview.Heading", [
            ("Custom.Treeheading.cell", {'sticky': 'nswe'}),
            ("Custom.Treeheading.border", {'sticky': 'nswe', 'children': [
                ("Custom.Treeheading.padding", {'sticky': 'nswe', 'children': [
                    ("Custom.Treeheading.image", {'side': 'right', 'sticky': ''}),
                    ("Custom.Treeheading.text", {'sticky': 'we'})
                ]})
            ]}),
        ])
        st.configure("Custom.Treeview.Heading",
                     background="black", foreground="cyan", relief="flat")
        st.map("Custom.Treeview.Heading",
               relief=[('active', 'groove'), ('pressed', 'sunken')])

    @staticmethod
    def show_table(which,window, tables, connection):
        window.ck = 0
        tableWin = customtkinter.CTkToplevel()
        tableWin.title(which)
        tableWin.geometry('1200x600')

        frameWin = customtkinter.CTkFrame(
            master=tableWin,
            width=600,
            height=200,
            border_width=1,
            border_color=("cyan"),
            fg_color="black"
        )
        frameWin.pack(anchor=N, expand=True, fill=BOTH)
        tableWin.resizable(False, False)
        tableWin.grab_set()
        combinedControls = (Controller.fields_creation(which, frameWin, window))
        tree = None
        tree = Controller.TreeCreate(tree, tables.self_definition(which), tableWin, connection)
        current_lb = customtkinter.CTkLabel(
            master=frameWin,
            width=20,
            height=5,
            text="??",
            text_color="Cyan",
            font=customtkinter.CTkFont(family="Consolas", size=18)
        )

        prev_btn = customtkinter.CTkButton(
            frameWin,
            width=2,
            height=2,
            text="←",
            corner_radius=25,
            border_width=1,
            border_color="cyan",
            hover_color="green",
            bg_color="black",
            text_color="cyan",
            fg_color="black",
            font=customtkinter.CTkFont(family="Courier new", size=15),
            command=lambda: tables.configure_list(False, tables.self_definition(which), combinedControls, current_lb,
                                                  connection, window)
        )

        next_btn = customtkinter.CTkButton(
            frameWin,
            width=2,
            height=2,
            text="→",
            corner_radius=25,
            border_width=1,
            border_color="cyan",
            hover_color="green",
            bg_color="black",
            text_color="cyan",
            fg_color="black",
            font=customtkinter.CTkFont(family="Courier new", size=15),
            command=lambda: tables.configure_list(True, tables.self_definition(which), combinedControls, current_lb,
                                                  connection, window)
        )

        delete_btn = customtkinter.CTkButton(
            frameWin,
            width=15,
            height=3,
            text="УДАЛИТЬ",
            corner_radius=25,
            border_width=1,
            border_color="cyan",
            hover_color="green",
            bg_color="black",
            text_color="cyan",
            fg_color="black",
            font=customtkinter.CTkFont(family="Courier new", size=15),
            command=lambda: tables.delete_element(tables.self_definition(which), window.ck, current_lb,
                                                  combinedControls, tree, connection, window)
        )

        add_btn = customtkinter.CTkButton(
            frameWin,
            width=15,
            height=3,
            text="ДОБАВИТЬ",
            corner_radius=25,
            border_width=1,
            border_color="cyan",
            hover_color="green",
            bg_color="black",
            text_color="cyan",
            fg_color="black",
            font=customtkinter.CTkFont(family="Courier new", size=15),
            command=lambda: tables.add_element(tables.self_definition(which), combinedControls, current_lb, tree,
                                               tableWin, connection, window)
        )

        update_btn = customtkinter.CTkButton(
            frameWin,
            width=15,
            height=3,
            text="ИЗМЕНИТЬ",
            corner_radius=25,
            border_width=1,
            border_color="cyan",
            hover_color="green",
            bg_color="black",
            text_color="cyan",
            fg_color="black",
            font=customtkinter.CTkFont(family="Courier new", size=15),
            command=lambda: tables.update_element(tables.self_definition(which), combinedControls, window.ck, tree,
                                                  connection)
        )
        searchLb = customtkinter.CTkLabel(
            frameWin,
            width=20,
            height=2,
            text="Введите номер для поиска",
            text_color="Cyan",
            font=customtkinter.CTkFont(family="Consolas", size=14)
        )

        searchTf = customtkinter.CTkEntry(
            frameWin,
            width=10,
            corner_radius=7,
            fg_color="black",
            border_color="cyan",
            border_width=1,
            text_color="cyan",
            font=customtkinter.CTkFont(family="Consolas", size=15)
        )

        search_btn = customtkinter.CTkButton(
            frameWin,
            width=15,
            height=3,
            text="НАЙТИ",
            corner_radius=25,
            border_width=1,
            border_color="cyan",
            hover_color="green",
            bg_color="black",
            text_color="cyan",
            fg_color="black",
            font=customtkinter.CTkFont(family="Courier new", size=15),
            command=lambda: tables.search_element(combinedControls, tables.self_definition(which), searchTf, current_lb,
                                                  connection, window)
        )
        grid_coef = round((len(combinedControls[0]) + len(combinedControls[1])) / 2)
        row1_empty_lb = customtkinter.CTkLabel(
            master=frameWin,
            width=1,
            height=10,
            text="",
            text_color="Cyan",
            font=customtkinter.CTkFont(family="Consolas", size=18)
        )
        column2_empty_lb = customtkinter.CTkLabel(
            master=frameWin,
            width=150,
            height=5,
            text="",
            text_color="Cyan",
            font=customtkinter.CTkFont(family="Consolas", size=18)
        )
        fields_multiplier = 0
        if (which == "Двери" or which == "Штрафы"):
            fields_multiplier = 3
            column2_empty_lb.grid(row=2, column=2, pady=10, padx=5)
        row1_empty_lb.grid(row=1, column=1, pady=10, padx=5)
        # prev_btn.grid(row=1, column=grid_coef, pady=10)
        # next_btn.grid(row=1, column=grid_coef + 2, pady=10)
        # current_lb.grid(row=1, column=grid_coef + 1, ipady=5)
        prev_btn.place(relx=0.3, rely=0.05)
        next_btn.place(relx=0.7, rely=0.05)
        current_lb.place(relx=0.5, rely=0.05)
        delete_btn.grid(row=4, column=grid_coef - 1 + fields_multiplier, pady=10, padx=10)
        add_btn.grid(row=4, column=grid_coef + fields_multiplier, pady=10)
        update_btn.grid(row=4, column=grid_coef + 1 + fields_multiplier, pady=10)
        search_btn.grid(row=4, column=grid_coef + 2 + fields_multiplier, pady=10)
        searchLb.grid(row=5, column=grid_coef + fields_multiplier, pady=5, padx=5)
        searchTf.grid(row=6, column=grid_coef + fields_multiplier, pady=5, padx=5, ipadx=15)
    @staticmethod
    def fields_creation(which, frameEx, window):
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
                lenlist = [13, 13, 3, 9, 1, 3, 11, 9, 7,
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
                lbnames = ["Наименование", "Кол-во дверей", "Тип", "Огр.время", "Огр.пол", "Огр.здоровье",
                           "Огр.судимости",
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
                lenlist = [16, 16, 9, 17, 4, 12, 14, 14, 14]
        fields_multiplier = 1
        if (which == "Двери"):
            fields_multiplier = 4
        if (which == "Штрафы"):
            fields_multiplier = 3
        for i in range(0, len(lbnames)):
            lblist.append(customtkinter.CTkLabel(
                master=frameEx,
                text=lbnames[i],
                width=30,
                height=10,
                text_color="Cyan",
                font=customtkinter.CTkFont(family="Courier new", size=15, weight="bold")
            ))
            lblist[i].grid(row=2, column=i + fields_multiplier, pady=12, padx=5)
            if i in combonumbers:
                combolist.append(customtkinter.CTkComboBox(
                    master=frameEx,
                    variable=StringVar(value=""),
                    values=combodict[i],
                    width=lenlist[i],
                    corner_radius=7,
                    border_color="cyan",
                    border_width=1,
                    fg_color="black",
                    button_hover_color="green",
                    dropdown_fg_color="black",
                    dropdown_hover_color="green",
                    dropdown_text_color="cyan",
                    text_color="cyan",
                    font=customtkinter.CTkFont(family="Consolas", size=15),
                    dropdown_font=customtkinter.CTkFont(family="Consolas", size=15)
                ))
                combolist[-1].grid(row=3, column=i + fields_multiplier, pady=5, padx=5, ipadx=lenlist[i] * 3)
            else:
                tflist.append(customtkinter.CTkEntry(
                    master=frameEx,
                    width=lenlist[i],
                    corner_radius=7,
                    fg_color="black",
                    border_color="cyan",
                    border_width=1,
                    text_color="cyan",
                    font=customtkinter.CTkFont(family="Consolas", size=15)
                ))
                tflist[-1].grid(row=3, column=i + fields_multiplier, pady=5, padx=5, ipadx=lenlist[i] * 3)

        validatedTFs = validator.validate_whole(tflist, which, window)
        return (validatedTFs, combolist)

    @staticmethod
    def clear(keyLabel, combinedControls, window):
        keyLabel.configure(text="??")
        for i in range(0, len(combinedControls[0])):
            combinedControls[0][i].delete(0, END)
        for i in range(0, len(combinedControls[1])):
            combinedControls[1][i].set("")
        window.ck = 0
    @staticmethod
    def TreeCreate(tree, table, tableWin, connection):
        if tree != None:
            tree.destroy()
            tree = None
        colnames = []
        colnamesTranslated = []
        match table:
            case "Passengers":
                colnames = ["ID", "Name", "Surname", "Age", "Rate", "Sex", "Room", "Judgements", "Medical_restrictions", "Education", "Qualification"]
                colnamesTranslated = ["Идентификатор", "Имя", "Фамилия", "Возраст", "Тариф", "Пол", "Комната", "Судимости", "Мед.Ограничения", "Образование", "Квалификация"]
            case "Doors":
                colnames = ["ID", "Name", "Room_it_belongs_to", "System_Time", "Number", "Status", "Opening_Speed", "Max_Amount"]
                colnamesTranslated = ["Идентификатор", "Наименование", "Принадлежность", "Системное время", "Номер", "Статус", "Скорость открытия", "Вместимость"]
            case "Rooms":
                colnames = ["ID", "Name", "Door_Amount", "Type", "Time_Restrictions", "Sex_Restrictions", "Med_Restrictions", "Judge_Restrictions", "Penalty_Restrictions", "Age_Restrictions"]
                colnamesTranslated = ["Идентификатор", "Наименование", "Кол-во дверей", "Тип", "Огр.Время", "Огр.Пол", "Огр.Здоровья", "Огр.Судимости", "Огр.Штраф", "Огр.Возраст"]
            case "Penalties":
                colnames = ["ID", "Is_active", "Is_removable", "Remove_wage", "Type", "Belongness", "Time_Created"]
                colnamesTranslated = ["Идентификатор", "Активность", "Возможность снять", "Сумма выкупа", "Тип", "Принадлежность", "Время создания"]
            case "Passengers_Underage":
                colnames = ["ID", "Name", "Surname", "Age", "Rate", "Sex", "Room", "Judgements", "Medical_restrictions", "Sattelite"]
                colnamesTranslated = ["Идентификатор", "Имя", "Фамилия", "Возраст", "Тариф", "Пол", "Комната", "Судимости", "Мед.Ограничения", "Сопровождающий"]
            case "Accesses":
                colnames = ["Psr_ID", "Dor_ID", "Access_age", "Access_sex", "Access_judge", "Access_penalty", "Access_health", "Access_number", "Access_time", "Access_rate"]
                colnamesTranslated = ["Идентификатор пассажира", "Идентификатор двери", "Огр.Возраст", "Огр.Пол", "Огр.Судимости","Огр.Штраф", "Огр.Здоровья", "Огр.Номер", "Огр.Время", "Огр.Тариф"]
            case "Accesses_ES":
                colnames = ["Psr_ID", "Dor_ID", "Does_contain_room", "Access_number", "Access_education", "Access_qualification"]
                colnamesTranslated = ["Идентификатор пассажира", "Идентификатор двери", "Ведёт ли в комнату", "Огр.Номер", "Огр.Образование", "Огр.Квалификация"]
        command = f"""
                        SELECT * FROM {table}
                        """
        cortage = utils.execute_read_query(connection, command)

        treestyle = ttk.Style()
        treestyle.theme_use('clam')
        treestyle.configure(
            "Treeview",
            background="black",
            foreground="cyan",
            fieldbackground="black",
            borderwidth=2,
            bordercolor="cyan"
        )
        treestyle.map('Treeview', background=[('selected', "green")], foreground=[('selected', "cyan")])
        tableWin.bind("<<TreeviewSelect>>", lambda event: tableWin.focus_set())

        headerstyle = ttk.Style()
        Controller.styles_init(headerstyle)
        tree = ttk.Treeview(tableWin, columns=colnames, show="headings", style="Custom.Treeview")
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
    @staticmethod
    def TreeRefresh(tree, table, connection):
        cursor = connection.cursor()
        cursor.execute(f''' SELECT * FROM {table} ''')
        [tree.delete(i) for i in
         tree.get_children()]
        [tree.insert('', 'end', values=row) for row in cursor.fetchall()]

    @staticmethod
    def MoveTo(id, table, combinedControls, currentLb, window, connection):
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