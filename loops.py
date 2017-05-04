def choose_loop(hand):
    is_in = True
    while is_in:
        card_index = int(input("Which card?"))
        if card_index > len(hand) - 1 or card_index < 0:
            print("Your hand is not that big")
        else:
            played_card = hand.pop(card_index)
            is_in = False
    print("You played", played_card.type)
    return played_card


def choice_loop(decker, cards, arr_players, turn_order):
    pick = True
    attack = False
    player = arr_players[turn_order]
    while pick:
        print("Player", player.name)
        print("There are currently ", decker.cards_left(), "cards left")
        pick, attack = phase_loop(pick, attack, decker, cards, player, arr_players, turn_order)
    return pick, attack


def exploding_kitten(player, cards, decker):
    print("EXPLODING KITTEN")
    if cards[1] in player.hand:
        decision = input("Would you like to play your defuse? (y/n): ")
        while decision != "n" and decision != "y":
            decision = input("Would you like to play your defuse? (y/n): ")
        if decision == "n":
            print("You have died! :(")
            return None, False
        elif decision == "y":
            player.hand.pop(player.hand.index(cards[1]))
            print("You have played a defuse\n There are currently", decker.cards_left() + 1, "cards left in the deck")
            deck_spot = int(input("Enter the location you want the exploding kitten to be placed"))
        while deck_spot > decker.cards_left() + 1 or deck_spot < 0:
            deck_spot = int(input("Enter the location you want the exploding kitten to be placed"))
        decker.add_card(cards[0], deck_spot - 1)
        return False, False
    return True, False


def phase_loop(pick, attack, decker, cards, player, arr_players, turn_order):
    choice = input("Do you want to draw a card or play a card from your hand (D/P) : ")
    if choice == "D":
        pick = False
        drawn = decker.draw_top()
        if drawn == cards[0]:
            return exploding_kitten(player, cards, decker)
        player.hand.append(drawn)
        print("You drew", drawn.type)
        return False, False
    elif choice == "P":
        pick, attack = player.play_card(decker, player.hand, pick, cards, attack, arr_players, turn_order)
    return pick, attack


def choosing_player(arr_players, player):
    print("There are", len(arr_players), "people playing")
    recipient = int(input("Select which player you want to take from"))
    while recipient < 0 or recipient > len(arr_players) - 1 or recipient == arr_players.index(player):
        recipient = int(input("Select which player you want to steal from"))
    return arr_players[recipient]


def card_stealing(arr_players, recipient):
    print("This player has ", recipient.len_hand(), " cards in their hand")
    stolen_card = int(input("Enter which card you want stolen"))
    while stolen_card > recipient.len_hand() or stolen_card < 0:
        stolen_card = int(input("Enter which card you want stolen"))
    return stolen_card


def give_card(recipient):
    recipient.show_hand()
    selected_card = int(input("Which card would you like to give away? "))
    while selected_card > recipient.len_hand() or selected_card < 0:
        selected_card = int(input("Which card would you like to give away?"))
    return recipient.hand[selected_card]


def phase_of_taking(arr_players, player):
    for k, v in enumerate(arr_players):
        print(str(k) + "-" + v.name)
    recipient = choosing_player(arr_players, player)
    return recipient


def turn_rollover(turn_order, number_players):
    if turn_order == number_players:
        turn_order = 0
    elif turn_order < 0:
        turn_order = number_players
    return turn_order

    # def main_loop(decker,cards,arr_players):
    #     turn_order = 0
    #     while len(arr_players) != 1:
    #         death,attack = choice_loop(decker,cards,arr_players,turn_order)
    #         if death == True:
    #             print("Yeah")
    #             arr_players.pop(turn_order)
    #             turn_order -= 1
    #             turn_order = turn_rollover(turn_order,len(arr_players))
    #         if attack:
    #             turn_order = turn_rollover(turn_order,len(arr_players))
    #             turn_order += 1
    #             death,attack = choice_loop(decker,cards,arr_players,turn_order)
    #         turn_order += 1
    #         turn_order = turn_rollover(turn_order,len(arr_players))
