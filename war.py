################################
# Module:  War.py              #
# Author:  D.D.Dontje          #
# Date:    01/11/11            #
# A simulation of the game War #
################################

import random
from random import shuffle



def tiebreaker(location, deckBlack, deckRed):
    if(len(deckBlack) > location) and (len(deckRed) > location):
        #If both decks are large enough to war, then war
        if deckBlack[location] > deckRed[location]:
            #If black won, end the round
            print(location)
            deckBlack, deckRed = endRound(deckBlack, deckRed, location+1)
        elif deckBlack[location] > deckRed[location]:
            #If red won, end the round
            print(location)
            deckRed, deckBlack = endRound(deckRed, deckBlack, location+1)
        else:
            #If no winner is declared, call tiebreaker again moving the location forward by four
            deckBlack, deckRed = tiebreaker(location+4, deckBlack, deckRed)
    else:
        #If a deck does not have enough cards to war, then give all of their cards to the winner
        #This will kill the loop in the main program
        if(len(deckBlack) > len(deckRed)):
            deckBlack, deckRed = endRound(deckBlack, deckRed, len(deckRed))
            print("Final War")
            print(location)
        elif(len(deckBlack) == len(deckRed)):
            #If in the unlikely event there is a tie, this just drains the cards into one
            #of the decks so that the while loop in the main program is killed.
            print("This game ended in a tie.")
            deckRed, deckBlack = endRound(deckRed, deckBlack, len(deckBlack))
        else:
            deckRed, deckBlack = endRound(deckRed, deckBlack, len(deckBlack))
            print("Final War")
            print(location)
        print("A deck does not have enough cards to perform war, therefore it loses..")
    return deckBlack, deckRed

def endRound(deck1, deck2, i):
    #'i' is a variable for how many iterations the loop should do
    for x in range(0,i):
        deck1.append(deck2[0])
        deck1.append(deck1[0])
        del deck1[0]
        del deck2[0]
    return deck1, deck2
    
            
def play():
    #Simple 'decks' were J,Q,K,A are represented by 11,12,13,14 respectively#
    deckRed=[2,3,4,5,6,7,8,9,10,11,12,13,14,2,3,4,5,6,7,8,9,10,11,12,13,14,2,3,4,5,6,7,8,9,10,11,12,13,14,2,3,4,5,6,7,8,9,10,11,12,13,14]
    deckBlack=[2,3,4,5,6,7,8,9,10,11,12,13,14,2,3,4,5,6,7,8,9,10,11,12,13,14,2,3,4,5,6,7,8,9,10,11,12,13,14,2,3,4,5,6,7,8,9,10,11,12,13,14]
    z = 0

    #Check to make sure both decks have alteast one card#
    while ((len(deckRed) != 0) and (len(deckBlack) != 0)):
        shuffle(deckRed)
        shuffle(deckBlack)
        z=z+1
        if deckBlack[0] == deckRed[0]:
            deckBlack, deckRed = tiebreaker(4, deckBlack, deckRed)
        else:
            if deckBlack[0] > deckRed[0]:
                deckBlack, deckRed = endRound(deckBlack, deckRed, 1)
            else:
                deckRed, deckBlack = endRound(deckRed, deckBlack, 1)
    return z

def main():
    plays = eval(input("How many games would you like to play? "))
    totalRounds = 0
    for x in range(0,plays):
        z = play()
        totalRounds = totalRounds + z
    print("On average, games took %d rounds to end" % (totalRounds/plays))

    

main()
