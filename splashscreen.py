from tkinter import *
from tkinter import ttk
from tkinter.ttk import Progressbar
from PIL import Image, ImageTk
import os

root = Tk()
root.title("Skin Care Recommender")
logo_path = "logoai (3).png"
logo_image = Image.open(logo_path)
new_width = 400  
new_height = 400 
logo_image = logo_image.resize((new_width, new_height))
logo = ImageTk.PhotoImage(logo_image)

height = 550  
width = 530
x = (root.winfo_screenwidth() // 2 - (width // 2))
y = (root.winfo_screenheight() // 2 - (height // 2))

root.geometry('{}x{}+{}+{}'.format(width, height, x, y))
root.config(background="#194F54")

bg_label = Label(root, image=logo, bg="#194F54")
bg_label.place(x=(width - new_width) // 2, y=(height - new_height) // 2) 

welcome_label = Label(text="Skin Care Product Recommender", bg="#194F54", font=("Trebuchet Ms", 15, "bold"), fg="#FFFFFF")
welcome_label.place(x= 120, y=50)

progress_label = Label(root, text="Loading...", font=("Trebuchet Ms", 15, "bold"), fg="#FFFFFF", bg="#194F54")
progress_label.place(x=190, y=450)

progress = ttk.Style()
progress. theme_use('clam')
progress. configure("red.Horizontal.TProgressbar", background="#108cff")

progress = Progressbar(root, orient=HORIZONTAL, length=400, mode='determinate', style="red.Horizontal.TProgressbar")
progress.place(x=60, y=390)

def top():
    root.withdraw()
    os.system("python uploadphoto.py")
    root.destroy()

i = 0

def load():
    global i
    if i <=10:
        txt = 'Loading...' + (str(10*i)+'%')
        progress_label.config(text=txt)
        progress_label.after(200, load)
        progress['value'] = 10 * i
        i += 1
    
    else:
        top()

load()
root.resizable(False, False)
root.mainloop()
