import loops
import os
import pygame


class Card():
    imgs = {
        "Exploding Kitten": os.getcwd() + '/cardImages/explodingkitten.JPG',
        "Defuse": os.getcwd() + '/cardImages/defuse.JPG',
        "Skip": os.getcwd() + '/cardImages/skip.JPG',
        "Rainbow Cat": os.getcwd() + '/cardImages/rainbowcat.JPG',
        "Attack": os.getcwd() + '/cardImages/attack.JPG',
        "Favor": os.getcwd() + '/cardImages/favor.JPG',
        "Shuffle": os.getcwd() + '/cardImages/shuffle.JPG',
        "Taco Cat": os.getcwd() + '/cardImages/tacocat.JPG',
        "Catermelon": os.getcwd() + '/cardImages/catermelon.JPG',
        "Hairy Potato Cat": os.getcwd() + '/cardImages/hairypotatocat.JPG',
        "Beard Cat": os.getcwd() + '/cardImages/beardcat.JPG',
        "Nope": os.getcwd() + '/cardImages/nope.JPG',
        "See the Future": os.getcwd() + '/cardImages/seethefuture.JPG',
    }
    card_size = (120, 168)

    # to make a card you must type Card("Name of Card")
    def check_cat(self, string):
        if "Cat" in string:
            return True
        return False

    def __init__(self, string):
        self.type = string
        self.cat = self.check_cat(self.type)
        self.image = pygame.transform.scale(pygame.image.load(self.imgs[self.type]), self.card_size)
        self.back_image = pygame.transform.scale(pygame.image.load(os.getcwd() + '/cardImages/deck.JPG'),
                                                 self.card_size)
        self.rect = pygame.rect.Rect((0, 0), self.card_size)

    def __str__(self):
        return self.type

    def play(self, player, arr_players, turn_order, decker):
        # negates any action, except a defuse
        if self.type == 'Nope':
            count = 0
            for i, k in enumerate(arr_players):
                if i != turn_order:
                    for i, k in enumerate(k.hand):
                        if k.type == 'Nope':
                            count += 1
            if count > 0:
                print("A nope card can be played")
                decision = input("Would a player like to play a nope card? (y/n)")
                while decision != "y" and decision != "n":
                    decision = input("Would a player like to play a nope card? (y/n) ")
                if decision == "n":
                    return False
                elif decision == 'y':
                    for i, k in enumerate(arr_players):
                        print(str(i) + "-" + k.name)
                    player = input("Which player would like to play the nope card?")
                    while (player < 0 or player > len(arr_players)) and player == turn_order:
                        player = int(input("Which player would like to play the nope card?"))
                    arr_players[player].hand.remove(self)
                    return True
            return False
        # makes another player choose a card to give away to current player
        elif self.type == 'Favor':
            recipient = loops.phase_of_taking(arr_players, player)
            card_taken = recipient.hand.remove(loops.give_card(recipient))
            print(card_taken, "was given")
            player.hand.append(card_taken)
            return True, False
            # allows a player to steal a card from another player
        elif self.type == 'Catermelon' or self.type == 'Hairy Potato Cat' or self.type == 'Rainbow Cat' or \
                        self.type == 'Taco Cat':
            recipient = loops.phase_of_taking(arr_players, player)
            card_stolen = recipient.hand.pop(loops.card_stealing(arr_players, recipient))
            print("You stole", card_stolen.type)
            player.hand.remove(self)
            player.hand.append(card_stolen)
            return True, False
        elif self.type == 'Skip':
            # makes the player skip a turn
            print("Your turn has been skipped")
            pick = False
            attack = True
            return pick, attack
            # the player makes the next person take his turn as well, forcing them to take 2 turns
        elif self.type == 'Attack':
            attack = True
            pick = False
            return pick, attack
            # see future draws the top three cards, prints the three cards, and puts the cards back in the correct positions
        elif self.type == 'See the Future':
            if decker.cards_left() < 3:
                for i in range(decker.cards_left()):
                    card = decker.draw_top(i)
                    print(card.type)
                    decker.add_card(card, i)
            else:
                for i in range(3):
                    card = decker.draw_top(i)
                    print(card.type)
                    decker.add_card(card, i)
