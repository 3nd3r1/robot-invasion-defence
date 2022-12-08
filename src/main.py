# TEE PELI TÄHÄN

import pygame

class Robot:
    pass

class Tower:
    pass

class Player:
    pass

class Level:
    pass

class RobotInvasionDefence:
    #Levels (Timestamp when bot is spawner. Etc)
    def __init__(self) -> None:
        pygame.init()
        self.__scr = pygame.display.set_mode((640, 480))

        self.isGameRunning = False

        self.__towers = []

        self.__gameTowers = []
        self.__gamePlayer = Player()
        self.__gameLevel = Level(1)

        self.__loadGame()

    #Events --->
    #Drag and drop?
    #Mouse click to put a tower
    def eventCheck(self) -> None:
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                exit()

    #Load game --->
    # Loads an arena with draw
    def __startGame(self) -> None:
        self.__drawArena()
        pygame.display.flip()
        

    def __drawArena(self) -> None:
        self.__scr.fill((0,255,0))