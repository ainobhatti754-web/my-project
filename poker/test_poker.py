"""
单元测试和集成测试
"""

import unittest
from card import Card, Suit, Rank, Deck
from hand_evaluator import HandEvaluator, HandRank
from player import Player, GameRound
from game import PokerGame

class TestCard(unittest.TestCase):
    """测试扑克牌"""
    
    def test_card_creation(self):
        card = Card(Suit.HEARTS, Rank.ACE)
        self.assertEqual(card.suit, Suit.HEARTS)
        self.assertEqual(card.rank, Rank.ACE)
    
    def test_card_string(self):
        card = Card(Suit.HEARTS, Rank.ACE)
        self.assertEqual(str(card), "A♥")

class TestDeck(unittest.TestCase):
    """测试牌堆"""
    
    def test_deck_creation(self):
        deck = Deck()
        self.assertEqual(len(deck), 52)
    
    def test_deck_draw(self):
        deck = Deck()
        initial_count = len(deck)
        card = deck.draw()
        self.assertIsInstance(card, Card)
        self.assertEqual(len(deck), initial_count - 1)

class TestHandEvaluator(unittest.TestCase):
    """测试手牌评估"""
    
    def test_royal_flush(self):
        cards = [
            Card(Suit.HEARTS, Rank.TEN),
            Card(Suit.HEARTS, Rank.JACK),
            Card(Suit.HEARTS, Rank.QUEEN),
            Card(Suit.HEARTS, Rank.KING),
            Card(Suit.HEARTS, Rank.ACE),
        ]
        rank, values = HandEvaluator.evaluate_hand(cards)
        self.assertEqual(rank, HandRank.ROYAL_FLUSH)
    
    def test_straight_flush(self):
        cards = [
            Card(Suit.DIAMONDS, Rank.FIVE),
            Card(Suit.DIAMONDS, Rank.SIX),
            Card(Suit.DIAMONDS, Rank.SEVEN),
            Card(Suit.DIAMONDS, Rank.EIGHT),
            Card(Suit.DIAMONDS, Rank.NINE),
        ]
        rank, values = HandEvaluator.evaluate_hand(cards)
        self.assertEqual(rank, HandRank.STRAIGHT_FLUSH)
    
    def test_four_of_a_kind(self):
        cards = [
            Card(Suit.HEARTS, Rank.KING),
            Card(Suit.DIAMONDS, Rank.KING),
            Card(Suit.CLUBS, Rank.KING),
            Card(Suit.SPADES, Rank.KING),
            Card(Suit.HEARTS, Rank.TWO),
        ]
        rank, values = HandEvaluator.evaluate_hand(cards)
        self.assertEqual(rank, HandRank.FOUR_OF_A_KIND)
    
    def test_full_house(self):
        cards = [
            Card(Suit.HEARTS, Rank.QUEEN),
            Card(Suit.DIAMONDS, Rank.QUEEN),
            Card(Suit.CLUBS, Rank.QUEEN),
            Card(Suit.HEARTS, Rank.FIVE),
            Card(Suit.DIAMONDS, Rank.FIVE),
        ]
        rank, values = HandEvaluator.evaluate_hand(cards)
        self.assertEqual(rank, HandRank.FULL_HOUSE)
    
    def test_flush(self):
        cards = [
            Card(Suit.CLUBS, Rank.TWO),
            Card(Suit.CLUBS, Rank.FOUR),
            Card(Suit.CLUBS, Rank.SIX),
            Card(Suit.CLUBS, Rank.EIGHT),
            Card(Suit.CLUBS, Rank.TEN),
        ]
        rank, values = HandEvaluator.evaluate_hand(cards)
        self.assertEqual(rank, HandRank.FLUSH)
    
    def test_straight(self):
        cards = [
            Card(Suit.HEARTS, Rank.THREE),
            Card(Suit.DIAMONDS, Rank.FOUR),
            Card(Suit.CLUBS, Rank.FIVE),
            Card(Suit.SPADES, Rank.SIX),
            Card(Suit.HEARTS, Rank.SEVEN),
        ]
        rank, values = HandEvaluator.evaluate_hand(cards)
        self.assertEqual(rank, HandRank.STRAIGHT)
    
    def test_three_of_a_kind(self):
        cards = [
            Card(Suit.HEARTS, Rank.JACK),
            Card(Suit.DIAMONDS, Rank.JACK),
            Card(Suit.CLUBS, Rank.JACK),
            Card(Suit.HEARTS, Rank.TWO),
            Card(Suit.DIAMONDS, Rank.THREE),
        ]
        rank, values = HandEvaluator.evaluate_hand(cards)
        self.assertEqual(rank, HandRank.THREE_OF_A_KIND)
    
    def test_two_pair(self):
        cards = [
            Card(Suit.HEARTS, Rank.NINE),
            Card(Suit.DIAMONDS, Rank.NINE),
            Card(Suit.CLUBS, Rank.FOUR),
            Card(Suit.SPADES, Rank.FOUR),
            Card(Suit.HEARTS, Rank.TWO),
        ]
        rank, values = HandEvaluator.evaluate_hand(cards)
        self.assertEqual(rank, HandRank.TWO_PAIR)
    
    def test_one_pair(self):
        cards = [
            Card(Suit.HEARTS, Rank.TEN),
            Card(Suit.DIAMONDS, Rank.TEN),
            Card(Suit.CLUBS, Rank.TWO),
            Card(Suit.SPADES, Rank.FIVE),
            Card(Suit.HEARTS, Rank.EIGHT),
        ]
        rank, values = HandEvaluator.evaluate_hand(cards)
        self.assertEqual(rank, HandRank.ONE_PAIR)
    
    def test_high_card(self):
        cards = [
            Card(Suit.HEARTS, Rank.TWO),
            Card(Suit.DIAMONDS, Rank.THREE),
            Card(Suit.CLUBS, Rank.FIVE),
            Card(Suit.SPADES, Rank.SEVEN),
            Card(Suit.HEARTS, Rank.KING),
        ]
        rank, values = HandEvaluator.evaluate_hand(cards)
        self.assertEqual(rank, HandRank.HIGH_CARD)

