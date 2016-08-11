import tkinter as tk
import time
from Weapon import *
from Move import Sprite

class Enemy(Sprite):
    def __init__(self, root, canvas, x = 300, y = 50, speed = 2,
                 vel_x = 0, vel_y = 1, photo='img/gif/alien1.gif'):
        super().__init__(root, canvas, x, y, speed, vel_x, vel_y, photo)
        self.health = 10
        self.hit = 0

    def update(self):
        self.health -= self.hit
        if self.health <= 0:
            return -1
        # update position
        self.x += self.speed * self.vel_x
        self.y += self.speed * self.vel_y
        # update weapon
        #self.weapon.update(self.x, self.y)
        # Redraw image
        self.redraw()
        return 0