import pygame as pg
from pygame import mixer
from pygame.locals import (K_UP, K_LEFT, K_RIGHT, K_DOWN)
import json

w = 1130
h = 800

class Mario:
    def __init__(self, x, y, surface):
        self.x_v = 0
        self.y_v = 0
        self.surface = surface
        self.i = 0
        self.pic = pg.image.load("mario/mario_standing.png").convert_alpha()
        self.inv = False
        self.jump = False
        self.hitbox = [x + 5, y, x + 45, y + 50]
        self.lasthb = [x+ 5, y, x + 45, y + 50]
        self.pipe = [False, 0, ""]
        self.star = False

    def draw(self):
        if self.inv:
            inv = "inv"
        else:
            inv = ""
        
        item = ""
        if self.star:
            item = "star/"
        
        if self.i == 0:
            self.pic = pg.image.load("mario/" + item + inv + "mario_run.png").convert_alpha()
        elif self.i == 2:
            self.pic = pg.image.load("mario/" + item + inv + "mario_run1.png").convert_alpha()
        elif self.i == 4:
            self.pic = pg.image.load("mario/" + item + inv + "mario_run2.png").convert_alpha()
        if self.x_v == 0:
            self.pic = pg.image.load("mario/" + item + inv + "mario_standing.png").convert_alpha()
        if not self.jump:
            self.pic = pg.image.load("mario/" + item + inv + "mario_jump.png").convert_alpha()
        
        self.surface.blit(self.pic, (self.hitbox[0] - 2, self.hitbox[1]))
        #pg.draw.rect(self.surface, (0,0,0), ((self.hitbox[0], self.hitbox[1]), (self.hitbox[2]-self.hitbox[0], self.hitbox[3]- self.hitbox[1])),3)
    
    def move(self):
        self.lasthb[1] = self.hitbox[1]
        self.lasthb[3] = self.hitbox[3]
        self.y_v += 1
        
        if self.x_v > 0 and not keys[K_RIGHT]:
            self.x_v -= 0.5
            
        if self.x_v < 0 and not keys[K_LEFT]:
            self.x_v += 0.5
        
        if keys[K_LEFT]:
            self.inv = True
            self.i = self.i + 1
            if self.star:
                if self.x_v >= -15:
                    self.x_v -= 0.5
            elif self.x_v >= -10:
                self.x_v -= 0.5
            
        if keys[K_RIGHT]:
            self.inv = False
            self.i = self.i + 1
            if self.star:
                if self.x_v <= 15:
                    self.x_v += 0.5
            elif self.x_v <= 10:
                self.x_v += 0.5
        
        if self.star:
            self.star_i += 1
            if self.star_i > 12 * 30:
                self.star = False            
                mixer.init()
                mixer.music.load('song.mp3')
                mixer.music.play()
        
        if self.i >= 6:
            self.i = 0
        
        if keys[K_UP] and self.jump:
            self.y_v = -20
            self.jump = False
            
        self.hitbox[1] += self.y_v
        self.hitbox[3] += self.y_v

    def pipeDown(self):
        global marioSave
        
        if self.hitbox[1] >= self.pipe[1] + 30:
            if self.pipe[2] == "UP":
                return False
            marioSave = [self.star, 0]
            if marioSave[0]:
                marioSave[1] = self.star_i
            loadMap(self.pipe[2] + ".json", 400, -50)
            mario.hitbox[1] = self.pipe[1] - 55
            mario.hitbox[3] = self.pipe[1] - 5
            return True
        else:
            self.hitbox[1] += 2
            self.hitbox[3] += 2
            self.lasthb[1] += 2
            self.lasthb[3] += 2
            return True
        
    def flag(self, pipes, grounds, blocks, bricks, entities, flag, window):
        clock = pg.time.Clock()
        
        cont = True
        
        color = (100,100,255)
        cloud = pg.image.load("clouds.png").convert_alpha()
        
        while cont:
            clock.tick(30)
            
            window.fill(color)
            window.blit(cloud, (600, 100))
            window.blit(cloud, (-50, 50))
            
            
            mario.draw()
            mario.x_v = 1
            mario.move()
            mario.hitbox[0] += 5
            mario.hitbox[2] += 5
            for ground in grounds:
                wallcolMario(mario, ground, entities)
            
            for obj in pipes + grounds + blocks + bricks + entities:
                obj.draw()
            
            flag.draw()
            
            
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    cont = False
        
            pg.display.flip()

