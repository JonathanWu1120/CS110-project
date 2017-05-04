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


def makePlayers(screen, arr_players, font, num_players, decker):
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
        decker.add_card(Card.Card('Exploding Kitten', (650, 300)))


def addDefuse(decker):
    # adding one extra defuse to the deck
    decker.add_card(Card.Card('Defuse'))


def initialize():
    screen = gui.View()
    player_buttons = screen.choosePlayerScreen()
    num_players = screen.determine_players(player_buttons)
    decker = deck.Deck()
    startDeck(decker)
    arr_players = []
    pygame.font.init()
    font = pygame.font.Font(None, 32)
    makePlayers(screen.gameDisplay, arr_players, font, num_players, decker)
    addExplosives(decker, num_players)
    decker.shuffle()
    game_display = screen.gameDisplay
    return decker, arr_players, game_display, font


def update_game_display(game_display, turn_phase, arr_players, elements_to_show, turn_order):
    game_display.fill((255, 255, 255))
    if turn_phase != 'cat':
        arr_players[turn_order].makeHandVisible(elements_to_show)
    for i in arr_players:
        pygame.draw.rect(game_display, (0, 0, 0), i.rect)
    for element in elements_to_show:
        game_display.blit(element.image, element)
    pygame.display.update()


def advance_turn(arr_players, turn_order, turn_marker, elements_to_show, attack):
    for i in arr_players[turn_order].hand:
        if i in elements_to_show:
            elements_to_show.remove(i)
    if attack:
        arr_players.pop(turn_order)
    else:
        arr_players.append(arr_players[turn_order])
        arr_players.pop(turn_order)
        turn_marker.rect = pygame.rect.Rect(
            (arr_players[turn_order].coords[0], arr_players[turn_order].coords[1] + 25),
            turn_marker.dimensions)
        time.sleep(3)

