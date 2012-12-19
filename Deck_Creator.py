##Creates a deck of cards where each card has three representations: a string representation, and octal representation, and a binary representation. The reasons for each representation are discussed in the project notes file.

from math import *
import pickle
## Defines a class to represent a 52 bit binary number. Overloads addition with anohter number such that it returns the but52binary class. The only difference between this class and an int is that its string rep has all 52 binary digits to make scanning the string is simple and easy. Note that to do a getitem method was added that gets the item as if the object were a string.
class binary52bit(int):
    
    def __init__(self, value):
        self.v = value

    def __str__(self):
        binary_rep = bin(self)
        length = len(binary_rep)
        zeros_needed = 52-(length - 2)
        zeros_string = "0"*zeros_needed
        binary_rep = "52b"+zeros_string+binary_rep[2:]
        return (binary_rep)
    
    def __repr__(self):
        binary_rep = bin(self)
        length = len(binary_rep)
        zeros_needed = 52-(length - 2)
        zeros_string = "0"*zeros_needed
        binary_rep = "52b"+zeros_string+binary_rep[2:]
        return (binary_rep)

    def __add__(self,x):
        new_value = self.v+x
        new_value = binary52bit(new_value)
        return(new_value)

    def __sub__(self,x):
        new_value = self.v-x
        new_value = binary52bit(new_value)
        return(new_value)

    def __getitem__(self, k):
        string_rep = str(self)
        return(string_rep[k])

## Uses the same functions as the 52 bit binary but only represents the face of the card. Thus every card in the deck does not have a unique octal13bit represention. This is only used for hands were suits don't matter
class octal13bit(int):

    def __init__(self, value):
        self.v = value

    def __str__(self):
        octal_rep = oct(self)
        length = len(octal_rep)
        zeros_needed = 13-(length - 2)
        zeros_string = "0"*zeros_needed
        octal_rep = "13o"+zeros_string+octal_rep[2:]
        return (octal_rep)
    
    def __repr__(self):
        octal_rep = oct(self)
        length = len(octal_rep)
        zeros_needed = 13-(length - 2)
        zeros_string = "0"*zeros_needed
        octal_rep = "13o"+zeros_string+octal_rep[2:]
        return (octal_rep)

    def __add__(self,x):
        new_value = self.v+x
        new_value = octal13bit(new_value)
        return(new_value)
        
    def __sub__(self,x):
        new_value = self.v-x
        new_value = octal13bit(new_value)
        return(new_value)
    
    def __getitem__(self, k):
        string_rep = str(self)
        return(string_rep[k])

## This is the string representaion. displays as a suit and face
class string_card:
    def __init__(self, f, s):
        self.face = f
        self.suite = s
    
    def __repr__(self):
        return "|%s, %s|" % (self.face, self.suite)
    
    def __str__(self):
        return "|%s, %s|" % (self.face, self.suite)



##This is the full card class containing all reps of the card. Default string rep is the string_rep. Adds methods for binary and octal addition with another full card class
class full_card:
    
    def __init__(self, binary_rep, octal_rep, string_rep):
        self.binary = binary_rep
        self.octal = octal_rep
        self.string = string_rep

    def __str__(self):
        return("{}".format(self.string))
    
    def __repr__(self):
        return("{}".format(self.string))
    
    def octal_add(self,x):
        new_value = self.octal + x.octal
        return(new_value)

    def binary_add(self,x):
        new_value = self.binary + x.binary
        return(new_value)

## make a list of the necessary int values for all cards to be repped in binary
def binary_numbers_cards():
    bin_numbers = []
    for n in range(0,52):
        bin_val = int(pow(2,n))
        val = binary52bit(bin_val)
        bin_numbers.append(val)
    return(bin_numbers)


def bin_numbers_with_suits():
    suites = []
    for n in range(0,13):
        suite = "Clubs"
        face = n+2
        string_rep = string_card(face,suite)
        suites.append(string_rep)
    
    face =2
    for n in range(0,13):
        suite = "Diamonds"
        string_rep = string_card(face,suite)
        suites.append(string_rep)
        face += 1

    face =2
    for n in range(0,13):
        suite = "Hearts"
        string_rep = string_card(face,suite)
        suites.append(string_rep)
        face += 1
    face =2
    for n in range(0,13):
        suite = "Spades"
        string_rep = string_card(face,suite)
        suites.append(string_rep)
        face += 1

    return(suites)


def create_octals():
    oct_nums = []
    for iter in range(0,4):
        for n in range(0,13):
            number = pow(8,n)
            oct_rep = octal13bit(number)
            oct_nums.append(oct_rep)
    return(oct_nums)


def make_deck(binary_cards,string_cards,octal_cards):
    deck = []
    for n in range(0,52):
        bin_val = binary_cards[n]
        string_val = string_cards[n]
        octal_val = octal_cards[n]
        the_card = full_card(bin_val,octal_val,string_val)
        deck.append(the_card)
    return(deck)

## Defines a method for retrieving the deck from the pickled file.
def load_deck():
    deck_file_location = "/Users/kevin/Desktop/10% Time/Poker_Player/full_deck.dat"
    deck_file = open(deck_file_location,"rb")
    deck = pickle.load(deck_file)
    deck_file.close()
    return(deck)


def remove_card_from_deck(deck,card):
    new_deck = []
    
    for a_card in deck:
        if a_card.binary != card.binary:
            new_deck.append(a_card)
    return(new_deck)

#cards_bin = binary_numbers_cards()
#cards_suit = bin_numbers_with_suits()
#cards_octals = create_octals()
#
#deck = make_deck(cards_bin,cards_suit,cards_octals)
#deck_file_location = "/Users/kevin/Desktop/10% Time/Poker_Player/full_deck.dat"
#deck_file = open(deck_file_location,"wb")
#pickle.dump(deck,deck_file)
#deck_file.close()





