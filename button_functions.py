from tkinter import *
from PIL import ImageTk, Image
from tkinter import filedialog
#import GUIConcept

isOpen = False
def file_type_button(menu):
    global isOpen
    #drop down is placeholder for eventual file type selector
    if(isOpen == False):
        menu.pack()
        isOpen=True
    elif(isOpen==True):
        menu.pack_forget()
        isOpen=False
    

#open file explorer
def file_button(frame2):
    filename = filedialog.askopenfilename()
    #print(filename)
    text_box = Text(frame2, width = 35, height = 1)
    text_box.insert("end-1c", filename)
    text_box.pack()
