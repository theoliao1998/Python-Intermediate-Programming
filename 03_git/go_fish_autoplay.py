#refer to https://en.wikipedia.org/wiki/Go_Fish and 
#https://bicyclecards.com/how-to-play/go-fish/ for the detailed rules

import random
import cards
import cards2
import cards3

def chooseRankAndPlayer(hand,playernum,num):
    print("Please choose one another player and a card rank you would like "\
    "to ask that if he has (between 1-13):")
    rank = random.sample([c.rank_num for c in hand.cards],1)[0]
    player = random.sample([(i+1) for i in range(num) if ((i+1)!= playernum)],1)[0]
    return rank,player

def checkbook(hand,book,playnum,verbose = True):
    cards = [[] for n in range(13)]
    for c in hand.cards:
        cards[c.rank_num-1].append(c)
    
    for i in range(13):
        if len(cards[i]) == 4:
            for c in cards[i]:
                hand.remove_card(c)
            book.append(i+1)
            if verbose:
                print("Player" + repr(playernum)+" gains a book of rank "+ repr(i+1)+".")
    
    
if __name__ == "__main__":
    deck = cards3.Deck()
    deck.shuffle()
    num = int(input("How many computer players would you like to take part in the simulation?(between 2 and 4)"))
    hands = deck.deal(num,7)
    books = [[] for i in range(num)]
    for i in range(num):
        checkbook(hands[i],books[i],i+1,False)

    playernum = 1
    outofgame = []
    while(deck.cards != [] or not all([h.cards == [] for h in hands])):
        print("####################################")
        if playernum in outofgame:
            print("Player"+repr(playernum)+" is out of game.")
            playernum = 1 if playernum == num else (playernum+1)
            continue
        print("Player" + repr(playernum)+"'s turn.")
        if books[playernum-1]==[]:
            print("Player"+ repr(playernum)+" has no book.")
        else:
            print("Player"+ repr(playernum)+" has book of rank "+ ", ".join(repr(r) for r in books[playernum-1])+".")
        
        if hands[playernum-1].cards == []:
            print("Player"+ repr(playernum)+" has no card in hand.")
            if deck.cards == []:
                print("There's also no card in the deck. Player"+repr(playernum)+" is out of game.")
                outofgame.append(playernum)
                playernum = 1 if playernum == num else (playernum+1)
                continue
            else:
                print("Player"+repr(playernum)+" draws a card from deck.")
                hands[playernum-1].draw(deck)
            
        print("Player" + repr(playernum)+"'s cards in hand are as follows.")
        for c in hands[playernum-1].cards:
            print(c.__str__())
        
        rank,player = chooseRankAndPlayer(hands[playernum-1],playernum,num)
        print("Player" + repr(playernum)+" chooses player"+repr(player)+" and rank "+ repr(rank)+".")
        handed_cards = []

        for c in hands[player-1].cards:
            if rank == c.rank_num:
                handed_cards.append(c)
        
        if handed_cards == []:
            print("Player"+repr(player)+" has no card with rank "+repr(rank)+".")
            print("Go fish.")
            print("Player" + repr(playernum)+" can draw a card.")
            if(deck.cards == []):
                print("Oops! There's no card in the deck.")
                playernum = 1 if playernum == num else (playernum+1) 
                continue

            card = deck.pop_card()
            hands[playernum-1].add_card(card)
            checkbook(hands[playernum-1],books[playernum-1],playernum)
            if card.rank_num == rank:
                print("Player" + repr(playernum)+" draws "+card.__str__()+\
                ". He/She can have another turn.")
                continue
        else:
            for c in handed_cards:
                print("Player" + repr(player)+" hands over "+c.__str__()+" to Player" + repr(playernum)+".")
                hands[playernum-1].add_card(c)
                hands[player-1].remove_card(c)
            checkbook(hands[playernum-1],books[playernum-1],playernum)
            print("Player"+repr(playernum)+"'s turn continues.")
            continue
            
        playernum = 1 if playernum == num else (playernum+1) 


    print("####################################")
    maxi = [0,-1,-1]
    print("All thirteen books have been won. The game ends.")
    for i in range(num):
        print("In the end, player"+repr(i+1)+" has "+repr(len(books[i]))+" books.")
        if len(books[i])>len(books[maxi[0]]):
            maxi = [i,-1,-1]
        elif i!=0 and len(books[i])==len(books[maxi[0]]):
            j = 2 if maxi[1]>=0 else 1
            maxi[j] = i
    if maxi[1]!=-1:
        print("The game ends with a tie.")
    else:
        print("Player"+repr(maxi[0]+1)+" wins.")
    
    