def gamePhase(decker, arr_players, game_display, font):
    game_display.fill((255, 255, 255))
    turn_order = 0
    elements_to_show = []
    for players in arr_players:
        elements_to_show.append(players)
    draw_button = button.Button(os.getcwd() + '\pictures\Draw.png', (150, 100), (1000, 400))
    elements_to_show.append(draw_button)
    turn_marker = button.Button(os.getcwd() + '\pictures\catarrow.png', (100, 100),
                                (arr_players[turn_order].coords[0], arr_players[turn_order].coords[1] + 25))
    elements_to_show.append(turn_marker)
    print(arr_players[turn_order])
    turn_phase = 'playing'
    selected_card = None
    player_selected = False
    attack = False
    while len(decker.deck) != 0:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if pygame.mouse.get_pressed()[0]:
                if turn_phase == 'playing':
                        if draw_button.rect.collidepoint(pygame.mouse.get_pos()):
                            drawn_card = arr_players[turn_order].draw(decker)
                            print(drawn_card, arr_players[turn_order].name, decker.cards_left())
                            if drawn_card.type == 'Exploding Kitten':
                                elements_to_show.append(drawn_card)
                                turn_phase = 'exploding kitten'
                            else:
                                advance_turn(arr_players, turn_order, turn_marker, elements_to_show, attack)
                                if attack:
                                    attack = False
                        for i in elements_to_show:
                                if i.rect.collidepoint(pygame.mouse.get_pos()):
                                    if i in arr_players[turn_order].hand:
                                        selected_card = i
                                        if i.type == 'Favor':
                                            turn_phase = 'favor'
                                            chosen_player = None
                                            player_selected = False
                                        elif 'Cat' in i.type:
                                            turn_phase = 'cat'
                                            chosen_player = None
                                            player_selected = False
                                        elif i.type == 'See the Future':
                                            seen_cards = i.play(arr_players[turn_order], arr_players, turn_order, decker, elements_to_show)
                                            update_game_display(game_display, turn_phase, arr_players, elements_to_show,
                                                                turn_order)
                                            time.sleep(3)
                                            for card in seen_cards:
                                                elements_to_show.remove(card)
                                        elif i.type == 'Skip':
                                            selected_card = i
                                            i.play(arr_players[turn_order], arr_players, turn_order, decker, elements_to_show)
                                            advance_turn(arr_players, turn_order, turn_marker, elements_to_show, attack)
                                        elif i.type == 'Attack':
                                            i.play(arr_players[turn_order], arr_players, turn_order, decker,
                                                   elements_to_show)
                                            advance_turn(arr_players, turn_order, turn_marker, elements_to_show, attack)
                                            attack = True
                                        else:
                                            i.play(arr_players[turn_order], arr_players, turn_order, decker, elements_to_show)
                elif turn_phase == 'favor' or turn_phase == 'cat':
                    for element in elements_to_show:
                        if not player_selected:
                            if element.rect.collidepoint(pygame.mouse.get_pos()):
                                if element in arr_players:
                                    chosen_player = element
                                    player_selected = True
                                    if turn_phase == 'favor':
                                        element.show_backs(elements_to_show)
                                    if turn_phase == 'cat':
                                        arr_players[turn_order].hide_cards(elements_to_show)
                                        update_game_display(game_display, turn_phase, arr_players, elements_to_show,
                                                            turn_order)
                                        # Adding time to pass device
                                        time.sleep(3)
                                        chosen_player.makeHandVisible(elements_to_show)
                                        update_game_display(game_display, turn_phase, arr_players, elements_to_show,
                                                            turn_order)
                        else:
                            if element in chosen_player.hand:
                                if element.rect.collidepoint(pygame.mouse.get_pos()):
                                    selected_card.play(arr_players[turn_order], arr_players, turn_order, decker, elements_to_show, chosen_player, element)
                                    chosen_player.hide_cards(elements_to_show)
                                    selected_card = None
                                    turn_phase = 'playing'
                                    update_game_display(game_display, turn_phase, arr_players, elements_to_show,
                                                        turn_order)
                                    if turn_phase == 'cat':
                                        time.sleep(3)
                elif turn_phase == 'exploding kitten':
                    if not arr_players[turn_order].defuse_check():
                        message = font.render('An Exploding Kitten!\nYou can\'t defuse it!', 1, (0, 0, 0))
                        message_button = button.Button(message, (68, 640), (5, 300))
                        new_elements = [message_button]
                    else:
                        message = font.render('An Exploding Kitten!\nWill you defuse it?', 1, (0, 0, 0))
                        message_button = button.Button(message, (68, 640), (5, 300))
                        yes_button = button.Button(os.getcwd() + '\pictures\\blah.png', (80, 80), (5, 372))
                        no_button = button.Button(os.getcwd() + '\pictures\\blah.png', (80, 80), (90, 372))
                        new_elements = [message_button, yes_button, no_button]
                    for element in new_elements:
                        if element not in elements_to_show:
                            elements_to_show.append(element)
                    update_game_display(game_display, turn_phase, arr_players, elements_to_show, turn_order)
                    if not arr_players[turn_order].defuse_check():
                        selected_card.play(arr_players[turn_order], arr_players, turn_order, decker, elements_to_show)
                    if no_button.rect.collidepoint(pygame.mouse.get_pos()[0]):
                        selected_card.play(arr_players[turn_order], arr_players, turn_order, decker, elements_to_show)
                        location = (arr_players[turn_order].coords[0] + 5, arr_players[turn_order].coords[1])
                        elements_to_show.append(button.Button(os.getcwd() + '\pictures\\blah.png', (80, 80), location))
                        break
                    elif yes_button.rect.collidepoint(pygame.mouse.get_pressed()[0]):
                        for card in arr_players[turn_order].hand:
                            if card.type == 'Defuse':
                                worked = False
                                while not worked:
                                    try:
                                        index = int(inputbox.ask(game_display, 'At which spot in the deck should the exploding kitten be placed:  '))
                                        card.play(arr_players[turn_order], arr_players, turn_order, decker,
                                                  elements_to_show, chosen_card=selected_card, exploding_kitten_index=index)
                                        elements_to_show.remove(selected_card)
                                        worked = True
                                    except TypeError:
                                        worked = False

        update_game_display(game_display, turn_phase, arr_players, elements_to_show, turn_order)
    pygame.quit()
    quit()


def main():
    decker, arr_players, game_display, font = initialize()
    time.sleep(3)
    gamePhase(decker, arr_players, game_display, font)
    for i, k in enumerate(arr_players):
        print(k.print_name())
        k.show_hand()


main()
