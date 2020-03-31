from tkinter import *
import os
from pygame import mixer
import tkinter.messagebox
from tkinter import filedialog
import time
import threading
from tkinter import ttk
from ttkthemes import themed_tk as tk
from mutagen.mp3 import MP3
import pyttsx3
import datetime

engine=pyttsx3.init('sapi5')
voices=engine.getProperty('voices')
engine.setProperty('voice',voices[1].id)
def speak(audio):
    engine.say(audio)
    engine.runAndWait()


rate = engine.getProperty('rate')
engine.setProperty('rate', 155)

def wishMe():
    hour=int(datetime.datetime.now().hour)
    if hour>0 and hour<12:
        speak("Good Morning  You can Listen to some morning music")
    elif hour>12 and hour<18:
        speak("Good Day  You can listen to some energetic music")
    else:
        speak("Good Evening  You can hear some relaxing music ")
wishMe()

root = tk.ThemedTk()
root.geometry("800x500")
root.get_themes()                
root.set_theme("clearlooks")         
root.configure(bg='light blue')

statusbar = ttk.Label(root, text="Musical", relief=SUNKEN, anchor=W, font='lucida 10 italic')
statusbar.pack(side=BOTTOM, fill=X)

menubar = Menu(root)
root.config(menu=menubar)

subMenu = Menu(menubar, tearoff=0)

playlist = []

def search_file():
    global filename_path
    filename_path = filedialog.askopenfilename()
    add_to_playlist(filename_path)

    mixer.music.queue(filename_path)

def add_to_playlist(filename):
    filename = os.path.basename(filename)
    index = 0
    playlistbox.insert(index, filename)
    playlist.insert(index, filename_path)
    index += 1


menubar.add_cascade(label="File", menu=subMenu)
subMenu.add_command(label="Open", command=search_file)
subMenu.add_command(label="Exit", command=root.destroy)

def about():
    tkinter.messagebox.showinfo('Its a music player.For any help Contact Madhura,Imdad or Janvi')

subMenu = Menu(menubar, tearoff=0)
menubar.add_cascade(label="Help", menu=subMenu)
subMenu.add_command(label="About Us", command=about)

mixer.init() 

root.title("Musical")
root.iconbitmap(r'a.ico')

add_del_frame = Frame(root,relief=RAISED, borderwidth=4)
add_del_frame.pack(side=RIGHT, padx=29, pady=30)

playlistbox = Listbox(add_del_frame)
playlistbox.pack()

addBtn = ttk.Button(add_del_frame, text="+ Add", command=search_file)
addBtn.pack(side=LEFT)

def delete_song():
    song_chosen = playlistbox.curselection()
    song_chosen = int(song_chosen[0])
    playlistbox.delete(song_chosen)
    playlist.pop(song_chosen)

del_Btn = ttk.Button(add_del_frame, text="- Remove", command=delete_song)
del_Btn.pack(side=LEFT)

right_frame = Frame(root,relief=RAISED, borderwidth=7)
right_frame.pack(pady=50)

topframe = Frame(right_frame)
topframe.pack()

lengthlabel = ttk.Label(topframe, text='Full Length : --:--',)
lengthlabel.pack(pady=5.5)

currenttimelabel = ttk.Label(topframe, text='Current Time : --:--', relief=GROOVE)
currenttimelabel.pack()

def show_details(play_song):
    file_data = os.path.splitext(play_song)

    if file_data[1] == '.mp3':
        audio = MP3(play_song)
        total_length = audio.info.length
    else:
        a = mixer.Sound(play_song)
        total_length = a.get_length()

    # div - total_length/60, mod - total_length % 60
    minutes, seconds = divmod(total_length, 60)
    minutes = round(minutes)
    seconds = round(seconds)
    timeformat = '{:02d}:{:02d}'.format(minutes, seconds)
    lengthlabel['text'] = "Full Length" + ' - ' + timeformat

    t1 = threading.Thread(target=start_count, args=(total_length,))
    t1.start()

def start_count(t):
    global paused
    current_time = 0
    while current_time <= t and mixer.music.get_busy():
        if paused:
            continue
        else:
            minutes, seconds = divmod(current_time, 60)
            minutes = round(minutes)
            seconds = round(seconds)
            timeformat = '{:02d}:{:02d}'.format(minutes, seconds)
            currenttimelabel['text'] = "Present Time" + ' - ' + timeformat
            time.sleep(1)
            current_time += 1

def play_music():
    global paused

    if paused:
        mixer.music.unpause()
        statusbar['text'] = "Music has been Resumed"
        paused = FALSE
    else:
        try:
            stop_music()
            time.sleep(1)
            selected_song = playlistbox.curselection()
            selected_song = int(selected_song[0])
            play_it = playlist[selected_song]
            mixer.music.load(play_it)
            mixer.music.play()
            statusbar['text'] = "Playing your music" + ' - ' + os.path.basename(play_it)
            show_details(play_it)
        except:
            tkinter.messagebox.showerror('File not found','Musical was unable to find this file. Try Again.')


def stop_music():
    mixer.music.stop()
    statusbar['text'] = "Music has been Stopped"

paused = FALSE
def pause_music():
    global paused
    paused = TRUE
    mixer.music.pause()
    statusbar['text'] = "Music has been Paused"

def rewind_music():
    play_music()
    statusbar['text'] = "Music has been Rewinded"

def set_vol(val):
    volume = float(val) / 100
    mixer.music.set_volume(volume)

muted = FALSE
def mute_music():
    global muted
    if muted: 
        mixer.music.set_volume(0.9)
        volumeBtn.configure(image=volume_Photo)
        scale.set(90)
        muted = FALSE
    else:  
        mixer.music.set_volume(0)
        volumeBtn.configure(image=mute_Photo)
        scale.set(0)
        muted = TRUE

middleframe = Frame(right_frame)
middleframe.pack(pady=30, padx=30)

play_Photo = PhotoImage(file='play.png')
playBtn = ttk.Button(middleframe, image=play_Photo, command=play_music)
playBtn.grid(row=0, column=0, padx=10)


pause_Photo = PhotoImage(file='pause.png')
pauseBtn = ttk.Button(middleframe, image=pause_Photo, command=pause_music)
pauseBtn.grid(row=0, column=1, padx=10)

stop_Photo = PhotoImage(file='stop.png')
stopBtn = ttk.Button(middleframe, image=stop_Photo, command=stop_music)
stopBtn.grid(row=0, column=2, padx=10)


bottomframe = Frame(right_frame)
bottomframe.pack()

rewind_Photo = PhotoImage(file='rewind.png')
rewindBtn = ttk.Button(bottomframe, image=rewind_Photo, command=rewind_music)
rewindBtn.grid(row=0, column=0)

mute_Photo = PhotoImage(file='mute.png')
volume_Photo = PhotoImage(file='volume.png')
volumeBtn = ttk.Button(bottomframe, image=volume_Photo, command=mute_music)
volumeBtn.grid(row=0, column=1)

scale = ttk.Scale(bottomframe, from_=0, to=100, orient=VERTICAL, command=set_vol)
scale.set(60) 
mixer.music.set_volume(0.6)
scale.grid(row=0, column=2, pady=15, padx=30)

def on_close():
    stop_music()
    root.destroy()

root.protocol("WM_DELETE_WINDOW", on_close)

root.mainloop()

