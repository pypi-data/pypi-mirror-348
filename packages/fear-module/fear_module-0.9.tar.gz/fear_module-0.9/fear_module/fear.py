import os
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
from tkinter import *
from tkinter import ttk
import pygame
import keyboard as kb

pygame.init()
pygame.mixer.init()
devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
sys_vol = cast(interface, POINTER(IAudioEndpointVolume))


class FearClassException(Exception):
    pass


class Fear:
    def __init__(self, fullscreen=True, title="Выбрался всё таки", sleep=30, main_text="Ваши действия?", main_image="",
                 kb_block=True, volume=100):
        if main_image and not os.path.exists(main_image):
            raise FearClassException(f'Image "{main_image}" does not exist.')
        if volume < 0 or volume > 100:
            raise FearClassException("The volume should be between 0 and 100.")

        self.wind = Tk()
        self.wind.title(title)
        self.w_size = (self.wind.winfo_screenwidth(), self.wind.winfo_screenheight())
        self.wind.geometry(f"{self.w_size[0]}x{self.w_size[1]}")
        self.wind.attributes('-fullscreen', fullscreen)

        self.scenes, self.buttons, self.data = {"main": Frame(self.wind), }, {}, {
            "main": [PhotoImage(file=main_image), main_text]}
        self._state = "main"
        self.sleep, self.volume, self.main_text, self.running, self.block = sleep, volume, main_text, False, kb_block
        self.main_image = None
        self.on_quit = lambda: os.system("shutdown /s /t 1")

    @property
    def state(self):
        return self._state

    @state.setter
    def state(self, new_state):
        self.scenes[self._state].pack_forget()
        self._state = new_state
        self.scenes[self._state].pack()

    def setup(self):
        for sc in self.scenes.keys():
            lb = ttk.Label(self.scenes[sc], text=self.data[sc][1], font=("Arial", 30), image=self.data[sc][0],
                           justify=CENTER, anchor="center", compound="bottom")
            lb.pack()
        for but in self.buttons.keys():
            self.buttons[but].pack()

    def run(self):
        if not self.running:
            self.running = True
            if self.sleep < 0:
                raise FearClassException("The sleep time should be >= 0.")
            if self.block:
                Fear.block_keyboard()
            self.setup()
            self.wind.after(self.sleep * 1000, self.on_quit)
            self.wind.after(self.sleep * 1000 + 1, self.wind.quit)
            self.state = "main"
            self.wind.mainloop()

    def add_scene(self, name, text, image, sound, button_text, final=False):
        if name in self.scenes.keys():
            raise FearClassException(f'Scene "{name}" already exists.')
        if not os.path.exists(image):
            raise FearClassException(f'Image "{image}" does not exist.')
        if not os.path.exists(sound):
            raise FearClassException(f'Sound "{sound}" does not exist.')

        self.scenes[name] = Frame(self.wind)
        self.buttons[name] = ttk.Button(self.scenes["main"], text=button_text, width=self.w_size[0], style="W.TButton",
                                        command=lambda: self._button_function(name, sound, final))
        self.data[name] = [PhotoImage(file=image), text]

    def _button_function(self, scene_name, sound, final=False):
        if scene_name not in self.scenes.keys():
            raise FearClassException(f'Scene "{scene_name}" does not exist.')
        self.state = scene_name
        Fear.play_sound(sound, self.volume)
        if final:
            self.wind.after(3500, self.on_quit)
            self.wind.after(3501, self.wind.quit)
        else:
            self.buttons[scene_name].configure(state="disabled")

            def return_menu():
                self.state = "main"

            self.wind.after(3500, lambda: return_menu())

    @staticmethod
    def play_sound(sound, volume):
        if not os.path.exists(sound):
            raise FearClassException(f'Sound "{sound}" does not exist.')
        sys_vol.SetMute(0, None)
        sys_vol.SetMasterVolumeLevelScalar(volume / 100, None)
        pygame.mixer.music.load(sound)
        pygame.mixer.music.play()

    @staticmethod
    def block_keyboard(reverse=False):
        for i in range(150):
            if reverse:
                kb.unblock_key(i)
            else:
                kb.block_key(i)
