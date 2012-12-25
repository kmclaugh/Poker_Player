import pickle
import sys
sys.path.append("/Users/kevin/Desktop/10% Time/Poker_Player")
from Deck_Creator import *
from Hand_Class import *
from itertools import combinations
import subprocess
from datetime import *
from random import shuffle
from probability_hand_look_up_table_creator import remove_card_from_deck

## Load the deck from the pickle file
deck_file_location = "/Users/kevin/Desktop/10% Time/Poker_Player/full_deck.dat"
deck_file = open(deck_file_location,"rb")
deck = pickle.load(deck_file)

def accurracy_check_combination(number_of_cards):
    
    start_time = datetime.now()
    print(start_time)
    possible_hands = list(combinations(deck,number_of_cards))

    straight_flush_count = 0
    four_of_a_kind_count = 0
    full_house_count = 0
    flush_count = 0
    straight_count = 0
    three_of_a_kind_count = 0
    two_pair_count = 0
    pair_count = 0
    high_card_count = 0
    subprocess.call(['say','Finished creating combinations'])
    

    for y in possible_hands:
        the_hand = hand(list(y))
        best_hand = find_best_hand(the_hand)
        
        if best_hand == 0:
            high_card_count += 1
        
        elif best_hand == 1:
            pair_count += 1
        
        elif best_hand == 2:
            two_pair_count += 1
        
        elif best_hand == 3:
            three_of_a_kind_count += 1
        
        elif best_hand == 4:
            straight_count += 1
        
        elif best_hand == 5:
            flush_count += 1
        
        elif best_hand == 6:
            full_house_count += 1
        
        elif best_hand == 7:
            four_of_a_kind_count += 1
        
        elif best_hand == 8:
            straight_flush_count += 1

    end_time = datetime.now()
    time_difference = end_time - start_time


    print(straight_flush_count)
    print(four_of_a_kind_count)
    print(full_house_count)
    print(flush_count)
    print(straight_count)
    print(three_of_a_kind_count)
    print(two_pair_count)
    print(pair_count)
    print(high_card_count)
    print("compare with:")
    print("http://wizardofodds.com/games/poker/")
    print("Test took:")
    totaltime = end_time - start_time
    print(totaltime)
    subprocess.call(['say','Finished program run'])

def montecarlo_probability_test_best_hand_module(a_hand,number_of_players, number_of_trails):
    
    start_time = datetime.now()
    print(start_time)
    
    deck = load_deck()
    new_deck = remove_card_from_deck(deck,a_hand.cards[0])
    new_deck = remove_card_from_deck(new_deck,a_hand.cards[1])
    
    hands_I_won = 0
    total_hands_played = 0
    for trail in range(0,number_of_trails):
        shuffle(new_deck)
        other_players_hands = []
        iterator = 0
        for a_player in range(0,number_of_players):
            this_players_hand = []
            for a_card in range(0,len(a_hand)):
                this_players_hand.append(new_deck[iterator])
                iterator += 1
            this_players_hand = hand(this_players_hand)
            other_players_hands.append(this_players_hand)
        for opponent_hand in other_players_hands:
            the_winning_hand = compare_two_hands(a_hand,opponent_hand)
            if the_winning_hand != "tie":
                if the_winning_hand.cards != opponent_hand.cards:
                    hands_I_won += 1
            else:
                hands_I_won += 1
            total_hands_played += 1

    end_time = datetime.now()
    totaltime = end_time - start_time
    print(totaltime)

    probability = hands_I_won/total_hands_played
    return(probability)



def montecarlo_probability_river_simulator(a_hand,trails):
    
    deck = load_deck()

    new_deck = remove_card_from_deck(deck,a_hand.cards[0])
    new_deck = remove_card_from_deck(new_deck,a_hand.cards[1])
    
    hands_I_won = 0
    total_hands_played = 0
    
    for trail in range(0,trails):
        shuffle(new_deck)
        the_opponent_hand = hand(new_deck[0:2])
        community_cards = hand(new_deck[2:7])

        
        my_hand = hand(a_hand.cards + community_cards.cards)
        opponent_hand = hand(the_opponent_hand.cards + community_cards.cards)
        the_winning_hand = compare_two_hands(my_hand,opponent_hand)
        if the_winning_hand != "tie":
            if the_winning_hand.cards != opponent_hand.cards:
                hands_I_won += 1
#                print(the_winning_hand.value)
#                print(("my hand",my_hand))
#                print(("op",opponent_hand))
            else:
                pass
        else:
            hands_I_won += 1
        total_hands_played += 1

    probability = hands_I_won/total_hands_played
    return(probability)

#test_hand = hand([deck[7],deck[15]])
#print(test_hand)
#test = montecarlo_probability_river_simulator(test_hand,100)
#print(test)



