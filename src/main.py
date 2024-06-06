import Controller
import Utils
import Tables
import customtkinter
from tkinter import *
from tkinter import messagebox
import asyncio

customtkinter.set_appearance_mode("dark")
customtkinter.set_default_color_theme("dark-blue")
isES = False
ck = 0
window = customtkinter.CTk()
window.title('Круиз DB')
window.geometry('600x150')
frame = customtkinter.CTkFrame(
    master=window,
    width=500,
    height=200,
    border_width=2,
    border_color=("cyan"),
    fg_color="black"
)
frame.pack(fill = Y, expand = 1)
controller = Controller.Controller()
utils = Utils.Utils()
tables = Tables.Tables()
window.resizable(False, False)
connection = utils.create_connection("D:\Drova&Utilyty\MSVS\Diploma1.db")

def on_closing():
    if messagebox.askokcancel("Quit", "Do you want to quit?"):
        window.destroy()


ask_lb = customtkinter.CTkLabel(
    master=frame,
    text="Выберите таблицу:",
    width= 30,
    height = 10,
    text_color= "Cyan",
    font= customtkinter.CTkFont(family="Courier new", size=18)
)

psr_btn = customtkinter.CTkButton(
    master=frame,
    width=18,
    height=10,
    text="Пассажиры",
    corner_radius=25,
    border_width=1,
    border_color="cyan",
    hover_color="green",
    bg_color= "black",
    text_color="cyan",
    fg_color= "black",
    font= customtkinter.CTkFont(family="Courier new", size=15),
    command=lambda: controller.show_table("Пассажиры", window, tables, connection)
)

psr_ua_btn = customtkinter.CTkButton(
    master=frame,
    width=18,
    height=10,
    text="Дети",
    corner_radius=25,
    border_width=1,
    border_color="cyan",
    hover_color="green",
    bg_color= "black",
    text_color="cyan",
    fg_color= "black",
    font= customtkinter.CTkFont(family="Courier new", size=15),
    command=lambda: controller.show_table("Дети", window, tables, connection)
)

drs_btn = customtkinter.CTkButton(
    master=frame,
    width=18,
    height=10,
    text="Двери",
    corner_radius=25,
    border_width=1,
    border_color="cyan",
    hover_color="green",
    bg_color= "black",
    text_color="cyan",
    fg_color= "black",
    font= customtkinter.CTkFont(family="Courier new", size=15),
    command=lambda: controller.show_table("Двери", window,tables, connection)
)

rms_btn = customtkinter.CTkButton(
    master=frame,
    width=18,
    height=10,
    text="Комнаты",
    corner_radius=25,
    border_width=1,
    border_color="cyan",
    hover_color="green",
    bg_color= "black",
    text_color="cyan",
    fg_color= "black",
    font= customtkinter.CTkFont(family="Courier new", size=15),
    command=lambda: controller.show_table("Комнаты", window, tables, connection)
)

pns_btn = customtkinter.CTkButton(
    master=frame,
    width=18,
    height=10,
    text="Штрафы",
    corner_radius=25,
    border_width=1,
    border_color="cyan",
    hover_color="green",
    bg_color= "black",
    text_color="cyan",
    fg_color= "black",
    font= customtkinter.CTkFont(family="Courier new", size=15),
    command=lambda: controller.show_table("Штрафы",window, tables, connection)
)
timer_lb = customtkinter.CTkLabel(
    master=frame,
    text="Системное время:",
    width= 30,
    height = 10,
    text_color= "Cyan",
    font= customtkinter.CTkFont(family="Courier new", size=14, weight="bold")
)

ask_lb.pack(side=TOP, pady=15)
timer_lb.pack(side=BOTTOM, pady=2)
psr_btn.pack(side=LEFT, padx=10, pady=2, expand = 1)
psr_ua_btn.pack(side=LEFT, padx=10, pady=2)
drs_btn.pack(side=LEFT, padx=10, pady=2)
rms_btn.pack(side=LEFT, padx=10, pady=2)
pns_btn.pack(side=LEFT, padx=10, pady=2)
window.protocol("WM_DELETE_WINDOW", on_closing)
asyncio.run(utils.asyncStart(window, timer_lb, connection))