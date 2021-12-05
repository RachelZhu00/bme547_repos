import tkinter as tk
from tkinter import ttk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
from datetime import datetime
from monitor_client import *
import base64
from utils import *

def load_and_resize_image(filename):
    """ Creates a tkinter image variable that can be displayed on GUI

    This function receives a filename as a parameter.  This should be the
    name of a file containing a digital image.  The file is first open
    and stored as a Pillow image file.  It uses the Image.size property and
    Image.resize() method to decrease the image size by 50%.  It then
    converts the Pillow image to a tk image.

    Note, while this code is written to decrease the size by 50%, a better
    approach may be to determine the aspect ratio of the picture and then
    adjust its size up or down to reach a default size.

    Args:
        filename (str): the name of the file containing an image to be loaded

    Returns:
        Pillow.ImageTk.PhotoImage: a tk-compatible image variable


    """
    pil_image = Image.open(filename)
    original_size = pil_image.size
    adj_factor = 0.5
    new_width = round(original_size[0] * adj_factor)
    new_height = round(original_size[1] * adj_factor)
    resized_image = pil_image.resize((new_width, new_height))
    tk_image = ImageTk.PhotoImage(resized_image)
    return tk_image


def design_window():
    """Creates the GUI window for monitoring station.


    Returns: None

    """

    def patient_nums_droplist():
        answer = get_nums()
        record_number_combo['values'] = answer


    def find_patient():
        global latest_ecg_str

        mrn = record_number_list.get()
        answer = request_patient_info(mrn)
        update_display(number_label, answer["MRN"])
        update_display(name_label, answer["name"])
        update_display(hr_label, answer["HR"][-1])
        history_combo["values"] = answer["ecg_time"]
        m_history_combo["values"] = answer["mi_time"]

        latest_ecg_str = answer["ecg_images"][-1]
        im = tk.PhotoImage(data=latest_ecg_str)
        image_label1['image'] = im

        latest_mi_str = answer["medical_images"][-1]
        im = ImageTk.PhotoImage(data=latest_mi_str)
        m_image_label1['image'] = im

    def update_display(label, value):
        """

        Returns:

        """
        value = str(value)
        label.configure(text=value)

    def indexing(list, item):
        for i in range(len(list)):
            if list[i] == item:
                return i


    def cancel_cmd():
        """Closes window upon click of Cancel button

        This function is connected to the "Cancel" button of the GUI.  It
        destroys the root window causing the GUI interface to close.
        """
        root.destroy()


    root = tk.Tk()
    root.title("Monitoring Station GUI")

    top_label = ttk.Label(root, text="Heart Rate and ECG Database")
    top_label.grid(column=0, row=0, columnspan=4)

    # load database
    load_button = ttk.Button(root, text="Load Database", command=patient_nums_droplist)
    load_button.grid(column=1, row=0)

    # start with selecting patient
    ttk.Label(root, text="select patient medical record number").\
        grid(column=0, row=1, sticky='e')

    record_number_list = tk.StringVar()
    record_number_combo = ttk.Combobox(root, textvariable=record_number_list)
    record_number_combo.state(["readonly"])
    record_number_combo.grid(column=1, row=1, columnspan=2)

    find_button = ttk.Button(root, text="Find Patient", command=find_patient)
    find_button.grid(row=1, column=3)

    # patient profile
    ttk.Label(root, text="Patient Profile").grid(column=0, row=2, columnspan=2)

    ttk.Label(root, text="Record Number: ").grid(column=0, row=3, sticky='e')
    number_label = ttk.Label(root, text='awaiting input')
    number_label.grid(column=1, row=3, sticky='w')


    ttk.Label(root, text="Patient Name: ").grid(column=0, row=4, sticky='e')
    name_label = ttk.Label(root, text="awaiting input")
    name_label.grid(column=1, row=4, sticky='w')

    ttk.Label(root, text="Latest Heart Rate (BPM)").grid(column=0, row=5, sticky='e')
    hr_label = ttk.Label(root, text="awaiting input")
    hr_label.grid(column=1, row=5, sticky='w')
    update_display(hr_label, 80)

    ttk.Label(root, text="Historical ECG Images").grid(column=0, row=6, sticky='e')
    history_string = tk.StringVar()
    history_combo = ttk.Combobox(root, textvariable=history_string)
    history_combo.state(["readonly"])
    history_combo.grid(column=1, row=6, columnspan=2)

    ttk.Label(root, text="Medical Images").grid(column=0, row=7, sticky='e')
    m_history_string = tk.StringVar()
    m_history_combo = ttk.Combobox(root, textvariable=m_history_string)
    m_history_combo.state(["readonly"])
    m_history_combo.grid(column=1, row=7, columnspan=2)

    ttk.Label(root, text="current date and time").grid(column=0, row=30, sticky='w')
    current_time_label = ttk.Label(root, text="awaiting input")
    current_time_label.grid(column=1, row=30, columnspan=2, sticky='w')

    def show_time():
        format = "%Y-%m-%d %H:%M:%S"
        curtime = datetime.now().strftime(format)
        current_time_label.configure(text=curtime)
        root.after(1000, show_time)

    refresh_button = ttk.Button(root, text="Refresh") # , command=refresh_button_cmd
    refresh_button.grid(column=4, row=30)

    cancel_button = ttk.Button(root, text="Cancel", command=cancel_cmd)
    cancel_button.grid(column=5, row=30)

    # ECG images
    ttk.Label(root, text="ECG Images").grid(column=0, row=11, columnspan=2)

    ttk.Label(root, text="Latest ECG Images").grid(column=0, row=12)
    ecg_image1 = load_and_resize_image("images/blank_pic.jpeg")
    ecg_image_label1 = ttk.Label(root, image=ecg_image1)
    ecg_image_label1.grid(column=0, row=13)


    ttk.Label(root, text="selected ECG Images").grid(column=1, row=12)
    ecg_image2 = load_and_resize_image("images/blank_pic.jpeg")
    ecg_image_label2 = ttk.Label(root, image=ecg_image2)
    ecg_image_label2.grid(column=1, row=13)

    # medical images
    ttk.Label(root, text="Medical Images").grid(column=0, row=14, columnspan=2)

    latest_ecg_str = tk.StringVar()
    ttk.Label(root, text="Latest ECG Images").grid(column=0, row=15)
    m_image1 = load_and_resize_image("images/blank_pic.jpeg")
    m_image_label1 = ttk.Label(root, image=m_image1)
    m_image_label1.grid(column=0, row=16)

    ttk.Label(root, text="selected ECG Images").grid(column=1, row=15)
    m_image2 = load_and_resize_image("images/blank_pic.jpeg")
    m_image_label2 = ttk.Label(root, image=m_image2)
    m_image_label2.grid(column=1, row=16)

    # update images
    def change_picture_ecg():
        """Allows user to select a new image to display

        This function opens a dialog box to allow the user to choose an image
        file.  If the user does not cancel the dialog box, the chosen filename
        is sent to an external function for opening and resizing.  The
        returned image is then added to the image_label widget for display
        on the GUI.

        """
        filename = filedialog.askopenfilename(initialdir="images")
        if filename == "":
            messagebox.showinfo("Cancel", "You cancelled the image load")
            return
        tk_image = load_and_resize_image(filename)
        ecg_image_label2.configure(image=tk_image)
        ecg_image_label2.image = tk_image  # Stores image as part of widget to
        # prevent garbage collection and loss of image

    display_button = ttk.Button(root, text="Select Local Image",
                                command=change_picture_ecg)
    display_button.grid(row=6, column=5)



    def ecg_display():
        time = history_string.get()
        mrn = record_number_list.get()
        answer = request_patient_info(mrn)
        time_list = answer["ecg_time"]
        image_list = answer["ecg_images"]
        inx = indexing(time_list, time)
        image_str = image_list[inx]
        image_bytes = base64.b64decode(image_str)
        im = tk.PhotoImage(data=image_bytes)
        ecg_image_label1['image'] = im
    show_button = ttk.Button(root, text="Show Online Image", command=ecg_display)
    show_button.grid(row=6, column=3)


    def image_download():
        time = history_string.get()
        mrn = record_number_list.get()
        answer = request_patient_info(mrn)
        time_list = answer["ecg_time"]
        image_list = answer["ecg_images"]
        inx = indexing(time_list, time)
        image_str = image_list[inx]
        filename = "Patient "+mrn+" ECG"+time
        save_b64_image(image_str, filename)
    download_button = ttk.Button(root, text="Download Selected Image", command=image_download)
    download_button.grid(row=6, column=4)


    def change_picture_m():
        """Allows user to select a new image to display

        This function opens a dialog box to allow the user to choose an image
        file.  If the user does not cancel the dialog box, the chosen filename
        is sent to an external function for opening and resizing.  The
        returned image is then added to the image_label widget for display
        on the GUI.

        """
        filename = filedialog.askopenfilename(initialdir="images")
        if filename == "":
            messagebox.showinfo("Cancel", "You cancelled the image load")
            return
        tk_image = load_and_resize_image(filename)
        m_image_label2.configure(image=tk_image)
        m_image_label2.image = tk_image  # Stores image as part of widget to
        # prevent garbage collection and loss of image


    m_display_button = ttk.Button(root, text="Select Local Image",
                                  command=change_picture_m)
    m_display_button.grid(row=7, column=5)

    def m_display():
        time = m_history_string.get()
        mrn = record_number_list.get()
        answer = request_patient_info(mrn)
        time_list = answer["mi_time"]
        image_list = answer["medical_images"]
        inx = indexing(time_list, time)
        image_str = image_list[inx]
        filename = "Patient " + mrn + " Medical Image " + time
        save_b64_image(image_str, filename)
        filepath = "image/" + filename + ".jpg"
        im = load_and_resize_image(filepath)
        m_image_label2['image'] = im

    m_show_button = ttk.Button(root, text="Show Online Image", command=m_display)
    m_show_button.grid(row=7, column=3)


    def m_image_download():
        time = m_history_string.get()
        mrn = record_number_list.get()
        answer = request_patient_info(mrn)
        time_list = answer["mi_time"]
        image_list = answer["medical_images"]
        inx = indexing(time_list, time)
        image_str = image_list[inx]
        filename = "Patient "+mrn+" Medical Image "+time
        save_b64_image(image_str, filename)

    m_download_button = ttk.Button(root, text="Download Selected Image", command=m_image_download)
    m_download_button.grid(row=7, column=4)

    root.after(1000, show_time)
    root.mainloop()


if __name__ == '__main__':
    design_window()