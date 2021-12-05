from PIL import Image, ImageTk

import tkinter as tk
from tkinter import filedialog
import tkinter.font
import time

from utils import *

from Client import send_request

import ecg_analysis


DEFAULT_IMAGE = 'image/blank_pic.jpg'
DEFAULT_FILE = 'image/blank_pic.jpg'


def open_image():
    global var_image
    file_path = filedialog.askopenfilename(
        title='Open Medical Image', filetypes=[('image', '.jpg .png')])
    if file_path != '':
        new_imgpath = Image.open(file_path).resize((300, 200))
        new_img = ImageTk.PhotoImage(new_imgpath)
        l_image.configure(image=new_img)
        l_image.image = new_img

        bs64 = read_file_as_b64(file_path)
        var_image.set(bs64)
    else:
        var_image.set('')


def open_file():

    global var_rate_image
    global rate

    file_path = filedialog.askopenfilename(
        title='Open ECG file', filetypes=[('chart', '.csv')])
    if file_path != '':
        rate.set(ecg_analysis.plot_data(file_path))

        l_rate.configure(text=f'heartrate:{rate.get()}')
        l_rate.text = f'heartrate:{rate.get()}'

        new_imgpath = Image.open('./image/new_image.jpg').resize((300, 200))
        new_img = ImageTk.PhotoImage(new_imgpath)
        l_file.configure(image=new_img)
        l_file.image = new_img

        bs64 = read_file_as_b64(file_path)
        var_rate_image.set(bs64)
    else:
        var_rate_image.set('')


def commit():
    if e_id.get() == '':
        print('Please enter medical record number')
    else:
        T = time.strftime('%Y-%m-%d  %H:%M:%S', time.localtime())
        name, id, TIME, image, rate_image = e_name.get(), int(
            e_id.get()), T, var_image, var_rate_image
        send_request(name, id, rate.get(),image.get(), rate_image.get())


window = tk.Tk()
window.title('Medical Data Analysis')
window.geometry('800x600')

ft = tk.font.Font(family='Arial', size=12,
                  weight=tk.font.BOLD
                  )

tk.Label(window, text='Medical Record Number:', font=ft).place(x=80, y=20)
e_id = tk.Entry(window)
e_id.place(x=250, y=20)


tk.Label(window, text='Patient Name:', font=ft).place(x=80, y=50)
e_name = tk.Entry(window)
e_name.place(x=250, y=50)

rate = tk.StringVar()

tk.Label(window, text='Medical Image:', font=ft).place(x=80, y=500)
tk.Label(window, text='ECG Image:', font=ft).place(x=80, y=300)

b_file = tk.Button(window, text="Select ECG File", command=open_file, font=ft)
b_file.place(x=200, y=110)

l_rate = tk.Label(window, text=f'bpm: ', font=ft)
l_rate.place(x=550, y=300)

b_image = tk.Button(window, text="Select Medical Image", command=open_image, font=ft)
b_image.place(x=200, y=80)

b_commit = tk.Button(window, text="Upload", command=commit, font=ft)
b_commit.place(x=400, y=100)

var_image = tk.StringVar()
var_image.set('')


imgpath = Image.open(DEFAULT_IMAGE).resize((200, 200))
img = ImageTk.PhotoImage(imgpath)
l_image = tk.Label(window, image=img)
l_image.place(x=200, y=380)


var_rate_image = tk.StringVar()


coverpath = Image.open(DEFAULT_FILE).resize((200, 200))
cover = ImageTk.PhotoImage(coverpath)
l_file = tk.Label(window, image=cover)
l_file.place(x=200, y=180)


window.mainloop()
