import sys
sys.path.append("/Users/kevin/Desktop/10% Time/Poker_Player")
from Deck_Creator import *
from Hand_Class import *
from random import shuffle
from Player_Class import *
from Poker_Game_Methods import *


## Defines the sequence of events for raising, folding and calling.
def action_logic(players_left,community_cards,pot,raise_amount,raise_cap,print_action = False,print_cards=False):
    current_bet = 0
    number_of_raises = 0
    remove_list = []
    for player in players_left:
        if len(players_left)-len(remove_list) != 1:
            player.owes = current_bet - player.current_bet
            decision = player.strategy(community_cards=community_cards, pot=pot, the_current_bet=current_bet, number_of_players_left=len(players_left))
            if decision == "fold":
                remove_list.append(player)
                player.owes = 0
                action = "{} folds with {}".format(player.name,player.hand)
            
            else:
                bet_results = betting_logic(player, pot, decision, current_bet, raise_amount, number_of_raises,raise_cap)
                player = bet_results[0]
                pot = bet_results[1]
                current_bet = bet_results[2]
                number_of_raises = bet_results[3]
                action = bet_results[4]
            
            if print_action == True:
                print(action)
        else:
            for a_folder in remove_list:
                players_left.remove(a_folder)
            return([players_left,pot])
    
    for a_folder in remove_list:
        players_left.remove(a_folder)
    remove_list = []
    
    pots_right = False
    while pots_right == False:
        pots_right = True
        for player in players_left:
            if len(players_left)-len(remove_list) != 1:
                player.owes = current_bet - player.current_bet
                if player.owes != 0:
                    decision = player.strategy(community_cards=community_cards, pot=pot, the_current_bet=current_bet, number_of_players_left=len(players_left))
                    if decision == "fold":
                        remove_list.append(player)
                        player.owes = 0
                        action = "{} folds with {}".format(player.name,player.hand)
                    
                    else:
                        bet_results = betting_logic(player, pot, decision, current_bet, raise_amount, number_of_raises,raise_cap)
                        player = bet_results[0]
                        pot = bet_results[1]
                        current_bet = bet_results[2]
                        number_of_raises = bet_results[3]
                        action = bet_results[4]
                    
                    if print_action == True:
                        print(action)
            else:
                for a_folder in remove_list:
                    players_left.remove(a_folder)
                return([players_left,pot])
        
        for a_folder in remove_list:
            players_left.remove(a_folder)
        remove_list = []
    
    return([players_left,pot])


