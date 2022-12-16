import os
import sys
import binascii
from tkinter import *
from PIL import ImageTk, Image
from tkinter import filedialog
from functools import partial

BLOCK_WIDTH = 22
BLOCK_HEIGHT = 38
BLOCK_SIZE = BLOCK_WIDTH * BLOCK_HEIGHT
ISOPEN = False
FILEOPEN = False
ENCODINGS = ("ASCII", "UTF-8", "UTF-16", "UTF-32")

class application:

    def __init__(self, parent):
        self.parent = parent
        self.create_variables()
        self.create_widgets()
        self.create_view()
        self.create_layout()
    

    def create_variables(self):
        self.filename = None
        self.encoding = StringVar()
        self.encoding.set(ENCODINGS[0])
    
    #Function to set up the UI
    def create_widgets(self):

        #basic sections of the UI, colours are just like that for now for me to see them easily
        frame1 = self.frame1 = Frame(master=self.parent, width=50, height=720, bg="red")
        frame2 = self.frame2 = Frame(master=self.parent, width=250, height=720, bg="yellow")
        frame3 = self.frame3 = Frame(master=self.parent, width=780, height=500, bg="blue")
        frame4 = self.frame4 = Frame(master=self.parent, width=780, height=220, bg="purple")

        #image sizes for buttons
        pixels_x = 50
        pixels_y = 50

        variable = self.variable = StringVar(frame2)
        self.variable.set("pick something") # default value
        menu = self.menu = OptionMenu(frame2, variable, "one", "two", "three")
        inner_menu = self.inner_menu = OptionMenu(menu, variable, "one1", "two2", "three3")
        menu.config(width=35)


        file_type_btn = self.file_type_btn = ImageTk.PhotoImage(Image.open('assets/file.png').resize((pixels_x, pixels_y)))
        file_btn = self.file_btn = ImageTk.PhotoImage(Image.open('assets/harddrive.png').resize((pixels_x, pixels_y)))


        button1 = self.button1 = Button(frame1, image = file_type_btn, command = partial(self.file_type_button, menu),
        borderwidth = 0)
        button2 = self.button2 = Button(frame1, image = file_btn, command = partial(self.file_button, frame2), borderwidth = 0)


    #Function to create the textbox for the hex/ascii views
    def create_view(self):
        self.viewText = Text(self.parent, height=500, width=780)

    #Function to add widgets to the display
    def create_layout(self):
        self.parent.geometry("1080x720")
        self.parent.resizable(0, 0)

        self.frame1.grid(row=0, column=0, rowspan=3, columnspan=1, sticky=NS)
        self.frame2.grid(row=0,column=1, rowspan=3, columnspan=2, sticky=NS)
        self.viewText.grid(row=0, column=3, rowspan=2, columnspan=3, sticky=NS)
        #self.frame3.grid(row=0, column=3, rowspan=2, columnspan=3, sticky=NS)
        self.frame4.grid(row=2, column=3, rowspan=1, columnspan=3, sticky=NS)

        self.button1.pack()
        self.button2.pack()

    #Function sets up text box and displays the file in hex-code and ASCII
    def show_block(self):
        self.viewText.delete("1.0", "end")  #Clears textbox
        if not self.filename:  #Finishes function execution if there is no file to open
            return
        with open(self.filename, "rb") as file:
            file.seek(0, os.SEEK_SET)
            block = file.read(512)  #Reads file up to specified number of bytes
            print(len(block))
            print("Done")

        rows = [block[i:i + BLOCK_WIDTH] for i in range(0, len(block), BLOCK_WIDTH)] #make rows of BLOCK_WIDTH number of bytes
        for row in rows:
            self.show_bytes(row)
            self.show_line(row)
        self.viewText.insert("end", "\n")
    

    # Function to add bytes to the viewText widget
    def show_bytes(self, row):
        for byte in row:
            self.viewText.insert("end", "{:02X}".format(byte))
            self.viewText.insert("end", " ")
        if len(row) < BLOCK_WIDTH:
            self.viewText.insert("end", " " * (BLOCK_WIDTH - len(row)) * 3)


    def show_line(self, row):
            for char in row.decode(self.encoding.get(), errors="replace"):
                tags = ()
                if char in "\n\t\v\r\f":
                    char = "."
                    tags = ("error",)
                
                elif 0x20 < ord(char) < 0x7F:
                    tags = ("ascii",)
                elif not 0x20 <= ord(char) <= 0xFFFF: 
                    char = "?"
                    tags = ("error",)
                
                self.viewText.insert("end", char, tags)
            self.viewText.insert("end", "\n")
    

    #Function that opens the file selected by the user
    def _open(self, filename):
            if filename and os.path.exists(filename):
                print("path exists")
                self.parent.title("{} — {}".format(filename, "Gremlin"))
                size = os.path.getsize(filename)
                size = (size - BLOCK_SIZE if size > BLOCK_SIZE else
                        size - BLOCK_WIDTH)
                #self.offsetSpinbox.config(to=max(size, 0))
                self.filename = filename
                self.show_block()
    
    
    #Function that makes the file type selector work
    def file_type_button(self, menu):
        #drop down is placeholder for eventual file type selector
        if(ISOPEN == False):
            menu.pack()
            isOpen=True
        elif(ISOPEN==True):
            menu.pack_forget()
            isOpen=False
        

    #Function to make the file selector button work
    def file_button(self, frame2):
        if (ISOPEN==False):
            if (FILEOPEN == False):
                filename = filedialog.askopenfilename()
                text_box = Text(frame2, width = 34, height = 1)
                text_box.insert("end-1c", filename)
                text_box.pack()
                self._open(filename)
                fileOpen = True

            elif (FILEOPEN == True):
                text_box.pack_forget()
                filename = filedialog.askopenfilename()
                text_box = Text(frame2, width = 34, height = 1)
                text_box.insert("end-1c", filename)
                text_box.pack()
                self._open(filename)
                #fileOpen = False


app = Tk()
app.title("Gremlin")
window = application(app)
app.resizable(width=False, height=False)
app.mainloop()

