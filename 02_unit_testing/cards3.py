from cards import Card
from cards import Deck as Dk
from cards2 import Hand as Hd
import unittest
        

class Hand(Hd):
    def remove_pairs(self):
        rank_card = {}
        for c in self.cards.copy():
            if c.rank in rank_card:
                self.cards.remove(rank_card[c.rank])
                rank_card.pop(c.rank)
                self.cards.remove(c)
            else:
                rank_card[c.rank] = c


class Deck(Dk):
    def deal(self,num_of_hands,num_of_cards_per_hand):
        hands = [Hand([]) for i in range(num_of_hands)]
        
        if(num_of_cards_per_hand == -1):
            i = 0
            while(self.cards != []):
                hands[i%num_of_hands].draw(self)
                i = i+1
        
        elif num_of_cards_per_hand >= 0:
            for i in range(num_of_cards_per_hand):
                for j in range(num_of_hands):
                    if self.cards == []:
                        break
                    else:
                        hands[j].draw(self)
            
        return hands


class TestExtra2(unittest.TestCase):
    
    def test_remove_pairs(self):
        # test for normal cases
        hand1 = Hand([Card(1,4),Card(2,3),Card(2,1),Card(1,3)])
        hand1.remove_pairs()
        self.assertEqual(sorted([c.__str__() for c in hand1.cards]),sorted([Card(1,4).__str__(),Card(2,1).__str__()]))
        
        #test for a hand with three cards having the same rank
        hand1 = Hand([Card(1,11),Card(2,11),Card(3,11)])
        hand1.remove_pairs()
        self.assertEqual(len(hand1.cards),1)
        self.assertEqual(hand1.cards[0].rank_num,11)
    
    def test_deal(self):
        deck = Deck()
        deck.pop_card()
        deck_cards_str = [c.__str__() for c in deck.cards]
        
        #test for the number of cards per hand set to -1
        hands1 = deck.deal(4,-1)
        self.assertEqual(deck.cards,[])
        self.assertIsInstance(hands1,list)
        self.assertTrue(all(isinstance(h,Hand) for h in hands1))
        hands1_str_list = [[c.__str__() for c in h.cards] for h in hands1]
        hands1_str = [s for l in hands1_str_list for s in l]
        self.assertEqual(sorted(hands1_str),sorted(deck_cards_str))
        self.assertTrue(all(len(h.cards)-len(hands1[0].cards) in [0,-1] for h in hands1))
        
        deck = Deck()
        deck.pop_card()
        deck_cards = deck.cards.copy()
        deck_cards_str = [c.__str__() for c in deck.cards]
        #test for the number of cards per hand set to an non-negative integer
        hands2 = deck.deal(4,7)
        self.assertEqual(deck.cards,deck_cards[:-28])
        self.assertIsInstance(hands1,list)
        self.assertTrue(all(isinstance(h,Hand) for h in hands1))
        hands2_str_list = [[c.__str__() for c in h.cards] for h in hands2]
        hands2_str = [s for l in hands2_str_list for s in l]
        self.assertEqual(sorted(hands2_str),sorted(deck_cards_str[-28:]))
        self.assertTrue(all(len(h.cards) == 7 for h in hands2))


if __name__ == "__main__":
    unittest.main(verbosity=2)
