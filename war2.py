
InPlay = namedtuple('InPlay', ['player_num','cards'])

def get_new_deck():
    return range(2,15) * 4

def play_tiebraker_round(decks, winning, losing):
    """
    given the decks in play and the lists of winning
    and losing players, tie break between the winners

    updates the decks, winning, and losing during round
    """

    # go through each of the winners, pulling out 3 cards
    # "face down" and than using the 4th card for comparison
    for player_num, cards_in_play in winning:

        # get the player's deck
        deck = decks[player_num]

        # update the player's cards in play,
        # pull four cards from the deck
        try:
            for i in xrange(4):
                cards_in_play.append( deck.pop() )
        except IndexError:
            # the player is out of cards, they can not
            # win

        #

def play_round(decks):
    """
    plays out a round of "war" with the given decks
    modifies decks during course of round

    returns the winning deck's key
    """

    # keep track of who is winning in this array
    # we need an array b/c there may be more than one "winner"
    # during the course of the round
    winning = []

    # keep track of the losers so that we can collect up their
    # cards at the end
    losing = []

    # go through each of the player's decks
    # the order is not important
    for player_num, deck in decks.iteritems():

        # pull the top card of the deck
        try:
            top_card = deck.pop()
        except IndexError:
            # their deck is empty, they can not be a winner
            losing.append( InPlay(player_num, [None]) )
            continue

        # if ther is not yet a winner or this player's top
        # card is greater than the current winner than add
        # the current player / card as winning
        if not winning or top_card > winning[0][1]:
            winning.append( InPlay(player_num, [top_card]) )

        # if it's a tie, for now, your also a winner
        elif top_card == winning[0][1]:
            winning.append( InPlay(player_num, [top_card]) )

        # if your not winning, ur losing
        else:
            losing.append( InPlay(player_num, [top_card]) )

    # now we should have sorted all our players into either
    # winners or losers

    # if there is more than one winner, than we need to have
    # a tie breaking round
    play_tiebreaker_round(decks, winning, losing)

    # we should now have a single winner
    assert len(winning) == 1, "There can't be more than one winner at war"

    # update the deck of the winner, adding the played cards
    # to the winner's deck

    # return the player # for our winner
    return winning[0][0]


def main():
    # get the user's input on how many games / players
    games = int(input("How many games would you like to play? ") or 1)
    players = int(input("How many players would you like to have? ") or 2)

    # dictionary lookup from player # => deck array
    decks = {}

    # hand out decks
    for player_num in xrange(players):
        decks[i] = get_new_deck()

    # infinite couting loop, starts at one
    for game_number in count(1):

        # we start off each game by shuffling all the decks
        for player_num, deck in decks.iteritems():
            shuffle(deck)

        # now that the decks are shuffled we can start the game
        # same as games, infinite round counter
        for round_number in count(1):

            # our play round function is going to play out
            # the round from the decks we provide and return
            # back the winner's number
            winning_player_num = play_round(decks)



