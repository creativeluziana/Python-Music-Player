import tkinter
from tkinter.ttk import Progressbar
import customtkinter
import pygame
from PIL import Image, ImageTk
import os
import math
from threading import Thread
import time

# Set appearance mode and color theme
customtkinter.set_appearance_mode("dark")
customtkinter.set_default_color_theme("blue")

# Initialize Pygame mixer
pygame.mixer.init()

# Define global variables
list_of_songs = [
    'music/One Direction - Night Changes.wav',
    'music/One Direction - What makes u beautiful.wav',
    'music/Knaan - Waving Flag.wav'
]

list_of_covers = [
    'img/One Direction - Night Changes.jpg',
    'img/One Direction - What makes u beautiful.jpg',
    'img/Knaan - Waving Flag.jpg',
    'img/Dua Lipa & Elton John - Cold Heart.jpg'
]

n = 0
playing = False
paused_position = 0

# Function to get album cover
def get_album_cover(n):
    global album_image
    # Extract artist name and song name from file names
    file_name = os.path.basename(list_of_songs[n])
    artist_name, song_title = file_name.split(' - ', 1)

    image1 = Image.open(list_of_covers[n])
    image2 = image1.resize((250, 250))
    album_image = ImageTk.PhotoImage(image2)

    label1.configure(image=album_image)
    label1.image = album_image

    # Display artist name and song name labels
    song_name_label.configure(text=song_title[:-4])
    artist_label.configure(text=artist_name)

# Function to update progress bar
def progress():
    global paused_position
    while playing:
        song_len = pygame.mixer.Sound(list_of_songs[n]).get_length() * 3
        for _ in range(math.ceil(song_len)):
            time.sleep(0.1)  # Reduce sleep time
            if playing:
                progressbar.set(pygame.mixer.music.get_pos() / 1000000)
                update_song_time()

# Function to start progress update in a separate thread
def start_progress_thread():
    t = Thread(target=progress)
    t.daemon = True  # Daemonize the thread to exit when the main program exits
    t.start()

# Function to update song time label
def update_song_time():
    song_len = pygame.mixer.Sound(list_of_songs[n]).get_length()
    current_pos = pygame.mixer.music.get_pos() / 1000
    elapsed_time = time.strftime("%M:%S", time.gmtime(current_pos))
    total_duration = time.strftime("%M:%S", time.gmtime(song_len))
    time_label.configure(text=f"{elapsed_time} / {total_duration}")

# Function to play or pause music
def play_music():
    global playing, paused_position, n
    if not playing:
        if pygame.mixer.music.get_pos() > 0:
            pygame.mixer.music.unpause()
        else:
            current_song = n
            if n > 2:
                n = 0
            song_name = list_of_songs[n]
            pygame.mixer.music.load(song_name)
            pygame.mixer.music.play(loops=0, start=paused_position)
            pygame.mixer.music.set_volume(0.5)
            get_album_cover(n)
            start_progress_thread()  # Start the progress thread

        playing = True
        play_button.configure(text='Pause')
    else:
        pygame.mixer.music.pause()
        paused_position = pygame.mixer.music.get_pos()
        playing = False
        play_button.configure(text='Play')

# Function to skip to the next song
def skip_forward():
    global n
    n = (n + 1) % len(list_of_songs)
    if playing:
        paused_position = 0
        pygame.mixer.music.stop()
        play_music()
        get_album_cover(n)

# Function to skip to the previous song
def skip_back():
    global n
    n = (n - 1) % len(list_of_songs)
    if playing:
        paused_position = 0
        pygame.mixer.music.stop()
        play_music()
        get_album_cover(n)

# Function to adjust volume
def volume(value):
    pygame.mixer.music.set_volume(value)

# Create the main window
root = customtkinter.CTk()
root.title('Music Player')
root.geometry('400x480')

# Create GUI elements
play_button = customtkinter.CTkButton(master=root, text='Play', command=play_music)
play_button.place(relx=0.5, rely=0.7, anchor=tkinter.CENTER)

skip_f = customtkinter.CTkButton(master=root, text='>', command=skip_forward, width=2)
skip_f.place(relx=0.7, rely=0.7, anchor=tkinter.CENTER)

skip_b = customtkinter.CTkButton(master=root, text='<', command=skip_back, width=2)
skip_b.place(relx=0.3, rely=0.7, anchor=tkinter.CENTER)

slider = customtkinter.CTkSlider(master=root, from_=0, to=1, command=volume, width=210)
slider.place(relx=0.5, rely=0.78, anchor=tkinter.CENTER)

progressbar = customtkinter.CTkProgressBar(master=root, progress_color='#32a85a', width=250)
progressbar.place(relx=.5, rely=.85, anchor=tkinter.CENTER)

time_label = tkinter.Label(root, text="", bg='#222222', fg='white')
time_label.place(relx=0.5, rely=0.9, anchor=tkinter.CENTER)

label1 = tkinter.Label(root, image=None, bg='#222222')
label1.place(relx=0.5, rely=0.3, anchor=tkinter.CENTER)

song_name_label = tkinter.Label(root, text="", bg='#222222', fg='white', font=('Helvetica', 16, 'bold'))
song_name_label.place(relx=0.5, rely=0.55, anchor=tkinter.CENTER)

artist_label = tkinter.Label(root, text="", bg='#222222', fg='white')
artist_label.place(relx=0.5, rely=0.6, anchor=tkinter.CENTER)

# Start the GUI main loop
root.mainloop()
