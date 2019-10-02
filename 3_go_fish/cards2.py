from cards import Card, Deck
import unittest


class Hand(object):
    # create the Hand with an initial set of cards
    # param: a list of cards
    def __init__(self, init_cards):
        self.cards = []
        cards_str = []
        for c in init_cards:
            if c.__str__() not in cards_str:
                self.cards.append(c)
                cards_str.append(c.__str__())

    # add a card to the hand
    # silently fails if the card is already in the hand
    # param: the card to add
    # returns: nothing
    def add_card(self, card): 
        for c in self.cards:
            if c.__str__() == card.__str__():
                return
        
        self.cards.append(card)
    
    # remove a card from the hand
    # param: the card to remove
    # returns: the card, or None if the card was not in the Hand
    def remove_card(self, card):
        for c in self.cards:
            if c.__str__() == card.__str__():
                self.cards.remove(c)
                return c
        
        return None

    # draw a card from a deck and add it to the hand
    # side effect: the deck will be depleted by one card
    # param:the deck from which to draw
    # returns: nothing
    def draw(self, deck):
        self.add_card(deck.pop_card())

class TestHand(unittest.TestCase):
    
    def test_1_Initializer(self):
        # a normal case 
        init_cards1 = [Card(),Card(2,11),Card(1,1)]
        hand1 = Hand(init_cards1)
        init_cards1_str = [c.__str__() for c in init_cards1]
        cards1_str = [c.__str__() for c in hand1.cards]
        self.assertEqual(sorted(list(set(init_cards1_str))),sorted(cards1_str))
        
        # a test for initial cards with repeated cards
        init_cards2 = [Card(),Card(),Card(1,1),Card(1,1)]
        hand2 = Hand(init_cards2)
        init_cards2_str = [c.__str__() for c in init_cards2]
        cards2_str = [c.__str__() for c in hand2.cards]
        self.assertEqual(sorted(list(set(init_cards2_str))),sorted(cards2_str))
    
    def test_2_AddAndRemove(self):
        hand = Hand([Card(),Card(2,11),Card(1,1)])
        cards_str0 = [c.__str__() for c in hand.cards]
        #test for adding an existing card
        card = Card()
        self.assertIs(hand.add_card(card),None)
        cards_str1 = [c.__str__() for c in hand.cards]
        self.assertEqual(set(cards_str0),set(cards_str1))
        
        #test for adding a card that doesn't exist
        card2 = Card(3,13)
        self.assertIs(hand.add_card(card2),None)
        cards_str2 = [c.__str__() for c in hand.cards]
        self.assertIn(card2.__str__(),cards_str2)
        self.assertTrue(len(cards_str2) - len(cards_str1) == 1)
        cards_str2.remove(card2.__str__())
        self.assertEqual(set(cards_str1),set(cards_str2))
        cards_str2 = [c.__str__() for c in hand.cards]
        
        #test for removing a card that exists
        self.assertEqual(card2.__str__(),hand.remove_card(card2).__str__())
        cards_str3 = [c.__str__() for c in hand.cards]
        self.assertTrue(len(cards_str2) - len(cards_str3) == 1)
        self.assertNotIn(card2.__str__(),cards_str3)
        cards_str2.remove(card2.__str__())
        self.assertEqual(set(cards_str3),set(cards_str2))
        cards_str2 = [c.__str__() for c in hand.cards]
        
        #test for removing a card that doesn't exist
        card3 = Card(1,8)
        self.assertIs(hand.remove_card(card3),None)
        cards_str4 = [c.__str__() for c in hand.cards]
        self.assertEqual(len(cards_str3),len(cards_str4))
        self.assertEqual(set(cards_str3),set(cards_str4))
    
    def test_3_Draw(self):
        deck = Deck()
        deck_cards_str0 = [c.__str__() for c in deck.cards]
        card = deck.cards[-1]
        hand = Hand([])
        self.assertIs(hand.draw(deck),None)
        self.assertEqual(hand.cards,[card])
        deck_cards_str1 = [c.__str__() for c in deck.cards]
        self.assertTrue(len(deck_cards_str0)-len(deck_cards_str1) == 1)
        deck_cards_str0.remove(card.__str__())
        self.assertEqual(set(deck_cards_str0),set(deck_cards_str1))  
        


if __name__ == "__main__":
    unittest.main(verbosity=2)
