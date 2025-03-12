import customtkinter as ct 
from customtkinter import *

ct.set_appearance_mode("dark")
ct.set_default_theme("dark-blue")


main_window = CTk()
main_window.geometry("600*400 + 200 + 150")
main_window.title("CTKswitch")

def changeMode():
    val = switch.get()
    if val:
        ct.set_appearance_mode("light")
    else:
        ct.set_appearance_mode("dark")

switch = CTkswitch(main_window, text="Dark Mode", command=changeMode,
                   onvalue = 1, offvalue = 0, command=changeMode)
switch.pack(pady=20)
print(switch.get())
main_window.mainloop()
