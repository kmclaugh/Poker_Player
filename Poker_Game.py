import sys
sys.path.append("/Users/kevin/Desktop/10% Time/Poker_Player")
from Deck_Creator import *
from Hand_Class import *
from random import shuffle
from Player_Class import *

## Deals cards to a given list of players at random from the deck
def deal_cards_to_players(players):
    ## Load the deck from the pickle file
    deck = load_deck()
    shuffle(deck)
    players_with_hands = []
    counter = 0

    for player in players:
        player_hand = hand(deck[counter:counter+2])
        player.hand = player_hand
        players_with_hands.append(player)
        counter += 2
    
    current_deck = deck[counter:]
    return((players_with_hands,current_deck))

def deal_TEST_cards_to_players(players):
    ## Load the deck from the pickle file
    deck = load_deck()
    players_with_hands = []
    counter = 0
    ## Test hands go here
    test_hand1 = hand(deck[0:2])
    used_cards = test_hand1.cards
    test_hand2 = hand(deck[0:2])
    used_cards = used_cards + test_hand2.cards
    test_hand3 = hand([deck[0],deck[25]])
    used_cards = used_cards + test_hand3.cards
    test_hand4 = hand([deck[0],deck[25]])
    used_cards = used_cards + test_hand4.cards
    test_hand5 = hand([deck[1],deck[30]])
    used_cards = used_cards + test_hand5.cards
    test_hand6 = hand(deck[0:2])
    used_cards = used_cards + test_hand6.cards
    test_hand7 = hand(deck[0:2])
    used_cards = used_cards + test_hand7.cards
    test_hands = [test_hand1,test_hand2,
                  test_hand3,test_hand4,test_hand5,test_hand6,test_hand7]
    
    for player in players:
        player.hand = test_hands[counter]
        players_with_hands.append(player)
        counter += 1
    
    current_deck = [deck[18],deck[3],deck[37],deck[7],deck[9]] ##test community cards
    return((players_with_hands,current_deck))

## deals out a given number of community cards and returns the cards and current deck
def deal_community_cards(number_of_cards_to_be_dealt,current_deck):
    community_cards = current_deck[0:number_of_cards_to_be_dealt] ##the new community cards
    current_deck = current_deck[number_of_cards_to_be_dealt:]
    return([community_cards,current_deck])

## Reset player.current_bet for all players in a given list
def reset_player_current_bet(players_left):
    for player in players_left:
        player.current_bet = 0
    return(players_left)

## Awards a pot to a winning player or a list of winning players.
def award_pot(winning_player,pot,print_winner=False):
    if type(winning_player) != list:
        winning_player.money = winning_player.money + pot
        if print_winner == True:
            print("{} has won {} with {}".format(winning_player.name,pot,winning_player.hand))
            print("")
        return(winning_player)
    else:
        pot_split = pot/len(winning_player)
        print_string = ""
        for a_player in winning_player:
            a_player.money = a_player.money + pot_split
            print_string = print_string +"{} ".format(a_player.name)
        if print_winner == True:
            print_string = print_string +"have split the pot. They each won {}.".format(pot_split)
            print(print_string)
            print("")
        return(winning_player)

## Adds the winning player, with updated money back into the player list. Also reset all single deal values for all players
def add_hand_winner_back_to_player_list(winning_player,player_list):
    if type(winning_player) != list:
        for a_player in player_list:
            a_player.current_bet = 0
            a_player.owes = 0
            a_player.hand = None
            if a_player.name == winning_player.name:
                player_list.remove(a_player)
                player_list.append(winning_player)
                return(player_list)
    else:
        for a_player in player_list:
            a_player.current_bet = 0
            a_player.owes = 0
            a_player.hand = None
            for a_winner in winning_player:
                if a_player.name == a_winner.name:
                    player_list.remove(a_player)
                    player_list.append(a_winner)
        return(player_list)

