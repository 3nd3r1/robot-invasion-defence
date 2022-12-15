# TEE PELI TÄHÄN

import pygame as pg
from random import randint
from math import sqrt, atan, cos, sin, pi


Colors = {"GRASS": (0,154,23), "ROAD": (40,0,0), "PROJECTILE": (0,0,0), "TOWER_RANGE_VALID": (0,0,200,100), "TOWER_RANGE_INVALID": (200,0,0,100), "TEXT": (0,0,0), "SIDEBAR_BG": (200,0,0), "SIDEBAR_TEXT": (0,0,0), "BUTTON_BORDER": (0,0,0), "BUTTON_BG": (200,0,0)}
Arenas = {"arena_1": {"blueprint": [[0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                                     [0, 0, 1, 0, 0, 0, 1, 1, 1, 1, 1, 0, 0, 0, 1, 1],
                                     [0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0],
                                     [0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0],
                                     [0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0],
                                     [0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0],
                                     [0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0],
                                     [0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0],
                                     [0, 0, 1, 1, 1, 1, 1, 0, 0, 0, 1, 1, 1, 1, 1, 0],
                                     [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]],
                        "robot_destinations": [(640, 72), (580, 72), (580, 408), (420, 408), (420, 72), (260, 72), (260, 408), (100, 408), (100, 0)]
                    }
         }
TowerTypes = {
    "tower_1":{"name": "tower_1", "cost": 20, "range":300, "damage": 1, "firerate":30, "color":(255,0,0)},
    "tower_2":{"name": "tower_2", "cost": 100, "range":300, "damage": 2, "firerate":20, "color":(0,0,255)},
    "tower_3":{"name": "tower_3", "cost": 1000, "range":500, "damage": 10, "firerate":5, "color":(230,230,250)},
}


class Button(pg.sprite.Sprite):
    def __init__(self, pos: tuple, id: str) -> None:
        super(Button, self).__init__()
        self.image = pg.Surface((50, 75))
        self.rect = self.image.get_rect()
        self.rect.center = pos
        
        self.font = pg.font.SysFont("Roboto", 22)

        self.id = id
        self.draw()
    
    def draw(self) -> None:
        self.image.fill(Colors["SIDEBAR_BG"])
        pg.draw.polygon(self.image, Colors["BUTTON_BORDER"], [(0,0),(0,50),(50,50),(50,0)])
        pg.draw.polygon(self.image, Colors["BUTTON_BG"], [(2,2),(2,48),(48,48),(48,2)])

        pg.draw.circle(self.image, TowerTypes[self.id]["color"], (20, 25), 15)
        dots = [(20,25+15),(20,25-15),(45,25-7.5),(45,25+7.5)]
        pg.draw.polygon(self.image, TowerTypes[self.id]["color"], dots)

        priceText = self.font.render("{} $".format(TowerTypes[self.id]["cost"]), True, Colors["SIDEBAR_TEXT"])
        self.image.blit(priceText, (25-priceText.get_width()/2,65-priceText.get_height()/2))
    
        
    def isClicked(self, pos: tuple) -> bool:
        return self.rect.move(0,90).collidepoint(pos)


class Sidebar(pg.sprite.Sprite):
    def __init__(self) -> None:
        super(Sidebar, self).__init__()
        self.image = pg.Surface((65, 300))
        self.rect = self.image.get_rect()
        self.rect.centery = 240
        self.buttons = pg.sprite.Group()

        self.update()
    
    def draw(self) -> None:
        self.image.fill(Colors["SIDEBAR_BG"])
        self.buttons.draw(self.image)
    
    def update(self) -> None:
        self.draw()
    
    def clickedButton(self, pos: tuple) -> Button or None:
        for btn in self.buttons.sprites():
            if btn.isClicked(pos):
                return btn
        return None

    def addButton(self, id: str, pos: tuple) -> None:
        self.buttons.add(Button(pos, id))
        self.update()

class Robot(pg.sprite.Sprite):
    def __init__(self, arena: dict) -> None:
        super(Robot, self).__init__()
        self.image = pg.image.load("robo.png")
        self.rect = self.image.get_rect()
        self.rect.center = arena["robot_destinations"][0]

        self.destinations = iter(arena["robot_destinations"])
        self.destination = next(self.destinations)

        self.health = 1
        self.damage = 1
        self.speed = [2, 2]

    def update(self) -> None:
        if (self.rect.centerx == self.destination[0] and self.rect.centery == self.destination[1]):
            self.destination = next(self.destinations, None)
        if self.destination == None or self.health <= 0:
            self.kill()
            return

        curdest = self.destination
        vel = [0, 0]
        vel[0] = min(self.speed[0], abs(curdest[0] - self.rect.centerx))
        vel[1] = min(self.speed[1], abs(curdest[1] - self.rect.centery))
        if curdest[0] - self.rect.centerx < 0:
            vel[0] = -vel[0]
        if curdest[1] - self.rect.centery < 0:
            vel[1] = -vel[1]

        self.rect = self.rect.move(vel)


class Projectile(pg.sprite.Sprite):

    def __init__(self, start: tuple, target: Robot) -> None:
        super(Projectile, self).__init__()
        self.image = pg.surface.Surface((10, 10))
        self.rect = self.image.get_rect()
        self.rect.center = start

        self.target = target
        self.speed = 15

        self.draw()

    def draw(self) -> None:
        self.image.fill((0, 0, 1))
        self.image.set_colorkey((0, 0, 1))
        pg.draw.circle(self.image, Colors["PROJECTILE"], (5, 5), 5)

    def update(self) -> None:
        if (self.target.rect.collidepoint(self.rect.center)):
            self.kill()
            return


        if self.target.rect.centerx-self.rect.centerx == 0:
            alph = pi/2
        else:
            alph = atan(abs(self.target.rect.centery-self.rect.centery)/abs(self.target.rect.centerx-self.rect.centerx))
            if self.target.rect.centery-self.rect.centery < 0:
                alph = -alph
            if self.target.rect.centerx - self.rect.centerx < 0:
                alph = pi - alph

        vel = [0, 0]
        vel[0] = min(cos(alph)*self.speed, abs(
            self.rect.centerx - self.target.rect.centerx))
        vel[1] = min(sin(alph)*self.speed, abs(
            self.rect.centery - self.target.rect.centery))

        self.rect = self.rect.move(vel)


class Tower(pg.sprite.Sprite):
    def __init__(self, position: tuple, towerType: str) -> None:
        super(Tower, self).__init__()
        self.image = pg.surface.Surface((50, 50))
        self.rect = self.image.get_rect()
        self.rect.center = position

        self.towerColor = TowerTypes[towerType]["color"]
        self.damage = TowerTypes[towerType]["damage"]
        self.range = TowerTypes[towerType]["range"]  # radius of a circle
        self.firerate = TowerTypes[towerType]["firerate"]  # Frame interval between shots
        self.cost = TowerTypes[towerType]["cost"]

        self.tickCounter = 0
        self.placing = True

        self.target = None
        self.projectiles = pg.sprite.Group()

        self.draw()

    def draw(self) -> None:
        self.image.fill(0)
        self.image.set_colorkey((0, 0, 0))
        pg.draw.circle(self.image, self.towerColor, (25, 25), 15)

        dots = []
        alph = 0
        if self.target and not self.placing:
            if self.target.rect.centerx-self.rect.centerx == 0:
                alph = pi/2
            else:
                alph = atan(abs(self.target.rect.centery-self.rect.centery) /
                            abs(self.target.rect.centerx-self.rect.centerx))

            if self.target.rect.centery-self.rect.centery < 0:
                alph = -alph
            if self.target.rect.centerx - self.rect.centerx < 0:
                alph = pi - alph


        dots.append((25+cos(alph+pi/2)*15, 25+sin(alph+pi/2)*15))
        dots.append((25+cos(alph-pi/2)*15, 25+sin(alph-pi/2)*15))
        dots.append((25+cos(alph-pi/10)*25, 25+sin(alph-pi/10)*25))
        dots.append((25+cos(alph+pi/10)*25, 25+sin(alph+pi/10)*25))

        pg.draw.polygon(self.image, self.towerColor, dots)

    def shoot(self) -> None:
        if not self.target or self.placing:
            return
        self.projectiles.add(Projectile(self.rect.center, self.target))

    def update(self) -> None:
        self.tickCounter += 1
        if self.placing: self.rect.center = pg.mouse.get_pos()

        if self.target != None and not self.placing:
            if self.tickCounter >= self.firerate:
                self.tickCounter = 0
            if self.tickCounter == 0:
                self.shoot()
            self.draw()
        
        for projectile in self.projectiles.sprites():
            projectile.update()
            if (not projectile.alive()) and (projectile.target.alive()):
                projectile.target.health -= self.damage


class Game:
    def __init__(self) -> None:
        pg.init()
        self.scr = pg.display.set_mode((640, 480))
        self.clock = pg.time.Clock()

        pg.display.set_caption("Robot Invasion Defence")
        pg.display.set_icon(pg.image.load("robo.png"))

        self.lost = False

        self.arena = Arenas["arena_1"]

        self.wave = 1
        self.waveLength = 60*60  # 60*60 frames (1 minute) per wave
        self.tickCounter = 0

        self.coins = 20
        self.health = 100

        self.towers = pg.sprite.Group()
        self.robots = pg.sprite.Group()

        self.placingTower = None

        self.menus = pg.sprite.Group()
        self.text = pg.font.SysFont("Roboto", 30)

        self.initSidebar()

    def update(self) -> None:

        #If tickCounter == waveLength raise wave number by 1
        if self.health <= 0:
            self.lost = True
        if self.lost:
            return
        if self.tickCounter > self.waveLength:
            self.tickCounter = 0
            self.wave += 1
        self.tickCounter += 1

        self.drawArena()

        #Spawn robots ?
        self.spawnBots()

        #Update robots 
        for robot in self.robots.sprites():
            robot.update()
            if not robot.alive() and robot.rect.center == self.arena["robot_destinations"][-1]:
                self.health -= robot.damage
            elif not robot.alive():
                self.coins += 1 # 1 Coin for killing a robot

        #Update tower
        for tower in self.towers.sprites():
            tower.target = self.closestRobot(tower)
            tower.update()
            tower.projectiles.draw(self.scr)

        #Draw robots, towers, menus and projectiles to screen
        self.robots.draw(self.scr)
        self.towers.draw(self.scr)
        self.menus.draw(self.scr)

        #Draw health and money
        healthText = self.text.render("{} HP".format(self.health), True, Colors["TEXT"])
        self.scr.blit(healthText, (35-healthText.get_width()/2, 20))
        coinText = self.text.render("{} $".format(self.coins), True, Colors["TEXT"])
        self.scr.blit(coinText, (35-coinText.get_width()/2, 50))

        #Draw wave number
        waveText = self.text.render("WAVE #{}".format(self.wave), True, Colors["TEXT"])
        self.scr.blit(waveText, (50-waveText.get_width()/2, 445))

        #Draw tower that is being placed
        if self.placingTower:
            rangeColor = Colors["TOWER_RANGE_INVALID"]
            if self.placingTowerValid(): rangeColor = Colors["TOWER_RANGE_VALID"]

            self.placingTower.update()
            rangeCircle = pg.Surface((self.placingTower.range*2, self.placingTower.range*2), pg.SRCALPHA)
            rangeCircle.set_colorkey((0,0,0))
            pg.draw.circle(rangeCircle, rangeColor, (self.placingTower.range,self.placingTower.range), self.placingTower.range)
            self.scr.blit(rangeCircle, self.placingTower.rect.move(-self.placingTower.range, -self.placingTower.range))
            self.scr.blit(self.placingTower.image, self.placingTower.rect)


        pg.display.flip()

    def spawnBots(self) -> None:
        #Robot damage and health scale with wave
        #Todo: Different set types of robots with different visuals
        if randint(0, int(100//self.wave)) == 1:
            newrobot = Robot(self.arena)
            lvl = randint(1, self.wave)
            newrobot.health = lvl
            newrobot.damage = lvl
            self.robots.add(newrobot)

    def spawnTower(self, position: tuple, towerType: str) -> None:
        self.towers.add(Tower(position, towerType))

    def eventCheck(self) -> None:
        for e in pg.event.get():
            if e.type == pg.QUIT:
                exit()

            if e.type == pg.MOUSEBUTTONDOWN:
                mousepos = pg.mouse.get_pos()
                for menu in self.menus.sprites():
                    self.handleClick(menu.clickedButton(mousepos))
            
            if e.type == pg.MOUSEBUTTONUP:
                if self.placingTower:
                    if self.placingTowerValid():
                        self.placingTower.placing = False
                        self.towers.add(self.placingTower)
                        self.coins -= self.placingTower.cost
                    self.placingTower = None


    def run(self) -> None:
        while not self.lost:
            self.eventCheck()
            self.update()
            self.clock.tick(60)


    def drawArena(self) -> None:
        # 16 x 10 Grid (tiles are 40x48)
        self.scr.fill(Colors["GRASS"])
        arenaBlueprint = self.arena["blueprint"]

        for y in range(0, 10):
            for x in range(0, 16):
                if arenaBlueprint[y][x] == 1:
                    tile = pg.Rect(x*40, y*48, 40, 48)
                    pg.draw.rect(self.scr, Colors["ROAD"], tile)
    
    def initSidebar(self) -> None:
        sidebar = Sidebar()
        sidebar.addButton("tower_1",(32.5,240))
        sidebar.addButton("tower_2",(32.5,160))
        sidebar.addButton("tower_3",(32.5,80))
        self.menus.add(sidebar)
    
    def handleClick(self, button: Button) -> None:
        if not button: return
        if TowerTypes[button.id]["cost"] > self.coins: return

        self.placingTower = Tower(pg.mouse.get_pos(), button.id)

    def closestRobot(self, tower: Tower) -> Robot or None:
        # Distance between the center robot and center of tower
        # Todo: This should also take into account the size of robot
        def distance(robot: Robot) -> int:
            return sqrt((robot.rect.centerx-tower.rect.centerx)**2 + (robot.rect.centery - tower.rect.centery)**2)

        if len(self.robots.sprites()) == 0:
            return None

        ret = min(self.robots.sprites(), key=distance)
        if distance(ret) > tower.range:
            return None
        else:
            return ret
    
    def placingTowerValid(self) -> bool:
        if not self.placingTower: return False

        #Colliding with other towers
        for tower in self.towers.sprites():
            if self.placingTower.rect.colliderect(tower.rect): return False

        #Is on the road
        tile = (self.placingTower.rect.centerx//40, self.placingTower.rect.centery//48)
        if self.arena["blueprint"][tile[1]][tile[0]] == 1: return False

        #Is in sidebar
        if self.placingTower.rect.centerx < 40: return False

        return True
        


if __name__ == "__main__":
    RobotInvasionDefence = Game()
    RobotInvasionDefence.run()
