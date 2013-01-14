import sys
sys.path.append("/Users/kevin/Desktop/10% Time/Poker_Player")
from Deck_Creator import *
from Hand_Class import *
from random import shuffle
from Player_Class import *


## Deals cards to a given list of players at random from the deck
def deal_cards_to_players(players):
    ## Load the deck from the pickle file
    deck = load_deck()
    shuffle(deck)
    players_with_hands = []
    counter = 0

    for player in players:
        player_hand = hand(deck[counter:counter+2])
        player.hand = player_hand
        players_with_hands.append(player)
        counter += 2
    
    current_deck = deck[counter:]
    return((players_with_hands,current_deck))

def deal_TEST_cards_to_players(players):
    ## Load the deck from the pickle file
    deck = load_deck()
    players_with_hands = []
    counter = 0
    ## Test hands go here
    test_hand1 = hand(deck[0:2])
    used_cards = test_hand1.cards
    test_hand2 = hand(deck[0:2])
    used_cards = used_cards + test_hand2.cards
    test_hand3 = hand([deck[0],deck[25]])
    used_cards = used_cards + test_hand3.cards
    test_hand4 = hand([deck[0],deck[25]])
    used_cards = used_cards + test_hand4.cards
    test_hand5 = hand([deck[1],deck[30]])
    used_cards = used_cards + test_hand5.cards
    test_hand6 = hand(deck[0:2])
    used_cards = used_cards + test_hand6.cards
    test_hand7 = hand(deck[0:2])
    used_cards = used_cards + test_hand7.cards
    test_hands = [test_hand1,test_hand2,
                  test_hand3,test_hand4,test_hand5,test_hand6,test_hand7]
    
    for player in players:
        player.hand = test_hands[counter]
        players_with_hands.append(player)
        counter += 1
    
    current_deck = [deck[18],deck[3],deck[37],deck[7],deck[9]] ##test community cards
    return((players_with_hands,current_deck))

## Deals out a given number of community cards and returns the cards and current deck
def deal_community_cards(number_of_cards_to_be_dealt,current_deck):
    community_cards = current_deck[0:number_of_cards_to_be_dealt] ##the new community cards
    current_deck = current_deck[number_of_cards_to_be_dealt:]
    return([community_cards,current_deck])

## Reset player.current_bet for all players in a given list
def reset_player_current_bet(players_left):
    for player in players_left:
        player.current_bet = 0
    return(players_left)


## Adds the winning player, with updated money back into the player list. Also reset all single deal values for all players
def add_hand_winner_back_to_player_list(winning_player,player_list):
    if type(winning_player) != list:
        for a_player in player_list:
            a_player.current_bet = 0
            a_player.owes = 0
            a_player.hand = None
            if a_player.name == winning_player.name:
                player_list.remove(a_player)
                player_list.append(winning_player)
                return(player_list)
    else:
        for a_player in player_list:
            a_player.current_bet = 0
            a_player.owes = 0
            a_player.hand = None
            for a_winner in winning_player:
                if a_player.name == a_winner.name:
                    player_list.remove(a_player)
                    player_list.append(a_winner)
        return(player_list)

## Adds the community cards to each player's hand.
def add_community_cards_to_all_players(a_list_of_players,the_community_cards):
    for a_player in a_list_of_players:
        a_player.hand.add_community_cards(the_community_cards)
    return(a_list_of_players)

## Compares a list of players with hands without assigned values and returns the winner
def compare_multiple_player_hands(a_list_of_players):
    for a_player in a_list_of_players:
        a_player.hand = assign_all_hand_values(a_player.hand)
    a_list_of_players = sorted(a_list_of_players, key=lambda player: player.hand.value,reverse=True)
    best_value = a_list_of_players[0].hand.value
    best_value_players = []
    for a_player in a_list_of_players:
        if a_player.hand.value == best_value:
            best_value_players.append(a_player)
    if len(best_value_players) == 1:
        winner = best_value_players[0]
    else:
        a_list_of_players = sorted(a_list_of_players, key=lambda player: player.hand.card_order,reverse=True)
        the_best_card_order = a_list_of_players[0].hand.card_order
        winning_player = []
        for a_player in a_list_of_players:
            if a_player.hand.card_order == the_best_card_order:
                winning_player.append(a_player)
        if len(winning_player) == 1:
            winner = winning_player[0]
        else:
            winner = winning_player
    return(winner)


class pot_class:

    def __init__(self,main=0,side1=0,side2=0,side3=0,side4=0,side5=0):
        self.main = main
        self.side1 = side1
        self.side2  = side2
        self.side3 = side3
        self.side4 = side4
        self.side5 = side5

    def __str__(self):
        return_string = "{}".format(self.main)
        return(return_string)

    def __repr(self):
        return_string = "{}".format(self.main)
        return(return_string)

    ## Awards the main pot to a winning player or a list of winning players. 
    def award(self,winning_player,print_winner=False):
        if type(winning_player) != list:
            winning_player.money = winning_player.money + self.main
            if print_winner == True:
                print("{} has won {} with {}".format(winning_player.name,self.main,winning_player.hand))
                print("")
            return(winning_player)
        else:
            pot_split = self.main/len(winning_player)
            print_string = ""
            for a_player in winning_player:
                a_player.money = a_player.money + pot_split
                print_string = print_string +"{} ".format(a_player.name)
            if print_winner == True:
                print_string = print_string +"have split the pot. They each won {}.".format(pot_split)
                print(print_string)
                print("")
            return(winning_player)


## Defines how betting works. Includes methods for split pots.
def betting_logic(a_player, pot, player_decision, current_bet, raise_amount, number_of_raises,raise_cap):
    a_player.owes = current_bet - a_player.current_bet
    if player_decision == "raise" and number_of_raises < raise_cap and a_player.money >= (a_player.owes+raise_amount):
        ## update player info
        player_raise = raise_amount + a_player.owes
        a_player.money = a_player.money - player_raise
        a_player.current_bet = a_player.current_bet + player_raise
        a_player.owes = 0
        
        ## update cummunity info
        current_bet += raise_amount
        pot.main += player_raise
        number_of_raises += 1
        
        action = "{} raises with {}. Pot equals {}".format(a_player.name,a_player.hand,pot)
    
    if player_decision == "raise" and number_of_raises < raise_cap and a_player.money <= (a_player.owes+raise_amount):
        all_in = True
        pot.main += a_player.money
    
    elif player_decision == "raise" and number_of_raises == raise_cap and a_player.money >= (a_player.owes+raise_amount):
        pot.main += a_player.owes
        a_player.money = a_player.money - a_player.owes
        a_player.current_bet = a_player.owes
        action = "{} calls with {}. Pot equals {}".format(a_player.name,a_player.hand, pot)
        a_player.owes = 0
            
    elif player_decision == "call" and a_player.money >= a_player.owes:
        pot.main += a_player.owes
        a_player.money = a_player.money - a_player.owes
        a_player.current_bet = a_player.owes
        if a_player.owes == 0:
            action = "{} checks with {}. Pot equals {}".format(a_player.name,a_player.hand, pot)
        else:
            action = "{} calls with {}. Pot equals {}".format(a_player.name,a_player.hand, pot)
        a_player.owes = 0
    return([a_player,pot,current_bet,number_of_raises,action])