class Star:
    def __init__(self, x, y, surface):
        self.hitbox = [x, y, x + 50, y + 50]
        self.lasthb = [x, y, x + 50, y + 50]
        self.pic = pg.image.load('star.png').convert_alpha()
        self.x_v = 2
        self.y_v = -5
        self.surface = surface
        self.dead = False
        self.friendlyFire = False
    
    def draw(self):
        if not self.dead:
            self.surface.blit(self.pic, (self.hitbox[0], self.hitbox[1]))
    
    def move(self):
        self.lasthb[0] = self.hitbox[0]
        self.lasthb[2] = self.hitbox[2]
        
        self.y_v += 0.5
        
        self.hitbox[0] += self.x_v
        self.hitbox[2] += self.x_v
        self.hitbox[1] += self.y_v
        self.hitbox[3] += self.y_v
        
        self.hitbox[0] -= mario.x_v
        self.hitbox[2] -= mario.x_v
        
    def die(self):
        self.dead = True
        self.x_v = 0
        mario.star = True
        mario.star_i = 0
        mixer.init()
        mixer.music.load('mario/star/star_song.mp3')
        mixer.music.play()
        
    def delete(self):
        self.die()
        
class Goomba:
    def __init__(self, x, y, surface):
        self.x_v = -3
        self.y_v = 0
        self.surface = surface
        self.hitbox = [x, y, x + 45, y + 45]
        self.lasthb = [x, y, x + 45, y + 45]
        self.i = 0
        self.pic = pg.image.load("goomba.png").convert_alpha()
        self.dead = False
        self.deadcount = 0
        self.inv = False
        self.friendlyFire = False
        self.moving = False
    
    def draw(self):
        if self.dead:
            if self.i < 12:
                self.pic = pg.image.load("goomba_stomp.png").convert_alpha()
                self.surface.blit(self.pic, (self.hitbox[0], self.hitbox[1]))
            else:
                return
        else:
            if self.i == 0:
                self.pic = pg.image.load("goomba.png").convert_alpha()
            if self.i == 12:
                self.pic = pg.image.load("invgoomba.png").convert_alpha()
                    
            self.surface.blit(self.pic, (self.hitbox[0], self.hitbox[1]))
            #pg.draw.rect(self.surface, (0,0,0), ((self.hitbox[0], self.hitbox[1]), (self.hitbox[2]-self.hitbox[0], self.hitbox[3]- self.hitbox[1])),3)
    
    def move(self):
        self.lasthb[0] = self.hitbox[0]
        self.lasthb[2] = self.hitbox[2]
        
        if not self.dead:
            self.y_v += 1
        
        self.hitbox[0] -= mario.x_v
        self.hitbox[2] -= mario.x_v
        
        self.hitbox[0] += self.x_v
        self.hitbox[2] += self.x_v
        self.hitbox[1] += self.y_v
        self.hitbox[3] += self.y_v
        
        self.i += 1
        if self.i == 24 and not self.dead:
            self.i = 0
        
    def die(self):
        self.dead = True
        self.x_v = 0
        self.i = 0
    
    def delete(self):
        self.die()
        

