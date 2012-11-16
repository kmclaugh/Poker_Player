import pickle
import sys
sys.path.append("/Users/kevin/Desktop/10% Time/Poker_Player")
from Deck_Creator import *
from Hand_Class import *
from Poker_Test_Benches import *
import subprocess

def load_current_preflop_two_players_probabilities():
    dictionary_file_location = "/Users/kevin/Desktop/10% Time/Poker_Player/current_probability_dictionary.dat"
    dictionary_file = open(dictionary_file_location,"rb")
    current_probability_dictionary = pickle.load(dictionary_file)
    dictionary_file.close()
    return(current_probability_dictionary)



def binomial(n, k):
    """binomial(n, k): return the binomial coefficient (n k)."""
    if k < 0 or k > n:
        return 0
    if k == 0 or k == n:
        return 1
    return factorial(n) // (factorial(k) * factorial(n-k))

probability_dictionary = load_current_preflop_two_players_probabilities()

##returns the probability that a given hand is currently the best for a given number of players before the flop
def probability_of_best_hand_current_preflop(a_hand,number_of_other_players):
    n = number_of_other_players
    probability_I_have_best_hand_against_1 = probability_dictionary[a_hand.crunch_binary()]
#    if n == 1:
#        return(probability_I_have_best_hand_against_1)
#    else:
    th = total_hands = 1000
    ib = hands_i_beat = int(total_hands*probability_I_have_best_hand_against_1)
    print(ib)
    hb = hands_that_beat_me = int(total_hands - hands_i_beat)
    total_probability_i_lose = 0
    for i in range(1,(n+1)):
        if i > hb:
            break
        beats_me_factors = factorial(hb)/factorial(hb-i)
        i_beat_factor = factorial(ib)/factorial(ib-(n-i))
        total_factor = factorial(th)/factorial(th-(n))
        binomial_factor = binomial(n,i)
        
        
        this_prob = (beats_me_factors*i_beat_factor/total_factor)*binomial_factor
        
        total_probability_i_lose += this_prob
    
    total_probability_i_win = float(1-total_probability_i_lose)
    return(total_probability_i_win)


#test_hand = hand([deck[0],deck[1]])
#print(test_hand)
#print(probability_dictionary[test_hand.crunch_binary()])
#
#probability_I_Good = probability_of_best_hand_current_preflop(test_hand,1)
#print(probability_I_Good)


