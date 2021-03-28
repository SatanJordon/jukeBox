from tkinter import *
from tkinter import filedialog
import pygame
import time
from mutagen.mp3 import MP3
from tkinter import ttk

root=Tk()
root.title("Jordon's Player")
root.iconbitmap()
root.geometry("500x450")

#Initialize Pygame mixer
pygame.mixer.init()



#Add song funcion
def add_song():
    song = filedialog.askopenfilename(initialdir='E:/PythonBasics/MusicPlayer/audio',title="Choose a song", filetypes=(("mp3 files","*.mp3"),))
    
    #Split out the dir name from song name
    song = song.replace("E:/PythonBasics/MusicPlayer/audio/","")
    song = song.replace(".mp3","")

    song_box.insert(END, song)

#Add many songs to playlists.
def add_many_songs():
    songs = filedialog.askopenfilenames(initialdir='E:/PythonBasics/MusicPlayer/audio',title="Choose a song", filetypes=(("mp3 files","*.mp3"),))

    # loop through song list and replace dir info.
    for song in songs:
        song = song.replace("E:/PythonBasics/MusicPlayer/audio/","")
        song = song.replace(".mp3","")
        song_box.insert(END,song)

#play selected song
def play():
    song = song_box.get(ACTIVE)
    song = f'E:/PythonBasics/MusicPlayer/audio/{song}.mp3'
    
    pygame.mixer.music.load(song)
    pygame.mixer.music.play(loops=0)
    
    #Call play tim func
    play_time()

    #Update slider to position
    slider_position = int(song_length)
    my_slider.config(to=slider_position, value=0)

#Stop playing current song
def stop():
    pygame.mixer.music.stop()    
    song_box.selection_clear(ACTIVE)

    status_bar.config(text="Time Elapsed: 00:00:00 / 00:00:00")

#Pause and Unpausw the current song
def pause(is_paused):
    global paused
    paused = is_paused
    
    if paused:
        pygame.mixer.music.unpause()
        paused= False
    else:    
        pygame.mixer.music.pause()
        paused = True
    
#Play the next song
def next_song():
    next_one = song_box.curselection()
    next_one = next_one[0]+1
    song = song_box.get(next_one)
    song = f'E:/PythonBasics/MusicPlayer/audio/{song}.mp3'

    pygame.mixer.music.load(song)
    pygame.mixer.music.play(loops=0)

    #Clear active bar in playlist
    song_box.selection_clear(0, END)
    #Activate new song
    song_box.activate(next_one)
    # Set active bar to nect song
    song_box.selection_set(next_one,last=None)

#Play previous song
def previous_song():
    next_one = song_box.curselection()
    next_one = next_one[0]-1
    song = song_box.get(next_one)
    song = f'E:/PythonBasics/MusicPlayer/audio/{song}.mp3'

    pygame.mixer.music.load(song)
    pygame.mixer.music.play(loops=0)

    #Clear active bar in playlist
    song_box.selection_clear(0, END)
    #Activate new song
    song_box.activate(next_one)
    # Set active bar to nect song
    song_box.selection_set(next_one,last=None)

#Delete a song
def delete_song():
    song_box.delete(ANCHOR)
    pygame.mixer.music.stop()

#Delete all songs
def delete_all_song():
    song_box.delete(0,END)
    pygame.mixer.music.stop()

#Grab song time info
def play_time():
    current_time = pygame.mixer.music.get_pos()/1000
    converted_current_time = time.strftime('%H:%M:%S', time.gmtime(current_time))
    

    #Get current playing song
    #current_song = song_box.curselection()
    song = song_box.get(ACTIVE)
    song = f'E:/PythonBasics/MusicPlayer/audio/{song}.mp3'
    
    # get song length.
    song_mut = MP3(song)
    global song_length
    song_length = song_mut.info.length
    converted_song_length = time.strftime('%H:%M:%S', time.gmtime(song_length))

    status_bar.config(text=f'Time Elapsed: {converted_current_time} / {converted_song_length}')
    my_slider.config(value=int(current_time))

    #update play time
    status_bar.after(1000, play_time)

#Create slider func
def slide(x):
    slider_label.config(text=f'{int(my_slider.get())} / {int(song_length)}')

#Create global variable
global paused
paused = False    

#Create Playist Box
song_box = Listbox(root, bg="black",fg="green",width=60, selectbackground="gray", selectforeground="black")
song_box.pack(pady=20)

#Define Player player control buttons
back_btn_img = PhotoImage(file='E:/PythonBasics/MusicPlayer/gui/backward_final.png')
for_btn_img = PhotoImage(file='E:/PythonBasics/MusicPlayer/gui/forward_final.png')
play_btn_img = PhotoImage(file='E:/PythonBasics/MusicPlayer/gui/play_final.png')
pause_btn_img = PhotoImage(file='E:/PythonBasics/MusicPlayer/gui/pause_final.png')
stop_btn_img = PhotoImage(file='E:/PythonBasics/MusicPlayer/gui/stop.png')

#Create player control frame
controls_frame = Frame(root)
controls_frame.pack()

#Create player control images
back_button =Button(controls_frame,image=back_btn_img,borderwidth=0, command=previous_song)
for_button =Button(controls_frame,image=for_btn_img,borderwidth=0, command=next_song)
play_button =Button(controls_frame,image=play_btn_img,borderwidth=0, command=play)
pause_button =Button(controls_frame,image=pause_btn_img,borderwidth=0, command=lambda: pause(paused))
stop_button =Button(controls_frame,image=stop_btn_img,borderwidth=0, command=stop)

back_button.grid(row=0,column=0,padx=10)
for_button.grid(row=0,column=1,padx=10)
play_button.grid(row=0,column=2,padx=10)
pause_button.grid(row=0,column=3,padx=10)
stop_button.grid(row=0,column=4,padx=10)

#Create Menu
my_menu = Menu(root)
root.config(menu=my_menu)

#Add song menu
add_song_menu = Menu(my_menu)
my_menu.add_cascade(label="Add Songs", menu=add_song_menu)
add_song_menu.add_command(label="Add one song to playlist",command=add_song)


#Add many song in menu
add_song_menu.add_command(label="Add more than one song to playlist", command=add_many_songs)

#Delete song menu
remove_song_menu = Menu(my_menu)
my_menu.add_cascade(label="Remove songs", menu=remove_song_menu)
remove_song_menu.add_command(label="Delete a song from playlist", command=delete_song)
remove_song_menu.add_command(label="Delete allsong from playlist", command=delete_all_song)

#Create status bar
status_bar = Label(root,text='' ,bd=1,relief=GROOVE,anchor=E)
status_bar.pack(fill=X, side=BOTTOM, ipady=2)

#Create slider
my_slider = ttk.Scale(root, from_=0, to=100, orient=HORIZONTAL, value=0, command=slide, length=360)
my_slider.pack(pady=30)

#Create temp slider label
slider_label = Label(root, text="0")
slider_label.pack(pady=10)

root.mainloop()

