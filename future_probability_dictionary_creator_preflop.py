import pickle
import sys
sys.path.append("/Users/kevin/Desktop/10% Time/Poker_Player")
from Deck_Creator import *
from Hand_Class import *
from Poker_Test_Benches import *
from Poker_Probability_Modules import *
from datetime import *
import subprocess
import os
from itertools import combinations
## Load the deck from the pickle file
deck = load_deck()

def remove_cards_from_hand(the_hand,cards_to_remove):
    new_hand_list = the_hand.cards
    for the_card in  cards_to_remove:
        if the_card in new_hand_list:
            new_hand_list.remove(the_card)
    
    new_hand = hand(new_hand_list)
    return(new_hand)
        

def create_future_probability_dictionary():
    
    start_time = datetime.now()
    print(start_time)
    
    future_probability_dictionary = {}
#    my_possible_starting_hands = list(combinations(deck,2))
    my_possible_starting_hands = [(deck[12],deck[25])]
    print(my_possible_starting_hands)
    for my_hand in my_possible_starting_hands:
        hands_I_won = 0
        total_hands_played = 0
        
        ## Convert the combinations() tuple to a hand class
        my_hand = hand(list(my_hand))
        
        
        ## Remove the cards used in my_hand from the deck and store as a new deck. Then make the possible combinations of oppenent hands with the new deck
        new_deck = remove_card_from_deck(deck,my_hand.cards[0])
        new_deck = remove_card_from_deck(new_deck,my_hand.cards[1])
        possbile_community_cards = list(combinations(new_deck,5))

        for community_cards in possbile_community_cards:
            
            community_cards = hand(list(community_cards))
            my_hand = hand(my_hand.cards + community_cards.cards)
            
            ## Defines the tie (best cards, kicker, etc) information for my_hand to speed up the comparison
            my_hand.value = find_best_hand(my_hand)
            my_kicker = find_kicker(my_hand,my_hand.value)
            my_hand.card1 = my_kicker.best_card1
            my_hand.card2 = my_kicker.best_card2
            my_hand.kicker = my_kicker.kicker_sum

            
            new_deck = remove_card_from_deck(new_deck,community_cards.cards[0])
            new_deck = remove_card_from_deck(new_deck,community_cards.cards[1])
            new_deck = remove_card_from_deck(new_deck,community_cards.cards[2])
            new_deck = remove_card_from_deck(new_deck,community_cards.cards[3])
            new_deck = remove_card_from_deck(new_deck,community_cards.cards[4])
            possbile_oppenent_hands = list(combinations(new_deck,2))

            for opponent_hand in possbile_oppenent_hands:
                opponent_hand = hand(list(opponent_hand))
                opponent_hand = hand(opponent_hand.cards + community_cards.cards)

                the_winning_hand = compare_two_hands(my_hand,opponent_hand)
                if the_winning_hand != "Equal":
                    if the_winning_hand.crunch_binary() != opponent_hand.crunch_binary():
                        hands_I_won += 1
                else:
                    hands_I_won += 1
                total_hands_played += 1
            my_hand = remove_cards_from_hand(my_hand,community_cards.cards)
        
        probability = hands_I_won/total_hands_played
        future_probability_dictionary[my_hand.crunch_binary()] = probability
        print((my_hand.crunch_binary(),probability))
    
    print(future_probability_dictionary)
    end_time = datetime.now()
    totaltime = end_time - start_time
    print(totaltime)
            
    current_directory = os.getcwd()
    dictionary_file_location = "{}/future_probability_dictionary.dat".format(current_directory)
    dictionary_file = open(dictionary_file_location,"wb")
    pickle.dump(future_probability_dictionary,dictionary_file)
    dictionary_file.close()

    


create_future_probability_dictionary()






