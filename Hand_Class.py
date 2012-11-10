## This defines the hand class with methods for adding cards to the current hand, reading off the best hand, and others.

import sys
sys.path.append("/Users/kevin/Desktop/10% Time/Poker_Player")
from Deck_Creator import *
the_deck_file_location = "/Users/kevin/Desktop/10% Time/Poker_Player/full_deck.dat"
the_deck_file = open(the_deck_file_location,"rb")
deck = pickle.load(the_deck_file)


class hand(list):
    
    
    def crunch_binary(self):
        bin_sum = self[0].binary
        for n in self[1:]:
            bin_sum = bin_sum + n.binary
        return(bin_sum)

    def crunch_octal(self):
        oct_sum = self[0].octal
        for n in self[1:]:
            oct_sum = oct_sum + n.octal
        return(oct_sum)

    def returnsuits(self):
        bin_val = self.crunch_binary()
        clubs = bin_val[42:]
        diamonds = bin_val[(42-13):42]
        hearts = bin_val[(42-13*2):(42-13)]
        spades = bin_val[(42-13*3):(42-13*2)]
        return([spades,hearts,diamonds,clubs])
    

def find_pair(a_hand):
    oct_val = str(a_hand.crunch_octal())
    if "2" in oct_val:
        return(True)
    else:
        return(False)

def find_straight(a_hand):
    oct_val = str(a_hand.crunch_octal())
    if "11111" in oct_val:
        return(True)
    else:
        return(False)

def find_straight_flush(a_hand):
    suites = a_hand.returnsuits()
    straight_flush_boole = False
    for y in suites:
        if "11111" in y:
            straight_flush_boole = True
    return(straight_flush_boole)

## Note that 3 is in the string "13b0000000000" for the octal rep of cards so this function must check only from oct_val[2] onward
def find_three_of_a_kind(a_hand):
    oct_val = str(a_hand.crunch_octal())
    if "3" in oct_val[2:]:
        return(True)
    else:
        return(False)

def find_four_of_a_kind(a_hand):
    oct_val = str(a_hand.crunch_octal())
    if "4" in oct_val[2:]:
        return(True)
    else:
        return(False)

def find_full_house(a_hand):
    oct_val = str(a_hand.crunch_octal())
    if "2" in oct_val[2:] and "3" in oct_val[2:]:
        return(True)
    else:
        return(False)

def find_flush(a_hand):
    suites = a_hand.returnsuits()
    flush_boole = False
    
    for suite in suites:
        count = 0
        for location in suite:
            if location == "1":
                count += 1
        if count > 4:
            flush_boole = True
    return(flush_boole)

## Test Bench
straight_flush_hand = hand(deck[0:5])
pairhand = hand([deck[0],deck[13]]+deck[20:23])
straight_hand = hand([deck[13]]+deck[1:5])
four_of_a_kind_hand = hand([deck[0],deck[13],deck[26],deck[39],deck[40]])
full_house_hand = hand([deck[0],deck[13],deck[26],deck[1],deck[40]])
flush_hand = hand([deck[0]]+deck[2:6])

this_hand = flush_hand
tester = this_hand.crunch_binary()
print(this_hand)


test = find_flush(this_hand)
print(test)



