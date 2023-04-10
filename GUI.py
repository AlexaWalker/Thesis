import os
import sys
import binascii
from tkinter import *
from PIL import ImageTk, Image
from tkinter import filedialog
from functools import partial
import re 

offset = 0 
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
        frame1 = self.frame1 = Frame(master=self.parent, width=50, height=720, bg="#D9D9D9")
        frame2 = self.frame2 = Frame(master=self.parent, width=250, height=720, bg="#CCCCCC")
        frame3 = self.frame3 = Frame(master=self.parent, width=780, height=500, bg="blue")
        frame4 = self.frame4 = Frame(master=self.parent, width=800, height=220, bg="#CCCCCC")

        searchFrame = self.searchFrame = Frame(master=self.frame4, width=500, height=29)

        #canvas3 = self.canvas3 = Canvas(master=self.frame3, bg="white", width=780, height=500)

        viewText = self.viewText = Text(master=self.frame3)#width=700)#,  height=500)
        searchLabel = self.searchLabel = Label(self.frame4, anchor="w", padx=5, pady=5, text="Search")
        searchBox = self.searchBox = Text(master=self.searchFrame, font=("Helvetica", 16))
        scrollbar = self.scrollbar = Scrollbar(master=self.frame3)

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
        search_btn = self.search_btn = ImageTk.PhotoImage(Image.open('assets/search_icon.png').resize((27, 27)))


        button1 = self.button1 = Button(frame1, image = file_type_btn, command = partial(self.file_type_button, menu),
        borderwidth = 0)
        button2 = self.button2 = Button(frame1, image = file_btn, command = partial(self.file_button, frame2), borderwidth = 0)
        button_search = self.button_search = Button(searchFrame, image = search_btn, command = partial(self.find),borderwidth=0)


    #Function to create the textbox for the hex/ascii views
    def create_view(self):
        self.viewText.tag_configure("ascii", foreground="green")
        self.viewText.tag_configure("error", foreground="red")
        self.viewText.tag_configure("hexspace", foreground="navy")
        self.viewText.tag_configure("graybg", background="lightgray")
        self.viewText.tag_configure("jpg", background = "purple", foreground = "white")
        self.viewText.tag_configure("null", background = "black", foreground="white")

        self.viewText.bind_all("<MouseWheel>", self.on_mousewheel)

    #Function to add widgets to the display
    def create_layout(self):
        self.parent.geometry("1080x720")
        self.parent.resizable(0, 0)

        self.frame1.grid(row=0, column=0, rowspan=3, columnspan=1, sticky='NS')
        self.frame2.grid(row=0,column=1, rowspan=3, columnspan=2, sticky='NS')
        self.frame3.grid(row=0, column=3, rowspan=2, columnspan=3, sticky='W')
        self.frame4.grid(row=2, column=3, rowspan=1, columnspan=3, sticky='NS')

        self.searchLabel.grid(row=0, column=0, sticky='NW') #frame4
        self.searchFrame.grid(row=0, column=1, sticky='NW') #frame4
        self.searchBox.grid(row=0, column=0) #searchframe
        self.button_search.place(x=471, y=0) #searchframe

        self.frame3.grid_propagate(False)
        self.frame4.grid_propagate(False)
        self.searchFrame.grid_propagate(False)

        self.viewText.grid(row=0, column=0, sticky='NSEW')
        self.viewText.grid_propagate(True)
        self.frame3.grid_columnconfigure(0, weight=1)
        self.frame3.grid_rowconfigure(0, weight=1)

        self.scrollbar.grid(row=0, column=1, sticky='NS')

        self.viewText.config(yscrollcommand=self.scrollbar.set)
        self.scrollbar.config(command=self.viewText.yview)


        self.button1.pack()
        self.button2.pack()


    #Function sets up text box and displays the file in hex-code and ASCII
    def show_block(self):
        global offset
        #self.viewText.delete("1.0", "end")  #Clears textbox
        if not self.filename:  #Finishes function execution if there is no file to open
            return
        with open(self.filename, "rb") as file:
            print(self.filename)
            file.seek(offset, os.SEEK_SET)
            block = file.read(4096)  #Reads file up to 4kb

        rows = [block[i:i + BLOCK_WIDTH] for i in range(0, len(block), BLOCK_WIDTH)] #make rows of BLOCK_WIDTH number of bytes
        #print(rows)
        for row in rows:
            self.show_bytes(row)
            self.show_line(row)
        self.viewText.insert("end", "\n")


    def load(self, mousepos):
        global offset
        if(mousepos == 1):
            offset += 4096
            self.show_block()
            

    # Function to add Hex bytes to the viewText widget
    def show_bytes(self, row):
        for byte in row:
            self.viewText.insert("end", "{:02X}".format(byte))
            self.viewText.insert("end", " ")
        if len(row) < BLOCK_WIDTH:
            self.viewText.insert("end", " " * (BLOCK_WIDTH - len(row)) * 3)


    def show_line(self, row):
        file_type = re.search("Exif", row.decode(self.encoding.get(), errors="replace"))
        if file_type is not None:
            file_type_location = file_type.span()
            print(file_type)

        for char in row.decode(self.encoding.get(), errors="replace"):
            tags = ()

            if char in "\u2028\u2029\t\n\r\v\f\uFFFD":
                char = "."
                tags = ("graybg" if char == "\uFFFD" else "error",)
            elif 0x20 < ord(char) < 0x7F:
                if file_type is not None:
                    if char in row.decode(self.encoding.get(), errors="replace")[file_type_location[0]:file_type_location[1]]:
                        tags = ("jpg",)
                else: tags = ("ascii",)
            elif ord(char) == 0x00:
                char = "-"
                tags = ("null",)
            elif not 0x20 <= ord(char) <= 0xFFFF: # Tcl/Tk limit
                char = "?"
                tags = ("error",)
            self.viewText.insert("end", char, tags)
        self.viewText.insert("end", "\n")
    

    #Function that opens the file selected by the user
    def _open(self, filename):
            global offset
            offset = 0
            self.viewText.delete("1.0", "end")
            if filename and os.path.exists(filename):
                print(filename, "path exists")
                self.parent.title("{} — {}".format(filename, "Gremlin"))
                size = os.path.getsize(filename)
                size = (size - BLOCK_SIZE if size > BLOCK_SIZE else
                        size - BLOCK_WIDTH)
                #self.offsetSpinbox.config(to=max(size, 0))
                self.filename = filename
                self.show_block()
                print("show block")
        
    def open_folder(self, foldername):
        for filename in os.listdir(foldername):
            file_path = os.path.join(foldername, filename)
            self._open(file_path)
            print("opened file")
    
    def find(self):
        self.viewText.tag_remove('found', '1.0', END)
        ser = self.viewText.get("1.0","end-1c")
        if ser:
            idx = '1.0'
            while 1:
                idx = self.viewText.search(ser, idx, nocase=1,
                                stopindex=END)
                if not idx: break
                lastidx = '%s+%dc' % (idx, len(ser))
                
                self.viewText.tag_add('found', idx, lastidx)
                idx = lastidx
            self.viewText.tag_config('found', foreground='blue')
        self.viewText.focus_set()
    
    
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
                #filename = filedialog.askopenfilename()
                foldername = filedialog.askdirectory() 
                #self._open(filename)
                self.open_folder(foldername)
                fileOpen = True

            elif (FILEOPEN == True):
                #filename = filedialog.askopenfilename()
                foldername = filedialog.askdirectory() 
                #self._open(filename)
                self.open_folder(foldername)
                #fileOpen = False
        
    def on_mousewheel(self, event):
        self.viewText.yview_scroll(int(-1*(event.delta/120)), "units")

        if (self.scrollbar.get()[1] == 1.0):
            self.load(1)


app = Tk()
app.title("Gremlin")
window = application(app)
app.resizable(width=False, height=False)
app.mainloop()

