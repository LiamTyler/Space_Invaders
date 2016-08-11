import tkinter as tk
import time

from player import Player
from Weapon import *
from Enemy import *

class Game:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Player movement")
        self.canvas = tk.Canvas(self.root, height = 600, width = 600)
        self.canvas.pack()
        self.canvas.focus_set()
        self.FPS = 60
        self.bkgd = tk.PhotoImage(file='img/gif/space_bkgd.gif')
        self.canvas.create_image(400,425,image=self.bkgd, tags='canvas')
        self.player_1 = Player(self.root, self.canvas)
        self.enemy = Enemy(self.root, self.canvas)
        self.update()
        self.root.mainloop()

    def update(self):
        self.player_1.update()
        self.player_1.collision_detection()
        self.enemy.update()
        self.root.after(1000 // self.FPS, self.update)

game = Game()
