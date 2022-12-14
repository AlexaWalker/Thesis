#GUI Concept with space for both HEX and Ascii views
from tkinter import *
from PIL import ImageTk, Image
import button_functions
from functools import partial


window = Tk()
window.geometry("1080x720")
window.resizable(0, 0)

#basic sections of the UI, colours are just like that for now for me to see them easily
frame1 = Frame(master=window, width=50, height=720, bg="red")
frame2 = Frame(master=window, width=250, height=720, bg="yellow")
frame3 = Frame(master=window, width=390, height=500, bg="blue")
frame4 = Frame(master=window, width=390, height=500, bg="green")
frame5 = Frame(master=window, width=780, height=220, bg="purple")

frame1.grid(row=0, column=0, rowspan=3, columnspan=1, sticky=NS)
frame2.grid(row=0, column=1, rowspan=3, columnspan=2, sticky=NS)
frame3.grid(row=0, column=2, rowspan=2, columnspan=3)
frame4.grid(row=0, column=4, rowspan=2, columnspan=3, sticky=E)
frame5.grid(row=2, column=3, rowspan=1, columnspan=3)


#image for file type selection
pixels_x = 50
pixels_y = 50


variable = StringVar(frame2)
variable.set("pick something") # default value
menu = OptionMenu(frame2, variable, "one", "two", "three")
inner_menu = OptionMenu(menu, variable, "one1", "two2", "three3")
menu.config(width=35)

file_type_btn = ImageTk.PhotoImage(Image.open('assets/file.png').resize((pixels_x, pixels_y)))
file_btn = ImageTk.PhotoImage(Image.open('assets/harddrive.png').resize((pixels_x, pixels_y)))


button1 = Button(frame1, image = file_type_btn, command = partial(button_functions.file_type_button, menu),
borderwidth = 0)
button2 = Button(frame1, image = file_btn, command = partial(button_functions.file_button, frame2), borderwidth = 0)

button1.pack()
button2.pack()



window.mainloop()
