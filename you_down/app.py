from tkinter import *
import tkinter.ttk as ttk
from pytube import YouTube
import pytube


class Tubers:

    def __init__(self, master):

        # main
        self.tube = master
        self.tube.title("The Downloader")
        self.tube.resizable(1, 1)
        self.tube.geometry('500x200')
        #self.tube.link = StringVar()

        # main frame
        frame = LabelFrame(self.tube, text='Let ripping start!!', font=('Helvetica', 26, 'bold'))
        frame.pack()

        # label name
        self.label_name = Label(frame, text='Paste your YouTube link here!!', font=('Calibri', 13))
        self.label_name.pack()
        self.link_enter = Entry(frame, font=('Calibri', 13))
        self.link_enter.focus()
        self.link_enter.pack()

        # button download

        s = ttk.Style()
        s.configure('my.TButton', font=('Calibri', 14, 'bold'))
        button_down = ttk.Button(text='DOWNLOAD', command=self.downloader, style='my.TButton')
        button_down.pack()

        # button reset

        s = ttk.Style()
        s.configure('my.TButton', font=('Calibri', 14, 'bold'))
        button_down = ttk.Button(text='RESET', command=self.Reset, style='my.TButton')
        button_down.pack()

        # message

        self.message = Label(text='', fg='red')
        self.message.pack()


    def downloader(self):
        url = self.link_enter.get()
        print(url)
        print(type(url))
        youtube = YouTube(url).streams.get_highest_resolution().download('../Video')
        print(youtube.title)
        ##url = YouTube(str(self.link_enter.get()))
        #video = youtube.streams.first()
        #video.download('../Video')
        #video.download('.../Videos')
        #Label(root, text = 'DOWNLOADED', font = 'arial 15').pack()


    def Reset(self):

        self.link_enter.delete(0, 'end')
        self.message['text'] = 'Re-enter your link'


if __name__ == '__main__':
    root = Tk()
    Tub = Tubers(root)
    root.mainloop()