import player_card_info
import game_functions
import time

number_of_players = int(input("Enter number of Players?"))

human_player_name = ''
while True:
    human_player_name = input("Enter Human Player name:")
    if len(human_player_name) > 0:
        player_card_info.players_dict[human_player_name] = player_card_info.Player(human_player_name)
        player_card_info.players_names.append(human_player_name)
        break

for i in range(1, number_of_players):
    ai_name = str(i)
    print ('Super AI Player %s created'%ai_name)
    player_card_info.players_dict[ai_name] = player_card_info.Super_AI_Player(ai_name)
    player_card_info.players_names.append(ai_name)

print ('Initializing Super AI Database')
for i in range(1, number_of_players):
    ai_name = str(i)
    player_card_info.players_dict[ai_name].initialize()


game_functions.assign_cards_randomly()
game_functions.check_existing_sets()
#game_functions.print_total_cards_info()
player_card_info.players_dict[human_player_name].print_player_cards_info()

print ('Game Begins Good Luck')
print ('Format of Asking Card is')
print ('player_name card_name no_of_cards')
print ('Ex: %s A 1 - Means Player %s is being asked for 1 Ace'%(player_card_info.players_dict.keys()[0],player_card_info.players_dict.keys()[0]))
current_player = player_card_info.players_names[0]
print ('Player %s Starts'%current_player)
while player_card_info.cards_set_list.values().count(-1) > 0:
    # check if you are not human player .. we need a more elegant way of representing this
    if current_player != player_card_info.players_names[0]:
        # generates a request for a card , Super AI will give a good request
        card_request = player_card_info.players_dict[current_player].request_generator()
        print (card_request)
        time.sleep(5)
    else:
        # to print human players cards
        player_card_info.players_dict[current_player].print_player_cards_info()
        # Takes input of the player and checks if input is correct
        while True:
            # print 'your are inside raw_input loop'
            card_request = input('>')
            if game_functions.check_card_request_format(card_request, current_player):
                break
            print ('Enter Correct Input Again:', 'player_number card_name no_of_cards')

    player_requested, card_requested, no_of_cards_requested = card_request.split()
    no_of_cards_requested_int = int(no_of_cards_requested)
    previous_current_player = current_player
    #time.sleep(5)
    current_player = game_functions.process_card_request(current_player, player_requested,
                                                         card_requested, no_of_cards_requested_int)
    time.sleep(5)
    # This is where AI rmembers stuff and tries  to beat human, wee send both success and failure scenarios
    for player in player_card_info.players_dict.values():
        if isinstance(player , player_card_info.Super_AI_Player):
            player.request_processor(previous_current_player, player_requested, card_requested,
                                   no_of_cards_requested_int, previous_current_player == current_player)
            #player.print_opponents_card_info()

    #print "i am here after updating database"

    while not player_card_info.players_dict[current_player].player_status:
        print ('Player %s cannot continue as their sets are complete'%current_player)
        # this is to iterate to the next player in the dictionary, better to use lists i guess
        current_player = player_card_info.players_names[
            (player_card_info.players_names.index(current_player) + 1) % number_of_players]
        print ('Player %s is selected' % current_player)
        if True not in [x.player_status for x in player_card_info.players_dict.values()]:
            break

game_functions.announce_winner()

print('Thanks for playing')
exit(0)