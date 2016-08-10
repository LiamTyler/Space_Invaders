import tkinter as tk
import time
from Weapon import *
from Move import Sprite

class Player(Sprite):
    def __init__(self, root, canvas, x = 300, y = 550, speed = 5,
                 vel_x = [0,0], vel_y = [0,0], photo = 'img/gif/ship.gif'):
        super().__init__(root, canvas, x, y, speed, vel_x, vel_y, photo)
        # Bind the movement keys + releases
        self.canvas.bind("<Left>",self.key_pressed_left)
        self.canvas.bind("<Right>",self.key_pressed_right)
        self.canvas.bind("<Up>",self.key_pressed_up)
        self.canvas.bind("<Down>",self.key_pressed_down)
        self.canvas.bind("<KeyRelease-Left>",self.key_released_left)
        self.canvas.bind("<KeyRelease-Right>",self.key_released_right)
        self.canvas.bind("<KeyRelease-Up>",self.key_released_up)
        self.canvas.bind("<KeyRelease-Down>",self.key_released_down)
        self.health = 10
        self.hit = 0
        self.weapon = PlayerWeapon(self.canvas, self.x, self.y)

    def update(self):
        self.health -= self.hit
        if self.health <= 0:
            return -1
        # update position
        self.x += self.speed * self.vel_x[0]
        self.y += self.speed * self.vel_y[0]
        # update weapon
        self.weapon.update(self.x, self.y)
        # Redraw image
        self.redraw()
        return 0

    def collision_detection(self):
        tags = self.get_colliding_tags()
        #print(tags)

    
    # Movement bindings with a sort of linked list principle, where
    #    the head 'node' (element here) is always the one that will be used for
    #    updating the position. If vel_x was [1, -1] the player would be moving
    #    right, but as soon as the let go of the right key, the list would
    #    become [-1, 0] (since they are still holding left) and allow for
    #    a smooth transition to moving left. No jerky frames.
    def key_pressed_left(self, event):
        if self.vel_x[0] != -1:
            self.vel_x = [-1] + self.vel_x[:1]
            
    def key_pressed_right(self, event):
        if self.vel_x[0] != 1:
            self.vel_x = [1] + self.vel_x[:1]

    def key_pressed_up(self, event):
        if self.vel_y[0] != -1:
            self.vel_y = [-1] + self.vel_y[:1]

    def key_pressed_down(self, event):
        if self.vel_y[0] != 1:
            self.vel_y = [1] + self.vel_y[:1]
     

    def key_released_left(self, event):
        if self.vel_x[0] == -1:
            self.vel_x = self.vel_x[1:] + [0]
        else:
            self.vel_x[1] = 0

    def key_released_right(self, event):
        if self.vel_x[0] == 1:
            self.vel_x = self.vel_x[1:] + [0]
        else:
            self.vel_x[1] = 0

    def key_released_up(self, event):
        if self.vel_y[0] == -1:
            self.vel_y = self.vel_y[1:] + [0]
        else:
            self.vel_y[1] = 0

    def key_released_down(self, event):
        if self.vel_y[0] == 1:
            self.vel_y = self.vel_y[1:] + [0]
        else:
            self.vel_y[1] = 0
        
