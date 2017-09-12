# Done in December 2014

from tkinter import *
import time
import random
import urllib.request as ul

class Sprite:
    #This class is a parent class for most objects that move on the scren
    #it records their position on the canvas, which canvas to display on,
    #tags the sprite has, and speed of the sprite
    def __init__(self, canvas, location, speed, tags = tuple('')):
        self.canvas = canvas
        self.x,self.y = location
        self.speed = speed
        self.tags = tags
        
    #Sprites need to know if they are overlapping, so this method and does that.
    #it finds the tags it is overlapping, and then if there are more than 2
    #(sprites always overlap themselves and the canvas), then look to see if
    #the collision was important. No_event_collision is a tuple of the first
    #letter of the tags the sprite shouldnt care about.
        
    def collision(self,no_event_collision):
        w = self.photo.width() / 2
        h = self.photo.height() / 2
        a = self.canvas.find_overlapping(self.x - w,\
                self.y - h,self.x + w,self.y + h)
        
        tags = []
        if len(a) > 2:
            for item in range(len(a)):
                b = list(self.canvas.gettags(a[item]))
                tags += [b[x] for x in range(len(b)) if \
                    b[x][0].lower() not in no_event_collision]

        return tags

class PlayerGroup:
    #This is just a list of the player objects that are playing
    def __init__(self, players, canvas):
        self.players = []
        self.canvas = canvas
        self.shots = 0

        #Initializes the players according to the number (1 or 2)
        if players == 1:
            self.canvas.create_text(100,25,text='P1 Health: ',fill='white',
                                    font=('Calibri',30), tags='canvas')
            self.players.append(Player(self.canvas,(400,773),
                                ('Left','Right','Up','Down','space'),(0,800),
                                (650,850),10,10,'../img/gif/ship1.gif',('player','p1')))
        elif players == 2:
            self.canvas.create_text(100,25,text='P1 Health: ',fill='white',
                                    font=('Calibri',30), tags='canvas')
            self.players.append(Player(self.canvas,(400,773),
                                ('Left','Right','Up','Down','Control_R'),(0,800),
                                (650,850),10,10,'../img/gif/ship1.gif',('player','p1')))
            self.canvas.create_text(600,25,text='P2 Health: ',fill='white',
                                    font=('Calibri',30), tags='canvas')
            self.players.append(Player(self.canvas,(600,773),
                                ('a','d','w','s','space'),(0,800),
                                (650,8504),10,10,'../img/gif/ship2.gif',('player','p2')))

    #Goes through each player and updates them. If the update returns that the
    #player has no health, the player is deleted from the list
    def update(self,keys):
        player = 0
        while player < len(self.players):
            if not(self.players[player].update(keys)):
                self.shots += self.players[player].total_shot
                del(self.players[player])
            else:
                player += 1
            
        return len(self.players)


