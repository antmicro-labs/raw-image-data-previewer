import tkinter as tk
from tkinter.filedialog import askopenfilename
from .core import (load_image, get_displayable)
from .image.color_format import AVAILABLE_FORMATS
from PIL import Image, ImageTk


class MainWindow(tk.Frame):
    def __init__(self, args, master=tk.Tk()):
        tk.Frame.__init__(self, master)
        self.master = master
        self.pack()
        self.imgtk = None
        self.createWidgets(args)
        self.path_to_File = args["FILE_PATH"]
        self.update_image()

    def open_file(self):
        self.path_to_File = askopenfilename(filetypes=[("All Files", "*.*")])
        if not os.path.isfile(args["FILE_PATH"]):
            raise Exception("Given path does not lead to a file")

    def update_image(self):
        resolution = [int(self.ent_width.get()), int(self.ent_width.get())]
        img = load_image(self.path_to_File, self.v.get(), resolution)
        im = Image.fromarray(get_displayable(img))
        self.imgtk = ImageTk.PhotoImage(image=im)

    def createWidgets(self, args):
        frm_control = tk.Frame(master=self, width=300, height=800)
        frm_control.pack(fill=tk.BOTH, side=tk.LEFT, expand=True)
        frm_image = tk.Frame(master=self, width=900)
        frm_image.pack(fill=tk.BOTH, side=tk.LEFT, expand=True)

        btn_read = tk.Button(master=frm_control,
                             width=20,
                             height=3,
                             text="Read data from file",
                             command=self.open_file)
        btn_read.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        optionList = list(AVAILABLE_FORMATS.keys())
        self.v = tk.StringVar(frm_control)

        for index in range(0, len(optionList)):
            if args["color_format"] == optionList[index]:
                self.v.set(optionList[index])

        opt_color_formats = tk.OptionMenu(frm_control, self.v, *optionList)
        opt_color_formats.config(width=18, height=2)
        opt_color_formats.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        btn_color_description = tk.Button(master=frm_control,
                                          width=20,
                                          height=3,
                                          text="Color format descripiton")
        btn_color_description.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        frm_size = tk.Frame(master=frm_control, width=20, height=3)
        self.ent_width = tk.Entry(master=frm_size, width=10)

        self.ent_width.insert(0, args["resolution"][0])
        self.ent_height = tk.Entry(master=frm_size, width=11)
        self.ent_height.insert(0, args["resolution"][1])
        self.ent_height.pack(fill=tk.BOTH, expand=True, side=tk.LEFT)
        self.ent_width.pack(fill=tk.BOTH, expand=True, side=tk.LEFT)
        frm_size.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        btn_create_color = tk.Button(master=frm_control,
                                     width=20,
                                     height=3,
                                     text="Create a color format")
        btn_create_color.pack(fill=tk.BOTH, expand=True, padx=5, pady=10)

        btn_update_image = tk.Button(master=frm_control,
                                     width=20,
                                     height=3,
                                     text="Update the image preview",
                                     command=self.update_image)
        btn_update_image.pack(fill=tk.BOTH, expand=True, padx=5, pady=10)

        image_label = tk.Label(master=frm_image, image=self.imgtk)
        image_label.pack()
