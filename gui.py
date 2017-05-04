import pygame
import colors
import os
import button

class view:
    def __init__(self):
        self.working = True
        self.gameDisplay = pygame.display.set_mode((1280, 720))

    def start_up(self):
        white = (255,255,255)
        black = (0,0,0)
        #display_width = 1280
        #display_height = 720
        #self.gameDisplay = pygame.display.set_mode((display_width,display_height))
        pygame.display.set_caption('Exploding Kittens')
        self.gameDisplay.fill(white)
        pygame.display.update()
        ref = {}
        # img = pygame.image.load("2players.png")
        # img = pygame.transform.scale(img,(350,75))
        butto = pygame.Surface((350,50))
        for i in range(4):
            num_players = "button" + str(i+2)
            button = pygame.draw.rect(self.gameDisplay,black,(350,50+i*150,350,75))
            ref[num_players] = [button,i+2,False]
            img = pygame.image.load(str(i+2)+"players.png")
            img = pygame.transform.scale(img,(350,75))
            self.gameDisplay.blit(img,button)
        pygame.display.update()
        return ref

    def determine_players(self,ref):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    running = False
                for i in range(2,6):
                    if ref["button"+str(i)][0].collidepoint(pygame.mouse.get_pos()):
                        if pygame.mouse.get_pressed()[0]:
                            ref["button"+str(i)][2] = True
                            running = False
        self.gameDisplay.fill(colors.black)
        num_players = 0
        for i,k in ref.items():
            if k[2] == True:
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

#        for i in range(arr_players[turn_order].len_hand()):
#           current_card = arr_players[turn_order].hand[i]
#           delta = 700 // arr_players[turn_order].len_hand()
#           current_card.rect = current_card.rect.move(300 + (delta * i), 530)
#           elements_to_show.append(current_card)

        card_played = pygame.Surface((120,168))
        self.gameDisplay.blit(card_played, (500,275))
        pygame.display.update()
        draw_button = button.Button(os.getcwd() + '\pictures\Draw.png', (150,100), (1000, 400))
        elements_to_show.append(draw_button)
        '''draw_button = pygame.draw.rect(self.gameDisplay,black,(700,260,150,100))
        play_button = pygame.draw.rect(self.gameDisplay,black,(700,370,150,100))
        play_img = pygame.image.load("Play.png")
        draw_img = pygame.image.load("Draw.png")
        play_img = pygame.transform.scale(play_img,(150,100))
        draw_img = pygame.transform.scale(draw_img,(150,100))
        self.gameDisplay.blit(draw_img,draw_button)
        self.gameDisplay.blit(play_img,play_button)
        pygame.display.update()
        '''
        print(arr_players[turn_order])
        while len(decker.deck) != 0:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                '''if play_button.collidepoint(pygame.mouse.get_pos()):
                    if pygame.mouse.get_pressed()[0]:

                        print("Play a card from your hand")
                '''
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

                for i in elements_to_show:
                    if i in arr_players[turn_order].hand:
                        if i.rect.collidepoint(pygame.mouse.get_pos()):
                            if pygame.mouse.get_pressed()[0]:
                                i.play(arr_players[turn_order], arr_players, turn_order, decker)
                                elements_to_show.remove(i)
            arr_players[turn_order].makeHandVisible(elements_to_show)
            self.gameDisplay.fill(colors.white)
            for i in arr_players:
                pygame.draw.rect(self.gameDisplay, (0, 0, 0), i.rect)
            for element in elements_to_show:
                self.gameDisplay.blit(element.image, element)

            pygame.display.update()
    # while len(arr_players) != 1:
    #     death,attack = loops.choice_loop(decker,cards,arr_players,turn_order)
    #     if death == None:
    #         arr_players.pop(turn_order)
    #         turn_order -= 1
    #         turn_order = loops.turn_rollover(turn_order,len(arr_players))
    #     if attack:
    #         turn_order = loops.turn_rollover(turn_order,len(arr_players))
    #         turn_order += 1
    #         death,attack = loops.choice_loop(decker,cards,arr_players,turn_order)
    #     turn_order += 1
    #     turn_order = loops.turn_rollover(turn_order,len(arr_players))
        pygame.quit()
        quit()