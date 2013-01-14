import sys
sys.path.append("/Users/kevin/Desktop/10% Time/Poker_Player")
from Deck_Creator import *
from Hand_Class import *
from random import shuffle
from Player_Class import *
from Poker_Game_Methods import *


## Defines how betting works. Includes methods for split pots.
def betting_process(a_player, player_decision, the_hand_info):
    a_player.owes = the_hand_info.current_bet - a_player.current_bet
    if player_decision == "raise" and the_hand_info.number_of_raises < the_hand_info.raise_cap and a_player.money >= (a_player.owes+the_hand_info.raise_amount):
        ## update player info
        player_raise = the_hand_info.raise_amount + a_player.owes
        a_player.money = a_player.money - player_raise
        a_player.current_bet = a_player.current_bet + player_raise
        a_player.owes = 0
        
        ## update cummunity info
        the_hand_info.current_bet += the_hand_info.raise_amount
        the_hand_info.pot.main += player_raise
        the_hand_info.number_of_raises += 1
        
        action = "{} raises with {}. Pot equals {}".format(a_player.name,a_player.hand,the_hand_info.pot)
    
    if player_decision == "raise" and the_hand_info.number_of_raises < the_hand_info.raise_cap and a_player.money <= (a_player.owes+the_hand_info.raise_amount):
        all_in = True
        the_hand_info.pot.main += a_player.money
    
    elif player_decision == "raise" and the_hand_info.number_of_raises == the_hand_info.raise_cap and a_player.money >= (a_player.owes+the_hand_info.raise_amount):
        print(("raise", a_player.owes))
        the_hand_info.pot.main += a_player.owes
        a_player.money = a_player.money - a_player.owes
        a_player.current_bet = a_player.owes
        if a_player.owes == 0:
            action = "{} checks with {}. Pot equals {}".format(a_player.name,a_player.hand, the_hand_info.pot)
        else:
            action = "{} calls with {}. Pot equals {}".format(a_player.name,a_player.hand, the_hand_info.pot)
        a_player.owes = 0
    
    elif player_decision == "call" and a_player.money >= a_player.owes:
        print(("call",a_player.owes))
        the_hand_info.pot.main += a_player.owes
        a_player.money = a_player.money - a_player.owes
        a_player.current_bet = a_player.owes
        if a_player.owes == 0:
            action = "{} checks with {}. Pot equals {}".format(a_player.name,a_player.hand, the_hand_info.pot)
        else:
            action = "{} calls with {}. Pot equals {}".format(a_player.name,a_player.hand, the_hand_info.pot)
        a_player.owes = 0
    return([a_player,the_hand_info,action])

