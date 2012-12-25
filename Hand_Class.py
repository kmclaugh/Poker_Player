## This defines the hand class with methods for adding cards to the current hand, reading off the best hand, and others.

import sys
sys.path.append("/Users/kevin/Desktop/10% Time/Poker_Player")
from Deck_Creator import *
the_deck_file_location = "/Users/kevin/Desktop/10% Time/Poker_Player/full_deck.dat"
the_deck_file = open(the_deck_file_location,"rb")
deck = pickle.load(the_deck_file)


class hand():
    
    def __init__(self,the_list,the_value = "Not Assigned",the_card_order = []):
        self.cards = the_list
        self.value = the_value
        self.card_order = the_card_order
    
    def __str__(self):
        return(self.cards.__str__())
    def __repr__(self):
        return(self.cards.__repr__())
    
    def __add__(self,x):
        new_value = hand((self.cards + [x]),self.value,self.card_order)
        return(new_value)
    
    def add_community_cards(self,the_community_cards):
        for a_card in the_community_cards:
            self.cards = self.cards + [a_card]
        return(self)

    
    def __len__(self):
        return(len(self.cards))
    
    def crunch_binary(self):
        bin_sum = self.cards[0].binary
        for n in self.cards[1:]:
            bin_sum = bin_sum + n.binary
        return(bin_sum)

    def crunch_octal(self):
        oct_sum = self.cards[0].octal
        for n in self.cards[1:]:
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
    oct_val = str(a_hand.crunch_octal()).replace("2","1")
    oct_val = oct_val.replace("3","1")
    if "11111" in oct_val:
        return(True)
    elif "11o1000000001111" == oct_val:
        return(True)
    else:
        return(False)

def find_straight_flush(a_hand):
    suites = a_hand.returnsuits()
    straight_flush_boole = False
    for y in suites:
        if "11111" in y:
            straight_flush_boole = True
        if "1000000001111" == y:
            straight_flush_boole = True
    return(straight_flush_boole)

## Note that 3 is in the string "13o0000000000" for the octal rep of cards so this function must check only from oct_val[2] onward
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
    oct_val = str(a_hand.crunch_octal())[2:]
    if "3" in oct_val:
        if "2" in oct_val:
            return(True)
        else: ##if there's at least one three but not a two
            oct_val = oct_val.replace("3","1",1)
            if "3" in oct_val: ##if there are two threes
                return(True)
            else: ##if there isn't a second three
                return(False)
    else: ##if no 3
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

def find_two_pair(a_hand):
    oct_val = str(a_hand.crunch_octal())
    count = 0
    for y in oct_val:
        if y == "2":
            count += 1
    if count > 1:
        return(True)
    else:
        return(False)

def find_best_hand(a_hand):
    
    if find_straight_flush(a_hand) == True:
        return(8)
    
    elif find_four_of_a_kind(a_hand) == True:
        return(7)

    elif find_full_house(a_hand) == True:
        return(6)

    elif find_flush(a_hand) == True:
        return(5)


    elif find_straight(a_hand) == True:
        return(4)
        

    elif find_three_of_a_kind(a_hand) == True:
        return(3)

    elif find_two_pair(a_hand) == True:
        return(2)

    elif find_pair(a_hand) == True:
        return(1)

    else:
        return(0)



## Defines the method for finding both the highest card of the cards used to make the value of the hand (ie straight, ace-high), and the sum of the kicker cards for easy comprison should the value of two hands and the highest card both be equal. For example if player both have a pair of twos and one has an ace and the other a king, the kicker sum of the Ace will be higher.
def find_card_order(a_hand,hand_value):

    if hand_value == 0: ## High card
        oct_val = str(a_hand.crunch_octal())
        oct_val = oct_val[3:]
        card_order = []
        counter = 0
        while oct_val != "0000000000000" and counter < 5:
            this_card = 14 - oct_val.index("1")
            card_order.append(this_card)
            oct_val = oct_val.replace("1","0",1)
            counter += 1
        return(card_order)
    
    if hand_value == 1: ## pair
        oct_val = str(a_hand.crunch_octal())
        oct_val = oct_val[3:]
        the_pair_card = 14 - oct_val.index("2")
        oct_val = oct_val.replace("2","0")
        card_order = [the_pair_card]
        counter = 0
        while oct_val != "0000000000000" and counter <3:
            this_card = 14 - oct_val.index("1")
            card_order.append(this_card)
            oct_val = oct_val.replace("1","0",1)
            counter += 1
        return(card_order)

    if hand_value == 2: ## two pair
        oct_val = str(a_hand.crunch_octal())
        oct_val = oct_val[3:]
        pair_card1 = 14 - oct_val.index("2")
        oct_val = oct_val.replace("2","0",1)
        pair_card2 = 14 - oct_val.index("2")
        kicker_card = 14 - oct_val.index("1")
        card_order = [pair_card1,pair_card2,kicker_card]
        return(card_order)

    if hand_value == 3: ## three of a kind
        oct_val = str(a_hand.crunch_octal())
        oct_val = oct_val[3:]
        three_card = 14 - oct_val.index("3")
        kicker_card1 = 14 - oct_val.index("1")
        oct_val = oct_val.replace("1","0",1)
        kicker_card2 = 14 - oct_val.index("1")
        card_order = [three_card,kicker_card1,kicker_card2]
        return(card_order)

    if hand_value == 4: ## straight
        oct_val = str(a_hand.crunch_octal())
        oct_val = oct_val[3:].replace("2","1")
        oct_val = oct_val.replace("3","1")
        if oct_val == "1000000001111":
            card_order = [5]
            return(card_order)
        else:
            high_card = 14-oct_val.index("11111")
            card_order = [high_card]
            return(card_order)


    if hand_value == 5: ## flush
        suites = a_hand.returnsuits()
        for suite in suites:
            count = 0
            for location in suite:
                if location == "1":
                    count += 1
                if count > 2:
                    card_order = []
                    for y in range(0,5):
                        a_card = 14 - suite.index("1")
                        card_order.append(a_card)
                        suite  = suite.replace("1","0",1)
                    break
        return(card_order)

    if hand_value == 6: ## full house
        oct_val = str(a_hand.crunch_octal())
        oct_val = oct_val[3:]
        three_card = 14 - oct_val.index("3")
        oct_val = oct_val.replace("3","1",1)
        if "3" in oct_val:
            pair_card = 14 - oct_val.index("3")
        else:
            pair_card = 14 - oct_val.index("2")
        card_order = [three_card,pair_card]
        return(card_order)

    if hand_value == 7: ## four of a kind
