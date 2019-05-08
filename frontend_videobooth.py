from tkinter import *
import tkinter as tk
from tkinter import ttk
from backend_videobooth import Videobooth
import Web_videobooth
from PIL import Image,ImageTk
import time
from gpiozero import Button as btn # Lib for GPIO 

# v0631 First trial with  GPIO support integrated

# v063
# rewrite to classes to support tkinter and GPIO in future release
# v05
# directory to variable
# v04
# adjusted show photo for resize, new window and close after time
# adjusted buttons text to wraplength



ImgandViddir = '/home/pi/Recordings/'
target_dir = "/mnt/data/Recordings/"

class Window(object):
    def __init__(self,window):

        self.window = window
#        self.window.attributes('-fullscreen',True)
        self.window.wm_title("VKW Babbelbox videobooth")
        style = ttk.Style()
        style.configure("BW.TLabel", foreground="black", background="white")
        self.window.geometry("480x320") #You want the size of the app to be 500x500
        self.window.resizable(0, 0) #Don't allow resizing in the x or y direction
        b1=Button(window,text="Start Opname film", bg="green", width=25, height=10,wraplength=80, justify=CENTER,command=self.video_record)
        b1.grid(row=1,column=1)

        b2=Button(window,text="Neem een foto", width=25,height=10,wraplength=80, justify=CENTER,command=self.photo)
        b2.grid(row=1,column=3)

        b3=Button(window,text="Speel video af", width=25,height=10,wraplength=80, justify=CENTER,command=self.playvideo)
        b3.grid(row=2,column=1)

        b4=Button(window,text="Toon Foto 5 seconden", width=25,height=10,wraplength=80, justify=CENTER, command=self.showphoto)
        b4.grid(row=2,column=3)

    def video_record(self):
        videobooth.video_record_start()

    def photo(self):
        videobooth.take_photo()

    def playvideo(self):
        print("play video")
        lastfile,path,name = videobooth.lastfile(target_dir,'mp4')
        print('lastfile = ' + lastfile)
        videobooth.playvideo(lastfile)

    def showphoto(self):
        print("Show photo")
        # lastfile,path,name = videobooth.lastfile(target_dir,'jpg')
        lastfile,path,name = videobooth.lastfile(target_dir,'jpg')
        print('lastfile = ' + lastfile)
        self.create_image(lastfile)

    def create_image(self,image):
        print (image)
        load = Image.open(image)
        root = Toplevel()
        root.title("Foto")
        root.geometry("480x320")
        img = ImageTk.PhotoImage(load.resize((480, 320))) # the one-liner I used in my app
#	root is vervangen door self.window
        label = Label(root, image=img)
        label.grid(row=0,column=0)
        label.image = img # this feels redundant but the image didn't show up without it in my app
#        label.place(relheight=0,relwidth=0,relx=0,rely=0)
        label.pack()
#       root is vervangen door self.window
        root.after(5000, lambda: root.destroy()) # Destroy the widget after 5 seconds


## Actions to be taken when specific button is pressed

def buttonmoviepressed():
    print("The Movie button is pressed")
    videobooth.video_record_start()
    

def buttonphotopressed():
    print("The Photo button is pressed")
    videobooth.take_photo()
    Web_videobooth.view()

if __name__ == "__main__":
    # window = tk.Tk()
    # window.iconbitmap('rekenenisleuk.ico')
    window=Tk()
    Window(window)
    videobooth = Videobooth()
#    webgui() = Web_videobooth()

    # Check for button GPIO press
    button_movie = btn(20)
    button_photo = btn(21)
    button_movie.when_pressed = buttonmoviepressed
    button_photo.when_pressed = buttonphotopressed
    window.mainloop()
