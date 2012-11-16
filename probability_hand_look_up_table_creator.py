## Creates two look up tables (dictionaries). The fist contains has the probability that a pre-flop hand is current the best hand. The second contains the probability that the current preflop hand will have the best hand by the time the river is dealt.

import pickle
import sys
sys.path.append("/Users/kevin/Desktop/10% Time/Poker_Player")
from Deck_Creator import *
from Hand_Class import *
from Poker_Test_Benches import *
import subprocess
from itertools import combinations
from datetime import *




## removes a given cards from a the deck and returns a new deck. This helps to preserve the complete deck and solves some error with .remove that I could not solve.
def remove_card_from_deck(deck,card):
    new_deck = []
    
    for a_card in deck:
        if a_card.binary != card.binary:
            new_deck.append(a_card)
    return(new_deck)


## iterates through all poosible two card starting hands to determine the probability that that hand is the best against one other player and stores the information for all possible starting hands in a dictionary, where the key is the hand's crunched binary format. Stores the dictionary in a pickle binary file
def create_two_player_current_dictionary():
    deck = load_deck()
    current_probability_dictionary_two_players = {}
    my_possible_starting_hands = list(combinations(deck,2))
    for my_hand in my_possible_starting_hands:
        
        ## Convert the combinations() tuple to a hand class
        my_hand = hand(list(my_hand))
        
        ## Remove the cards used in my_hand from the deck and store as a new deck. Then make the possible combinations of oppenent hands with the new deck
        new_deck = remove_card_from_deck(deck,my_hand.cards[0])
        new_deck = remove_card_from_deck(new_deck,my_hand.cards[1])
        possbile_opponent_hands = list(combinations(new_deck,2))
        
        ## Defines the tie (best cards, kicker, etc) information for my_hand to speed up the comparison
        my_hand.value = find_best_hand(my_hand)
        my_kicker = find_kicker(my_hand,my_hand.value)
        my_hand.card1 = my_kicker.best_card1
        my_hand.card2 = my_kicker.best_card2
        my_hand.kicker = my_kicker.kicker_sum
        
        ## Loop through all possible oppenent hands, compare with my hand, and if my hand wins added it to the winning total. After each comparison, no matter the outcome add one to the total hands played
        total_hands_played = 0
        hands_I_won = 0
        for opponent_hand in possbile_opponent_hands:
            opponent_hand = hand(list(opponent_hand))
            the_winning_hand = compare_two_hands(my_hand,opponent_hand)
            if the_winning_hand != "Equal":
                if the_winning_hand.cards != opponent_hand.cards:
                    hands_I_won += 1
            else:
                hands_I_won += 1
            total_hands_played += 1
        
        ## calculate the probability that my hand is the current best hand by dividing the hand I win by the total hands played
        probability = hands_I_won/total_hands_played
    
        ## Store the new value in the probability dictionary. The key is the crunched binary version of of the hand and the value is the probability
        current_probability_dictionary_two_players[my_hand.crunch_binary()] = probability

    print(current_probability_dictionary_two_players)
    print(total_hands_played)

#    dictionary_file_location = "/Users/kevin/Desktop/10% Time/Poker_Player/current_probability_dictionary.dat"
#    dictionary_file = open(dictionary_file_location,"wb")
#    pickle.dump(current_probability_dictionary_two_players,dictionary_file)
#    dictionary_file.close()
#
#
### Use this to rewrite the dictionary
#create_two_player_current_dictionary()



    