## defines the sequence of events for raising, folding and calling.
def action_logic(players_left,community_cards,pot,raise_amount,raise_cap,print_action = False,print_cards=False):
    current_bet = 0
    number_of_raises = 0
    remove_list = []
    for player in players_left:
        if len(players_left)-len(remove_list) != 1:
            player.owes = current_bet - player.current_bet
            decision = player.strategy(community_cards=community_cards, pot=pot, the_current_bet=current_bet, number_of_players_left=len(players_left))
            if decision == "fold":
                remove_list.append(player)
                player.owes = 0
                action = "{} folds with {}".format(player.name,player.hand)
            
            elif decision == "raise" and number_of_raises < raise_cap:
                ## update player info
                player_raise = raise_amount + player.owes
                player.money = player.money - player_raise
                player.current_bet = player.current_bet + player_raise
                player.owes = 0
                
                ## update cummunity info
                current_bet += raise_amount
                pot += player_raise
                number_of_raises += 1
                
                action = "{} raises with {}. Pot equals {}".format(player.name,player.hand,pot)
                pots_right = False
            
            else: ##decision == "call" or (decision == "raise" and number_of_raises == raise_cap)
                pot += player.owes
                player.money = player.money - player.owes
                player.current_bet = player.owes
                if player.owes == 0:
                    action = "{} checks with {}. Pot equals {}".format(player.name,player.hand, pot)
                else:
                    action = "{} calls with {}. Pot equals {}".format(player.name,player.hand, pot)
                player.owes = 0
                
                pots_right = True
            if print_action == True:
                print(action)
        else:
            for a_folder in remove_list:
                players_left.remove(a_folder)
            return([players_left,pot])

    for a_folder in remove_list:
        players_left.remove(a_folder)
    remove_list = []
                
    pots_right = False
    while pots_right == False:
        pots_right = True
        for player in players_left:
            if len(players_left)-len(remove_list) != 1:
                player.owes = current_bet - player.current_bet
                if player.owes != 0:
                    decision = player.strategy(community_cards=community_cards, pot=pot, the_current_bet=current_bet, number_of_players_left=len(players_left))
                    if decision == "fold":
                        remove_list.append(player)
                        player.owes = 0
                        action = "{} folds with {}".format(player.name,player.hand)
                    
                    elif decision == "raise" and number_of_raises < raise_cap:
                        ## update player info
                        player_raise = raise_amount + player.owes
                        player.money = player.money - player_raise
                        player.current_bet = player.current_bet + player_raise
                        player.owes = 0
                        
                        ## update cummunity info
                        current_bet += raise_amount
                        pot += player_raise
                        number_of_raises += 1
                        
                        action = "{} raises with {}. Pot equals {}".format(player.name,player.hand,pot)
                        pots_right = False
                    
                    else: ##decision == "call" or (decision == "raise" and number_of_raises == raise_cap)
                        pot += player.owes
                        player.money = player.money - player.owes
                        player.current_bet = player.owes
                        if player.owes == 0:
                            action = "{} checks with {}. Pot equals {}".format(player.name,player.hand, pot)
                        else:
                            action = "{} calls with {}. Pot equals {}".format(player.name,player.hand, pot)
                        player.owes = 0
                        pots_right = True
                
                    if print_action == True:
                        print(action)
            else:
                for a_folder in remove_list:
                    players_left.remove(a_folder)
                return([players_left,pot])

        for a_folder in remove_list:
            players_left.remove(a_folder)
        remove_list = []
            
    return([players_left,pot])

## Adds the community cards to each player's hand.
def add_community_cards_to_all_players(a_list_of_players,the_community_cards):
    for a_player in a_list_of_players:
        a_player.hand.add_community_cards(the_community_cards)
    return(a_list_of_players)

## Compares a list of players with hands without assigned values and returns the winner
def compare_multiple_player_hands(a_list_of_players):
    for a_player in a_list_of_players:
        a_player.hand = assign_all_hand_values(a_player.hand)
    a_list_of_players = sorted(a_list_of_players, key=lambda player: player.hand.value,reverse=True)
    best_value = a_list_of_players[0].hand.value
    best_value_players = []
    for a_player in a_list_of_players:
        if a_player.hand.value == best_value:
            best_value_players.append(a_player)
    if len(best_value_players) == 1:
        winner = best_value_players[0]
    else:
        a_list_of_players = sorted(a_list_of_players, key=lambda player: player.hand.card_order,reverse=True)
        the_best_card_order = a_list_of_players[0].hand.card_order
        winning_player = []
        for a_player in a_list_of_players:
            if a_player.hand.card_order == the_best_card_order:
                winning_player.append(a_player)
        if len(winning_player) == 1:
            winner = winning_player[0]
        else:
            winner = winning_player
    return(winner)

