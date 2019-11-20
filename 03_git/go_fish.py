import cards
import cards2
import cards3


def chooseRank(hand):
    rank = int(input("Please choose a card rank you would like "\
    "to ask the other player if they have (between 1-13):"))
    if rank not in [c.rank_num for c in hand.cards]:
        print("Illigal rank! Choose again.")
        return chooseRank(hand)
    return rank

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
    hands = deck.deal(2,7)
    books = [[],[]]
    checkbook(hands[0],books[0],1,False)
    checkbook(hands[1],books[1],2,False)
    playernum = 1
    while(deck.cards != [] or hands[0].cards!=[] or hands[1].cards!=[]):
        print("####################################")
        print("Player" + repr(playernum)+"'s turn.")
        if books[playernum-1]==[]:
            print("Player"+ repr(playernum)+" has no book.")
        else:
            print("Player has book of rank "+ ", ".join(repr(r) for r in books[playernum-1])+".")
        
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
        
        if(str(input("Want to check your cards in hand?(y/n)")) == 'y'):
            for c in hands[playernum-1].cards:
                print(c.__str__())
        
        rank = chooseRank(hands[playernum-1])
        handed_cards = []
        for c in hands[playernum%2].cards:
            if rank == c.rank_num:
                handed_cards.append(c)
        
        if handed_cards == []:
            print("Player" + repr(3-playernum)+" has no card with rank "+repr(rank)+".")
            print("Go fish.")
            print("Player" + repr(playernum)+" draws a card.")
            card = deck.pop_card()
            hands[playernum-1].add_card(card)
            checkbook(hands[playernum-1],books[playernum-1],playernum)
            if card.rank_num == rank:
                print("Player" + repr(playernum)+" draws "+card.__str__()+\
                ". He/She can have another turn.")
                continue
        else:
            for c in handed_cards:
                print("Player" + repr(3-playernum)+" hands over "+c.__str__()+" to Player" + repr(playernum)+".")
                hands[playernum-1].add_card(c)
                hands[playernum%2].remove_card(c)
            checkbook(hands[playernum-1],books[playernum-1],playernum)
            print("Player"+ repr(playernum)+"'s turn continues.")
            continue
        playernum = 3 - playernum
    
    print("""
    ####################################
    All thirteen books have been won. The game ends.
    """
    )
    for i in range(2):
        print("In the end, player"+repr(i+1)+" has "+repr(len(books[i]))+" books.")
    
    maxi = 1 if len(books[0]) > len(books[1]) else 2
    print("Player"+repr(maxi)+" wins!")
        
        
