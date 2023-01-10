import player_card_info
import game_functions
import time
from sys import argv

script, number_of_players = argv
number_of_players = int(number_of_players)

for i in range(0, number_of_players):
    ai_name = str(i)
    print 'Super AI Player %s created'%ai_name
    player_card_info.players_dict[ai_name] = player_card_info.Super_AI_Player(ai_name)
    player_card_info.players_names.append(ai_name)

print 'Initializing Super AI Database'
for player in player_card_info.players_dict.values():
    player.initialize()


game_functions.assign_cards_randomly()
game_functions.check_existing_sets()
game_functions.print_total_cards_info()
#player_card_info.players_dict[human_player_name].print_player_cards_info()

print 'Game Begins Good Luck'
current_player = player_card_info.players_names[0]
print 'Player %s Starts'%current_player
while player_card_info.cards_set_list.values().count(-1) > 0:
    # check if you are not human player .. we need a more elegant way of representing this

    # generates a request for a card , Super AI will give a good request
    card_request = player_card_info.players_dict[current_player].request_generator()
    print card_request
    #time.sleep(1)

    player_requested, card_requested, no_of_cards_requested = card_request.split()
    no_of_cards_requested_int = int(no_of_cards_requested)
    previous_current_player = current_player
    #time.sleep(5)
    current_player = game_functions.process_card_request(current_player, player_requested,
                                                         card_requested, no_of_cards_requested_int)
    #time.sleep(1)
    # This is where AI rmembers stuff and tries  to beat human, wee send both success and failure scenarios
    for player in player_card_info.players_dict.values():
        if isinstance(player , player_card_info.Super_AI_Player):
            player.request_processor(previous_current_player, player_requested, card_requested,
                                   no_of_cards_requested_int, previous_current_player == current_player)
            #player.print_opponents_card_info()

    #print "i am here after updating database"

    while not player_card_info.players_dict[current_player].player_status:
        print 'Player %s cannot continue as their sets are complete'%current_player
        # this is to iterate to the next player in the dictionary, better to use lists i guess
        current_player = player_card_info.players_names[
            (player_card_info.players_names.index(current_player) + 1) % number_of_players]
        print 'Player %s is selected' % current_player
        if True not in [x.player_status for x in player_card_info.players_dict.values()]:
            break

game_functions.announce_winner()

print 'Thanks for playing'
exit(0)