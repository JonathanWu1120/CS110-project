import deck
import player
import Card
import gui

    #makes all the cards needed for the game
def initialize():
    screen = gui.view()
    buttons = screen.start_up()
    num_players = screen.determine_players(buttons)
    '''
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
    '''
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
    # num_players = -1
    # while num_players < 2 or num_players > 5:
    #     try:
    #         num_players = int(input("Enter the number of players (2-5): "))
    #     except ValueError:
    #         print("That's not a valid integer.")
    arr_players = []
    for i in range(num_players):
        new_player = player.Player(input("Enter the name of player "+str(i+1)+": "))
        new_player.starting_hand(decker,Card.Card(arr[1]))
        arr_players.append(new_player)
    #exploding kittens are added to the deck
    for i in range(num_players-1):
        decker.add_card(Card.Card(arr[0]))
    #there is one extra defuse card in the deck
    decker.add_card(Card.Card(arr[1]))
    decker.shuffle()
    return decker,arr_players,arr,screen

def main():
    #screen = screen.make_screen()
    decker,arr_players,cards,screen = initialize()
    screen.game_phase(decker,arr_players,cards)
    for i,k in enumerate(arr_players):
        print(k.print_name())
        k.show_hand()
main()