import os
import pygame


class Card:
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

    def __init__(self, string, coords=(0,0)):
        self.type = string
        self.cat = self.check_cat(self.type)
        self.front_image = pygame.transform.scale(pygame.image.load(self.imgs[self.type]), self.card_size).convert_alpha()
        self.image = self.front_image
        self.back_image = pygame.transform.scale(pygame.image.load(os.getcwd() + '/cardImages/deck.JPG'),
                                                 self.card_size).convert_alpha()
        self.rect = pygame.rect.Rect(coords, self.card_size)

    def __str__(self):
        return self.type

    def play(self, player, arr_players, turn_order, decker, elements_to_show, chosen_player=None, chosen_card=None, exploding_kitten_index=0):
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
                    player.hand.remove(self)
                    elements_to_show.remove(self)
                    return True
            return False
        # makes another player choose a card to give away to current player
        elif self.type == 'Favor':
            chosen_player.hand.remove(chosen_card)
            print(chosen_card, "was given")
            player.hand.append(chosen_card)
            player.hand.remove(self)
            elements_to_show.remove(self)
            return True, False
            # allows a player to steal a card from another player
        elif 'Cat' in self.type:
            print("You stole", chosen_card.type)
            chosen_player.hand.remove(chosen_card)
            player.hand.remove(self)
            player.hand.append(chosen_card)
            return True, False
        elif self.type == 'Skip':
            # makes the player skip a turn
            print("Your turn has been skipped")
            player.hand.remove(self)
            elements_to_show.remove(self)
            # the player makes the next person take his turn as well, forcing them to take 2 turns
        elif self.type == 'Attack':
            arr_players.insert(1, arr_players[turn_order + 1])
            player.hand.remove(self)
            elements_to_show.remove(self)
            # see future draws the top three cards, prints the three cards, and puts the cards back in the correct positions
        elif self.type == 'See the Future':
            cards = []
            if decker.cards_left() < 3:
                num = decker.cards_left()
            else:
                num = 3
            for card in decker.deck[0:num]:
                cards.append(card)
                card.image = card.front_image
                if card not in elements_to_show:
                    elements_to_show.append(card)
            i = 0
            delta = 600 // num
            for card in cards:
                card.rect = pygame.rect.Rect((300 + (delta * i), 300), card.card_size)
                i += 1
            player.hand.remove(self)
            elements_to_show.remove(self)
            return cards
        elif self.type == 'Shuffle':
            decker.shuffle()
            player.hand.remove(self)
            elements_to_show.remove(self)
        elif self.type == 'Exploding Kitten':
            arr_players.pop(turn_order)
        elif self.type == 'Defuse':
            decker.deck.insert(exploding_kitten_index, chosen_card)
            player.hand.remove(self)
            elements_to_show.remove(self)