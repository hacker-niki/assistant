import json
import tkinter as tk
from tkinter import Tk, Canvas, Entry, Button, PhotoImage

import sounddevice as sd
from tkPDFViewer2 import tkPDFViewer as pdf


class App:
    window = Tk()
    window.title("Log in")
    window.geometry("300x390")
    window.configure(bg="#362955")

    canvas = Canvas(
        window,
        bg="#362955",
        height=390,
        width=300,
        bd=0,
        highlightthickness=0,
        relief="ridge"
    )

    canvas.place(x=0, y=0)
    entry_image_1 = PhotoImage(
        file=("uiData/entry_1.png"))
    entry_bg_1 = canvas.create_image(
        149.49999999999994,
        109.00000000000003,
        image=entry_image_1
    )
    entry_1 = Entry(
        bd=0,
        bg="#5B4D71",
        fg="#FFFFFF",
        highlightthickness=0

    )
    entry_1.place(
        x=64.99999999999994,
        y=94.00000000000003,
        width=169.0,
        height=28.0
    )

    entry_image_2 = PhotoImage(
        file="uiData/entry_2.png")
    entry_bg_2 = canvas.create_image(
        149.49999999999994,
        180.00000000000003,
        image=entry_image_2
    )
    entry_2 = Entry(
        bd=0,
        bg="#5B4D71",
        fg="#FFFFFF",
        highlightthickness=0
    )
    entry_2.place(
        x=64.99999999999994,
        y=165.00000000000003,
        width=169.0,
        height=28.0
    )

    entry_image_3 = PhotoImage(
        file="uiData/entry_3.png")
    entry_bg_3 = canvas.create_image(
        149.49999999999994,
        251.00000000000003,
        image=entry_image_3
    )
    entry_3 = Entry(
        bd=0,
        bg="#5B4D71",
        fg="#FFFFFF",
        highlightthickness=0
    )
    entry_3.place(
        x=64.99999999999994,
        y=236.00000000000003,
        width=169.0,
        height=28.0
    )

    canvas.create_text(
        50.99999999999994,
        28.00000000000003,
        anchor="nw",
        text="LOG IN",
        fill="#FFFFFF",
        font=("Inter", 12 * -1)
    )

    canvas.create_rectangle(
        51.99999999999994,
        44.50000000000003,
        267.99999999999994,
        45.50000000000003,
        fill="#EEC110",
        outline="")

    canvas.create_text(
        52.99999999999994,
        216.00000000000003,
        anchor="nw",
        text="Picovoice key",
        fill="#7C829A",
        font=("Inter", 11 * -1)
    )

    canvas.create_text(
        52.99999999999994,
        148.00000000000003,
        anchor="nw",
        text="Town",
        fill="#7C829A",
        font=("Inter", 11 * -1)
    )

    canvas.create_rectangle(
        15.999999999999943,
        313.0,
        154.99999999999994,
        368.0,
        fill="#362955",
        outline="")

    canvas.create_text(
        51.99999999999994,
        75.00000000000003,
        anchor="nw",
        text="Username",
        fill="#7C829A",
        font=("Inter", 11 * -1)
    )

    button_image_1 = PhotoImage(
        file="uiData/button_1.png")
    button_1 = Button(
        image=button_image_1,
        borderwidth=0,
        highlightthickness=0,
        command=lambda: check_microphone(),
        relief="flat"
    )
    button_1.place(
        x=38.99999999999994,
        y=330.0,
        width=23.0,
        height=23.0
    )

    button_image_2 = PhotoImage(
        file="uiData/button_2.png")
    button_2 = Button(
        image=button_image_2,
        borderwidth=0,
        highlightthickness=0,
        command=lambda: App.open_manual(),
        relief="flat"
    )
    button_2.place(
        x=66.99999999999994,
        y=330.0,
        width=23.0,
        height=23.0
    )

    button_image_3 = PhotoImage(
        file="uiData/button_3.png")
    button_3 = Button(window,
                      image=button_image_3,
                      borderwidth=0,
                      highlightthickness=0,
                      command=lambda: get_text(),
                      relief="flat"
                      )
    button_3.place(
        x=101.99999999999994,
        y=330.0,
        width=146.0,
        height=23.0
    )
    window.resizable(False, False)

    @staticmethod
    def open_manual():
        root = tk.Toplevel(App.window)

        root.geometry("600x900")
        root.title("Manual")
        root.configure(bg="white")

        filename = "uiData/Квант.pdf"

        v1 = pdf.ShowPdf()
        v2 = v1.pdf_view(root, pdf_location=open(filename, "r"), width=220, height=350)
        v2.pack()


def check_microphone():
    try:
        sd.query_devices()
        label = tk.Label(App.window, text="Working!", background="#362955", foreground="white")
        label.place(
            x=25.99999999999994,
            y=355.0,
            width=63.0,
            height=18.0
        )
        # self.label.setText("Microphone is working!")
    except OSError:
        label = tk.Label(App.window, text="Not working!", background="#362955", foreground="white")
        label.place(
            x=34.99999999999994,
            y=355.0,
            width=63.0,
            height=18.0
        )


def get_text():
    username = App.entry_1.get()
    town = App.entry_2.get()
    picovoice_key = App.entry_3.get()

    data = {
        "username": username,
        "town": town,
        "picovoice_key": picovoice_key,
        "language": "rus"
    }

    with open("data.json", "w") as f:
        json.dump(data, f)

    print(username)
    print(town)
    print(picovoice_key)

    App.window.destroy()


def auto_fill():
    with open("data.json", 'r') as f:
        data = json.load(f)
    username = data['username']
    town = data['town']
    picovoice_key = data['picovoice_key']

    App.entry_1.insert(0, username)
    App.entry_2.insert(0, town)
    App.entry_3.insert(0, picovoice_key)

    print('Data autofilled')


def open_manual():
    root = tk.Toplevel(App.window)

    root.geometry("600x900")
    root.title("PDF Viever")
    root.configure(bg="white")

    filename = "uiData/Квант.pdf"

    v1 = pdf.ShowPdf()
    v2 = v1.pdf_view(root, pdf_location=open(filename, "r"), width=220, height=350)
    v2.pack()
