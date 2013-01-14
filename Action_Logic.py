import sys
sys.path.append("/Users/kevin/Desktop/10% Time/Poker_Player")
from Deck_Creator import *
from Hand_Class import *
from random import shuffle
from Player_Class import *
from Poker_Game_Methods import *
from Betting_Process import *

## Defines the sequence of events for raising, folding and calling.
def action_logic(the_hand_info):
    for player in the_hand_info.players_left:
        if len(the_hand_info.players_left)-len(the_hand_info.remove_list) != 1:
            player.owes = the_hand_info.current_bet - player.current_bet
            player_decision = player.strategy(the_hand_info=the_hand_info, number_of_players_left=len(the_hand_info.players_left))
            if player_decision == "fold":
                the_hand_info.remove_list.append(player)
                player.owes = 0
                action = "{} folds with {}".format(player.name,player.hand)
            
            else:
                bet_results = betting_process(player,player_decision,the_hand_info)
                player = bet_results[0]
                the_hand_info = bet_results[1]
                action = bet_results[2]
            
            if the_hand_info.print_action == True:
                print(action)
        else:
            for a_folder in the_hand_info.remove_list:
                the_hand_info.players_left.remove(a_folder)
            return(the_hand_info)
    
    for a_folder in the_hand_info.remove_list:
        the_hand_info.players_left.remove(a_folder)
    the_hand_info.remove_list = []
    
    pots_right = False
    while pots_right == False:
        pots_right = True
        for player in the_hand_info.players_left:
            if len(the_hand_info.players_left)-len(the_hand_info.remove_list) != 1:
                player.owes = the_hand_info.current_bet - player.current_bet
                if player.owes != 0:
                    player_decision = player.strategy(the_hand_info=the_hand_info,number_of_players_left=len(the_hand_info.players_left))
                    if player_decision == "fold":
                        the_hand_info.remove_list.append(player)
                        player.owes = 0
                        action = "{} folds with {}".format(player.name,player.hand)
                    
                    else:
                        bet_results = betting_process(player,player_decision,the_hand_info)
                        player = bet_results[0]
                        the_hand_info = bet_results[1]
                        action = bet_results[2]
                
                    if the_hand_info.print_action == True:
                        print(action)
            else:
                for a_folder in the_hand_info.remove_list:
                    the_hand_info.players_left.remove(a_folder)
                return(the_hand_info)
        
        for a_folder in the_hand_info.remove_list:
            the_hand_info.players_left.remove(a_folder)
        the_hand_info.remove_list = []
        the_hand_info.current_bet = 0
            
    return(the_hand_info)

