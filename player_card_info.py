from random import choice

cards_set_list = {'A': -1, '2': -1, '3': -1, '4': -1, '5': -1, '6': -1, '7': -1,
                  '8': -1, '9': -1, '10': -1, 'J': -1, 'Q': -1, 'K': -1}

players_dict = {}
players_names = []


class Player(object):
    player_status = True
    def __init__(self, name):
        self.name = name
        self.cards_info = {'A': 0, '2': 0, '3': 0, '4': 0, '5': 0, '6': 0, '7': 0,
                           '8': 0, '9': 0, '10': 0, 'J': 0, 'Q': 0, 'K': 0}

    def print_player_cards_info(self):
        print ('Player %s Card Details' % self.name)
        for card_name in self.cards_info.keys():
            print (card_name, self.cards_info[card_name],';',)
        print

    def card_count(self):
        print (sum(self.cards_info.values()))

    def check_and_set_status(self):
        if len([x for x in self.cards_info.values() if x != 0 and x != 4]) == 0:
            self.player_status = False
        return self.player_status

class AI_Player(Player):

    def __init__(self,name):
        super(AI_Player,self).__init__(name)

    def request_generator(self):
        # generating a player number to ask a card from who is not AI player itself and who is alive
        player_name = choice([x.name for x in players_dict.values() if x.name != self.name and x.player_status])
        # selection of a card, we need to make sure that computer does  have this card, n
        # and the card is not the finished set
        # you cannot access the card info of other player
        card_name = choice([x for x in players_dict[player_name].cards_info.keys()
                            if (cards_set_list[x] == -1) & (self.cards_info[x] > 0)])
       #   break ( OLD CODE see if it makese sense)
        return player_name + ' ' + card_name + ' ' + str(1)


class Super_AI_Player(AI_Player):

    #opponents_cards_info = {}

    def __init__(self,name):
        super(Super_AI_Player,self).__init__(name)
        self.opponents_cards_info = {}

    def initialize(self):
        for player in players_dict.values():
            if self.name != player.name:
                self.opponents_cards_info[player.name] = {'A': 0, '2': 0, '3': 0, '4': 0, '5': 0, '6': 0, '7': 0,
                                                      '8': 0, '9': 0, '10': 0, 'J': 0, 'Q': 0, 'K': 0}

    def print_opponents_card_info(self):
        print ("Super AI Name:%s"%self.name)
        for player_name in self.opponents_cards_info.keys():
            print ('Player %s Card Details' % player_name)
            for card_name in self.opponents_cards_info[player_name].keys():
                print (card_name, self.opponents_cards_info[player_name][card_name], ';')
            

    # once a set has been made in the database, other players cards must be set to zero
    def clear_opponent_card_to_zero(self, card_name, player_name):
        for player in self.opponents_cards_info.keys():
            if player != player_name:
                self.opponents_cards_info[player][card_name] = 0

    def request_processor(self, current_player, player_requested, card_requested, no_of_cards_requested, is_success):
        # need to add functionality such that a request without a card, which fails is processed correctly

        if is_success: # request was successful
            # Super AI didnt make the request
            if self.name != current_player:
                # check if the player database already has cards, if not increment by 1 more else no
                if self.opponents_cards_info[current_player][card_requested] == 0:
                    self.opponents_cards_info[current_player][card_requested] += no_of_cards_requested + 1
                else:
                    self.opponents_cards_info[current_player][card_requested] += no_of_cards_requested
                if self.name != player_requested:
                    if self.opponents_cards_info[player_requested][card_requested] >= no_of_cards_requested:
                        self.opponents_cards_info[player_requested][card_requested] -= no_of_cards_requested
                if self.opponents_cards_info[current_player][card_requested] == 4:
                    self.clear_opponent_card_to_zero(card_requested, current_player)
            # Super AI made the request
            else:
                if self.opponents_cards_info[player_requested][card_requested] >= no_of_cards_requested:
                    self.opponents_cards_info[player_requested][card_requested] -= no_of_cards_requested


        else: # a request was made and they failed

            # Super AI was not involved in the request
            #if self.name != current_player or self.name != player_requested:
             #   self.opponents_cards_info[current_player][card_requested] = no_of_cards_requested + 1
                # this ensures that Super AI database is correct, if more than 1 card was stored
                # MORE THOUGHT ON FAILURE SCENARIO IS REQUIRED
                #if self.opponents_cards_info[player_requested][card_requested] >= no_of_cards_requested:
                #    self.opponents_cards_info[player_requested][card_requested] = -1
            # Super AI made the request, this can happen if the database is not maintained properly
            if self.name == current_player:
                # card count of that player is reset
                if no_of_cards_requested == 1:
                    self.opponents_cards_info[player_requested][card_requested] = -1
            #else: # someone requested Super AI and failed, assuming they have atleast 1 card
             #   if self.opponents_cards_info[current_player][card_requested] <= 0:
         #           self.opponents_cards_info[current_player][card_requested] = 1



    def request_generator(self):
        player_name =''
        card_name = ''
        # generating a player number to ask a card from
        # only cards that are present with Super AI
        valid_cards = [x for x in self.cards_info.keys() if self.cards_info[x] not in [0,4]]
        #print "valid cards that player has are ", valid_cards
        # choose players that have cards present with Super AI
        for card in valid_cards:
            possible_players = [x for x in self.opponents_cards_info.keys()
                                if self.opponents_cards_info[x][card] not in [0, -1, 4] ]
            #print "for card" + card + "these are teh players who have it", possible_players
            if len(possible_players) !=0:
                card_name = card
                player_name = choice(possible_players)
                #print "i choose " + card_name + " and this player" + player_name
                break

        # selection of a card, we need to make sure that computer has this card, neither can it ask for a full set of cards -- add intelligence
        # add intelligence where it iterates through greatest card to least card
        #card_options = [x for x in self.opponents_cards_info[player_name].keys()
                       # if self.opponents_cards_info[player_name][x] == max(max_cards_count) and self.cards_info[x] not in [0,4]]
        #if len(card_options) == 0:
            # AI card chooser
          #  print 'DUMMY AI MODE'
         #   card_name = choice([x for x in players_dict[player_name].cards_info.keys()
          #                  if players_dict[player_name].cards_info[x] not in [0, 4]])
        #else:
         #   card_name = choice(card_options)
        # if player_card_info.players_dict[curr_player].cards_info[car d_name] not in [0,4]:
        #   break ( OLD CODE see if it makese sense)

        if card_name == '':
            #print "no such card exists"
            card_name = choice(valid_cards)
        if player_name == '':
            #print "no such player exists"
            possible_players = [x for x in self.opponents_cards_info.keys()
                                if self.opponents_cards_info[x][card_name] not in [-1, 4]]
            player_name = choice(possible_players)

        no_of_cards = self.opponents_cards_info[player_name][card_name]
        if no_of_cards <= 0:
            no_of_cards = 1
        return player_name + ' ' + card_name + ' ' + str(no_of_cards)