#        print(a_hand)
        oct_val = str(a_hand.crunch_octal())
        oct_val = oct_val[3:]
#        print(oct_val)
        four_card = 14 - oct_val.index("4")
        oct_val = oct_val.replace("2","1")
        oct_val = oct_val.replace("3","1")
        kicker_card = kicker_card = 14 - oct_val.index("1")
        card_order = [four_card,kicker_card]

    if hand_value == 8: ## straight flush
        suites = a_hand.returnsuits()
        for suite in suites:
            count = 0
            for location in suite:
                if location == "1":
                    count += 1
                if count > 2:
                    if suite == "1000000001111":
                        high_card = 5
                        card_order = [high_card]
                        return(card_order)
                    else:
                        high_card = 14-suite.index("11111")
                        card_order = [high_card]
                        return(card_order)

def assign_all_hand_values(a_hand):
    a_hand.value = find_best_hand(a_hand)
    a_hand.card_order = find_card_order(a_hand,a_hand.value)
    return(a_hand)

def compare_two_card_orders(hand1, hand2):
    for card1, card2 in zip(hand1.card_order,hand2.card_order):
        if card1 > card2:
            return(hand1)
        elif card2 > card1:
            return(hand2)
    return("tie")

def compare_two_hands(first_hand,second_hand):
    first_hand.value = find_best_hand(first_hand)
    second_hand.value = find_best_hand(second_hand)
    if first_hand.value > second_hand.value:
        return(first_hand)
    elif second_hand.value > first_hand.value:
        return(second_hand)
    else:
        first_hand.card_order = find_card_order(first_hand,first_hand.value)
        second_hand.card_order = find_card_order(second_hand,second_hand.value)
        winner = compare_two_card_orders(first_hand,second_hand)
        return(winner)




# Test Bench
#two_card_hand = hand(deck[0:2])
#straight_flush_hand = hand(deck[0:4]+[deck[4],deck[5],deck[20]])
#pair_hand = hand([deck[0],deck[13],deck[50]]+deck[20:23])
#pair_hand2 = hand([deck[0],deck[13],deck[51]]+deck[20:23])
#straight_hand = hand([deck[13],deck[25],deck[17]]+deck[1:5])
#straight_hand_ace_low = hand(deck[0:4]+[deck[25]])
#four_of_a_kind_hand = hand([deck[0],deck[13],deck[26],deck[39],deck[40],deck[51]])
#full_house_hand = hand([deck[0],deck[13],deck[26],deck[1],deck[40],deck[14],deck[20]])
#flush_hand = hand([deck[0],deck[12]]+deck[2:6])
#two_pair_hand = hand([deck[0],deck[13],deck[12],deck[25],deck[1],deck[30]])
#three_of_a_kind_hand = hand([deck[0],deck[13],deck[39]]+deck[20:23])
#high_card_hand = hand([deck[0],deck[1],deck[37],deck[2],deck[3],deck[18],deck[21]])
##



#first_hand = straight_flush_hand
#print(first_hand)
#first_hand.value = find_best_hand(this_hand)
#print(first_hand.value)
#
#
#first_hand.card_order = find_card_order(this_hand,value_test)
#print(first_hand.card_order)


#first_hand = pair_hand
#print(("first hand: ",first_hand))
#second_hand = pair_hand2
#print(("second hand: ",second_hand))
#
#test = compare_two_hands(first_hand,second_hand)
#print(test)




