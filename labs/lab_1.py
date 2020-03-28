"""
1. Розробити программу для  виконання ввода/вивода зображень
   в заданих растрових графічних форматах
   та типових операцій фільтрації  над цими зображеннями.
   Вивести на формі параметри зображення. (which?)
2. Програма повина допускати пряме та зворотне перетворення зображення
   та зміну його якості (роздільної здатності, роздільне масштабування
   по 2-х координатах - Х, Y) - від 1/2...4
3. Для оформлення програми використати пакет TkInter.

from: PNG
to: BMP
operation: EMBOSS
"""
import tkinter as tk
from PIL import Image, ImageFilter, ImageTk
from tkinter import filedialog

from pathlib import Path

ROOT = Path(__file__).parent.parent
DATA_DIR = ROOT / 'data'


class ImageProcessor(tk.Frame):
    open_btn: tk.Button
    transform_btn: tk.Button
    filter_btn: tk.Button
    save_btn: tk.Button

    scale_x_label: tk.Label
    scale_x: tk.Scale
    scale_y_label: tk.Label
    scale_y: tk.Scale

    image: Image
    image_label: tk.Label

    statusbar: tk.Label

    MIN_SCALE = 0.5
    MAX_SCALE = 4

    def __init__(self, master):
        super().__init__(master)
        self.master = master
        self.pack(expand=1, fill=tk.BOTH)
        # Setup buttons
        self.open_btn = tk.Button(self, text='Open image', command=self.open)
        self.transform_btn = tk.Button(
            self, text='Transform image', command=self.transform, state=tk.DISABLED,
        )
        self.filter_btn = tk.Button(
            self, text='Filter image', command=self.filter, state=tk.DISABLED,
        )
        self.save_btn = tk.Button(
            self, text='Save image', command=self.save, state=tk.DISABLED,
        )

        self.open_btn.grid(row=0, column=0)
        self.transform_btn.grid(row=0, column=1)
        self.filter_btn.grid(row=0, column=2)
        self.save_btn.grid(row=0, column=3)

        # Setup scale labels
        self.scale_x_label = tk.Label(self, text='X scale: ')
        self.scale_y_label = tk.Label(self, text='Y scale: ')
        self.scale_x = tk.Scale(
            self, from_=self.MIN_SCALE, to=self.MAX_SCALE,
            resolution=-1, orient=tk.HORIZONTAL
        )
        self.scale_y = tk.Scale(
            self, from_=self.MIN_SCALE, to=self.MAX_SCALE,
            resolution=-1, orient=tk.HORIZONTAL
        )
        self.scale_x_label.grid(row=1, column=0)
        self.scale_x.grid(row=1, column=1)
        self.scale_y_label.grid(row=1, column=2)
        self.scale_y.grid(row=1, column=3)

        # Setup image label
        self.image_label = tk.Label(self)
        self.image_label.grid(row=2, columnspan=4, sticky="ew")
        self.grid_rowconfigure(2, weight=1)

        # Setup status-bar
        self.statusbar = tk.Label(
            self, bd=1, relief=tk.SUNKEN, anchor=tk.W,
        )
        self.statusbar.grid(row=3, column=0, columnspan=4, sticky="ew")

    def update_image_label(self):
        self.update_statusbar()
        tk_img = ImageTk.PhotoImage(self.image)
        self.image_label.config(image=tk_img)
        self.image_label.image = tk_img

    def update_statusbar(self):
        image = self.image
        self.statusbar.config(text=f'{image.format=}, {image.size=}')
        self.statusbar.update_idletasks()

    def open(self):
        source_filename = filedialog.askopenfilename(
            title='Open',
            initialdir=DATA_DIR,
            filetypes=[("Image files", ".png .bmp")],
        )
        self.image = Image.open(source_filename)
        self.update_image_label()

        self.save_btn['state'] = tk.NORMAL
        self.transform_btn['state'] = tk.NORMAL
        self.filter_btn['state'] = tk.NORMAL

    def save(self):
        dest_filename = filedialog.asksaveasfilename(
            title='Save as',
            initialdir=DATA_DIR,
            filetypes=[("Image files", ".png .bmp")],
        )
        self.image.save(dest_filename)

    def transform(self):
        x, y = self.image.size
        new_x, new_y = int(x * self.scale_x.get()), int(y * self.scale_y.get())
        self.image = self.image.resize((new_x, new_y))
        self.update_image_label()

    def filter(self):
        self.image = self.image.filter(ImageFilter.EMBOSS)
        self.update_image_label()


if __name__ == '__main__':
    app = tk.Tk()
    ImageProcessor(app)

    app.title("Image Loader")
    app.geometry("700x700+300+150")
    app.resizable(width=True, height=True)

    app.mainloop()
