import tkinter as tk
import time
from Weapon import *
from Move import Sprite

class Enemy(Sprite):
    def __init__(self, root, canvas, x = 300, y = 50, speed = 5,
                 vel_x = 0, vel_y = 0, photo='img/gif/alien1.gif'):
        super().__init__(root, canvas, x, y, speed, vel_x, vel_y, photo)
        self.health = 10
        self.hit

    def update(self):
        self
