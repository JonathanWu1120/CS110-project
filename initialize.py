import deck
import player
import Card
import loops

    #makes all the cards needed for the game
def initialize():
    exploding_kitten = Card.Card("Exploding Kitten")
    defuse = Card.Card("Defuse")
    skip = Card.Card("Skip")
    attack = Card.Card("Attack")
    rainbow_cat = Card.Card("Rainbow Cat")
    favor = Card.Card("Favor")
    shuffle = Card.Card("Shuffle")
    tacocat = Card.Card("Taco Cat")
    catermelon = Card.Card("Catermelon")
    hairy_potato_cat = Card.Card("Hairy Potato Cat")
    beard_cat = Card.Card("Beard Cat")
    nope = Card.Card("Nope")
    see_future = Card.Card("See the Future")
    decker = deck.Deck()
    #array containing all the cards which will be used for the calling of their specific function
    arr = [exploding_kitten,defuse,skip,attack,favor,shuffle,rainbow_cat,tacocat,catermelon,hairy_potato_cat,beard_cat,nope,see_future]
    #adds 4 of every card that is not an exploding kitten or defuse
    for i in range(4):
        for i in range(2,13):
            decker.add_card(arr[i])
    #these two cards appear 5 times in the deck so they are added again
    decker.add_card(nope)
    decker.add_card(see_future)
    decker.shuffle()
    num_players = -1
    while num_players < 2 or num_players > 5:
        try:
            num_players = int(input("Enter the number of players (2-5): "))
        except ValueError:
            print("That's not a valid integer.")
    arr_players = []
    for i in range(num_players):
        player_name = player.Player(input("Enter the name of player "+str(i+1)+": "))
        player_name.starting_hand(decker,arr[1])
        arr_players.append(player_name)
    #exploding kittens are added to the deck
    for i in range(num_players-1):
        decker.add_card(exploding_kitten)
    #there is one extra defuse card in the deck
    decker.add_card(defuse)
    decker.shuffle()
    return decker,arr_players,arr

def main():
    #screen = screen.make_screen()
    decker,arr_players,cards = initialize()
    for i,k in enumerate(arr_players):
        print(k.print_name())
        arr_players[i].show_hand()
    turn_order = 0
    while len(arr_players) != 1:
        death,attack = loops.choice_loop(decker,cards,arr_players,turn_order)
        if death == None:
            arr_players.pop(turn_order)
            turn_order -= 1
            turn_order = loops.turn_rollover(turn_order,len(arr_players))
        if attack:
            turn_order = loops.turn_rollover(turn_order,len(arr_players))
            turn_order += 1
            death,attack = loops.choice_loop(decker,cards,arr_players,turn_order)
        turn_order += 1
        turn_order = loops.turn_rollover(turn_order,len(arr_players))

main()