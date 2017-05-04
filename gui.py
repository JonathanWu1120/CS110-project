import pygame
import os
import button


class view:
    def __init__(self):
        self.working = True
        self.gameDisplay = pygame.display.set_mode((1280, 720))

    def start_up(self):
        pygame.display.set_caption('Exploding Kittens')
        self.gameDisplay.fill((255,255,255))
#        self.gameDisplay.blit(pygame.transform.scale(pygame.image.load(os.getcwd() + '\pictures\woodbackground.jpg'), (1280, 720)), (0,0))
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
#        self.gameDisplay.blit(pygame.transform.scale(pygame.image.load(os.getcwd() + '\pictures\woodbackground.jpg'), (1280, 720)), (0, 0))
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

    def game_phase(self,decker,arr_players):
        display_width = 1280
        display_height = 720
        self.gameDisplay = pygame.display.set_mode((display_width,display_height))
        pygame.display.set_caption('Exploding Kittens')
        self.gameDisplay.fill((255, 255, 255))
        turn_order = 0
        elements_to_show = []
        for player in arr_players:
            elements_to_show.append(player)
        card_played = pygame.Surface((120,168))
        self.gameDisplay.blit(card_played, (500,275))
        pygame.display.update()
        draw_button = button.Button(os.getcwd() + '\pictures\Draw.png', (150,100), (1000, 400))
        elements_to_show.append(draw_button)
        turn_marker = button.Button(os.getcwd() + '\pictures\catarrow.png', (100, 100), (arr_players[turn_order].coords[0],arr_players[turn_order].coords[1] + 25))
        elements_to_show.append(turn_marker)
        print(arr_players[turn_order])
        while len(decker.deck) != 0:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                if draw_button.rect.collidepoint(pygame.mouse.get_pos()):
                    if pygame.mouse.get_pressed()[0]:
                        drawn_card = arr_players[turn_order].draw(decker)
                        print(drawn_card,arr_players[turn_order].name,decker.cards_left())
                        if drawn_card.type == 'Exploding Kitten':
                            print('FUCK')
                        else:
                            for i in arr_players[turn_order].hand:
                                if i in elements_to_show:
                                    elements_to_show.remove(i)
                            arr_players.append(arr_players[turn_order])
                            arr_players.pop(turn_order)
                            turn_marker.rect = pygame.rect.Rect((arr_players[turn_order].coords[0], arr_players[turn_order].coords[1] + 25),turn_marker.dimensions)

                for i in elements_to_show:
                    if i in arr_players[turn_order].hand:
                        if i.rect.collidepoint(pygame.mouse.get_pos()):
                            if pygame.mouse.get_pressed()[0]:
                                i.play(arr_players[turn_order], arr_players, turn_order, decker)
                                elements_to_show.remove(i)
            self.gameDisplay.fill((255,255,255))
#            self.gameDisplay.blit(pygame.transform.scale(pygame.image.load(os.getcwd() + '\pictures\woodbackground.jpg'), (1280, 720)),(0, 0))
            arr_players[turn_order].makeHandVisible(elements_to_show)
            for i in arr_players:
                pygame.draw.rect(self.gameDisplay, (0, 0, 0), i.rect)
            for element in elements_to_show:
                self.gameDisplay.blit(element.image, element)

            pygame.display.update()
        pygame.quit()
        quit()