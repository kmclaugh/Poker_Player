## This defines the hand class with methods for adding cards to the current hand, reading off the best hand, and others.

import sys
sys.path.append("/Users/kevin/Desktop/10% Time/Poker_Player")
from Deck_Creator import *
the_deck_file_location = "/Users/kevin/Desktop/10% Time/Poker_Player/full_deck.dat"
the_deck_file = open(the_deck_file_location,"rb")
deck = pickle.load(the_deck_file)


class hand():
    
    def __init__(self,the_list,the_value = "Not Assigned",the_best_card1=0, the_best_card2=0, the_kicker=0):
        self.cards = the_list
        self.value = the_value
        self.card1 = the_best_card1
        self.card2 = the_best_card2
        self.kicker = the_kicker
    
    def __str__(self):
        return(self.cards.__str__())
    def __repr__(self):
        return(self.cards.__repr__())
    
    def __add__(self,x):
        new_value = hand((self.cards + [x]),self.value,self.card1,self.card2,self.kicker)
        return(new_value)
    
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

def find_best_hand_dynamic(a_hand,memo):
    oct_val = a_hand.crunch_octal()
    
    if find_straight_flush(a_hand) == True:
        return((8,memo))
    
    elif find_four_of_a_kind(a_hand) == True:
        return((7,memo))
    
    elif find_full_house(a_hand) == True:
        return((6,memo))
    
    elif find_flush(a_hand) == True:
        return((5,memo))

    
    elif oct_val in memo:
        return((memo[oct_val],memo))

    elif find_straight(a_hand) == True:
        memo[oct_val] = 4
        return((4,memo))
    
    elif find_three_of_a_kind(a_hand) == True:
        memo[oct_val] = 3
        return((3,memo))
    
    elif find_two_pair(a_hand) == True:
        memo[oct_val] = 2
        return((2,memo))
    
    elif find_pair(a_hand) == True:
        memo[oct_val] = 1
        return((1,memo))
    
    else:
        memo[oct_val] = 0
        return((0,memo))

class kicker:

    def __init__(self, high_card_of_value_cards_one , sum_of_kicker_cards=0, high_card_of_value_cards_two = 0):
        self.best_card1 = high_card_of_value_cards_one
        self.best_card2 = high_card_of_value_cards_two
        self.kicker_sum = sum_of_kicker_cards

    def __str__(self):
        if self.best_card2 == 0:
            return ("best card: {}, kicker sum: {}".format(self.best_card1, self.kicker_sum))
        else:
            return("best card1: {}, best card2: {}, kicker sum: {}".format(self.best_card1,self.best_card2,self.kicker_sum))

    def __repr__(self):
        if self.best_card2 == 0:
            return ("best card: {}, kicker sum: {}".format(self.best_card1, self.kicker_sum))
        else:
            return("best card1: {}, best card2: {}, kicker sum: {}".format(self.best_card1,self.best_card2,self.kicker_sum))

