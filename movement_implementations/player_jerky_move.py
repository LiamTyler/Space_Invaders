import tkinter as tk

class Player:
    
    key_map = {'Up'    : ( 0,-1),
               'Down'  : ( 0, 1),
               'Left'  : (-1, 0),
               'Right' : ( 1, 0)}
        
    def __init__(self, root, canvas, x = 300, y = 50, speed = 5):
        self.root = root
        self.ship_image = tk.PhotoImage(file = 'ship.gif')
        self.canvas = canvas
        self.image = canvas.create_image(x, y, image = self.ship_image)
        self.canvas.bind("<Key>",self.key_pressed)
        self.canvas.bind("<KeyRelease>",self.key_released)
        self.x = x
        self.vel_x = 0
        self.y = y
        self.vel_y = 0
        self.speed = speed

    def update(self):
        self.x += self.vel_x
        self.y += self.vel_y
        self.canvas.delete(self.image)
        self.image = self.canvas.create_image(self.x, self.y, image = self.ship_image)
        self.root.after(1000 // 60, self.update)
        
        
    def key_pressed(self, event):
        self.vel_x = self.speed * Player.key_map[event.keysym][0]
        self.vel_y = self.speed * Player.key_map[event.keysym][1]

    def key_released(self, event):
        self.vel_y = {'Up':  0, 'Down': 0,
                      'Left': self.vel_y, 'Right': self.vel_y}[event.keysym]
        self.vel_x = {'Up':  self.vel_x, 'Down': self.vel_x,
                      'Left': 0, 'Right': 0}[event.keysym]
    
window = tk.Tk()
window.title("Player movement")
canvas = tk.Canvas(window, height = 600, width = 600)
canvas.pack()
canvas.focus_set()

FPS = 60
player = Player(window, canvas, speed = 4)
player.update()
window.mainloop()
        
