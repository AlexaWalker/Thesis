import os
import sys
import binascii
from tkinter import *
from PIL import ImageTk, Image
from tkinter import filedialog
from functools import partial


data_length = 500
num_cols = 16
block_pos = 0
BLOCK_HEIGHT = 32
BLOCK_WIDTH = 16
BLOCK_SIZE = 500
ISOPEN = False
FILEOPEN = False

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
        #self.encoding.set(ENCODINGS[0])
    
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
        self.canvas3.bind_all("<MouseWheel>", self.on_mousewheel)

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
            self.show_data(-1)
    
    
    def show_data(self):
        global block_pos
        global data_length
        data_length = 1000

        with open(self.filename, "rb") as file:
            file.seek(block_pos, os.SEEK_SET)
            binary_data = file.read(BLOCK_SIZE)

        self.bin_data_list = bin_data_list = list(binary_data)   
        hex_labels = []

        print(self.scrollbar.get())
        for row in range(BLOCK_SIZE // BLOCK_WIDTH):
        # hex output
            for col in range(BLOCK_WIDTH):
                label = Label(self.grid, text=f'{binary_data[row * num_cols + col]:02X}', bg='white')
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
        #block_pos += BLOCK_SIZE

    def load(self, mousepos):
        global block_pos

        if(mousepos == 1.0):
            block_pos += BLOCK_SIZE
            self.show_data()
        elif(mousepos == 0.0):
            block_pos -= BLOCK_SIZE
            self.show_data()

                  
    
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
        self.canvas3.yview_scroll(int(-1*(event.delta/120)), "units")
        print(self.scrollbar.get())
        if (self.scrollbar.get()[1] == 1.0):
            self.load(1.0)
        elif(self.scrollbar.get()[1] == 0.0):
            self.load(0.0)


app = Tk()
app.title("Gremlin")
window = application(app)
app.resizable(width=False, height=False)
app.mainloop()