class Player(Sprite):
    #This class holds all the info for the player. The variable names
    #are pretty self explanatory
    def __init__(self, canvas, location, controls, x_boundaries,y_boundaries,
                 health, speed, photo,tags):
        #using super() to inherit the master sprite classes's attributes
        super().__init__(canvas,location,speed, tags)
        self.health = health
        #Display the health of the player on the top of the screen
        self.canvas.create_text(210 + 500*(self.tags[1] == 'p2'),25,
                        text= str(self.health), fill='white',
                        font=('Calibri',30), tags=(self.tags[1] + 'health'))
        #controls is a list of key presses that do things. The first 4 elements
        #correspond to the keys that make the character move left, right, up,
        #down, and the last element is the fire button
        self.controls = controls[:4]
        self.fire = controls[4]
        self.move = {controls[0] : (-1,0), controls[1] : (1,0),
                     controls[2] : (0,-1), controls[3] : (0,1)}
        self.photo = PhotoImage(file = photo)
        self.x_min = x_boundaries[0] + 2 + self.photo.width()/2
        self.x_max = x_boundaries[1] - self.photo.width()/2
        self.y_min = y_boundaries[0] + 2 + self.photo.height()/2
        self.y_max = y_boundaries[1] - self.photo.height()/2
        self.image = canvas.create_image(self.x,self.y,image=self.photo,tags=self.tags)
        self.last_shot = 0
        self.total_shot = 0
        self.weapon = Weapon('player',canvas,
            (self.x,self.y - self.photo.height()//2),self.photo,speed, tags[1])

    #This method finds out where to move the object, shoot if told to, and
    #Checks for collision. If it hits a real enemy, it dies automatically.
    #if it just hits a bullet, it takes that bullets damage
    def update(self,keys):
        self.canvas.delete(self.image)
        self.last_shot += 1
        for key in keys:
            if key in self.controls:
                self.x = max(self.x_min,min(self.x_max,
                                             self.x+self.move[key][0]*self.speed))
                self.y = max(self.y_min,min(self.y_max,
                                             self.y+self.move[key][1]*self.speed))
                
            elif key == self.fire and self.last_shot > 10:
                self.last_shot = 0
                self.total_shot += 1
                self.weapon.fire()
        self.weapon.update(self.x,self.y)
        self.image = self.canvas.create_image(self.x,self.y,image=self.photo,tags=self.tags)
        a = self.collision(('c','p'))
        if a:
            if 'Enemy' in a:
                self.health = 0
            else:
                #bullet damage is held in the tag. The tag after 'eb' will be
                #'eb_x' where x is the damage amount for that bullet
                self.health -= int(a[a.index('eb') + 1][3:])
                self.canvas.delete(self.tags[1] + ('health'))
                self.canvas.create_text(210 + 500*(self.tags[1] == 'p2'),
                        25,text=str(self.health),
                        fill='white',font=('Calibri',30),
                        tags=(self.tags[1] + 'health'))

            if self.health <= 0:
                for tag in self.tags:
                    self.canvas.delete(tag)
        return (self.health > 0)

class Enemy(Sprite):
    #This creates the enemy, and all the info about that enemy
    #There are 3 main types of enemies, just with varrying health
    def __init__(self, name, rate, canvas,location,health=0):
        self.name = name
        if name == 'E1':
            self.photo = '../img/gif/alien1.gif'
            self.tags = ('Enemy', 'E1')
            self.health = 5
        elif name == 'E2':
            self.photo = '../img/gif/alien2.gif'
            self.tags = ('Enemy', 'E2')
            self.health = 2
        elif name == 'E3':
            self.photo = '../img/gif/alien3.gif'
            self.tags = ('Enemy', 'E1')
            self.health = 1
        
        self.rate = rate
        if health:
            self.health = health
        self.dead = False
        super().__init__(canvas,location,None, self.tags)
        self.photo = PhotoImage(file = self.photo)
        self.image = canvas.create_image(self.x,self.y,image=self.photo, tags=self.tags)
        self.weapon = Weapon('E',canvas,location,self.photo,5,('E'))


    def update(self,dx,dy):
        self.x += dx
        self.y += dy
        self.weapon.update(self.x,self.y)
        a = self.collision(('c','e'))
        #Only check for collisions if the enemy is alive
        if a and not(self.dead):
            if 'pb' in a:
                self.health -= int(a[a.index('pb') + 1][3:])
                if 0 >= self.health:
                    self.dead = True
        self.canvas.delete(self.image)
        if not(random.randint(0,self.rate)):
            self.weapon.fire()
        if self.health > 0:
            self.image = self.canvas.create_image(self.x,self.y,image=self.photo,tags = self.tags)
           
        return self.dead
        
     
class EnemyGroup:
    #based on a set up number, create a group of enemies. Each set up has differnt
    #characteristics
    def __init__(self, set_up, canvas, location):
        self.canvas = canvas
        self.distance = 0
        self.group = []
        if set_up == 1:            
            for r in range(3):
                self.group.append([])
                for c in range(10):
                    if not(r % 3):
                        e = 'E1'
                    if r % 3 == 1:
                        e = 'E2'
                    if r % 3 == 2:
                        e = 'E3'
                    self.group[r].append(Enemy(e,300,self.canvas,
                        (location[0] + c*56,location[1] + r*42)))
            #total health of the group
            self.total_health = 90
            self.speed = 1
            self.direction = [1,0]
            self.xdirec = 1
        
    #This method simply finds out where the enemy should go, and if the enemy
    #is alive. The enemies move from side to side, and when the left or right
    #most enemy hits a side, the whole group slides down a set distance,
    #then goes to the other side. If the group is at the bottom, it just goes
    #side to side.
    def update(self):
        furthest_left = 800
        furthest_right = 0        
        for enemy_row in self.group:
            if enemy_row[0].x < furthest_left:
                furthest_left = enemy_row[0].x
            if enemy_row[-1].x > furthest_right:
                furthest_right = enemy_row[-1].x

        if self.group[-1][0].y > 797:
            dy = 0
            if (furthest_right + 25.5 + self.speed) > 800 or \
                (furthest_left - 25.5 - self.speed) < 0:
                self.xdirec *= -1
            dx = self.speed*self.xdirec
        else:    
            if self.direction[0]:
                if (furthest_right + 25.5 + self.speed) > 800 or \
                    (furthest_left - 25.5 - self.speed) < 0:
                    dx = 0
                    dy = self.speed
                    self.direction = [0,1]
                else:
                    dx = self.speed*self.xdirec
                    dy = 0
            else:
                if self.distance >= 50:
                    dy = 0
                    self.xdirec = self.xdirec * -1
                    dx = self.speed*self.xdirec
                    self.direction = [self.xdirec, 0]
                    self.distance = 0
                else:
                    dx = 0
                    dy = self.speed
                    self.distance += dy
                
        row = 0
        num_alive = 0
        #even if the enemy is dead, it wont actually be deleted out of the
        #list until all of its bullets are gone, because we need the enemy
        #to know where its bullets are.
        while row < len(self.group):
            enemy = 0
            while enemy < len(self.group[row]):
                if self.group[row][enemy].update(dx,dy) and \
                   self.group[row][enemy].weapon.bullets == []:
                    del(self.group[row][enemy])
                    self.speed += .2
                else:
                    enemy += 1
            if self.group[row] == []:
                del(self.group[row])
            row += 1
            num_alive += enemy
        return num_alive
                

class Weapon(Sprite):
    def __init__(self, name, canvas, location, photo, speed, tags):
        super().__init__(canvas,location,speed,tags)
        self.canvas = canvas
        self.bullets = []
        self.count = 0
        if name == 'player':
            self.name = 'pw'
            self.damage = 1
            self.shape = 'circle'
            self.color = 'blue'
            self.ox = 0
            self.oy = -photo.height() / 2
            self.y += self.oy
        if name == 'E':
            self.name = 'ew'
            self.damage = 2
            self.shape = 'line'
            self.color = 'red'
            self.ox = 0
            self.oy = photo.height() / 2 + 5
            self.y += self.oy
        
    def fire(self):
        self.count += 1
        if self.name == 'pw':
            bullet = Bullet(self.canvas, 'pb', 5, self.color, (self.x,self.y),
                            14,tags=(self.tags,'pb','pb_1'))
        if self.name == 'ew':
            bullet = Bullet(self.canvas, 'eb',20, self.color,(self.x,self.y),
                            5,tags=(self.tags,'eb','eb_1'))

        bullet.draw_bullet()    
        self.bullets.append(bullet)

    def update(self,x,y):
        self.x = x + self.ox
        self.y = y + self.oy
        bullet = 0
        while bullet < len(self.bullets):
            b = self.bullets[bullet]
            if b.hit == True:
                b.canvas.delete(b.image)
                del(self.bullets[bullet])
                bullet -= 1
            bullet += 1

        for b in self.bullets:
            b.canvas.delete(b.image)
            if b.type == 'pb':
                b.y -= b.speed
                b.draw_bullet()
                if b.y < 0 or 'Enemy' in b.collision():
                    b.hit = True
            if b.type == 'eb':
                b.y += b.speed
                b.draw_bullet()
                if b.y > 800 or 'player' in b.collision():
                    b.hit = True
                    
class Bullet(Sprite):
        def __init__(self, canvas, kind, size, color, location, speed, tags):
            super().__init__(canvas,location,speed,tags)
            self.type = kind
            self.ix,self.iy = self.x,self.y
            self.color = color
            self.hit = False
            self.size = size
            self.image = ''
            
        def draw_bullet(self):    
            if self.type == 'pb':
                r = self.size
                self.image = self.canvas.create_oval(self.x-r,self.y-r,self.x+r,
                        self.y+r, fill=self.color, tags=self.tags)
            if self.type == 'eb':
                self.image = self.canvas.create_line(self.x,self.y,
                    self.x,self.y+self.size,width=5,fill=self.color,tags=self.tags)

        def collision(self):
            a = self.canvas.find_overlapping(self.x - self.size,\
                            self.y - self.size,self.x + self.size,\
                            self.y + self.size)
            tags = []
            if len(a) > 2:
                for item in range(len(a)):
                    tags += list(self.canvas.gettags(a[item]))
            return tags


class Game:
    def __init__(self, menu, root,canvas, players, fps):
        self.menu = menu
        self.root = root
        self.canvas = canvas
        self.FPS = fps
        self.bkgd1 = PhotoImage(file='../img/gif/space_bkgd.gif')
        self.canvas.create_image(400,425,image=self.bkgd1, tags='canvas')
        self.canvas.create_line(0,25,800,25,fill = 'black',
                                width = 50, tags = 'canvas')
        self.canvas.create_line(0,50,800,50, fill = 'white',
                                width = 3, tags = 'canvas')
        self.keys = []
        self.canvas.pack()
        self.canvas.bind("<Key>",self.key_press)
        self.canvas.bind("<KeyRelease>",self.key_release)
        self.canvas.focus_set()
        self.after = None
        self.nplayers = players
        self.players = PlayerGroup(players,canvas)
        self.enemyG = EnemyGroup(1, self.canvas, (100,100))
        self.time = time.time()

    def key_press(self,event):
        if event.keysym not in self.keys:
            self.keys.append(event.keysym)

    def key_release(self,event):
        if event.keysym in self.keys:
            del(self.keys[self.keys.index(event.keysym)])

    def update(self):
        if not(self.players.update(self.keys)):
            self.gameover()
        elif not(self.enemyG.update()):
            self.win()
        else:
            self.after = self.root.after(1000//self.FPS,self.update)


    def gameover(self):
        self.root.after_cancel(self.after)
        self.canvas.create_text(400,400,text='GAME OVER', fill = 'white',
                                font=('Calibri',72))

        for x in range(self.FPS * 3):
            self.enemyG.update()
            self.canvas.update()
            time.sleep(1/self.FPS)

        self.keys = []
        self.high_scores()            
            
    def high_score_update(self, keys):
        if keys:
            self.root.after_cancel(self.after)
            self.root.destroy()
            self.menu.__init__()
            self.menu.root.focus_force()
            self.menu.main()
        else:
            self.after = self.root.after(1000//self.FPS,self.high_score_update,self.keys)

    def high_scores(self):
        self.canvas.delete(ALL)
        self.canvas.create_image(400,425,image = self.bkgd1, tags='canvas')
        self.canvas.create_text(400,100,text="High Scores", fill = "white",
                                font=('Calibri', 50), tags='text')
        self.canvas.create_text(250,300,text = 'Single Player', fill = "white",
                                font=('Calibri', 28), tags='text')
        self.canvas.create_text(550,300,text = 'Two Player',fill = "white",
                                font=('Calibri', 28), tags='text')
        self.canvas.create_text(400,750,text = 'Press Any Key to Return',
                                fill = 'white', font=('Calibri',18),tags='text')
        try:
            file = open('si_highscores.txt','r+')
        except:
            file = open('si_highscores.txt','w')
            for x in range(8):
                file.write('000000\n')
            for x in range(8):
                file.write('000000\n')
            file.close()
            file = open('si_highscores.txt','r+') 

        file_r = file.readlines()
        line =  0
        while line < len(file_r)/2:
            self.canvas.create_text(250,350 + line*30,text = \
                                file_r[line].strip(), fill = "white",
                                font=('Calibri', 18 ), tags='text')
            self.canvas.create_text(550,350 + line*30,text = \
                                file_r[line+8].strip(), fill = "white",
                                font=('Calibri', 18 ), tags='text')
            line += 1

        file.close()
        self.high_score_update(self.keys)           

    def win(self):
        self.root.after_cancel(self.after)
        self.time = max(0, 300 - time.time() + self.time)
        self.phealths = 0
        self.accuracy = 0
        for player in self.players.players:
            self.phealths += player.health
            self.accuracy += player.total_shot
        self.phealths /= len(self.players.players)
        self.accuracy = 90/(self.accuracy + self.players.shots)
        self.score = int(self.time * self.phealths * self.accuracy)
        self.canvas.delete(ALL)
        self.canvas.create_image(400,425,image = self.bkgd1, tags='canvas')
        self.canvas.create_text(400,100,text="High Scores", fill = "white",
                                font=('Calibri', 50), tags='text')
        self.canvas.create_text(250,300,text = 'Single Player', fill = "white",
                                font=('Calibri', 28), tags='text')
        self.canvas.create_text(550,300,text = 'Two Player',fill = "white",
                                font=('Calibri', 28), tags='text')
        try:
            file = open('si_highscores.txt','r+')
        except:
            file = open('si_highscores.txt','w')
            for x in range(8):
                file.write('0\n')
            for x in range(8):
                file.write('0\n')
            file.close()
            file = open('si_highscores.txt','r+')

        file_r = file.readlines()
        line =  0
        self.highscores1 = []
        self.highscores2 = []
        while line < len(file_r)/2:
            self.highscores1.append(int(file_r[line].strip()))
            self.highscores2.append(int(file_r[line+8].strip()))
            self.canvas.create_text(250,350 + line*30,text = \
                                file_r[line].strip(), fill = "white",
                                font=('Calibri', 18 ), tags='text')
            self.canvas.create_text(550,350 + line*30,text = \
                                file_r[line+8].strip(), fill = "white",
                                font=('Calibri', 18 ), tags='text')
            line += 1

        file.close()
        self.canvas.update()
        time.sleep(3)
        self.canvas.delete(ALL)
        self.canvas.create_image(400,425,image = self.bkgd1, tags='canvas')
        

        if (self.nplayers == 1 and self.score > self.highscores1[-1]) or \
            (self.nplayers == 2 and self.score > self.highscores2[-1]):
            self.canvas.create_text(250,300,text = 'NEW HIGHSCORE!', fill = "white",
                                font=('Calibri', 28), tags='text')
            self.canvas.update()
            time.sleep(2)

            if self.nplayers == 1:
                self.highscores1[-1] = self.score
                self.highscores1.sort()
                self.highscores1 = self.highscores1[::-1]
            else:
                self.highscores2[-1] = self.score
                self.highscores2.sort()
                self.highscores2 = self.highscores2[::-1]

            file = open('si_highscores.txt','r+')
            for x in self.highscores1:
                file.write(str(x) + '\n')
            for x in self.highscores2:
                file.write(str(x) + '\n')
            file.close()

            self.root.destroy()
            self.menu.__init__()
            self.menu.root.focus_force()
            self.menu.main()
            
            
        else:
            self.root.destroy()
            self.menu.__init__()
            self.menu.root.focus_force()
            self.menu.main()
            

    def main(self):
        self.update()
        self.root.mainloop()


class Menu:
    def __init__(self):
        self.FPS = 30
        self.root = Tk()
        self.canvas = Canvas(self.root, width = 800, height = 850, bd = 0 )
        self.bkgd = PhotoImage(file='../img/gif/space_bkgd.gif')
        self.canvas.create_image(400,425,image=self.bkgd, tags='canvas')
        self.keys = []
        self.canvas.pack()
        self.player = Player(self.canvas,(150,773),('Left','Right','Up','Down','space'),
                             (0,800),(600,800),30,10,'../img/gif/ship.gif',('player','p1'))
        self.canvas.bind("<Key>",self.key_press)
        self.canvas.bind("<KeyRelease>",self.key_release)
        self.canvas.focus_set()
        self.game = None
        self.enemies = [Enemy('E3',0,self.canvas,(100,350)),
                        Enemy('E2',0,self.canvas,(300,350)),
                        Enemy('E1',0,self.canvas,(500,350)),
                        Enemy('E2',0,self.canvas,(700,350))]

        self.after = None
                        
    def key_press(self,event):
        if event.keysym not in self.keys:
            self.keys.append(event.keysym)

    def key_release(self,event):
        if event.keysym in self.keys:
            del(self.keys[self.keys.index(event.keysym)])

    def play(self, players):
        self.canvas.delete(ALL)
        self.game = Game(self, self.root,self.canvas,players,self.FPS)
        self.game.update()

    def high_score_update(self,keys):
        if 'Escape' in keys:
            self.root.after_cancel(self.after)
            self.set_up()
            self.update()
        else:
            self.after = self.root.after(1000//self.FPS,self.high_score_update,self.keys)

    def high_scores(self):
        self.canvas.delete(ALL)
        self.canvas.create_image(400,425,image = self.bkgd, tags='canvas')
        self.canvas.create_text(400,100,text="High Scores", fill = "white",
                                font=('Calibri', 50), tags='text')
        self.canvas.create_text(250,300,text = 'Single Player', fill = "white",
                                font=('Calibri', 28), tags='text')
        self.canvas.create_text(550,300,text = 'Two Player',fill = "white",
                                font=('Calibri', 28), tags='text')
        self.canvas.create_text(400,750,text = 'Press Esc to Return',
                                fill = 'white', font=('Calibri',18),tags='text')
        try:
            file = open('si_highscores.txt','r+')
        except:
            file = open('si_highscores.txt','w')
            for x in range(8):
                file.write('0\n')
            for x in range(8):
                file.write('0\n')
            file.close()
            file = open('si_highscores.txt','r+') 

        file_r = file.readlines()
        line =  0
        while line < len(file_r)/2:
            self.canvas.create_text(250,350 + line*30,text = \
                                file_r[line].strip(), fill = "white",
                                font=('Calibri', 18 ), tags='text')
            self.canvas.create_text(550,350 + line*30,text = \
                                file_r[line+8].strip(), fill = "white",
                                font=('Calibri', 18 ), tags='text')
            line += 1

        file.close()
        self.high_score_update(self.keys)

    def controls(self):
        self.canvas.delete(ALL)
        self.canvas.create_image(400,425,image = self.bkgd, tags='canvas')
        self.canvas.create_text(200,100,text='One Player:',fill = 'white',
                                font=('Calibri',24), tags='text')
        self.canvas.create_text(200,200,text='Left: Left Arrow',fill = 'white',
                                font=('Calibri',16), tags='text')
        self.canvas.create_text(200,300,text='Right: Right Arrow',fill = 'white',
                                font=('Calibri',16), tags='text')
        self.canvas.create_text(200,400,text='Up: Up Arrow',fill = 'white',
                                font=('Calibri',16), tags='text')
        self.canvas.create_text(200,500,text='Down: Down Arrow',fill = 'white',
                                font=('Calibri',16), tags='text')
        self.canvas.create_text(200,600,text='Fire: Space Bar',fill = 'white',
                                font=('Calibri',16), tags='text')
        self.canvas.create_text(500,100,text='Two Player:',fill = 'white',
                                font=('Calibri',24), tags='text')
        self.canvas.create_text(500,200,text='P1 Controls:',fill = 'white',
                                font=('Calibri',20), tags='text')
        self.canvas.create_text(500,250,text='SAME MOVEMENT', fill = 'white',
                                font=('Calibri',20), tags='text')
        self.canvas.create_text(500,300,text='Fire: Right Control',fill = 'white',
                                font=('Calibri',20), tags='text')
        self.canvas.create_text(500,200,text='P2 Controls:',fill = 'white',
                                font=('Calibri',20), tags='text')
        self.canvas.create_text(500,350,text='Left: a',fill = 'white',
                                font=('Calibri',16), tags='text')
        self.canvas.create_text(500,400,text='Right: d',fill = 'white',
                                font=('Calibri',16), tags='text')
        self.canvas.create_text(500,450,text='Up: w',fill = 'white',
                                font=('Calibri',16), tags='text')
        self.canvas.create_text(500,500,text='Down: s',fill = 'white',
                                font=('Calibri',16), tags='text')
        self.canvas.create_text(500,550,text='Fire: Space Bar',fill = 'white',
                                font=('Calibri',16), tags='text')

        self.canvas.create_text(400,750,text = 'Press Esc to Return',
                                fill = 'white', font=('Calibri',18),tags='text')
        self.controls_update(self.keys)

    def controls_update(self,keys):
        if 'Escape' in keys:
            self.root.after_cancel(self.after)
            self.set_up()
            self.update()
        else:
            self.after = self.root.after(1000//self.FPS,self.controls_update,self.keys)

        
    def update(self):
        self.player.update(self.keys)
        enemy = 0
        flag = 0
        while enemy < len(self.enemies):
            if self.enemies[enemy].collision(('c','e')):
                flag = enemy + 1
                enemy = 3

            enemy += 1
            
        if flag:
            self.root.after_cancel(self.after)
            if flag == 1:
                self.play(1)
            if flag == 2:
                self.play(2)
            if flag == 3:
                self.high_scores()
            if flag == 4:
                self.controls()
        else:
            self.after = self.root.after(1000//self.FPS,self.update)

    def set_up(self):
        self.canvas.delete(ALL)
        self.canvas.create_image(400,425,image = self.bkgd, tags='canvas')
        self.canvas.create_text(400,100,text="Space Invaders", fill = "white",
                                font=('Calibri', 72), tags='text')
        self.canvas.create_line(105,160,690,160, fill = 'white',
                                width=5,tags='text')
        self.canvas.create_text(100,300,text="One Player", fill = "white",
                                font=('Calibri',24), tags='text')
        self.canvas.create_text(300,300,text="Two Player", fill = "white",
                                font=('Calibri',24), tags='text')
        self.canvas.create_text(500,300,text="High Scores", fill = "white",
                                font=('Calibri',24), tags='text')
        self.canvas.create_text(700,300,text="Controls", fill = "white",
                                font=('Calibri',24), tags='text')

        for enemy in self.enemies:
            self.canvas.create_image(enemy.x,enemy.y,image = enemy.photo,
                                     tags = enemy.tags)
    
    def main(self):
        self.player.update(self.keys)
        self.set_up()
        self.update()
        self.root.mainloop()
    

a = Menu()
a.main()
