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
    
fileOpen = False
#open file explorer
def file_button(frame2):
    global fileOpen
    global text_box
    if (isOpen==False):
        if (fileOpen == False):
            filename = filedialog.askopenfilename()
            text_box = Text(frame2, width = 34, height = 1)
            text_box.insert("end-1c", filename)
            text_box.pack()
            _open(filename)
            fileOpen = True

        elif (fileOpen == True):
            text_box.pack_forget()
            filename = filedialog.askopenfilename()
            text_box = Text(frame2, width = 34, height = 1)
            text_box.insert("end-1c", filename)
            text_box.pack()
            _open(filename)
            #fileOpen = False

    