class Turtle:
    def __init__(self, x, y, surface):
        self.x_v = -2
        self.y_v = 0
        self.surface = surface
        self.hitbox = [x, y, x + 40, y + 40]
        self.lasthb = [x, y, x + 40, y + 40]
        self.i = 0
        self.j = 1
        self.pic = pg.image.load("turtle_walk0.png").convert_alpha()
        self.dead = False
        self.inv = False
        self.shell= False
        self.friendlyFire = False
        self.moving = False
    
    def draw(self):
        if self.dead:
            return
        if self.inv:
            inv = ''
        else: inv = 'inv'
        
        self.pic = pg.image.load(inv + "turtle_walk0.png").convert_alpha()
        
        if self.shell:
            self.pic = pg.image.load("turtle_shell.png").convert_alpha()
        
            
        self.surface.blit(self.pic, (self.hitbox[0] + 4, self.hitbox[1] - self.i/2))
        #pg.draw.rect(self.surface, (0,0,0), ((self.hitbox[0], self.hitbox[1]), (self.hitbox[2]-self.hitbox[0], self.hitbox[3]- self.hitbox[1])),3)
    
    def move(self):
        self.lasthb[0] = self.hitbox[0]
        self.lasthb[2] = self.hitbox[2]
        
        if not self.dead and self.moving:
            self.y_v += 1
        
        self.hitbox[0] -= mario.x_v
        self.hitbox[2] -= mario.x_v
        
        if self.moving:
            self.hitbox[0] += self.x_v
            self.hitbox[2] += self.x_v
            self.hitbox[1] += self.y_v
            self.hitbox[3] += self.y_v
            
            self.i += self.j
            if self.i == 6:
                self.j = -1
            if self.i == 0:
                self.j = 1

    def die(self):
        self.shell = True
        if self.x_v == 0:
            self.x_v = 12
            self.friendlyFire = True
        else:
            self.x_v = 0
            self.friendlyFire = False
    
    def delete(self):
        self.dead = True

class Brick:
    def __init__(self, x, y, surface):
        self.x_v = 0
        self.surface = surface
        self.hitbox = [x, y, x + 50, y + 50]
        self.lasthb = [x, y, x + 50, y + 50]
        self.broken = False
    
    def draw(self):
        pic = pg.image.load("brick.png").convert_alpha()
        self.surface.blit(pic, (self.hitbox[0], self.hitbox[1]))
        
    def move(self):
        self.lasthb[0] = self.hitbox[0]
        self.lasthb[2] = self.hitbox[2]
        self.hitbox[0] -= mario.x_v
        self.hitbox[2] -= mario.x_v

    def under(self, entities):
        self.broken = True
        
class Block:
    def __init__(self, x, y, surface, item = ""):
        self.x_v = 0
        self.surface = surface
        self.hitbox = [x, y, x + 50, y + 50]
        self.lasthb = [x, y, x + 50, y + 50]
        self.broken = False
        self.pic = pg.image.load("block.png").convert_alpha()
        self.item = item
        self.used = False
        
    def draw(self):
        self.surface.blit(self.pic, (self.hitbox[0], self.hitbox[1]))
            
    def move(self):
        self.lasthb[0] = self.hitbox[0]
        self.lasthb[2] = self.hitbox[2]
        self.hitbox[0] -= mario.x_v
        self.hitbox[2] -= mario.x_v
        
    def under(self, entities):
        if self.used:
            return
        self.used = True
        self.pic = pg.image.load("block_used.png").convert_alpha()
        if self.item == "":
            return
        if self.item == "star":
            entities.append(Star(self.hitbox[0], self.hitbox[1] - 51, self.surface))
            
            
    
class Ground:
    def __init__(self, x, y, x0, y0, surface):
        self.surface = surface
        self.hitbox = [x, y, x0, y0]
        self.lasthb = [x, y, x0, y0]
    
    def draw(self):
        pic = pg.image.load("ground.png").convert_alpha()
        j = 0
        while self.hitbox[1] + 50 * j < self.hitbox[3]:
            i = 0
            while self.hitbox[0] + 50 * i < self.hitbox[2]:
                self.surface.blit(pic, (self.hitbox[0] + 50 * i, self.hitbox[1] + 50 * j))
                i += 1
            j += 1
            
    def move(self):
        self.lasthb[0] = self.hitbox[0]
        self.hitbox[2] = self.hitbox[2]
        self.hitbox[0] -= mario.x_v
        self.hitbox[2] -= mario.x_v

