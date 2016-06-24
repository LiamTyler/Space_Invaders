try:
    import Tkinter as tk
except ImportError:
    import tkinter as tk
 
DIRECT_DICT = {'Up'    : ( 0,-1),
               'Down'  : ( 0, 1),
               'Left'  : (-1, 0),
               'Right' : ( 1, 0)}
 
 
class Sprite():
    def __init__(self,location,size):
        self.x,self.y = location
        self.width,self.height = size
        self.speed = 10
 
    def updater(self,canvas,keys):
        rect = (self.x,self.y,self.x+self.width,self.y+self.height)
        canvas.create_image(self.x,self.y, image = ship)
        for key in DIRECT_DICT:
            if keys.get(key,False):
                self.x += DIRECT_DICT[key][0]*self.speed
                self.y += DIRECT_DICT[key][1]*self.speed
 
 
class Control():
    def __init__(self):
        self.root = tk.Tk()
        self.canvas = tk.Canvas(self.root,width=500,height=500,bg='dark slate gray')
        self.canvas.focus_set()
        self.canvas.bind("<Key>",self.key_pressed)
        self.canvas.bind("<KeyRelease>",self.key_released)
        self.canvas.pack()
        self.fps = 60
        self.player = Sprite((250,250),(50,50))
        self.pressed = {}
 
    def key_pressed(self,event):
        self.pressed[event.keysym] = True
 
    def key_released(self,event):
        self.pressed[event.keysym] = False
 
    def update(self):
        self.canvas.delete(tk.ALL)
        self.player.updater(self.canvas,self.pressed)
        self.root.after(1000//self.fps,self.update)
 
    def main(self):
        self.update()
        self.root.mainloop()
 
 
if __name__ == "__main__":
    run_it = Control()
    ship = tk.PhotoImage(file = 'ship.gif')
    run_it.main()
