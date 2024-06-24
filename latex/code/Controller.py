from tkinter import *
from tkinter import ttk, messagebox
import Validator
import customtkinter

import Utils

class Controller:
    def __init__(self, uti, val):
        self.utils = uti
        self.validator = val

    def show_acc(self, connection, isES, tables, window, stylecolors):
        tableWin = customtkinter.CTkToplevel()
        tableWin.title("Проверка доступа")
        tableWin.geometry('1200x600')

        frameWin = customtkinter.CTkFrame(
            master=tableWin,
            width=600,
            height=200,
            border_width=1,
            border_color=(stylecolors[0]),
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
            text_color=stylecolors[0],
            font=customtkinter.CTkFont(family="Courier New", size=18)
        )
        title_lb.place(relx=0.4, rely=0.05)

        psr_lb = customtkinter.CTkLabel(
            master=frameWin,
            width=20,
            height=5,
            text="Ребёнок:",
            text_color=stylecolors[0],
            font=customtkinter.CTkFont(family="Consolas", size=17)
        )
        psr_lb.place(relx=0.25, rely=0.35)

        dor_lb = customtkinter.CTkLabel(
            master=frameWin,
            width=20,
            height=5,
            text="Дверь:",
            text_color=stylecolors[0],
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
            fg_color= stylecolors[1],
            border_color= stylecolors[0],
            button_color= "grey",
            button_hover_color = "aquamarine",
            text_color= stylecolors[0],
            onvalue= "Пассажир",
            offvalue= "Ребёнок",
            text = "Ребёнок",
            font=customtkinter.CTkFont(family="Consolas", size=15),
            command= lambda : self.toggle_switch(psr_switch, psr_lb, tables, connection, tree, isES)
        )
        psr_switch.place(relx=0.43, rely=0.2)

        psr_tf = customtkinter.CTkEntry(
            master = frameWin,
            width=100,
            corner_radius=7,
            fg_color="black",
            border_color=stylecolors[0],
            border_width=1,
            text_color=stylecolors[0],
            font=customtkinter.CTkFont(family="Consolas", size=15)
        )
        psr_tf.place(relx = 0.235, rely =0.45)


        dor_tf = customtkinter.CTkEntry(
            master=frameWin,
            width=100,
            corner_radius=7,
            fg_color="black",
            border_color=stylecolors[0],
            border_width=1,
            text_color=stylecolors[0],
            font=customtkinter.CTkFont(family="Consolas", size=15)
        )
        dor_tf.place(relx=0.625, rely=0.45)


        acc_btn = customtkinter.CTkButton(
            frameWin,
            width=100,
            text="Проверить доступ",
            corner_radius=15,
            border_width=1,
            border_color=stylecolors[0],
            hover_color=stylecolors[1],
            bg_color="black",
            text_color=stylecolors[0],
            fg_color="black",
            font=customtkinter.CTkFont(family="Consolas", size=15),
            command=lambda: tables.check_access(self.validator.validate_single(psr_tf,window,"Number"),  self.validator.validate_single(dor_tf, window, "Number"), psr_switch, connection, isES)
        )
        acc_btn.place(relx=0.415, rely=0.45)

        tables.start_accesses(connection, psr_switch, isES)
        tree = None
        which = "Доступы"
        if isES:
            which = "ДоступыЧС"
        tree = self.TreeCreate(tree, tables.self_definition(which), tableWin, connection, stylecolors)

    def toggle_switch(self, switch, psrlb, tables,connection, tree, isES):
        switch.configure(text=switch.get())
        psrlb.configure(text=switch.get() + ":")
        which = "Доступы"
        if isES:
            which = "ДоступыЧС"
        tables.start_accesses(connection,switch,isES)
        tree = self.TreeRefresh(tree, tables.self_definition(which), connection)

    @staticmethod
    def styles_init(st, stylecolors):
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
                     background="black", foreground=stylecolors[0], relief="flat")
        st.map("Custom.Treeview.Heading",
               relief=[('active', 'groove'), ('pressed', 'sunken')])

    def show_table(self, which,window, tables, connection, stylecolors):
        window.ck = 0
        tableWin = customtkinter.CTkToplevel()
        tableWin.title(which)
        tableWin.geometry('1200x600')

        frameWin = customtkinter.CTkFrame(
            master=tableWin,
            width=600,
            height=200,
            border_width=1,
            border_color=(stylecolors[0]),
            fg_color="black"
        )
        frameWin.pack(anchor=N, expand=True, fill=BOTH)
        tableWin.resizable(False, False)
        tableWin.grab_set()
        combinedControls = (self.fields_creation(which, frameWin, window, stylecolors))
        tree = None
        tree = self.TreeCreate(tree, tables.self_definition(which), tableWin, connection, stylecolors)
        current_lb = customtkinter.CTkLabel(
            master=frameWin,
            width=20,
            height=5,
            text="??",
            text_color=stylecolors[0],
            font=customtkinter.CTkFont(family="Consolas", size=18)
        )

        prev_btn = customtkinter.CTkButton(
            frameWin,
            width=2,
            height=2,
            text="←",
            corner_radius=25,
            border_width=1,
            border_color=stylecolors[0],
            hover_color=stylecolors[1],
            bg_color="black",
            text_color=stylecolors[0],
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
            border_color=stylecolors[0],
            hover_color=stylecolors[1],
            bg_color="black",
            text_color=stylecolors[0],
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
            border_color=stylecolors[0],
            hover_color=stylecolors[1],
            bg_color="black",
            text_color=stylecolors[0],
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
            border_color=stylecolors[0],
            hover_color=stylecolors[1],
            bg_color="black",
            text_color=stylecolors[0],
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
            border_color=stylecolors[0],
            hover_color=stylecolors[1],
            bg_color="black",
            text_color=stylecolors[0],
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
            text_color=stylecolors[0],
            font=customtkinter.CTkFont(family="Consolas", size=14)
        )

        searchTf = customtkinter.CTkEntry(
            frameWin,
            width=10,
            corner_radius=7,
            fg_color="black",
            border_color=stylecolors[0],
            border_width=1,
            text_color=stylecolors[0],
            font=customtkinter.CTkFont(family="Consolas", size=15)
        )

        search_btn = customtkinter.CTkButton(
            frameWin,
            width=15,
            height=3,
            text="НАЙТИ",
            corner_radius=25,
            border_width=1,
            border_color=stylecolors[0],
            hover_color=stylecolors[1],
            bg_color="black",
            text_color=stylecolors[0],
            fg_color="black",
            font=customtkinter.CTkFont(family="Courier new", size=15),
            command=lambda: tables.search_element(combinedControls, tables.self_definition(which), searchTf, current_lb, connection, window)
        )