class Pipe:
    def __init__(self, x, y, item, surface):
        self.surface = surface
        self.item = item
        self.hitbox = [x, y, x + 100, 900]
        self.lasthb = [x, y, x + 100, 900]
    
    def draw(self):
        pic1 = pg.image.load("pipe_top.png").convert_alpha()
        pic2 = pg.image.load("pipe_bottom.png").convert_alpha()
    
        self.surface.blit(pic1, (self.hitbox[0], self.hitbox[1]))
        i = 2
        while self.hitbox[1] + 40 * i < self.hitbox[3]:
            self.surface.blit(pic2, (self.hitbox[0], self.hitbox[1] + 40 * i))
            i += 1
            
    def move(self):
        self.lasthb[0] = self.hitbox[0]
        self.hitbox[2] = self.hitbox[2]
        self.hitbox[0] -= mario.x_v
        self.hitbox[2] -= mario.x_v

class Flag:
    def __init__(self, x, y, surface):
        self.x = x
        self.y = y
        self.surface = surface
        self.pic = pg.image.load("flag.png").convert_alpha()
        
    def draw(self):
        self.surface.blit(self.pic, (self.x - 25, self.y - 528))
        
    def move(self):
        self.x -= mario.x_v
        
    def check(self, pipes, grounds, blocks, bricks, entities, window):
        
        if mario.hitbox[0] > self.x:
            mario.flag(pipes, grounds, blocks, bricks, entities, self, window)
            return True
        return False
        

def wallcolMario(mario, brick, entities):
    if (mario.hitbox[3] >= brick.hitbox[1] and mario.hitbox[3] <= brick.hitbox[3]
        and ((mario.hitbox[0] >= brick.hitbox[0] and mario.hitbox[0] <= brick.hitbox[2])
        or (mario.hitbox[2] >= brick.hitbox[0] and mario.hitbox[2] <= brick.hitbox[2]))):
        if brick.hitbox[1] > mario.lasthb[3] - 1:
            mario.y_v = 0
            mario.hitbox[1] = brick.hitbox[1] - 50
            mario.hitbox[3] = mario.hitbox[1] + 50
            mario.jump = True
            
            if type(brick) == Pipe and brick.item != "":
                if keys[K_DOWN]:
                    mario.pipe[0] = True
                    mario.pipe[1] = brick.hitbox[1]
                    mario.pipe[2] = brick.item
                    mario.x_v = 0
                    mario.hitbox[0] = brick.hitbox[0] + 30
                    mario.hitbox[2] = mario.hitbox[0] + 45
                    
        elif brick.hitbox[0] < mario.hitbox[2] and brick.hitbox[0] > mario.hitbox[0]:
            mario.x_v = 0
            mario.hitbox[0] = brick.hitbox[0] - 45
            mario.hitbox[2] = brick.hitbox[0]
        elif brick.hitbox[2] > mario.hitbox[0] and brick.hitbox[2] < mario.hitbox[2]:
            mario.x_v = 0
            mario.hitbox[0] = brick.hitbox[2]
            mario.hitbox[2] = brick.hitbox[2] + 45
            
    elif (mario.hitbox[1] > brick.hitbox[1] and mario.hitbox[1] < brick.hitbox[3]
        and ((mario.hitbox[0] > brick.hitbox[0] and mario.hitbox[0] < brick.hitbox[2])
        or (mario.hitbox[2] > brick.hitbox[0] and mario.hitbox[2] < brick.hitbox[2]))):
        if brick.hitbox[3] <= mario.lasthb[1]:
            mario.y_v = 0
            mario.hitbox[1] = brick.hitbox[3]
            mario.hitbox[3] = mario.hitbox[1] + 50
            if (type(brick) == Brick or type(brick) == Block):
                brick.under(entities)
        elif brick.lasthb[0] < mario.hitbox[2] and brick.lasthb[2] > mario.hitbox[2]:
            mario.x_v = 0
        elif brick.lasthb[2] > mario.hitbox[0] and brick.lasthb[0] < mario.hitbox[2]:
            mario.x_v = 0