## defines the event for a single deal of cards. ie from the dealing of cards through showdown, if necessary. Awards the winner the pot and returns the list of players with the 
def single_deal(player_list,print_action=False,print_cards=False,print_winner=False):
    pots_right = True
    players_left = player_list
    raise_amount = 1
    raise_cap = 3
    
    ## Deal the cards and return the deck without the dealt cards
    deal_cards_result = deal_cards_to_players(players_left)
    players_left = deal_cards_result[0]
    current_deck = deal_cards_result[1]
    
    ##preflop
    if print_action == True:
        print("")
        print("preflop:")
    community_cards =[]
    pot=0
    preflop_results = action_logic(community_cards=community_cards, raise_amount=raise_amount, raise_cap=raise_cap, pot=pot, players_left=players_left, print_action=print_action, print_cards=print_cards)
    
    ##setup for flop
    players_left = preflop_results[0]
    pot = preflop_results[1]
    if len(players_left) == 1:
        winning_player = award_pot(players_left[0],pot=pot,print_winner=print_winner)
        player_list = add_hand_winner_back_to_player_list(winning_player,player_list)
        return(player_list)
    
    players_left = reset_player_current_bet(players_left)


    deal_community_cards_result = deal_community_cards(3,current_deck)
    community_cards = deal_community_cards_result[0] #the flop cards
    current_deck = deal_community_cards_result[1]
    
    ##flop
    if print_action == True:
        print("")
        print("flop:")
    flop_results = action_logic(community_cards=community_cards, raise_amount=raise_amount, raise_cap=raise_cap, pot=pot, players_left=players_left, print_action=print_action, print_cards=print_cards)

    ##setup for turn
    players_left = flop_results[0]
    pot = flop_results[1]
    if len(players_left) == 1:
        winning_player = award_pot(players_left[0],pot=pot,print_winner=print_winner)
        player_list = add_hand_winner_back_to_player_list(winning_player,player_list)
        return(player_list)

    players_left = reset_player_current_bet(players_left)

    
    deal_community_cards_result = deal_community_cards(1,current_deck)
    community_cards = community_cards + deal_community_cards_result[0] # turn card
    current_deck = deal_community_cards_result[1]
    
    ##turn
    if print_action == True:
        print("")
        print("turn:")
    turn_results = action_logic(community_cards=community_cards, raise_amount=raise_amount, raise_cap=raise_cap, pot=pot, players_left=players_left, print_action=print_action, print_cards=print_cards)

    ##setup for river
    players_left = turn_results[0]
    pot = turn_results[1]
    if len(players_left) == 1:
        winning_player = award_pot(players_left[0],pot=pot,print_winner=print_winner)
        player_list = add_hand_winner_back_to_player_list(winning_player,player_list)
        return(player_list)
    players_left = reset_player_current_bet(players_left)

    
    deal_community_cards_result = deal_community_cards(1,current_deck)
    community_cards = community_cards + deal_community_cards_result[0] #the river card
    current_deck = deal_community_cards_result[1]
    
    ##river
    if print_action == True:
        print("")
        print("river:")
    river_results = action_logic(community_cards=community_cards, raise_amount=raise_amount, raise_cap=raise_cap, pot=pot, players_left=players_left, print_action=print_action, print_cards=print_cards)
    
    players_left = river_results[0]
    pot = river_results[1]
    if len(players_left) == 1:
        winning_player = award_pot(players_left[0],pot=pot,print_winner=print_winner)
        player_list = add_hand_winner_back_to_player_list(winning_player,player_list)
        return(player_list)



    ##showdown
    players_left = add_community_cards_to_all_players(players_left,community_cards)
    if print_action == True:
        print("")
        print("showdown")
        for a_player in players_left:
            print("{} has {}".format(a_player.name,a_player.hand))
        print("")
    winning_player = compare_multiple_player_hands(players_left)
    winning_player = award_pot(winning_player,pot=pot,print_winner=print_winner)
    player_list = add_hand_winner_back_to_player_list(winning_player,player_list)

    return(player_list)


## Test Here
def always_call(hand,community_cards,pot,the_current_bet,player_current_bet,owes,number_of_players_left):
    return("call")

def always_raise(hand,community_cards,pot,the_current_bet,player_current_bet,owes,number_of_players_left):
    return("raise")

def always_fold(hand,community_cards,pot,the_current_bet,player_current_bet,owes,number_of_players_left):
    return("fold")

def random_decision(hand,community_cards,pot,the_current_bet,player_current_bet,owes,number_of_players_left):
    if owes == 0:
        options = ["call","raise"]
        shuffle(options)
        return(options[0])
    else:
        options = ["fold","call","raise"]
        shuffle(options)
        return(options[0])

always_raise_player1 = player(name="always_raiser1",the_strategy=always_raise,money=10)
always_raise_player2 = player(name="always_raiser2",the_strategy=always_raise,money=10)
always_call_player = player(name="always_caller",the_strategy=always_call,money=10)
always_fold_player = player(name="always_folder1",the_strategy=always_fold,money=10)
always_fold_player2 = player(name="always_folder2",the_strategy=always_fold,money=10)
always_players = [always_fold_player,always_fold_player2,always_raise_player1, always_raise_player2,always_call_player]

random1 = player(name="random1",the_strategy=random_decision,money=10)
random2 = player(name="random2",the_strategy=random_decision,money=10)
random3 = player(name="random3",the_strategy=random_decision,money=10)
random4 = player(name="random4",the_strategy=random_decision,money=10)
random_players = [random1,random2,random3,random4]

player_list = single_deal(random_players,print_winner=True,print_action=True)
print(player_list)
for a_player in player_list:
    print((a_player.name,a_player.money))



