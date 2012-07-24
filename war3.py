from collections import namedtuple, deque
from itertools import count
from random import shuffle

# how we are going to represent each player
Player = namedtuple('Player',
                    ['number','deck','cards_in_play'])

def get_new_deck():
    return deque(range(2,15) * 4)

def players_with_decks(players):
    """
    returns list of players who still have cards
    in their deck
    """
    return [p for p in players if len(p.deck)]

def compare_top_card(p1, p2):
    """
    compare's the top cards of two players
    returns the player who's card is greatest
    if they are equal returns None
    """

    # must have cards
    assert p1.cards_in_play, "Player %s has no cards to compare" % p1.number
    assert p2.cards_in_play, "Player %s has no cards to compare" % p2.number

    p1_card = p1.cards_in_play[0]
    p2_card = p2.cards_in_play[0]

    print 'COMPARE TOP CARD: %s %s' % (p1_card, p2_card)

    if p1_card > p2_card:
        return p1
    if p2_card > p1_card:
        return p2
    return None

def game_over(players):
    """
    the game is over when one or less players have
    cards left

    return bool
    """
    print 'CHECKING GAME OVER',
    active_players = players_with_decks(players)
    if not active_players or len(active_players) == 1:
        print 'OVER'
        return True
    print 'NOT'
    return False

def winning_game_player(players):
    """
    evaluates if there is a player who has
    won the game
    returns list of winning players (multiples in case
        of tie)
    returns None if game is not over
    """

    print 'WINNING GAME PLAYER'

    # in order for there to be a winner, the game must
    # be over
    if not game_over(players):
        print 'GAME NOT OVER'
        return None

    # if the game is over, it could be that there is no
    # winner
    active_players = players_with_decks(players)
    if not active_players:
        return False

    # if the game is over than find the winner
    return players_with_decks(players)[0]

def winning_round_player(players):
    """
    evaluates if there is currently a winning
    player. If there is returns that player
    """

    assert players, "Must have players to determine winner"

    print 'WINNING ROUND PLAYER'

    # a winner player is defined as the player
    # with the highest top card
    top = None
    for player in players:

        # only compare if the player has something to compare
        if not player.cards_in_play: continue

        print 'player: %s' % str(player)

        # if top isn't set, we'll go with current
        if not top:
            top = player
        else:
            # will return None if it's a tie
            top = compare_top_card(player, top)

    # if it's a tie, no winner
    if top is None:
        print 'TIE'
        return False

    print 'top: %s' % str(top)
    return top

def hand_over_cards(round_winner, players):
    """
    consolidate's all the cards that were in play
    into the winner's deck
    """

    print 'HANDING OVER CARDS: %s' % str(round_winner)

    # go through each of the players
    for player in players:

        # hand over all their cards
        while True:
            try:
                round_winner.deck.append(
                    player.cards_in_play.popleft())
            except IndexError:
                # no more cards
                break

# normal round - pull one card off deck
# war round - pull four cards off deck

def play_normal_round(player):
    """
    normal round moves one card off deck and into play
    puts new card on top of cards in play
    """
    print 'PLAY NORMAL RUOND: %s' % str(player)
    player.cards_in_play.appendleft(player.deck.popleft())
    return player

def play_war_round(player):
    """
    war round moves four cards off deck and into play
    """
    print 'PLAY WAR ROUND: %s' % str(player)
    for i in xrange(4):
        play_normal_round(player)

    return player

def create_players(num_players):
    """
    creates and returns an array of players
    with decks
    """
    players = []
    for player_number in xrange(num_players):
        # create new players
        players.append(
                Player(player_number, get_new_deck(), deque()))

    return players

def play_round(players):
    """
    plays one full round for all players
    this could include going to war
    """

    # start off playing a normal round
    play_round = play_normal_round

    # we shuffle the cards at the begining of every round?
    for player in players:
        shuffle(player.deck)

    print 'PLAY ROUND: %s' % str(players)

    # while we dont have a winner, and there are still
    # cards to play, keep playing
    while not winning_round_player(players) and players_with_decks(players):
        # go through all the players who still have cards
        # in their deck
        for player in players_with_decks(players):
            try:
                play_round(player)
            except IndexError:
                # one of the players has run out of cards
                # in their deck
                pass

        # it's WAR !
        play_round = play_war_round

    # did we actually have a winner this round
    if players_with_decks(players):
        # we now have a winner
        # all cards from play go to the winner
        round_winner = winning_round_player(players)
        hand_over_cards(round_winner, players)

    return players

def play_game(players):

    print "PLAY GAME: %s" % str(players)

    # infinite number of rounds, starting @ 1
    for round_number in count(1):

        print "ROUND: %s" % round_number

        # play our players through the next round
        play_round(players)

        # check if the game is over
        if game_over(players):
            break

    # return our winner, and the # of rounds
    return ( winning_game_player(players), round_number )



def play_reporting(game_count, player_count):

    assert player_count >= 2, "Must have at least two players"

    # play and report
    for game_number in xrange(1, game_count+1):

        players = create_players(player_count)
        winner, rounds = play_game(players)

        print 'WINNER: %s' % str(winner)
        print 'ROUNDS: %s' % str(rounds)
        print 'PLAYERS: %s' % str(players)

        # start reporting
        print ('Game [%s] (%s)' % (game_number, rounds)),

        # if winner is False, it was a tie
        if winner is False:
            print 'TIE'

        else:
            print winner.number

def play_interactive():

    # get the user's input on how many games / players
    game_count = int(input("How many games would you like to play? ") or 1)
    player_count = int(input("How many players would you like to have? ") or 2)
    play_reporting(game_count, player_count)

def play_cmdline():
    import sys
    game_count, player_count = map(int, sys.argv[1:])
    play_reporting(game_count, player_count)

if __name__ == '__main__':
    play_cmdline()

