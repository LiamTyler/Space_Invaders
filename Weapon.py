import tkinter
import time

class Bullet:
    def __init__(self, canvas, x, y):
        self.x = x
        self.y = y
        self.width = 5
        self.height = 12
        self.speed = 3
        self.color = 'red'
        # Is the bullet 'alive' and not need deletion?
        self.alive = True
        self.canvas = canvas
        self.image = canvas.create_rectangle(x, y,
                                            x + self.width, y + self.height, fill=self.color)

    def update(self):
        self.canvas.delete(self.image)
        self.y -= self.speed
        # if our new position is off screen, delete the bullet
        if self.y < 0:
            self.alive = False
            return False
        else:
            # Else, draw new bullet and return don't delete
            self.image = self.canvas.create_rectangle(self.x, self.y,
                        self.x + self.width, self.y + self.height, fill=self.color)
            return True

class Weapon:
    def __init__(self, canvas, x, y):
        self.x = x
        self.y = y
        self.canvas = canvas
        self.canvas.bind("<space>", self.fire)
        self.canvas.bind("<KeyRelease-space>", self.fire_release)
        self.power = 1
        self.bullets = []
        self.last_fire = -1000
        self.fire_rate = .3
        self.shots_fired = 0
        # So we don't have to keep pressing the space bar to fire while moving
        self.firing = False
        

    def fire(self, event):
        new_fire = time.time()
        # Limit the firing to the fire_rate (shots / sec)
        if new_fire - self.last_fire > self.fire_rate:
            self.firing = True
            self.shots_fired += 1
            self.last_fire = new_fire
            self.bullets.append(Bullet(self.canvas, self.x, self.y - 20))

    def fire_release(self, event):
        self.firing = False

    def update(self, x, y):
        self.x = x
        self.y = y
        # Still firing / holding down the space bar?
        if self.firing:
            self.fire(None)

        # move all bullets, only add still alive bullets to new list
        new_bullets_list = []
        for bullet in self.bullets:
            if bullet.update():
                new_bullets_list.append(bullet)
                
        self.bullets = new_bullets_list

class PlayerStd(Weapon):
    
    def __init__(self, canvas, x, y, r = 4, d = 1):
        super().__init__(canvas, x, y, d)
        

        
