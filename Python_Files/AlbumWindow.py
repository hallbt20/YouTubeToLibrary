from pydub import AudioSegment
from tkinter import *
from tkinter import ttk
from tkinter.messagebox import *

import eyed3
import os #Adding folder directory
import sys
import youtube_dl

class albumInfo():
    def __init__(self):
        self.root = Tk()

        # Terminate program upon exiting window
        self.root.protocol("WM_DELETE_WINDOW", (lambda: sys.exit(0)))
        
        # Creates tab object with tab widgets
        tabs = ttk.Notebook(self.root, width=600, height=350)
        tab1 = ttk.Frame(tabs)
        tab2 = ttk.Frame(tabs)

        tabs.add(tab1, text = 'Album Info')
        tabs.add(tab2, text = 'Track Info')
        tabs.grid(row=0, column=0)

        # Initialize entry widgets
        self.url = Entry(tab1, bd=5, width=50)
        self.artist = Entry(tab1, bd=5, width=50)
        self.album = Entry(tab1, bd=5, width=50)
        self.album_artist = Entry(tab1, bd=5, width=50)
        self.genre = Entry(tab1, bd=5, width=10)
        self.year = Entry(tab1, bd=5, width=10)
        self.textBox = Text(tab2)
        self.folder_name = ""
        
        # Place entry widgets
        self.url.grid(row=1, column=1, sticky=W, pady=(50, 0))
        self.artist.grid(row=2, column=1, sticky=W)
        self.album.grid(row=3, column=1, sticky=W)
        self.album_artist.grid(row=4, column=1, sticky=W)
        self.genre.grid(row=5, column=1, sticky=W)
        self.year.grid(row=6, column=1, sticky=W)
        self.textBox.grid(row=1, column=0, columnspan=5) 
        
        # Place label widgets
        Label(tab1, text='URL', padx=10).grid(row=1, column=0, sticky=E, pady=(50, 0))
        Label(tab1, text='Artist', padx=10).grid(row=2, column=0, sticky=E)
        Label(tab1, text='Album', padx=10).grid(row=3, column=0, sticky=E)
        Label(tab1, text='Album Artist', padx=10).grid(row=4, column=0, sticky=E)
        Label(tab1, text='Genre', padx=10).grid(row=5, column=0, sticky=E)
        Label(tab1, text='Year', padx=10).grid(row=6, column=0, sticky=E)
        Label(tab2, text='Place track info here.').grid(row=0, column=2)

        # Help button on Track Info tab
        example = "The track info should be organized as follows:\n\n0:00 Track 1\n3:42 Track 2\n ...\n50:47 Track 10"
        photo = PhotoImage(file = r"Button.png")
        B = Button(tab2, text='Help', image = photo, command = lambda: showinfo("Track Info Formatting Example", example))
        B.image = photo
        B.grid(row=0, column=4)
        
        # Creates frame object containing button widgets
        buttonFrame = Frame(self.root)
        Button(buttonFrame, text='OK', width=5, relief="raised", command=lambda: self.setEntries()).grid(row=0, column=0, sticky=W)
        Button(buttonFrame, text='Cancel', width=5, command=lambda: sys.exit(0)).grid(row=0, column=1, sticky=W)
        
        buttonFrame.grid(row=2, column=0, sticky=W)
    
    def setter(self):
        self.url = self.url.get()
        self.artist = self.artist.get()
        self.album = self.album.get()
        self.album_artist = self.album_artist.get()
        self.genre = self.genre.get()
        self.year = self.year.get()
        self.textBox = self.textBox.get("1.0", END)
        if self.artist or self.album or self.year:
            self.folder_name = self.artist + " - " + self.album + " (" + self.year + ")"

    def setFolderName(self, folder_name):
        self.folder_name = folder_name
    
    def setEntries(self):
        if not self.url.get():
            showerror("Error", "URL is a required field.")

        elif not self.textBox.get("1.0",END).strip():
            response = askyesno("Warning", "The track listing is empty. Would you like to continue?")
            
            if response:
                self.instructions()
        else:
            self.instructions()

    def dataCleaning(self):
        track_listing = [track.strip().split(' ', 1) for track in self.textBox.split('\n') if track]

        for i in range(len(track_listing)):
            time_partition = track_listing[i][0].split(':')

            if(len(time_partition) == 2):
                track_listing[i][0] = (int(time_partition[0])*60 + int(time_partition[1])) * 1000

            elif(len(time_partition) == 3):
                track_listing[i][0] = (int(time_partition[0])*3600 + int(time_partition[0])*60 + int(time_partition[1])) * 1000

        self.textBox = track_listing

    def createFolder(self):
        try:
            os.makedirs(self.folder_name)
        
        except FileExistsError:
            folder_name_window = Tk()
            
            folder_name_window.bind('<Return>', (lambda event: [self.setFolderName(B.get()), folder_name_window.destroy(), self.createFolder()]))
            
            Label(folder_name_window, text="The file name " + self.folder_name + " already exists.").grid(row=0, column=0, columnspan=2)
            Label(folder_name_window, text="Please provide folder name.").grid(row=1, column=0, columnspan=2)
            
            B = Entry(folder_name_window, bd = 5)
            B.grid(row=2, column=0, columnspan=2)
            
            Button(folder_name_window, bd = 5, text="Ok", command = lambda: [self.setFolderName(B.get()), folder_name_window.destroy(), self.createFolder()]).grid(row=3, column=0)
            Button(folder_name_window, bd = 5, text="Cancel", command = lambda: sys.exit(0)).grid(row=3, column=1)
            
            folder_name_window.mainloop()
        
        except FileNotFoundError:
            folder_name_window = Tk()
            
            folder_name_window.bind('<Return>', (lambda event: [self.setFolderName(B.get()), folder_name_window.destroy(), self.createFolder()]))
            
            Label(folder_name_window, text="Please provide folder name. (Required field)").grid(row=0, column=0, columnspan=2)
            
            B = Entry(folder_name_window, bd = 5)
            B.grid(row=1, column=0, columnspan=2)
            
            Button(folder_name_window, bd = 5, text="Ok", command = lambda: [self.setFolderName(B.get()), folder_name_window.destroy(), self.createFolder()]).grid(row=2, column=0)
            Button(folder_name_window, bd = 5, text="Cancel", command = lambda: sys.exit(0)).grid(row=2, column=1)
            
            folder_name_window.mainloop()

    def downloader(self):
        ydl_opts = {
            'format': 'bestaudio/best',
            'extractaudio': True,
            'audioformat': 'mp3',
            'outtmpl': self.folder_name + '/Temp.%(ext)s',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
        }

        try:
            sys.stderr = open(os.devnull, "w")
            with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                ydl.download([self.url])
            sys.stderr = sys.__stderr__

        except youtube_dl.utils.DownloadError:
            showerror("Error", "The URL provided is not valid. Please try again.")
            sys.exit(0)

    def trackSplitter(self):
        album = AudioSegment.from_mp3(self.folder_name + "/Temp.mp3")
        for track_num in range(len(self.textBox)):
            print(self.textBox[track_num][1] + " is processing.")
            start_time = self.textBox[track_num][0]

            if track_num != len(self.textBox) - 1:
                end_time = self.textBox[track_num + 1][0]
                song = album[start_time:end_time]

            else:
                song = album[start_time:]

            song_path = self.folder_name + "/" + self.textBox[track_num][1] + ".mp3"
            
            song.export(song_path, format = "mp3")

            self.metadataTagger(self.textBox[track_num][1], track_num + 1)

    def metadataTagger(self, song_name, track_num):
        song = eyed3.load(self.folder_name + "/" + song_name + ".mp3")
        song.tag.artist = self.artist
        song.tag.album = self.album
        song.tag.album_artist = self.album_artist
        song.tag.title = song_name
        song.tag.recording_date = self.year
        song.tag.track_num = track_num
        song.tag.genre = self.genre
        song.tag.save()

    def instructions(self):
        self.setter()
        self.root.destroy()
        self.dataCleaning()
        self.createFolder()
        self.downloader()
        self.trackSplitter()
