import deck
import player
import Card
import gui
import inputbox
import time
import button
import os
import pygame


def startDeck(decker):
    # array containing all the card types with the exception of exploding kittens and defuse cards
    arr = ['Skip', 'Attack', 'Favor', 'Shuffle', 'Rainbow Cat', 'Taco Cat', 'Catermelon', 'Hairy Potato Cat',
           'Beard Cat', 'Nope', 'See the Future']
    # adds 4 of every card that is not an exploding kitten or defuse
    for i in range(4):
        for j in range(0, 11):
            decker.add_card(Card.Card(arr[j]))
    # these two cards appear 5 times in the deck so they are added again
    decker.add_card(Card.Card(arr[9]))
    decker.add_card(Card.Card(arr[10]))
    decker.shuffle()


def createPlayers(screen, arr_players, font, num_players, decker):
    for i in range(num_players):
        name = inputbox.ask(screen, 'Player %d, enter your name:  ' % (i + 1))
        coords = (40 + i * (1200 // num_players), 80)
        label = font.render(name, 1, (255, 255, 255))
        new_player = player.Player(name, coords, label)
        new_player.starting_hand(decker, Card.Card('Defuse'))
        arr_players.append(new_player)


def addExplosives(decker, num_players):
    # exploding kittens are added to the deck
    for i in range(num_players - 1):
        decker.add_card(Card.Card('Exploding Kitten'))


def addDefuse(decker):
    # adding one extra defuse to the deck
    decker.add_card(Card.Card('Defuse'))


def initialize():
    screen = gui.View()
    buttons = screen.start_up()
    num_players = screen.determine_players(buttons)
    decker = deck.Deck()
    startDeck(decker)
    arr_players = []
    pygame.font.init()
    font = pygame.font.Font(None, 32)
    createPlayers(screen.gameDisplay, arr_players, font, num_players, decker)
    addExplosives(decker, num_players)
    decker.shuffle()
    game_display = screen.gameDisplay
    return decker, arr_players, game_display


def gamePhase(decker, arr_players, game_display):
    game_display.fill((255, 255, 255))
    turn_order = 0
    elements_to_show = []
    for players in arr_players:
        elements_to_show.append(players)
    card_played = pygame.Surface((120, 168))
    game_display.blit(card_played, (500, 275))
    pygame.display.update()
    draw_button = button.Button(os.getcwd() + '\pictures\Draw.png', (150, 100), (1000, 400))
    elements_to_show.append(draw_button)
    turn_marker = button.Button(os.getcwd() + '\pictures\catarrow.png', (100, 100),
                                (arr_players[turn_order].coords[0], arr_players[turn_order].coords[1] + 25))
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
                    print(drawn_card, arr_players[turn_order].name, decker.cards_left())
                    if drawn_card.type == 'Exploding Kitten':
                        print('FUCK')
                    else:
                        for i in arr_players[turn_order].hand:
                            if i in elements_to_show:
                                elements_to_show.remove(i)
                        arr_players.append(arr_players[turn_order])
                        arr_players.pop(turn_order)
                        turn_marker.rect = pygame.rect.Rect(
                            (arr_players[turn_order].coords[0], arr_players[turn_order].coords[1] + 25),
                            turn_marker.dimensions)
                        time.sleep(5)
            for i in elements_to_show:
                if i in arr_players[turn_order].hand:
                    if i.rect.collidepoint(pygame.mouse.get_pos()):
                        if pygame.mouse.get_pressed()[0]:
                            i.play(arr_players[turn_order], arr_players, turn_order, decker)
                            elements_to_show.remove(i)
        game_display.fill((255, 255, 255))
        arr_players[turn_order].makeHandVisible(elements_to_show)
        for i in arr_players:
            pygame.draw.rect(game_display, (0, 0, 0), i.rect)
        for element in elements_to_show:
            game_display.blit(element.image, element)
        pygame.display.update()
    pygame.quit()
    quit()


def main():
    decker, arr_players, game_display = initialize()
    time.sleep(3)
    gamePhase(decker, arr_players, game_display)
    for i, k in enumerate(arr_players):
        print(k.print_name())
        k.show_hand()


main()
