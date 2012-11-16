import pickle
import sys
sys.path.append("/Users/kevin/Desktop/10% Time/Poker_Player")
from Deck_Creator import *
from Hand_Class import *
from Poker_Test_Benches import *
from Poker_Probability_Modules import *
import subprocess
from itertools import combinations
## Load the deck from the pickle file
deck = load_deck()




#accurracy_check_combination(2)


prob_dict = load_current_preflop_two_players_probabilities()


test_hand = hand([deck[0],deck[13]])
print(test_hand)



print(prob_dict[test_hand.crunch_binary()])
test = montecarlo_probability_test_best_hand_module_dynamic(test_hand,1,100000)
print(test)

