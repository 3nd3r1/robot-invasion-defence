# TEE PELI TÄHÄN

import pygame as pg
import random
from enum import Enum


class Color(Enum):
    GRASS = (0, 154, 23)
    ROAD = (40, 0, 0)
    TOWER = (255, 0, 0)

class Arena_1(Enum):
    BLUEPRINT = [[0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], 
                 [0, 0, 1, 0, 0, 0, 1, 1, 1, 1, 1, 0, 0, 0, 1, 1],
                 [0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0], 
                 [0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0],
                 [0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0],
                 [0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0],
                 [0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0],
                 [0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0],
                 [0, 0, 1, 1, 1, 1, 1, 0, 0, 0, 1, 1, 1, 1, 1, 0],
                 [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]

    ROBOT_DESTINATIONS = [(640, 72), (580, 72), (580, 408), (420, 408),
                          (420, 72), (260, 72), (260, 408), (100, 408), (100, 0)]


class Arena(Enum):
    ARENA_1 = Arena_1


class Robot(pg.sprite.Sprite):
    def __init__(self, arena) -> None:
        super(Robot, self).__init__()
        self.image = pg.image.load("robo.png")
        self.rect = self.image.get_rect()
        self.rect.move_ip(arena.ROBOT_DESTINATIONS.value[0])

        self.destinations = iter(arena.ROBOT_DESTINATIONS.value)
        self.destination = next(self.destinations)

        self.health = 10
        self.damage = 1
        self.speed = [2, 2]

    def update(self) -> None:
        if (self.rect.centerx == self.destination[0] and self.rect.centery == self.destination[1]): self.destination = next(self.destinations, None)
        if self.destination == None: 
            self.kill()
            return

        curdest = self.destination
        vel = [0, 0]
        vel[0] = min(self.speed[0], abs(curdest[0] - self.rect.centerx))
        vel[1] = min(self.speed[1], abs(curdest[1] - self.rect.centery))
        if curdest[0] - self.rect.centerx < 0: vel[0] = -vel[0]
        if curdest[1] - self.rect.centery < 0: vel[1] = -vel[1]

        self.rect = self.rect.move(vel)


class Tower(pg.sprite.Sprite):
    def __init__(self, arena, position) -> None:
        super(Tower, self).__init__()
        self.image = pg.surface.Surface((50,50))
        self.drawTower()
        self.rect = self.image.get_rect()
        self.rect.move_ip(position[0]-25,position[1]-25)

        self.health = 50
        self.damage = 20
    
    def drawTower(self) -> None:
        self.image.fill(Color.GRASS.value)
        pg.draw.circle(self.image, Color.TOWER.value, (25,25), 15)
        dots = [(25,15),(25,35),(50,30),(50,20)]
        pg.draw.polygon(self.image, Color.TOWER.value, dots)


class Game:
    def __init__(self) -> None:
        pg.init()
        self.scr = pg.display.set_mode((640, 480))
        self.clock = pg.time.Clock()

        self.lost = False

        self.arena = Arena.ARENA_1.value

        self.wave = 1
        self.waveLength = 60*60  # 1 Minuutti per wave
        self.tickCounter = 0

        self.coins = 0
        self.health = 100

        self.towers = pg.sprite.Group()
        self.robots = pg.sprite.Group()

    def update(self) -> None:
        if self.health <= 0: self.lost = True
        if self.lost: return
        if self.tickCounter > self.waveLength:
            self.tickCounter = 0
            self.wave += 1
            print("wave: {}".format(self.wave))
        self.tickCounter += 1

        self.drawArena()

        self.spawnBots()
        for robot in self.robots.sprites():
            robot.update()
            if not robot.alive() and robot.rect.center == self.arena.ROBOT_DESTINATIONS.value[-1]: self.health -= robot.damage

        self.robots.draw(self.scr)

        self.towers.draw(self.scr)

        pg.display.flip()

    def spawnBots(self) -> None:
        if random.randint(0, int(100//self.wave)) == 1:
            self.robots.add(Robot(self.arena))
    
    def spawnTower(self) -> None:
        self.towers.add(Tower(self.arena, pg.mouse.get_pos()))

    def eventCheck(self) -> None:
        for e in pg.event.get():
            if e.type == pg.QUIT:
                exit()
            
            if e.type == pg.MOUSEBUTTONDOWN:
                self.spawnTower()

    def run(self) -> None:
        while not self.lost:
            self.eventCheck()
            self.update()
            self.clock.tick(60)

    # 16 x 10 Grid (tiles are 40x48)

    def drawArena(self) -> None:
        self.scr.fill(Color.GRASS.value)
        arenaBlueprint = self.arena.BLUEPRINT.value

        for y in range(0, 10):
            for x in range(0, 16):
                if arenaBlueprint[y][x] == 1:
                    tile = pg.Rect(x*40, y*48, 40, 48)
                    pg.draw.rect(self.scr, Color.ROAD.value, tile)



if __name__ == "__main__":
    RobotInvasionDefence = Game()
    RobotInvasionDefence.run()
