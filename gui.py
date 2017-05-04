import pygame
import os


class View:
    def __init__(self):
        self.working = True
        self.gameDisplay = pygame.display.set_mode((1280, 720))

    def choosePlayerScreen(self):
        pygame.display.set_caption('Exploding Kittens')
        self.gameDisplay.fill((255,255,255))
        pygame.display.update()
        ref = {}
        for i in range(4):
            num_players = "button" + str(i+2)
            butto = pygame.draw.rect(self.gameDisplay,(0, 0, 0),(350,50+i*150,350,75))
            ref[num_players] = [butto,i+2,False]
            img = pygame.image.load(os.getcwd() + '\pictures\\' + str(i+2)+"players.png")
            img = pygame.transform.scale(img,(350,75))
            self.gameDisplay.blit(img,butto)
        pygame.display.update()
        return ref

    def determine_players(self,ref):
        self.gameDisplay.fill((255,255,255))
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    running = False
                for i in range(2,6):
                    if ref["button"+str(i)][0].collidepoint(pygame.mouse.get_pos()):
                        if pygame.mouse.get_pressed()[0]:
                            ref["button"+str(i)][2] = True
                            running = False
        num_players = 0
        for i,k in ref.items():
            if k[2]:
                num_players = k[1]
        return num_players