import tkinter as tk

class Move:
    def __init__(self, root, canvas, x, y, speed, vel_x, vel_y):
        self.root = root
        self.canvas = canvas
        self.x = x
        self.y = y
        self.speed = speed
        self.vel_x = vel_x
        self.vel_y = vel_y

    def update_position(self, x, y):
        self.x = x
        self.y = y

    def update_velocity(self, vel_x, vel_y):
        self.vel_x = vel_x
        self.vel_y = vel_y

class Sprite(Move):
    def __init__(self, root, canvas, x, y, speed, vel_x, vel_y, photo):
        super().__init__(root, canvas, x, y, speed, vel_x, vel_y)
        self.photo = tk.PhotoImage(file = photo)
        self.image = canvas.create_image(x, y, image = self.photo)
        self.hWidth = self.photo.width() / 2
        self.hHeight = self.photo.height() / 2

    def redraw(self):
        self.canvas.delete(self.image)
        self.image = self.canvas.create_image(self.x, self.y, image = self.photo)

    def get_colliding_tags(self):
        overlapping_items = self.canvas.find_overlapping(self.x - self.hWidth,
                                                         self.y - self.hHeight,
                                                         self.x + self.hWidth,
                                                         self.y + self.hHeight)
        tags = []
        if len(overlapping_items) > 2:
            for item in overlapping_items:
                tags.append(self.canvas.gettags(item))
        return tags
