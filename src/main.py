import Controller
import Utils
import Tables
import customtkinter
from tkinter import *
from tkinter import messagebox
import asyncio

import main

customtkinter.set_appearance_mode("dark")
customtkinter.set_default_color_theme("dark-blue")
ck = 0
syscolor = "cyan"
EScolor = "red"
colorToProceed = ""
window = customtkinter.CTk()
window.title('Круиз DB')
window.geometry('600x250')
frame = customtkinter.CTkFrame(
    master=window,
    width=500,
    height=250,
    border_width=2,
    border_color=("cyan"),
    fg_color="black",

)
frame.pack(fill = Y, expand = 1)
controller = Controller.Controller()
utils = Utils.Utils()
tables = Tables.Tables()
window.resizable(False, False)
connection = utils.create_connection("D:\Drova&Utilyty\MSVS\Diploma1.db")
isES = False



ask_lb = customtkinter.CTkLabel(
    master=frame,
    text="Выберите таблицу:",
    width= 30,
    height = 10,
    text_color= syscolor,
    font= customtkinter.CTkFont(family="Courier new", size=18)
)

psr_btn = customtkinter.CTkButton(
    master=frame,
    width=18,
    height=10,
    text="Пассажиры",
    corner_radius=25,
    border_width=1,
    border_color=syscolor,
    hover_color="green",
    bg_color= "black",
    text_color=syscolor,
    fg_color= "black",
    font= customtkinter.CTkFont(family="Courier new", size=16),
    command=lambda: controller.show_table("Пассажиры", window, tables, connection)
)

psr_ua_btn = customtkinter.CTkButton(
    master=frame,
    width=18,
    height=10,
    text="Дети",
    corner_radius=25,
    border_width=1,
    border_color=syscolor,
    hover_color="green",
    bg_color= "black",
    text_color=syscolor,
    fg_color= "black",
    font= customtkinter.CTkFont(family="Courier new", size=16),
    command=lambda: controller.show_table("Дети", window, tables, connection)
)

drs_btn = customtkinter.CTkButton(
    master=frame,
    width=18,
    height=10,
    text="Двери",
    corner_radius=25,
    border_width=1,
    border_color=syscolor,
    hover_color="green",
    bg_color= "black",
    text_color=syscolor,
    fg_color= "black",
    font= customtkinter.CTkFont(family="Courier new", size=16),
    command=lambda: controller.show_table("Двери", window,tables, connection)
)

rms_btn = customtkinter.CTkButton(
    master=frame,
    width=18,
    height=10,
    text="Комнаты",
    corner_radius=25,
    border_width=1,
    border_color=syscolor,
    hover_color="green",
    bg_color= "black",
    text_color=syscolor,
    fg_color= "black",
    font= customtkinter.CTkFont(family="Courier new", size=16),
    command=lambda: controller.show_table("Комнаты", window, tables, connection)
)

pns_btn = customtkinter.CTkButton(
    master=frame,
    width=18,
    height=10,
    text="Штрафы",
    corner_radius=25,
    border_width=1,
    border_color=syscolor,
    hover_color="green",
    bg_color= "black",
    text_color=syscolor,
    fg_color= "black",
    font= customtkinter.CTkFont(family="Courier new", size=16),
    command=lambda: controller.show_table("Штрафы",window, tables, connection)
)
timer_lb = customtkinter.CTkLabel(
    master=frame,
    text="Системное время:",
    width= 30,
    height = 10,
    text_color= syscolor,
    font= customtkinter.CTkFont(family="Courier new", size=16)
)
acs_btn = customtkinter.CTkButton(
    master=frame,
    width=18,
    height=10,
    text="Проверка доступа",
    corner_radius=25,
    border_width=1,
    border_color=syscolor,
    hover_color="green",
    bg_color= "black",
    text_color=syscolor,
    fg_color= "black",
    font= customtkinter.CTkFont(family="Courier new", size=16),
    command=lambda: controller.show_acc(connection, isES, tables, window)
)

ES_switch = customtkinter.CTkSwitch(
        master=frame,
        width= 20,
        height = 8,
        switch_height= 24,
        switch_width= 60,
        border_width= 1,
        fg_color= "green",
        border_color=syscolor,
        button_color= "grey",
        button_hover_color = "aquamarine",
        text_color= syscolor,
        onvalue= "ЧС",
        offvalue= "Штатный",
        text = "Штатный",
        font=customtkinter.CTkFont(family="Consolas", size=15),
    command= lambda : change_state(isES, ES_switch)
)
list_btn = [psr_btn, psr_ua_btn, acs_btn, pns_btn, rms_btn, drs_btn]
ask_lb.pack(side=TOP, pady=15)
acs_btn.pack(side = BOTTOM, pady = 10)
ES_switch.pack(side = BOTTOM, pady = 10)
timer_lb.pack(side=BOTTOM, pady=2)
psr_btn.pack(side=LEFT, padx=10, pady=2, ipadx = 10, ipady = 7)
psr_ua_btn.pack(side=LEFT, padx=10, pady=2, ipadx = 10, ipady = 7)
drs_btn.pack(side=LEFT, padx=10, pady=2, ipadx = 10, ipady = 7)
rms_btn.pack(side=LEFT, padx=10, pady=2, ipadx = 10, ipady = 7)
pns_btn.pack(side=LEFT, padx=10, pady=2, ipadx = 10, ipady = 7)
def on_closing():
    if messagebox.askokcancel("Quit", "Do you want to quit?"):
        window.destroy()

def change_state(isES,switch):
    main.isES = not isES
    fg=""
    switch.configure(text=switch.get())
    if main.isES:
        colorToProceed = EScolor
        fg = "Yellow"
    else:
        colorToProceed = syscolor
        fg = "green"
    for button in list_btn:
        button.configure(border_color=colorToProceed, text_color= colorToProceed)
    ES_switch.configure(border_color=colorToProceed)
    timer_lb.configure(text_color=colorToProceed)
    ask_lb.configure(text_color=colorToProceed)
    frame.configure(border_color=colorToProceed)
    switch.configure(text_color= colorToProceed, border_color= colorToProceed, fg_color= fg)
window.protocol("WM_DELETE_WINDOW", on_closing)
asyncio.run(utils.asyncStart(window, timer_lb, connection))