class TestPlayer(unittest.TestCase):
    """测试玩家"""
    
    def test_player_creation(self):
        player = Player(0, "Alice", 1000)
        self.assertEqual(player.name, "Alice")
        self.assertEqual(player.chips, 1000)
    
    def test_player_bet(self):
        player = Player(0, "Alice", 1000)
        bet_amount = player.place_bet(100)
        self.assertEqual(bet_amount, 100)
        self.assertEqual(player.chips, 900)
    
    def test_player_all_in(self):
        player = Player(0, "Alice", 100)
        bet_amount = player.place_bet(200)
        self.assertEqual(bet_amount, 100)
        self.assertEqual(player.chips, 0)
        self.assertTrue(player.is_all_in)

class TestPokerGame(unittest.TestCase):
    """测试德州扑克游戏"""
    
    def setUp(self):
        self.game = PokerGame(
            player_names=["Alice", "Bob", "Charlie", "David", "Eve"],
            initial_chips=1000
        )
    
    def test_game_creation(self):
        self.assertEqual(len(self.game.players), 5)
        self.assertEqual(self.game.players[0].name, "Alice")
    
    def test_start_round(self):
        self.game.start_new_round()
        self.assertIsNotNone(self.game.current_round)
        # 检查每个玩家是否有2张牌
        for player in self.game.players:
            self.assertEqual(len(player.hole_cards), 2)
    
    def test_flop(self):
        self.game.start_new_round()
        self.game.current_round.flop()
        self.assertEqual(len(self.game.current_round.community_cards), 3)
    
    def test_turn(self):
        self.game.start_new_round()
        self.game.current_round.flop()
        self.game.current_round.turn()
        self.assertEqual(len(self.game.current_round.community_cards), 4)
    
    def test_river(self):
        self.game.start_new_round()
        self.game.current_round.flop()
        self.game.current_round.turn()
        self.game.current_round.river()
        self.assertEqual(len(self.game.current_round.community_cards), 5)

if __name__ == "__main__":
    unittest.main()
