
## A somewhat messy player class that's most curcial part is the player strategy. Player stratey is created by the_strategy and called by player.strategy. Also note player_current_bet is what the player has bet and the_current_bet is what the table current bet is. Note that the player class wiil throw up an error if the strategy function does not take all the necessary arguements even if the strategy function doesn't use those arguements.

class player:
    def __init__(self,name,the_strategy,hand=None,money=0,player_current_bet=0,owes=0):
        self.name = name
        self.hand = hand
        self.money = money
        self.player_strategy = the_strategy
        self.current_bet = player_current_bet
        self.owes = owes
    
    def strategy(self,the_hand_info,number_of_players_left):
        result = self.player_strategy(the_hand_info=the_hand_info, hand=self.hand, player_current_bet = self.current_bet, owes = self.owes,number_of_players_left=number_of_players_left)
        return(result)
    
    def __str__(self):
        return(self.name)
    def __repr__(self):
        return(self.name)
    def print_all_info(self):
        print("{},{}, money: {}, current bet: {}, owes: {}".format(self.name,self.hand,self.money,self.current_bet,self.owes))



## Here is an template to use for new class strategies
#def base_strategy_function(hand,community_cards,pot,the_current_bet,player_current_bet,owes,number_of_players_left):

##Test starts here
#def test_strategy(hand,community_cards,pot,the_current_bet,player_current_bet,owes,number_of_players_left):
#    print(player_current_bet)
#    print(the_current_bet)
#    if the_current_bet == player_current_bet:
#        return("raise")
#    else:
#        return("fold")
#
#
#always_raise_player1 = player(name="always_raiser1",the_strategy=always_raise,money=10)
#always_raise_player1.current_bet = 1
#test = always_raise_player1.strategy(pot=0,community_cards=[],the_current_bet=1,number_of_players_left=1)
#print(test)


