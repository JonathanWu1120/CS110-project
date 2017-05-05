import deck
import player
import Card
import gui
import inputbox
import time
import button
import os
import pygame
import json


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
        name = inputbox.ask(screen, 'Player %d, enter your name:  ' % (i + 1), (screen.get_width() / 2) - 200,
                            (screen.get_height() / 2) - 15)
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


def update_game_display(game_display, turn_phase, arr_players, total_players, elements_to_show, turn_order, override=False):
    game_display.fill((187, 153, 119))
    if turn_phase != 'over':
        if turn_phase != 'favor' and turn_phase != 'nope' and override is False:
            arr_players[turn_order].makeHandVisible(elements_to_show)
        for i in total_players:
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


def nope_check(arr_players):
    for players in arr_players:
        for card in players.hand:
            if card.type == 'Nope':
                return True


def gamePhase(decker, arr_players, game_display, font):
    game_display.fill((187, 153, 119))
    turn_order = 0
    elements_to_show = []
    total_players = []
    for players in arr_players:
        elements_to_show.append(players)
        total_players.append(players)
    draw_button = button.Button(os.getcwd() + '\pictures\Draw.png', (150, 100), (1000, 400))
    elements_to_show.append(draw_button)
    turn_marker = button.Button(os.getcwd() + '\pictures\catarrow.png', (100, 100),
                                (arr_players[turn_order].coords[0], arr_players[turn_order].coords[1] + 25))
    elements_to_show.append(turn_marker)
    turn_phase = 'playing'
    selected_card = None
    player_selected = False
    attack = False
    start_exploding_kitten = True
    first_nope_instance = True
    nope_pass = False
    deciding_to_play_nope = True
    new_elements = []
    done_once = False
    while len(arr_players) >= 1:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if len(arr_players) == 1:
                if not done_once:
                    turn_phase = 'over'
                    elements_to_show = []
                    congratulations = font.render(
                        '%s is the only one who didn\'t meet a furry demise! Congratulations!' % arr_players[
                            turn_order].name, 1, (0, 0, 0))
                    congratulations_button = button.Button(None, (68, 640), (300, 150), text_surface=congratulations)
                    elements_to_show.append(congratulations_button)
                    name_title = font.render('Number of wins', 1, (0, 0, 0))
                    name_title_button = button.Button(None, (68, 640), (300, 220), text_surface=name_title)
                    score_title = font.render('Score', 1, (0, 0, 0))
                    score_title_button = button.Button(None, (68, 640), (800, 220), text_surface=score_title)
                    elements_to_show.append(score_title_button)
                    elements_to_show.append(name_title_button)
                    high_scores_file = open('High Scores.json', 'r')
                    high_scores = json.load(high_scores_file)
                    replay = font.render('Click me to play again!', 1, (0, 0, 0))
                    replay_button = button.Button(None, (68, 320), (1000, 360), text_surface=replay)
                    elements_to_show.append(replay_button)
                    if arr_players[turn_order].name in high_scores:
                        high_scores[arr_players[turn_order].name] += 1
                    else:
                        high_scores[arr_players[turn_order].name] = 1
                    items = list(high_scores.items())
                    items_in_order = []
                    scores = []
                    for i in items:
                        scores.append(i[1])
                    if len(scores) < 5:
                        num = len(scores)
                    else:
                        num = 5
                    for i in range(num):
                        index = scores.index(max(scores))
                        items_in_order.append(items[index])
                        items.pop(index)
                        scores.pop(index)
                    for i in range(len(items_in_order)):
                        name = font.render(items_in_order[i][0], 1, (0, 0, 0))
                        name_button = button.Button(None, (68, 640), (300, 260 + 60 * i), text_surface=name)
                        score = font.render(str(high_scores[items_in_order[i][0]]), 1, (0, 0, 0))
                        score_button = button.Button(None, (68, 640), (800, 260 + 60 * i), text_surface=score)
                        elements_to_show.append(name_button)
                        elements_to_show.append(score_button)
                    new_high_scores = {}
                    for i in items_in_order:
                        new_high_scores[i[0]] = i[1]
                    new_high_scores = str(new_high_scores)
                    for i in range(len(new_high_scores)):
                        if new_high_scores[i] == '\'':
                            new_high_scores = new_high_scores[:i] + '"' + new_high_scores[i + 1:]
                    high_scores_file.close()
                    os.remove('High Scores.json')
                    done_once = True
                    new_high_scores_file = open('High Scores.json', 'w')
                    json.dump(high_scores, new_high_scores_file)
                    new_high_scores_file.close()
                else:
                    if replay_button.rect.collidepoint(pygame.mouse.get_pos()):
                        if pygame.mouse.get_pressed()[0]:
                            go()
                            pygame.quit()
                            exit()
            if turn_phase == 'playing':
                if draw_button.rect.collidepoint(pygame.mouse.get_pos()):
                    if pygame.mouse.get_pressed()[0]:
                        drawn_card = arr_players[turn_order].draw(decker)
                        if drawn_card.type == 'Exploding Kitten':
                            elements_to_show.append(drawn_card)
                            selected_card = drawn_card
                            turn_phase = 'exploding kitten'
                        else:
                            arr_players[turn_order].hide_cards(elements_to_show)
                            update_game_display(game_display, turn_phase, arr_players, total_players, elements_to_show, turn_order, override=True)
                            time.sleep(3)
                            advance_turn(arr_players, turn_order, turn_marker, elements_to_show, attack)
                            if attack:
                                attack = False
                for i in elements_to_show:
                    if i.rect.collidepoint(pygame.mouse.get_pos()):
                        if pygame.mouse.get_pressed()[0]:
                            if i in arr_players[turn_order].hand:
                                selected_card = i
                                chosen_player = None
                                player_selected = False
                                if not nope_pass:
                                    if nope_check(arr_players):
                                        turn_phase = 'nope'
                                    else:
                                        nope_pass = True
                                        first_nope_instance = True
                                if nope_pass:
                                    if 'Cat' in i.type:
                                        if len([card for card in arr_players[turn_order].hand if
                                                card.type == i.type]) > 1:
                                            turn_phase = 'cat'
                                    elif i.type == 'Favor':
                                        turn_phase = 'favor'
                                    elif i.type == 'See the Future':
                                        seen_cards = i.play(arr_players[turn_order], arr_players, turn_order, decker,
                                                            elements_to_show)
                                        for card in seen_cards:
                                            if card not in elements_to_show:
                                                elements_to_show.append(card)
                                        update_game_display(game_display, turn_phase, arr_players, total_players,
                                                            elements_to_show,
                                                            turn_order)
                                        time.sleep(3)
                                        for card in seen_cards:
                                            elements_to_show.remove(card)
                                    elif i.type == 'Skip':
                                        selected_card = i
                                        i.play(arr_players[turn_order], arr_players, turn_order, decker,
                                               elements_to_show)
                                        advance_turn(arr_players, turn_order, turn_marker, elements_to_show, attack)
                                        attack = False
                                    elif i.type == 'Attack':
                                        i.play(arr_players[turn_order], arr_players, turn_order, decker,
                                               elements_to_show)
                                        advance_turn(arr_players, turn_order, turn_marker, elements_to_show, attack)
                                        attack = True
                                    elif i.type == 'Defuse' or i.type == 'Nope':
                                        pass
                                    else:
                                        i.play(arr_players[turn_order], arr_players, turn_order, decker,
                                               elements_to_show)
                                    nope_pass = False
            elif turn_phase == 'favor' or turn_phase == 'cat':
                for element in elements_to_show:
                    if not player_selected:
                        if element.rect.collidepoint(pygame.mouse.get_pos()):
                            if pygame.mouse.get_pressed()[0]:
                                if element in arr_players:
                                    chosen_player = element
                                    player_selected = True
                                    if turn_phase == 'cat':
                                        element.show_backs(elements_to_show)
                                    if turn_phase == 'favor':
                                        arr_players[turn_order].hide_cards(elements_to_show)
                                        update_game_display(game_display, turn_phase, arr_players, total_players,
                                                            elements_to_show,
                                                            turn_order)
                                        # Adding time to pass device
                                        time.sleep(3)
                                        chosen_player.makeHandVisible(elements_to_show)
                                        update_game_display(game_display, turn_phase, arr_players, total_players,
                                                            elements_to_show,
                                                            turn_order)
                    else:
                        if element in chosen_player.hand:
                            if element.rect.collidepoint(pygame.mouse.get_pos()):
                                if pygame.mouse.get_pressed()[0]:
                                    selected_card.play(arr_players[turn_order], arr_players, turn_order, decker,
                                                       elements_to_show, chosen_player, element)
                                    chosen_player.hide_cards(elements_to_show)
                                    selected_card = None
                                    turn_phase = 'playing'
                                    update_game_display(game_display, turn_phase, arr_players, total_players,
                                                        elements_to_show,
                                                        turn_order)
                                    if turn_phase == 'cat':
                                        time.sleep(3)
            elif turn_phase == 'exploding kitten':
                if start_exploding_kitten:
                    if not arr_players[turn_order].defuse_check():
                        message = font.render('An Exploding Kitten! You can\'t defuse it!', 1, (0, 0, 0))
                        message_button = button.Button(None, (68, 640), (40, 300), text_surface=message)
                        location = (arr_players[turn_order].coords[0] + 5, arr_players[turn_order].coords[1] - 20)
                        elements_to_show.append(button.Button(os.getcwd() + '\pictures\\redxmark.png', (80, 80), location))
                        turn_phase = 'playing'
                        new_elements.append(message_button)
                        update_game_display(game_display, turn_phase, arr_players, total_players,
                                            elements_to_show,
                                            turn_order)
                        time.sleep(3)
                        for element in new_elements:
                            if element in elements_to_show:
                                elements_to_show.remove(element)
                        elements_to_show.remove(selected_card)
                        selected_card.play(arr_players[turn_order], arr_players, turn_order, decker, elements_to_show)
                    else:
                        message = font.render('An Exploding Kitten! Will you defuse it?', 1, (0, 0, 0))
                        message_button = button.Button(None, (68, 640), (40, 300), text_surface=message)
                        yes_button = button.Button(os.getcwd() + '\pictures\greencheckmark.png', (80, 80), (40, 372))
                        no_button = button.Button(os.getcwd() + '\pictures\\redxmark.png', (80, 80), (140, 372))
                        new_elements = [message_button, yes_button, no_button]
                        for element in new_elements:
                            elements_to_show.append(element)
                        start_exploding_kitten = False
                        update_game_display(game_display, turn_phase, arr_players, total_players, elements_to_show, turn_order)
                if not arr_players[turn_order].defuse_check():
                    selected_card.play(arr_players[turn_order], arr_players, turn_order, decker, elements_to_show)
                    start_exploding_kitten = True
                    elements_to_show.remove(selected_card)
                if no_button.rect.collidepoint(pygame.mouse.get_pos()):
                    if pygame.mouse.get_pressed()[0]:
                        location = (arr_players[turn_order].coords[0] + 5, arr_players[turn_order].coords[1] - 20)
                        elements_to_show.append(
                            button.Button(os.getcwd() + '\pictures\\redxmark.png', (80, 80), location))
                        selected_card.play(arr_players[turn_order], arr_players, turn_order, decker, elements_to_show)
                        turn_phase = 'playing'
                        for element in new_elements:
                            elements_to_show.remove(element)
                        elements_to_show.remove(selected_card)
                        start_exploding_kitten = True
                        update_game_display(game_display, turn_phase, arr_players, total_players, elements_to_show,
                                            turn_order)
                elif yes_button.rect.collidepoint(pygame.mouse.get_pos()):
                    if pygame.mouse.get_pressed()[0]:
                        for card in arr_players[turn_order].hand:
                            if card.type == 'Defuse':
                                worked = False
                                while not worked:
                                    try:
                                        index = int(inputbox.ask(game_display,
                                                                 'There are %d cards left. Where should the exploding kitten be placed:  ' % decker.cards_left(),
                                                                 200, 360))
                                        worked = True
                                    except ValueError:
                                        worked = False
                                if index >= decker.cards_left():
                                    index = decker.cards_left() - 1
                                card.play(arr_players[turn_order], arr_players, turn_order, decker,
                                          elements_to_show, chosen_card=selected_card, exploding_kitten_index=index)
                                advance_turn(arr_players, turn_order, turn_marker, elements_to_show, attack)
                                update_game_display(game_display, turn_phase, arr_players, total_players,
                                                    elements_to_show,
                                                    turn_order)
                        turn_phase = 'playing'
                        start_exploding_kitten = True
                        for element in new_elements:
                            elements_to_show.remove(element)
            elif turn_phase == 'nope':
                arr_players[turn_order].hide_cards(elements_to_show)
                if first_nope_instance:
                    message = font.render('A player has a nope card! Does somebody want to play one?', 1, (0, 0, 0))
                    message_button = button.Button(None, (68, 640), (400, 300), text_surface=message)
                    yes_button = button.Button(os.getcwd() + '\pictures\greencheckmark.png', (80, 80), (40, 372))
                    no_button = button.Button(os.getcwd() + '\pictures\\redxmark.png', (80, 80), (140, 372))
                    new_elements = [message_button, yes_button, no_button]
                    for element in new_elements:
                        elements_to_show.append(element)
                    first_nope_instance = False
                elif deciding_to_play_nope:
                    if yes_button.rect.collidepoint(pygame.mouse.get_pos()):
                        if pygame.mouse.get_pressed()[0]:
                            deciding_to_play_nope = False
                            elements_to_show.remove(message_button)
                            elements_to_show.remove(yes_button)
                            message = font.render('Click the player who will play the nope!', 1, (0, 0, 0))
                            message_button = button.Button(None, (68, 640), (400, 300), text_surface=message)
                            new_elements.append(message_button)
                            elements_to_show.append(message_button)
                            update_game_display(game_display, turn_phase, arr_players, total_players, elements_to_show,
                                                turn_order)
                    if no_button.rect.collidepoint(pygame.mouse.get_pos()):
                        if pygame.mouse.get_pressed()[0]:
                            turn_phase = 'playing'
                            nope_pass = True
                            first_nope_instance = True
                            for element in new_elements:
                                elements_to_show.remove(element)
                            update_game_display(game_display, turn_phase, arr_players, total_players, elements_to_show,
                                                turn_order)
                else:
                    for element in elements_to_show:
                        if element in arr_players:
                            if element.rect.collidepoint(pygame.mouse.get_pos()):
                                if pygame.mouse.get_pressed()[0]:
                                    nope_exists = False
                                    nope_card = None
                                    for i in element.hand:
                                        if i.type == 'Nope':
                                            nope_exists = True
                                            nope_card = i
                                    if nope_exists:
                                        turn_phase = 'playing'
                                        nope_card.play(element, arr_players, turn_order, decker, elements_to_show,
                                                       chosen_card=selected_card, chosen_player=arr_players[turn_order])
                                        first_nope_instance = True
                                        nope_pass = False
                                        deciding_to_play_nope = True
                                        for thing in new_elements:
                                            if thing in elements_to_show:
                                                elements_to_show.remove(thing)
                        if no_button.rect.collidepoint(pygame.mouse.get_pos()):
                            if pygame.mouse.get_pressed()[0]:
                                turn_phase = 'playing'
                                nope_pass = True
                                for thing in new_elements:
                                    if thing in elements_to_show:
                                        elements_to_show.remove(thing)

        update_game_display(game_display, turn_phase, arr_players, total_players, elements_to_show, turn_order)
    pygame.quit()
    quit()


def go():
    decker, arr_players, game_display, font = initialize()
    time.sleep(3)
    gamePhase(decker, arr_players, game_display, font)
    for i, k in enumerate(arr_players):
        print(k.print_name())
        k.show_hand()
