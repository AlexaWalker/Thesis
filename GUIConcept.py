import os
import sys
import binascii
from tkinter import *
from PIL import ImageTk, Image
from tkinter import filedialog
from functools import partial


data_length = 500
num_cols = 16
BLOCK_HEIGHT = 32
BLOCK_WIDTH = 16
BLOCK_SIZE = 500
ISOPEN = False
FILEOPEN = False
ENCODINGS = ("ASCII", "UTF-8", "UTF-16", "UTF-32")

class application:

    def __init__(self, parent):
        self.parent = parent
        self.create_variables()
        self.create_widgets()
        #self.create_view()
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
        frame3 = self.frame3 = Frame(master=self.parent, width=780, height=500, bg="white")
        canvas3 = self.canvas3 = Canvas(master=frame3, width=780, height=500)
        frame4 = self.frame4 = Frame(master=self.parent, width=800, height=220, bg="purple")

        #setting up the scrollbar 
        scrollbar = self.scrollbar = Scrollbar(master=frame3, orient=VERTICAL, command=canvas3.yview)

        #image sizes for buttons
        pixels_x = 50
        pixels_y = 50

        #drop down menu, eventually to be the file type selector stuff
        variable = self.variable = StringVar(frame2)
        self.variable.set("pick something") # default value
        menu = self.menu = OptionMenu(frame2, variable, "one", "two", "three")
        self.inner_menu = self.inner_menu = OptionMenu(menu, variable, "one1", "two2", "three3")
        menu.config(width=35)

        #buttons
        file_type_btn = self.file_type_btn = ImageTk.PhotoImage(Image.open('assets/file.png').resize((pixels_x, pixels_y)))
        file_btn = self.file_btn = ImageTk.PhotoImage(Image.open('assets/harddrive.png').resize((pixels_x, pixels_y)))

        button1 = self.button1 = Button(frame1, image = file_type_btn, command = partial(self.file_type_button, menu),
        borderwidth = 0)
        button2 = self.button2 = Button(frame1, image = file_btn, command = partial(self.file_button, frame2), borderwidth = 0)


    #Function to create the textbox for the hex/ascii views
    #def create_view(self):
        #viewText = self.viewText = Text(master=self.frame3)#width=700)#,  height=500)


    #Function to add widgets to the display
    def create_layout(self):
        self.parent.geometry("1080x720")
        self.parent.resizable(0, 0)

        self.frame1.grid(row=1, column=0, rowspan=3, columnspan=1, sticky='NS')
        self.frame2.grid(row=1,column=1, rowspan=3, columnspan=2, sticky='NS')
        self.frame3.grid(row=1, column=3, rowspan=2, columnspan=3, sticky='W')
        self.frame4.grid(row=3, column=3, rowspan=1, columnspan=3, sticky='NS')

        self.frame1.propagate(False)

        #frame 3 layout
        self.frame3.grid_propagate(False)
        self.frame3.grid_rowconfigure(0, weight=1)
        self.frame3.grid_columnconfigure(0, weight=1)

        #canvas layout
        #self.canvas3.grid_rowconfigure(0, weight=1)
        #self.canvas3.grid_columnconfigure(0, weight=1)
        self.canvas3.grid(row=0, column=0, sticky="NESW")
        self.grid = Frame(self.canvas3, bg="white")
        self.canvas3.create_window((0, 0), window=self.grid, anchor='nw')


        self.frame4.grid_propagate(False)

        #self.viewText.grid(row=0, column=0, sticky='NSEW')
        self.frame3.grid_columnconfigure(0, weight=1)
        self.frame3.grid_rowconfigure(0, weight=1)

        self.scrollbar.grid(row=0, column=1, sticky='NS')
        self.canvas3.configure(yscrollcommand=self.scrollbar.set)



        self.button1.pack()
        self.button2.pack()


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
            #self.show_block()
            self.show_data()
    
    def show_data(self):
        print("does this even work?")
        #binary_data = self.binary_data = []
        #ascii = 'I feel your presence amongst us You cannot hide in the darkness Can you hear the rumble? Can you hear the rumble that\'s calling? I know your soul is not tainted Even though you\'ve been told so Can you hear the rumble? Can you hear the rumble that\'s calling? I can feel the thunder that\'s breaking in your heart I can see through the scars inside you I can feel the thunder that\'s breaking in your heart I can see through the scars inside you A candle casting a faint glow You and I see eye to eye Can you hear the thunder? How can you hear the thunder that\'s breaking? Now there is nothing between us From now our merge is eternal Can\'t you see that you\'re lost? Can\'t you see that you\'re lost without me? I can feel the thunder that\'s breaking in your heart I can see through the scars inside you I can feel the thunder that\'s breaking in your heart I can see through the scars inside you Can\'t you see that you\'re lost without me? I can feel the thunder that\'s breaking in your heart I can see through the scars inside you I can feel the thunder that\'s breaking in your heart I can see through the scars inside you I can feel the thunder that\'s breaking in your heart I can see through the scars inside you I can feel the thunder that\'s breaking in your heart I can see through the scars inside you'
        with open(self.filename, "rb") as file:
            file.seek(0, os.SEEK_SET)
            binary_data = file.read()

        #binary_data = []
        #for i in range(BLOCK_SIZE):
            #binary_data.append(ord(ascii[i]))
        print(type(binary_data))
        self.bin_data_list = bin_data_list = list(binary_data)   

        hex_labels = []
        for row in range(BLOCK_SIZE // BLOCK_WIDTH):
        # hex output
            for col in range(BLOCK_WIDTH):
                label = Label(self.grid, text=f'{binary_data[row * num_cols + col]:02x}', bg='white')
                label.grid(row=row, column=col)
                hex_labels.append(label)

            # ascii output
            for col in range(BLOCK_WIDTH):
                byte = bin_data_list[row * BLOCK_WIDTH + col]
                ascii_val = chr(byte)
                label = Label(self.grid, text=ascii_val, bg='white')
                label.grid(row=row, column=BLOCK_WIDTH + col + 1)
        
        self.grid.update_idletasks()

        grid_width = sum([hex_labels[i].winfo_width() for i in range(0, BLOCK_WIDTH)])
        row_height = hex_labels[0].winfo_height()
        col_width = hex_labels[0].winfo_width()
        self.canvas3.config(width=col_width * 32 + self.scrollbar.winfo_width(), height=row_height * 16)

        self.canvas3.config(scrollregion=self.canvas3.bbox("all"))
            

    def show_bytes(self, row, col):
        for byte in row:
            self.viewText.insert("end", "{:02X}".format(byte))
            self.viewText.insert("end", " ")

    def show_line(self, row, col):
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
                #text_box = Text(frame2, width = 34, height = 1)
                #text_box.insert("end-1c", filename)
                #text_box.pack()
                self._open(filename)
                fileOpen = True

            elif (FILEOPEN == True):
                #text_box.pack_forget()
                filename = filedialog.askopenfilename()
                #text_box = Text(frame2, width = 34, height = 1)
                #text_box.insert("end-1c", filename)
                #text_box.pack()
                self._open(filename)
                #fileOpen = False

def on_mousewheel(self, event):
    self.canvas3.yview_scroll(event.delta, "units")
    self.canvas3.bind_all("<MouseWheel>", on_mousewheel)


app = Tk()
app.title("Gremlin")
window = application(app)
app.resizable(width=False, height=False)
app.mainloop()

