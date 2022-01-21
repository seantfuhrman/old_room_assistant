from __future__ import unicode_literals
from tkinter import *
import youtube_dl, os

url = ""

ydl_opts = {
    'format': 'bestaudio/best',
    'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'mp3',
        'preferredquality': '192',
    }],
}

class Application(Frame):
    
    def store(self):
        url = self.e.get()
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        dirs = os.listdir()
        for file in dirs:
            if ".mp3" in file and not "empty" in file:
                os.rename("C:\\Users\\drfuh\\Home\\dist\\" + file, "C:\\Users\\drfuh\\Home\\Music\\" + file )
    
    def create_widgets(self):
        self.QUIT = Button(self)
        self.QUIT["text"] = "QUIT"
        self.QUIT["command"] =  self.quit
        self.QUIT.grid(row=2, sticky=W, padx=4)

        self.e = Entry(self)
        self.e.grid(row=1, column=1)
        
        self.add = Button(self)
        self.add["text"] = "ADD",
        self.add["command"] = self.store
        self.add.grid(row=2, column=2, sticky=E, pady=4)

    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.pack()
        self.create_widgets()

root = Tk()
app = Application(master=root)
app.mainloop()

