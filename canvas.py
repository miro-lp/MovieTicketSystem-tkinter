import os
from tkinter import Tk, Label, Canvas, Button

from PIL import ImageTk, Image

base_folder = os.path.dirname(__file__)


def create_app():
    tk = Tk()
    tk.geometry("1200x560")
    tk.title("MoviesTicketSystem")
    tk.config(bg='blue')
    img = Image.open(os.path.join(base_folder, "imgs/background.png"))

    bg = ImageTk.PhotoImage(img)
    bg.resize = ("1200x560")

    label1 = Label(image=bg, bg='black')
    label1.image = bg
    label1.place(x=0, y=0, relwidth=1, relheight=1)


    return tk


tk = create_app()

# img1 = Image.open(os.path.join(base_folder, "imgs/GettyImages.png"))
#
# bg = ImageTk.PhotoImage(img1)
#
# back_btn = Button(tk, compound= 'top', bg='red',image=bg, fg="black", text="Dolby Theater", font=('bold',15), height=150, width=150,
#                   command=lambda: print('here'))
# back_btn.grid(row=1, column=2, padx=20, pady=20)
#
# tk.mainloop()
