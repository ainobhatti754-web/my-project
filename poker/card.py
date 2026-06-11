from enum import Enum
from typing import List, Tuple

class Suit(Enum):
    """扑克牌花色"""
    HEARTS = '♥'
    DIAMONDS = '♦'
    CLUBS = '♣'
    SPADES = '♠'

class Rank(Enum):
    """扑克牌等级"""
    TWO = 2
    THREE = 3
    FOUR = 4
    FIVE = 5
    SIX = 6
    SEVEN = 7
    EIGHT = 8
    NINE = 9
    TEN = 10
    JACK = 11
    QUEEN = 12
    KING = 13
    ACE = 14

class Card:
    """扑克牌类"""
    def __init__(self, suit: Suit, rank: Rank):
        self.suit = suit
        self.rank = rank
    
    def __str__(self):
        rank_names = {
            2: '2', 3: '3', 4: '4', 5: '5', 6: '6', 7: '7', 8: '8', 9: '9', 10: '10',
            11: 'J', 12: 'Q', 13: 'K', 14: 'A'
        }
        return f"{rank_names[self.rank.value]}{self.suit.value}"
    
    def __repr__(self):
        return self.__str__()
    
    def __eq__(self, other):
        if not isinstance(other, Card):
            return False
        return self.suit == other.suit and self.rank == other.rank
    
    def __hash__(self):
        return hash((self.suit.value, self.rank.value))

class Deck:
    """扑克牌堆"""
    def __init__(self):
        self.cards: List[Card] = []
        self.reset()
    
    def reset(self):
        """重置牌堆"""
        self.cards = []
        for suit in Suit:
            for rank in Rank:
                self.cards.append(Card(suit, rank))
    
    def shuffle(self):
        """洗牌"""
        import random
        random.shuffle(self.cards)
    
    def draw(self) -> Card:
        """抽一张牌"""
        if not self.cards:
            raise ValueError("牌堆为空")
        return self.cards.pop()
    
    def __len__(self):
        return len(self.cards)
