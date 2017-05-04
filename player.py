import pygame


class Player:
    def __init__(self, name, coords, font):
        self.name = name
        self.hand = []
        self.coords = coords
        self.rect = pygame.rect.Rect((coords[0], coords[1]), (15 * len(name), 30))
        self.image = font

    def __str__(self):
        string = "This player is %s. They have %d cards in their hand. They have the following cards: \n" % \
                 (self.name, self.len_hand()) + str([i.type for i in self.hand])
        return string

    def starting_hand(self, decker, defuse):
        self.hand.append(defuse)
        for i in range(4):
            self.hand.append(decker.draw_top())

    def len_hand(self):
        return len(self.hand)

    def print_name(self):
        return (self.name)

    def show_hand(self):
        for i, k in enumerate(self.hand):
            print(str(i) + "-" + k.type)

    def draw(self, decker):
        drawn_card = decker.draw_top()
        self.hand.append(drawn_card)
        return drawn_card

    def makeHandVisible(self, elements_to_show):
        for card in self.hand:
            if card not in elements_to_show:
                elements_to_show.append(card)
        i = 0
        delta = 1200 // self.len_hand()
        for card in self.hand:
            card.rect = pygame.rect.Rect((40 + (delta * i), 530), card.card_size)
            i += 1
