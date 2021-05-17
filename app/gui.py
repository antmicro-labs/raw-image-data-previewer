import os
import tkinter as tk
import tkinter.font as tkFont
from tkinter.filedialog import askopenfilename

from .canvas import CanvasImage
from .core import (load_image, get_displayable)
from .image.color_format import AVAILABLE_FORMATS
from PIL import Image, ImageTk


class MainWindow(tk.Frame):
    def __init__(self, args, master=tk.Tk()):
        tk.Frame.__init__(self, master)
        self.master = master
        self.master.geometry('1200x600')

        self.bg_color = "#C9C9C9"

        self.photoframe = tk.Frame(self.master)
        self.photoframe.rowconfigure(0, weight=1)
        self.photoframe.columnconfigure(0, weight=1)
        self.photoframe.pack(fill=tk.BOTH, side=tk.LEFT)

        self.pack()
        self.init_width = args["width"]
        self.path_to_File = args["FILE_PATH"]
        self.init_color_format = args["color_format"]
        self.widget_font = tkFont.Font(family='Gill Sans MT',
                                       size=10,
                                       weight=tkFont.NORMAL)
        self.img_tk = None
        self.canvas = None
        if self.path_to_File != None:
            self.canvas = CanvasImage(self.photoframe, self.path_to_File,
                                      self.init_color_format, self.init_width)
            self.canvas.grid(row=0, column=0)
        self.create_widgets(args)

    def open_file(self):
        self.path_to_File = askopenfilename(filetypes=[("All Files", "*")])
        if not os.path.isfile(self.path_to_File):
            raise Exception("Given path does not lead to a file")

    def update_image(self):
        if self.canvas != None:
            self.canvas.destroy()
        self.canvas = CanvasImage(self.photoframe, self.path_to_File,
                                  self.v.get(), int(self.ent_width.get()))
        self.ent_height.delete(0, len(self.ent_height.get()))
        self.ent_width.delete(0, len(self.ent_width.get()))
        self.ent_width.insert(0, self.canvas.imwidth)
        self.ent_height.insert(0, self.canvas.imheight)
        self.canvas.grid()

    def create_widgets(self, args):
        # Main window
        self.master.title('Raw image data previewer')
        self.master.configure(bg=self.bg_color)

        # Control buttons frame
        frm_control = tk.Frame(master=self, width=300, bg=self.bg_color)
        frm_control.pack(fill=tk.BOTH, side=tk.LEFT, expand=True)

        # Read from file button
        btn_read = tk.Button(master=frm_control,
                             width=20,
                             height=3,
                             text="Read data from file",
                             font=self.widget_font,
                             borderwidth=0,
                             command=self.open_file)
        btn_read.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        # Color format option button
        option_list = list(AVAILABLE_FORMATS.keys())
        self.v = tk.StringVar(frm_control)

        for index in range(0, len(option_list)):
            if args["color_format"] == option_list[index]:
                self.v.set(option_list[index])

        opt_color_formats = tk.OptionMenu(frm_control, self.v, *option_list)
        opt_color_formats.config(width=18,
                                 height=2,
                                 font=self.widget_font,
                                 borderwidth=0)
        opt_color_formats.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        # Color description button (UNSUPPORTED)
        btn_color_description = tk.Button(master=frm_control,
                                          width=20,
                                          height=3,
                                          text="Color format descripiton",
                                          font=self.widget_font,
                                          borderwidth=0,
                                          state=tk.DISABLED)
        btn_color_description.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        # Resolution change entry
        frm_size = tk.Frame(master=frm_control,
                            width=20,
                            height=3,
                            bg=self.bg_color)

        frm_width = tk.Frame(master=frm_size, width=10)
        text_width = tk.Label(master=frm_width,
                              text="Width",
                              bg=self.bg_color,
                              font=self.widget_font)
        text_width.pack(fill=tk.BOTH, side=tk.TOP, expand=True)
        frm_width.pack(fill=tk.BOTH, side=tk.LEFT, expand=True, padx=2, pady=5)

        frm_height = tk.Frame(master=frm_size, width=10)
        text_height = tk.Label(master=frm_height,
                               text="Height",
                               bg=self.bg_color,
                               font=self.widget_font)
        text_height.pack(fill=tk.BOTH, side=tk.TOP, expand=True)
        frm_height.pack(fill=tk.BOTH,
                        side=tk.LEFT,
                        expand=True,
                        padx=2,
                        pady=5)

        self.ent_width = tk.Entry(master=frm_width,
                                  width=10,
                                  font=self.widget_font)

        self.ent_height = tk.Entry(master=frm_height,
                                   width=10,
                                   font=self.widget_font)

        if self.path_to_File != None:
            self.ent_width.insert(0, self.canvas.imwidth)
            self.ent_height.insert(0, self.canvas.imheight)
        else:
            self.ent_width.insert(0, 0)
            self.ent_height.insert(0, 0)
        self.ent_height.pack(fill=tk.BOTH, expand=True, side=tk.LEFT)
        self.ent_width.pack(fill=tk.BOTH, expand=True, side=tk.LEFT)
        frm_size.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        # Create color format button (UNSUPPORTED)
        btn_create_color = tk.Button(master=frm_control,
                                     width=20,
                                     height=3,
                                     text="Create a color format",
                                     font=self.widget_font,
                                     borderwidth=0,
                                     state=tk.DISABLED)
        btn_create_color.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        # Update image button
        btn_update_image = tk.Button(master=frm_control,
                                     width=20,
                                     height=3,
                                     text="Update preview",
                                     font=self.widget_font,
                                     command=self.update_image,
                                     borderwidth=0)
        btn_update_image.pack(fill=tk.BOTH,
                              expand=True,
                              side=tk.BOTTOM,
                              padx=5,
                              pady=100)