## Defines the method for finding both the highest card of the cards used to make the value of the hand (ie straight, ace-high), and the sum of the kicker cards for easy comprison should the value of two hands and the highest card both be equal. For example if player both have a pair of twos and one has an ace and the other a king, the kicker sum of the Ace will be higher.
def find_kicker(a_hand,hand_value):
    
    if hand_value == 0: ## High card
        oct_val = str(a_hand.crunch_octal())
        oct_val = oct_val[3:]
        kicker_sum = 0
        for y in range(0,5):
            if oct_val != "0000000000000":
                kicker_sum += 14 - oct_val.index("1")
                oct_val = oct_val.replace("1","0",1)
            else:
                break
        the_best_card1 = 0 
        the_kicker = kicker(the_best_card1,kicker_sum)
        return(the_kicker)
    
    if hand_value == 1: ## pair
        oct_val = str(a_hand.crunch_octal())
        oct_val = oct_val[3:]
        the_best_card1 = 14 - oct_val.index("2")
        oct_val = oct_val.replace("2","0")
        kicker_sum = 0
        for y in range(0,3):
            if oct_val != "0000000000000":
                kicker_sum += 14 - oct_val.index("1")
                oct_val = oct_val.replace("1","0",1)
            else:
                break
        the_kicker = kicker(the_best_card1,kicker_sum)
        return(the_kicker)

    if hand_value == 2: ## two pair
        oct_val = str(a_hand.crunch_octal())
        oct_val = oct_val[3:]
        the_best_card1 = 14 - oct_val.index("2")
        oct_val = oct_val.replace("2","0",1)
        the_best_card2 = 14 - oct_val.index("2")
        kicker_sum = 14 - oct_val.index("1")
        the_kicker = kicker(the_best_card1,kicker_sum,the_best_card2)
        return(the_kicker)

    if hand_value == 3: ## three of a kind
        oct_val = str(a_hand.crunch_octal())
        oct_val = oct_val[3:]
        the_best_card1 = 14 - oct_val.index("3")
        kicker_sum = 0
        for y in range(0,2):
            kicker_sum += 14 - oct_val.index("1")
            oct_val = oct_val.replace("1","0",1)
        the_kicker = kicker(the_best_card1,kicker_sum)
        return(the_kicker)

    if hand_value == 4: ## straight
        oct_val = str(a_hand.crunch_octal())
        oct_val = oct_val[3:].replace("2","1")
        oct_val = oct_val.replace("3","1")
        if oct_val == "1000000001111":
            the_best_card1 = 5
            the_kicker = kicker(the_best_card1)
            return(the_kicker)
        else:
            the_best_card1 = 14 - oct_val.index("1")
            the_kicker = kicker(the_best_card1)
            return(the_kicker)


    if hand_value == 5: ## flush
        suites = a_hand.returnsuits()

        for suite in suites:
            count = 0
            for location in suite:
                if location == "1":
                    count += 1
                if count > 2:
                    the_best_card1 = 14 - suite.index("1")
                    break
        the_kicker = kicker(the_best_card1)
        return(the_kicker)

    if hand_value == 6: ## full house
        oct_val = str(a_hand.crunch_octal())
        oct_val = oct_val[3:]
        the_best_card1 = 14 - oct_val.index("3")
        oct_val = oct_val.replace("3","1",1)
        if "3" in oct_val:
            the_best_card2 = 14 - oct_val.index("3")
        else:
            the_best_card2 = 14 - oct_val.index("2")
        kicker_sum = 0
        the_kicker = kicker(the_best_card1,kicker_sum,the_best_card2)
        return(the_kicker)

    if hand_value == 7: ## four of a kind
        oct_val = str(a_hand.crunch_octal())
        oct_val = oct_val[3:]
        the_best_card1 = 14 - oct_val.index("4")
        kicker_sum = 14 - oct_val.index("1")
        the_kicker = kicker(the_best_card1,kicker_sum)
        return(the_kicker)

    if hand_value == 8: ## straight flush
        suites = a_hand.returnsuits()
        for suite in suites:
            count = 0
            for location in suite:
                if location == "1":
                    count += 1
                if count > 2:
                    if suite == "1000000001111":
                        the_best_card1 = 5
                    else:
                        the_best_card1 = 14 - suite.index("1")
                    break
        the_kicker = kicker(the_best_card1)
        return(the_kicker)

def compare_two_hands(first_hand,second_hand):
    if first_hand.value == "Not Assigned":
        first_hand.value = find_best_hand(first_hand)
        first_kicker = find_kicker(first_hand,first_hand.value)
        first_hand.card1 = first_kicker.best_card1
        first_hand.card2 = first_kicker.best_card2
        first_hand.kicker = first_kicker.kicker_sum
        
        second_hand.value = find_best_hand(second_hand)
        if first_hand.value > second_hand.value:
            return(first_hand)
        elif second_hand.value > second_hand.value:
            return(second_hand)
        else:
            second_kicker = find_kicker(second_hand,second_hand.value)
            second_hand.card1 = second_kicker.best_card1
            if first_hand.card1 > second_hand.card1:
                return(first_hand)
            elif second_hand.card1 > first_hand.card1:
                return(second_hand)
            else:
                second_hand.card2 = second_kicker.best_card2
                if first_hand.card2 > second_hand.card2:
                    return(first_hand)
                elif second_hand.card2 > first_hand.card2:
                    return(second_hand)
                else:
                    second_hand.kicker = second_kicker.kicker_sum
                    if first_hand.kicker > second_hand.kicker:
                        return(first_hand)
                    elif second_hand.kicker > first_hand.kicker:
                        return(second_hand)
                    else:
                        return("Equal")
    elif first_hand.value != "Not Assigned":
        second_hand.value = find_best_hand(second_hand)
        if first_hand.value > second_hand.value:
            return(first_hand)
        elif second_hand.value > second_hand.value:
            return(second_hand)
        else:
            second_kicker = find_kicker(second_hand,second_hand.value)
            second_hand.card1 = second_kicker.best_card1
            if first_hand.card1 > second_hand.card1:
                return(first_hand)
            elif second_hand.card1 > first_hand.card1:
                return(second_hand)
            else:
                second_hand.card2 = second_kicker.best_card2
                if first_hand.card2 > second_hand.card2:
                    return(first_hand)
                elif second_hand.card2 > first_hand.card2:
                    return(second_hand)
                else:
                    second_hand.kicker = second_kicker.kicker_sum
                    if first_hand.kicker > second_hand.kicker:
                        return(first_hand)
                    elif second_hand.kicker > first_hand.kicker:
                        return(second_hand)
                    else:
                        return("Equal")

