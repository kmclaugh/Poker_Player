import pickle
import sys
sys.path.append("/Users/kevin/Desktop/10% Time/Poker_Player")
from Deck_Creator import *

## Load the deck from the pickle file
deck_file_location = "/Users/kevin/Desktop/10% Time/Poker_Player/full_deck.dat"
deck_file = open(deck_file_location,"rb")
deck = pickle.load(deck_file)
for y in deck:
    print(y.octal)

