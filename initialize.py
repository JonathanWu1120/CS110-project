import deck
import player
import Card
import gui
import inputbox
import time
import pygame

def initialize():
    screen = gui.view()
    buttons = screen.start_up()
    num_players = screen.determine_players(buttons)
    decker = deck.Deck()
    #array containing all the cards which will be used for the calling of their specific function
    arr = ['Exploding Kitten','Defuse','Skip','Attack','Favor','Shuffle','Rainbow Cat','Taco Cat','Catermelon','Hairy Potato Cat','Beard Cat','Nope','See the Future']
    #adds 4 of every card that is not an exploding kitten or defuse
    for i in range(4):
        for j in range(2,13):
            decker.add_card(Card.Card(arr[j]))
    #these two cards appear 5 times in the deck so they are added again
    decker.add_card(Card.Card(arr[11]))
    decker.add_card(Card.Card(arr[12]))
    decker.shuffle()
    arr_players = []
    pygame.font.init()
    font = pygame.font.Font(None, 32)
    for i in range(num_players):
        name = inputbox.ask(screen.gameDisplay, 'Player %d, enter your name:  ' % (i + 1))
        coords = (40 + i * (1200//num_players), 80)
        label = font.render(name, 1, (255, 255, 255))
        new_player = player.Player(name, coords, label)
        new_player.starting_hand(decker, Card.Card(arr[1]))
        arr_players.append(new_player)
    # exploding kittens are added to the deck
    for i in range(num_players - 1):
        decker.add_card(Card.Card(arr[0]))
    # there is one extra defuse card in the deck
    decker.add_card(Card.Card(arr[1]))
    decker.shuffle()
    return decker, arr_players, arr, screen

def main():
    decker,arr_players,cards,screen = initialize()
    time.sleep(3)
    screen.game_phase(decker,arr_players)
    for i,k in enumerate(arr_players):
        print(k.print_name())
        k.show_hand()
main()