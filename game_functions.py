import player_card_info
from random import randint,shuffle

def assign_cards_randomly():
    player_count = 0
    player_list = player_card_info.players_dict.keys()
    cards_index = range(0,52)
    shuffle(cards_index)
    #print cards_index
    for i in cards_index:
        card = player_card_info.cards_set_list.keys()[i%13]
        if check_card_count(card) < 4:
            player_card_info.players_dict[player_list[player_count]].cards_info[card] += 1
        player_count = (player_count+1)%len(player_card_info.players_dict)

def check_card_count(card_name):
    count = 0
    for player in player_card_info.players_dict.values():
        count += player.cards_info[card_name]
    return count

# prints all the card details of all the players
def print_total_cards_info():
    for player in player_card_info.players_dict.values():
        player.card_count()
        player.print_player_cards_info()

def check_card_request_format(card_request, curr_player):
    word_list = card_request.split()
    #getting the list of player names without the current player
    player_list = [x for x in player_card_info.players_names
                            if x!=curr_player]
    if len(word_list) == 3:
        if word_list[0] in player_list:
            if word_list[1] in player_card_info.cards_set_list.keys():
                if int(word_list[2]) in range(1,5):
                    # print 'all good'
                    return True
                else:
                    print 'Incorrect Number of Cards Requested'
                    print range(1,5)
                    return False
            else:
                print 'Enter correct Card Name'
                print player_card_info.cards_set_list.keys()
                return False
        else:
            print 'Enter correct Player Name'
            print player_list
            # In future add functionality to ignore current player
            return False
    else:
        print 'Incorrect Number of Arguments'
        return False

# research about using vairables to access class variables but with their short form and need to modify them

def process_card_request(curr_player, player_req, card_request, no_of_cards_req):
    if player_card_info.players_dict[curr_player].cards_info[card_request] > 0:
        if player_card_info.players_dict[player_req].cards_info[card_request] >= no_of_cards_req:
            player_card_info.players_dict[player_req].cards_info[card_request] -= no_of_cards_req
            player_card_info.players_dict[curr_player].cards_info[card_request] += no_of_cards_req
            print 'Player %s has taken %d %s from Player %s'\
                  %(player_card_info.players_dict[curr_player].name,no_of_cards_req,card_request,
                    player_card_info.players_dict[player_req].name)
            if player_card_info.players_dict[curr_player].cards_info[card_request] == 4:
                player_card_info.cards_set_list[card_request] = player_card_info.players_dict[curr_player].name
            #check if both players can continue or not
            player_card_info.players_dict[curr_player].check_and_set_status()
            player_card_info.players_dict[player_req].check_and_set_status()
            #print player_card_info.cards_set_list
            return curr_player
        else:
            print 'GO FISH!'
            print 'Player %s loses turn to Player %s' \
                  % (player_card_info.players_dict[curr_player].name,
                     player_card_info.players_dict[player_req].name)
            return player_req
    else:
        print 'Player %s does not have this card %s' \
              % (player_card_info.players_dict[curr_player].name, card_request)
        print 'Player %s loses turn to Player %s' \
              % (player_card_info.players_dict[curr_player].name,
                 player_card_info.players_dict[player_req].name)
        return player_req


def announce_winner():
    count_dict = {x:player_card_info.cards_set_list.values().count(x) for x in player_card_info.cards_set_list.values()}
    print count_dict

def check_existing_sets():
    for player in player_card_info.players_dict.values():
        for card in player_card_info.cards_set_list.keys():
            if player.cards_info[card] == 4:
                player_card_info.cards_set_list[card] = player.name