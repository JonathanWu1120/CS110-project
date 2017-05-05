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

    def __init__(self, string, coords=(0,0)):
        self.type = string
        self.front_image = pygame.transform.scale(pygame.image.load(self.imgs[self.type]), self.card_size).convert_alpha()
        self.image = self.front_image
        self.back_image = pygame.transform.scale(pygame.image.load(os.getcwd() + '/cardImages/deck.JPG'),
                                                 self.card_size).convert_alpha()
        self.rect = pygame.rect.Rect(coords, self.card_size)

    def __str__(self):
        return self.type

    def play(self, player, arr_players, turn_order, decker, elements_to_show, chosen_player=None, chosen_card=None, exploding_kitten_index=0):
        # makes another player choose a card to give away to current player
        if self.type == 'Favor':
            chosen_player.hand.remove(chosen_card)
            print(chosen_card, "was given")
            player.hand.append(chosen_card)
            player.hand.remove(self)
        elif self.type == 'Nope':
            player.hand.remove(self)
            chosen_player.hand.remove(chosen_card)
            # allows a player to steal a card from another player
        elif 'Cat' in self.type:
            print("You stole", chosen_card.type)
            card_type = self.type
            chosen_player.hand.remove(chosen_card)
            player.hand.remove(self)
            elements_to_show.remove(self)
            for card in player.hand:
                if card.type == card_type:
                    player.hand.remove(card)
                    elements_to_show.remove(card)
                    break
            player.hand.append(chosen_card)
            return True, False
        elif self.type == 'Skip':
            # makes the player skip a turn
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
            for card in player.hand:
                elements_to_show.remove(card)
        elif self.type == 'Defuse':
            decker.deck.insert(exploding_kitten_index, chosen_card)
            player.hand.remove(self)
            elements_to_show.remove(self)
            elements_to_show.remove(chosen_card)