def compare_two_hands_dynamic(first_hand,second_hand,memo):
    
    if first_hand.value == "Not Assigned":
        dynamic_values = find_best_hand_dynamic(first_hand,memo)
        first_hand.value = dynamic_values[0]
        memo = dynamic_values[1]
        
        dynamic_values = find_best_hand_dynamic(second_hand,memo)
        second_hand.value = dynamic_values[0]
        memo = dynamic_values[1]
        if first_hand.value > second_hand.value:
            return((first_hand,memo))
        elif second_hand.value > second_hand.value:
            return((second_hand,memo))
        else:
            first_kicker = find_kicker(first_hand,first_hand.value)
            first_hand.card1 = first_kicker.best_card1
            first_hand.card2 = first_kicker.best_card2
            first_hand.kicker = first_kicker.kicker_sum
        
            second_kicker = find_kicker(second_hand,second_hand.value)
            second_hand.card1 = second_kicker.best_card1

            if first_hand.card1 > second_hand.card1:
                return((first_hand,memo))
            elif second_hand.card1 > first_hand.card1:
                return((second_hand,memo))
            else:
                second_hand.card2 = second_kicker.best_card2
                if first_hand.card2 > second_hand.card2:
                    return((first_hand,memo))
                elif second_hand.card2 > first_hand.card2:
                    return((second_hand,memo))
                else:
                    second_hand.kicker = second_kicker.kicker_sum
                    if first_hand.kicker > second_hand.kicker:
                        return((first_hand,memo))
                    elif second_hand.kicker > first_hand.kicker:
                        return((second_hand,memo))
                    else:
                        return(("Equal",memo))
    elif first_hand.value != "Not Assigned":
        dynamic_values = find_best_hand_dynamic(second_hand,memo)
        second_hand.value = dynamic_values[0]
        memo = dynamic_values[1]
        if first_hand.value > second_hand.value:
            return((first_hand,memo))
        elif second_hand.value > second_hand.value:
            return((second_hand,memo))
        else:
            second_kicker = find_kicker(second_hand,second_hand.value)
            second_hand.card1 = second_kicker.best_card1
            if first_hand.card1 > second_hand.card1:
                return((first_hand,memo))
            elif second_hand.card1 > first_hand.card1:
                return((second_hand,memo))
            else:
                second_hand.card2 = second_kicker.best_card2
                if first_hand.card2 > second_hand.card2:
                    return((first_hand,memo))
                elif second_hand.card2 > first_hand.card2:
                    return((second_hand,memo))
                else:
                    second_hand.kicker = second_kicker.kicker_sum
                    if first_hand.kicker > second_hand.kicker:
                        return((first_hand,memo))
                    elif second_hand.kicker > first_hand.kicker:
                        return((second_hand,memo))
                    else:
                        return(("Equal",memo))

# Test Bench
#two_card_hand = hand(deck[0:2])
#straight_flush_hand = hand(deck[0:4]+[deck[4]])
#pair_hand = hand([deck[0],deck[13],deck[50]]+deck[20:23])
#straight_hand = hand([deck[13],deck[17]]+deck[1:5])
#straight_hand_ace_low = hand(deck[0:4]+[deck[25]])
#four_of_a_kind_hand = hand([deck[0],deck[13],deck[26],deck[39],deck[40],deck[51]])
#full_house_hand = hand([deck[0],deck[13],deck[26],deck[1],deck[40],deck[14]])
#flush_hand = hand([deck[0],deck[51]]+deck[2:6])
#two_pair_hand = hand([deck[0],deck[13],deck[12],deck[25],deck[1]])
#three_of_a_kind_hand = hand([deck[0],deck[13],deck[39]]+deck[20:23])
#high_card_hand = hand([deck[0],deck[1],deck[37]]+deck[20:23])

#this_hand = high_card_hand
#memo = {}
#value_test = find_best_hand_dynamic(this_hand,memo)
#print(this_hand)
#print(value_test)
#print(memo)
#
#this_hand = this_hand +deck[14]
#
#print(this_hand)
#value_test = find_best_hand_dynamic(this_hand,memo)
#print(value_test)
#print(memo)
#
#test = find_kicker(this_hand,value_test)
#print(test)


#first_hand = pair_hand
#print(("first hand: ",first_hand))
#second_hand = high_card_hand
#print(("second hand: ",second_hand))
#
#memo = {}
#test = compare_two_hands_dynamic(first_hand,second_hand,memo)
#print(test)