def wallcolEntity(entity, brick):
    if (entity.hitbox[3] >= brick.hitbox[1] and entity.hitbox[3] <= brick.hitbox[3]
        and ((entity.hitbox[0] >= brick.hitbox[0] and entity.hitbox[0] <= brick.hitbox[2])
        or (entity.hitbox[2] >= brick.hitbox[0] and entity.hitbox[2] <= brick.hitbox[2]))):
        if brick.hitbox[1] > entity.lasthb[3] - 1:
            entity.y_v = 0
            entity.hitbox[1] = brick.hitbox[1] - (entity.hitbox[3] - entity.hitbox[1])
            entity.hitbox[3] = entity.hitbox[1] + (-entity.lasthb[1] + entity.lasthb[3])
        elif brick.hitbox[0] < entity.hitbox[2] and brick.hitbox[0] > entity.hitbox[0]:
            entity.x_v *= -1
            entity.inv = not entity.inv
        elif brick.hitbox[2] > entity.hitbox[0] and brick.hitbox[2] < entity.hitbox[2]:
            entity.x_v *= -1
            entity.inv = not entity.inv
            
    elif (entity.hitbox[1] > brick.hitbox[1] and entity.hitbox[1] < brick.hitbox[3]
        and ((entity.hitbox[0] > brick.hitbox[0] and entity.hitbox[0] < brick.hitbox[2])
        or (entity.hitbox[2] > brick.hitbox[0] and entity.hitbox[2] < brick.hitbox[2]))):
        if brick.hitbox[3] <= entity.lasthb[1]:
            entity.y_v *= -1
        elif brick.lasthb[0] < entity.hitbox[2] and brick.lasthb[2] > entity.hitbox[2]:
            entity.x_v *= -1
            entity.inv = not entity.inv
        elif brick.lasthb[2] > entity.hitbox[0] and brick.lasthb[0] < entity.hitbox[2]:
            entity.x_v *= -1
            entity.inv = not entity.inv
    
    
    
def entitycolMario(mario, entity, cont):
    if (mario.hitbox[3] >= entity.hitbox[1] and mario.hitbox[3] <= entity.hitbox[3]
        and ((mario.hitbox[0] >= entity.hitbox[0] and mario.hitbox[0] <= entity.hitbox[2])
        or (mario.hitbox[2] >= entity.hitbox[0] and mario.hitbox[2] <= entity.hitbox[2]))):
        if mario.star:
            entity.delete()
            return True
        if type(entity) == Star:
            entity.die()
            return True
        if entity.hitbox[1] > mario.lasthb[3] - 1:
            entity.die()
            mario.y_v = -12
            return True
        else:
            return False
    return True

def entitycolEntity(e1, e2):
    if e1.friendlyFire and e1 != e2:
        if ((e1.hitbox[3] >= e2.hitbox[1] and e1.hitbox[3] <= e2.hitbox[3]
            and ((e1.hitbox[0] >= e2.hitbox[0] and e1.hitbox[0] <= e2.hitbox[2])
            or (e1.hitbox[2] >= e2.hitbox[0] and e1.hitbox[2] <= e1.hitbox[2])))
        or (e1.hitbox[1] > e2.hitbox[1] and e1.hitbox[1] < e2.hitbox[3]
            and ((e1.hitbox[0] > e2.hitbox[0] and e1.hitbox[0] < e2.hitbox[2])
            or (e1.hitbox[2] > e2.hitbox[0] and e1.hitbox[2] < e2.hitbox[2])))):
            if (e2.hitbox[1] > e1.lasthb[1] - 1
                or (e2.hitbox[0] < e1.hitbox[2] and e2.hitbox[0] > e1.hitbox[0])
                or (e2.hitbox[2] > e1.hitbox[0] and e2.hitbox[2] < e1.hitbox[2])):
                e2.delete()

