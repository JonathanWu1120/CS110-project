import pygame


class GUI:
    def __init__(self):

        white = (255,255,255)
        display_width = 1280
        display_height = 720

        self.gameDisplay = pygame.display.set_mode((display_width,display_height))
        pygame.display.set_caption('Exploding Kittens')
        self.gameDisplay.fill(white)
        
        

        #cardImg = pygame.image.load("/home/mcorcor1/cs110/finalproject/AofS.png")
        #cardImg = pygame.transform.scale(cardImg, (100,100))

        self.middleDeck = pygame.Surface((120,168))     #deck icon
        self.gameDisplay.blit(self.middleDeck, (350,275))
        

        self.player_one = pygame.Surface((100,100))     #player1 icon
        self.gameDisplay.blit(self.player_one, ((50,50)))
        self.player_two = pygame.Surface((100,100))     #player2 icon
        self.gameDisplay.blit(self.player_two, ((400,50)))
        self.player_three = pygame.Surface((100,100))   #player3 icon
        self.gameDisplay.blit(self.player_three, ((772.5,50)))
        self.player_four = pygame.Surface((100,100))    #player4 icon
        self.gameDisplay.blit(self.player_four, ((1130,50)))
        self.player_five = pygame.Surface((100,100))    #player5 icon current player
        self.gameDisplay.blit(self.player_five, ((100,600)))
        
        self.card_in_hand_one = pygame.Surface((120,168))   #card_one
        self.gameDisplay.blit(self.card_in_hand_one, (300, 531))
        self.card_in_hand_one = pygame.Surface((120,168))           #card_two
        self.gameDisplay.blit(self.card_in_hand_one, (450, 531))
        self.card_in_hand_one = pygame.Surface((120,168))           #card_three
        self.gameDisplay.blit(self.card_in_hand_one, (600, 531))
        self.card_in_hand_one = pygame.Surface((120,168))           #card_four
        self.gameDisplay.blit(self.card_in_hand_one, (750, 531))
        self.card_in_hand_one = pygame.Surface((120,168))           #card_five
        self.gameDisplay.blit(self.card_in_hand_one, (900, 531))
        self.card_in_hand_one = pygame.Surface((120,168))           #card_six
        self.gameDisplay.blit(self.card_in_hand_one, (300, 531))
        self.card_in_hand_one = pygame.Surface((120,168))           #card_seven
        self.gameDisplay.blit(self.card_in_hand_one, (1050, 531))
   
        self.card_played = pygame.Surface((120,168))
        self.gameDisplay.blit(self.card_played, (500,275)) 

    


        pygame.display.update()
       
                

        gameExit = False
        
        while not gameExit:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    gameExit = True                    
                #print(event) 
            
            pygame.display.update()
        pygame.quit()
        quit()
    
      
         
                


def main():
    GUI()

main()

