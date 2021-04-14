from tkinter import *
from gtts import gTTS
import tkinter.ttk as ttk
import tkinter as tk
from playsound import playsound
#import os
#import playsound

class Fenetre:

    def __init__(self, master):
        self.fen = master
        self.fen.title("Speech Tool")
        self.fen.resizable(1, 1)
        
        frame = LabelFrame(self.fen, text="Text Speaker Tool", font=('Helvetica', 16, 'bold'))
        frame.grid(row=0, column=0, columnspan=3, pady=15)

        #self.lab_text = Label(frame, text="Enter the text here:", font=('Calibri, 13'))
        #self.lab_text.grid(row=2, column=0, sticky=W)

        Msg = tk.StringVar()
        #Label(master, text="Enter Text", font = 'arial 15 bold', bg ='white smoke')
        self.textbox = ttk.Entry(master, textvariable=Msg, width=50, text="Enter the Text Here")
        self.textbox.grid(row=3, columnspan=3)
        self.textbox.focus()

        #self.input_text = tk.Text(frame, height=5, width=20)
        #self.input_text.grid(row=4, column=0)

        b = ttk.Style()
        b.configure('my.TButton', font=('Calibri', 14, 'bold'))
        button_sound = ttk.Button(text='Click and Listen', command=self.play, style='my.TButton')
        button_sound.grid(row=5, column=0, sticky=W + E)

        b = ttk.Style()
        b.configure('my.TButton', font=('Calibri', 14, 'bold'))
        button_sound = ttk.Button(text='Reset', command=self.Reset, style='my.TButton')
        button_sound.grid(row=5, column=1, sticky=W + E)

        b = ttk.Style()
        b.configure('my.TButton', font=('Calibri', 14, 'bold'))
        button_sound = ttk.Button(text='Exit', command=self.Exit, style='my.TButton')
        button_sound.grid(row=5, column=2, sticky=W + E)

    def play(self):
        Message = self.textbox.get()
        speech = gTTS(text=Message)
        speech.save('mysentence.mp3')
        #speech = speech.replace(" ", "%20")
        playsound('mysentence.mp3')

    def Exit(self):
        root.destroy()

    def Reset(self):
        self.textbox.delete(0, 'end')

if __name__ == '__main__':
    root = Tk()
    Fen = Fenetre(root)
    root.mainloop()