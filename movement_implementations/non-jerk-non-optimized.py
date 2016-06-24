import tkinter as tk
import time

class Player:
    
    key_map = {'Up'    : [True, -1],
               'Down'  : ( 0, 1),
               'Left'  : (-1, 0),
               'Right' : ( 1, 0)}
        
    def __init__(self, root, canvas, x = 300, y = 50, speed = 5):
        self.root = root
        self.ship_image = tk.PhotoImage(file = 'ship.gif')
        self.canvas = canvas
        self.image = canvas.create_image(x, y, image = self.ship_image)
        self.canvas.bind("<Left>",self.key_pressed_left)
        self.canvas.bind("<Right>",self.key_pressed_right)
        self.canvas.bind("<Up>",self.key_pressed_up)
        self.canvas.bind("<Down>",self.key_pressed_down)
        self.canvas.bind("<KeyRelease-Left>",self.key_released_left)
        self.canvas.bind("<KeyRelease-Right>",self.key_released_right)
        self.canvas.bind("<KeyRelease-Up>",self.key_released_up)
        self.canvas.bind("<KeyRelease-Down>",self.key_released_down)
        self.x = x
        self.vel_x = [[False, -1], [False, 1]]
        self.y = y
        self.vel_y = [[False, -1], [False, 1]]
        self.speed = speed
        self.health = None

    def update(self):
        if self.vel_x[0][0]:
            self.x += self.speed * self.vel_x[0][1]
        if self.vel_y[0][0]:
            self.y += self.speed * self.vel_y[0][1]
        self.canvas.delete(self.image)
        self.image = self.canvas.create_image(self.x, self.y, image = self.ship_image)
        self.root.after(1000 // 60, self.update)
        
        
    def key_pressed_left(self, event):
        if self.vel_x[0][1] == -1:
            self.vel_x[0][0] = True
        else:
            right, left = self.vel_x[0], self.vel_x[1]
            left[0] = True
            self.vel_x = [left, right]
            
    def key_pressed_right(self, event):
        if self.vel_x[0][1] == 1:
            self.vel_x[0][0] = True
        else:
            left, right = self.vel_x[0], self.vel_x[1]
            right[0] = True
            self.vel_x = [right, left]

    def key_pressed_up(self, event):
        if self.vel_y[0][1] == -1:
            self.vel_y[0][0] = True
        else:
            down, up = self.vel_y[0], self.vel_y[1]
            up[0] = True
            self.vel_y = [up, down]

    def key_pressed_down(self, event):
        if self.vel_y[0][1] == 1:
            self.vel_y[0][0] = True
        else:
            up, down = self.vel_y[0], self.vel_y[1]
            down[0] = True
            self.vel_y = [down, up]

    def key_released_left(self, event):
        if self.vel_x[0][1] == -1:
            self.vel_x[0][0] = False
            if self.vel_x[1][0]:
                self.vel_x = [self.vel_x[1], self.vel_x[0]]
        else:
            self.vel_x[1][0] = False

    def key_released_right(self, event):
        if self.vel_x[0][1] == 1:
            self.vel_x[0][0] = False
            if self.vel_x[1][0]:
                self.vel_x = [self.vel_x[1], self.vel_x[0]]
        else:
            self.vel_x[1][0] = False

    def key_released_up(self, event):
        if self.vel_y[0][1] == -1:
            self.vel_y[0][0] = False
            if self.vel_y[1][0]:
                self.vel_y = [self.vel_y[1], self.vel_y[0]]
        else:
            self.vel_y[1][0] = False

    def key_released_down(self, event):
        if self.vel_y[0][1] == 1:
            self.vel_y[0][0] = False
            if self.vel_y[1][0]:
                self.vel_y = [self.vel_y[1], self.vel_y[0]]
        else:
            self.vel_y[1][0] = False
    
window = tk.Tk()
window.title("Player movement")
canvas = tk.Canvas(window, height = 600, width = 600)
canvas.pack()
canvas.focus_set()

FPS = 60
player = Player(window, canvas, speed = 4)
player.update()
window.mainloop()
        