def inFrame(obj):
    if ((obj.hitbox[0] < 0 and obj.hitbox[2] < 0)
        or (obj.hitbox[0] > 1300 and obj.hitbox[2] > -150)):
        return False
    else: return True



def loadMap(mapFile, xMario, yMario):
    global keys
    global mario
    global window
    global cont
    global marioSave

    mixer.init()
    mixer.music.load('song.mp3')
    mixer.music.play()

    clock = pg.time.Clock()

    pg.init()
    window = pg.display.set_mode([w,h])

    mario = Mario(xMario, yMario, window)
    mario.star = marioSave[0]
    if mario.star:
        mario.star_i = marioSave[1]        
        mixer.music.load('mario/star/star_song.mp3')
        mixer.music.play()

    bricks = []
    pipes = []
    grounds = []
    blocks = []
    entities = []

    color = (100,100,255)

    with open(mapFile, "r") as file:
        lvMap = json.load(file)

    flag = 0    

    for item in lvMap:
        if item["group"] == "background":
            print()
            color = item["contain"]
        if item["group"] == "brick":
            bricks.append(Brick(item["x"], item["y"], window))
        if item["group"] == "pipe":
            pipes.append(Pipe(item["x"], item["y"], item["contain"], window))
        if item["group"] == "block":
            blocks.append(Block(item["x"], item["y"], window, item["contain"]))
        if item["group"] == "ground":
            grounds.append(Ground(item["x"], item["y"], item["x0"], item["y0"], window))
        if item["group"] == "entity":
            if item["item"] == "goomba":
                entities.append(Goomba(item["x"], item["y"], window))
            elif item["item"] == "turtle":
                entities.append(Turtle(item["x"], item["y"], window))
        if item["group"] == "flag":
            flag = Flag(item["x"], item["y"], window)

    cloud = pg.image.load("clouds.png").convert_alpha()

    cont = True
    time = 0
    while cont:
        time += 1
        #if (int(time/3) == time/3):
            #print(time / 30)
        mario.backtrack = False
    
        keys = pg.key.get_pressed()
        clock.tick(30)
    
        window.fill(color)
        window.blit(cloud, (600, 100))
        window.blit(cloud, (-50, 50))
    
        if mario.hitbox[1] > 2000:
            break
    
        mario.draw()
        if not mario.pipe[0]:
            mario.move()
        else:
            if not mario.pipeDown():  
                mario.pipe = [False, 0, ""]
                break
    
        for pipe in pipes:
            if inFrame(pipe):
                pipe.draw()
                wallcolMario(mario, pipe, entities)
    
        for ground in grounds:
            if inFrame(ground):
                ground.draw()
            wallcolMario(mario, ground, entities)

        for brick in bricks:
            if not brick.broken:
                if inFrame(brick):
                    brick.draw()
                    wallcolMario(mario, brick, entities)
            
        for block in blocks:
            if not block.broken:
                if inFrame(block):
                    block.draw()
                    wallcolMario(mario, block, entities)
                    
        for entity in entities:
            if not entity.dead:
                if not entitycolMario(mario, entity, cont):
                    cont = False
            if inFrame(entity):
                entity.draw()
        
            for entity0 in entities:
                if not entity0.dead:
                    entitycolEntity(entity,entity0)
        
            for obsticle in bricks + grounds + pipes + blocks:
                wallcolEntity(entity, obsticle)
        
        if not flag == 0:
            flag.draw()
            flag.move()
            
            if flag.check(pipes, grounds, blocks, bricks, entities, window):
                break
        
        
        for obj in bricks + grounds + entities + pipes + blocks:
            if (inFrame(obj)):
                obj.moving = True
            else:
                obj.moving = False
            obj.move()
    
        for event in pg.event.get():
            if event.type == pg.QUIT:
                cont = False
    
        pg.display.flip()

marioSave = [False, 0]
loadMap("map-1.json", 400, 500)
pg.quit()