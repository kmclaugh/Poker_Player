import sys
sys.path.append("/Users/kevin/Desktop/10% Time/Poker_Player")
from Deck_Creator import *
from Hand_Class import *
from random import shuffle
from Player_Class import *
from Poker_Game_Methods import *
from Action_Logic import *



def single_deal_2(the_hand_info):
    pots_right = True
    player_list = the_hand_info.players_left
    
    ## Deal the cards and return the deck without the dealt cards
    deal_cards_result = deal_cards_to_players(the_hand_info.players_left)
    the_hand_info.players_left = deal_cards_result[0]
    the_hand_info.current_deck = deal_cards_result[1]
    
    ##preflop
    if the_hand_info.print_action == True:
        print("")
        print("preflop:")
    the_hand_info.pot = pot_class(0)
    the_hand_info.current_bet = 0
    preflop_results = action_logic(the_hand_info)
    
    ##setup for flop
    the_hand_info = preflop_results
    if len(the_hand_info.players_left) == 1:
        winning_player = the_hand_info.pot.award(the_hand_info.players_left[0],print_winner=the_hand_info.print_winner)
        the_hand_info.players_left = add_hand_winner_back_to_player_list(winning_player,player_list)
        return(the_hand_info)
    else:
        pass

    the_hand_info.players_left = reset_player_current_bet(the_hand_info.players_left)
    
    
    deal_community_cards_result = deal_community_cards(3,the_hand_info.current_deck)
    the_hand_info.community_cards = deal_community_cards_result[0] #the flop cards
    the_hand_info.current_deck = deal_community_cards_result[1]

#    for test in the_hand_info.players_left:
#        print(test.owes)

    ##flop
    if the_hand_info.print_action == True:
        print("")
        print("flop:")
    flop_results = action_logic(the_hand_info)
    
    ##setup for turn
    the_hand_info = flop_results
    if len(the_hand_info.players_left) == 1:
        winning_player = the_hand_info.pot.award(the_hand_info.players_left[0],print_winner=the_hand_info.print_winner)
        the_hand_info.players_left = add_hand_winner_back_to_player_list(winning_player,player_list)
        return(the_hand_info)
    
    the_hand_info.players_left = reset_player_current_bet(the_hand_info.players_left)
    
    
    deal_community_cards_result = deal_community_cards(1,the_hand_info.current_deck)
    the_hand_info.community_cards = the_hand_info.community_cards + deal_community_cards_result[0] # turn card
    the_hand_info.current_deck = deal_community_cards_result[1]
    
    ##turn
    if the_hand_info.print_action == True:
        print("")
        print("turn:")
    turn_results = action_logic(the_hand_info)
    
    ##setup for river
    the_hand_info = turn_results
    if len(the_hand_info.players_left) == 1:
        winning_player = the_hand_info.pot.award(the_hand_info.players_left[0],print_winner=the_hand_info.print_winner)
        the_hand_info.players_left = add_hand_winner_back_to_player_list(winning_player,player_list)
        return(the_hand_info)

    the_hand_info.players_left = reset_player_current_bet(the_hand_info.players_left)
    
    
    deal_community_cards_result = deal_community_cards(1,the_hand_info.current_deck)
    the_hand_info.community_cards = the_hand_info.community_cards + deal_community_cards_result[0] #the river card
    the_hand_info.current_deck = deal_community_cards_result[1]
    
    ##river
    if the_hand_info.print_action == True:
        print("")
        print("river:")

    river_results = action_logic(the_hand_info)
    
    the_hand_info = river_results

    if len(the_hand_info.players_left) == 1:
        winning_player = the_hand_info.pot.award(the_hand_info.players_left[0],print_winner=the_hand_info.print_winner)
        the_hand_info.player_left = add_hand_winner_back_to_player_list(winning_player,player_list)
        return(the_hand_info)
    
    
    
    ##showdown
    players_left = add_community_cards_to_all_players(a_list_of_players=the_hand_info.players_left,the_community_cards=the_hand_info.community_cards)
    if the_hand_info.print_action == True:
        print("")
        print("showdown")
        for a_player in the_hand_info.players_left:
            print("{} has {}".format(a_player.name,a_player.hand))
        print("")
    winning_player = compare_multiple_player_hands(the_hand_info.players_left)
    winning_player = the_hand_info.pot.award(winning_player,print_winner=the_hand_info.print_winner)
    the_hand_info.players_left = add_hand_winner_back_to_player_list(winning_player,the_hand_info.player_list)
    
    return(the_hand_info)






## Test Bench
def always_call(hand,the_hand_info,player_current_bet,owes,number_of_players_left):
    return("call")

def always_raise(hand,the_hand_info,player_current_bet,owes,number_of_players_left):
    return("raise")

def always_fold(hand,the_hand_info,player_current_bet,owes,number_of_players_left):
    return("fold")

def random_decision(hand,the_hand_info,player_current_bet,owes,number_of_players_left):
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

the_hand_info = hand_info_class(raise_amount=1,raise_cap=3,print_action=True,print_cards=True,print_winner=True,number_of_raises=0, current_deck=None,community_cards=[],current_bet=None,remove_list=[],players_left=random_players,pot=None)

the_hand_info = single_deal_2(the_hand_info)

for a_player in the_hand_info.players_left:
    print((a_player.name,a_player.money))
