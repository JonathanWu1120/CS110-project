import random
import Card

class Deck:
    #makes an empty list for the cards to be stored in
    def __init__(self):
        self.deck = []

    #returns the contents of the deck
    def __str__(self):
        length = "There are %d cards in the deck right now.\n" % len(self.deck)
        cards = 'The deck currently contains: \n'
        for card in self.deck:
            cards += card + '\n'
        return length + cards
    #checks to see if the deck is empty
    def is_empty(self):
        return self.cards_left() == 0
    #checks to see how many cards are currently in the deck
    def cards_left(self):
        return len(self.deck)
    #adds a card, the card parameter is the card class that is put in, index=0 means it will, at default, add the card to the top of the deck, the index value is only changed if the see the future card is played
    def add_card(self,card,index=0):
        self.deck.insert(index,card)
    #prints the entire deck line by line
    def print_deck(self):
        for card in self.deck:
            print(card.type)
    #draws a card from the top of the deck, checks to see if there are cards left in the deck first, in order to see the card you have to enter print(draw_top)
    def draw_top(self,num=0):
        if self.is_empty():
            print("some shit messed up")
        else:
            card_drawn = self.deck.pop(num)
            return card_drawn
    #draws from bottom
    def draw_bottom(self):
        if self.is_empty():
            print("empty deck my guy")
        else:
            card_drawn = self.deck.pop()
            return card_drawn
    #peek is for seeing the future and altering the future
    def peek(self,card_index):
        return self.deck[card_index]
    #shuffles the deck
    def shuffle(self):
        random.shuffle(self.deck)
    # def change_future(self):
    # 	if self.cards_left():
#           print("hi")