## defines the event for a single deal of cards. ie from the dealing of cards through showdown, if necessary. Awards the winner the pot and returns the list of players with the
def single_deal(player_list,print_action=False,print_cards=False,print_winner=False):
    pots_right = True
    players_left = player_list
    raise_amount = 1
    raise_cap = 3
    
    ## Deal the cards and return the deck without the dealt cards
    deal_cards_result = deal_cards_to_players(players_left)
    players_left = deal_cards_result[0]
    current_deck = deal_cards_result[1]
    
    ##preflop
    if print_action == True:
        print("")
        print("preflop:")
    community_cards =[]
    pot=pot_class(0)
    preflop_results = action_logic(community_cards=community_cards, raise_amount=raise_amount, raise_cap=raise_cap, pot=pot, players_left=players_left, print_action=print_action, print_cards=print_cards)

    ##setup for flop
    players_left = preflop_results[0]
    pot = preflop_results[1]
    if len(players_left) == 1:
        winning_player = pot.award(players_left[0],print_winner=print_winner)
        player_list = add_hand_winner_back_to_player_list(winning_player,player_list)
        return(player_list)

    players_left = reset_player_current_bet(players_left)


    deal_community_cards_result = deal_community_cards(3,current_deck)
    community_cards = deal_community_cards_result[0] #the flop cards
    current_deck = deal_community_cards_result[1]

    ##flop
    if print_action == True:
        print("")
        print("flop:")
    flop_results = action_logic(community_cards=community_cards, raise_amount=raise_amount, raise_cap=raise_cap, pot=pot, players_left=players_left, print_action=print_action, print_cards=print_cards)

    ##setup for turn
    players_left = flop_results[0]
    pot = flop_results[1]
    if len(players_left) == 1:
        winning_player = pot.award(players_left[0],print_winner=print_winner)
        player_list = add_hand_winner_back_to_player_list(winning_player,player_list)
        return(player_list)

    players_left = reset_player_current_bet(players_left)


    deal_community_cards_result = deal_community_cards(1,current_deck)
    community_cards = community_cards + deal_community_cards_result[0] # turn card
    current_deck = deal_community_cards_result[1]

    ##turn
    if print_action == True:
        print("")
        print("turn:")
    turn_results = action_logic(community_cards=community_cards, raise_amount=raise_amount, raise_cap=raise_cap, pot=pot, players_left=players_left, print_action=print_action, print_cards=print_cards)

    ##setup for river
    players_left = turn_results[0]
    pot = turn_results[1]
    if len(players_left) == 1:
        winning_player = pot.award(players_left[0],print_winner=print_winner)
        player_list = add_hand_winner_back_to_player_list(winning_player,player_list)
        return(player_list)
    players_left = reset_player_current_bet(players_left)


    deal_community_cards_result = deal_community_cards(1,current_deck)
    community_cards = community_cards + deal_community_cards_result[0] #the river card
    current_deck = deal_community_cards_result[1]

    ##river
    if print_action == True:
        print("")
        print("river:")
    river_results = action_logic(community_cards=community_cards, raise_amount=raise_amount, raise_cap=raise_cap, pot=pot, players_left=players_left, print_action=print_action, print_cards=print_cards)

    players_left = river_results[0]
    pot = river_results[1]
    if len(players_left) == 1:
        winning_player = pot.award(players_left[0],print_winner=print_winner)
        player_list = add_hand_winner_back_to_player_list(winning_player,player_list)
        return(player_list)



    ##showdown
    players_left = add_community_cards_to_all_players(players_left,community_cards)
    if print_action == True:
        print("")
        print("showdown")
        for a_player in players_left:
            print("{} has {}".format(a_player.name,a_player.hand))
        print("")
    winning_player = compare_multiple_player_hands(players_left)
    winning_player = pot.award(winning_player,print_winner=False)
    player_list = add_hand_winner_back_to_player_list(winning_player,player_list)

    return(player_list)


## Test Here
def always_call(hand,community_cards,pot,the_current_bet,player_current_bet,owes,number_of_players_left):
    return("call")

def always_raise(hand,community_cards,pot,the_current_bet,player_current_bet,owes,number_of_players_left):
    return("raise")

def always_fold(hand,community_cards,pot,the_current_bet,player_current_bet,owes,number_of_players_left):
    return("fold")

def random_decision(hand,community_cards,pot,the_current_bet,player_current_bet,owes,number_of_players_left):
    if owes == 0:
        options = ["call","raise"]
        shuffle(options)
        return(options[0])
    else:
        options = ["fold","call","raise"]
        shuffle(options)
        return(options[0])

always_raise_player1 = player(name="always_raiser1",the_strategy=always_raise,money=10)
always_raise_player2 = player(name="always_raiser2",the_strategy=always_raise,money=10)
always_call_player = player(name="always_caller",the_strategy=always_call,money=10)
always_fold_player = player(name="always_folder1",the_strategy=always_fold,money=10)
always_fold_player2 = player(name="always_folder2",the_strategy=always_fold,money=10)
always_players = [always_fold_player,always_fold_player2,always_raise_player1, always_raise_player2,always_call_player]

random1 = player(name="random1",the_strategy=random_decision,money=10)
random2 = player(name="random2",the_strategy=random_decision,money=10)
random3 = player(name="random3",the_strategy=random_decision,money=10)
random4 = player(name="random4",the_strategy=random_decision,money=10)
random_players = [random1,random2,random3,random4]

player_list = single_deal(random_players,print_winner=True,print_action=True)
print(player_list)
for a_player in player_list:
    print((a_player.name,a_player.money))
