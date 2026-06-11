from typing import List, Tuple
from enum import Enum
from card import Card, Rank

class HandRank(Enum):
    """德州扑克手牌等级"""
    HIGH_CARD = 0
    ONE_PAIR = 1
    TWO_PAIR = 2
    THREE_OF_A_KIND = 3
    STRAIGHT = 4
    FLUSH = 5
    FULL_HOUSE = 6
    FOUR_OF_A_KIND = 7
    STRAIGHT_FLUSH = 8
    ROYAL_FLUSH = 9

class HandEvaluator:
    """手牌评估器"""
    
    @staticmethod
    def evaluate_hand(cards: List[Card]) -> Tuple[HandRank, List[int]]:
        """
        评估手牌等级
        返回: (手牌等级, 比较值列表)
        """
        if len(cards) != 5:
            raise ValueError("必须有5张牌")
        
        # 检查各种牌型
        if HandEvaluator.is_royal_flush(cards):
            return (HandRank.ROYAL_FLUSH, [14])
        elif HandEvaluator.is_straight_flush(cards):
            return (HandRank.STRAIGHT_FLUSH, HandEvaluator.get_straight_high_card(cards))
        elif HandEvaluator.is_four_of_a_kind(cards):
            return (HandRank.FOUR_OF_A_KIND, HandEvaluator.get_four_of_a_kind_values(cards))
        elif HandEvaluator.is_full_house(cards):
            return (HandRank.FULL_HOUSE, HandEvaluator.get_full_house_values(cards))
        elif HandEvaluator.is_flush(cards):
            return (HandRank.FLUSH, HandEvaluator.get_flush_values(cards))
        elif HandEvaluator.is_straight(cards):
            return (HandRank.STRAIGHT, HandEvaluator.get_straight_high_card(cards))
        elif HandEvaluator.is_three_of_a_kind(cards):
            return (HandRank.THREE_OF_A_KIND, HandEvaluator.get_three_of_a_kind_values(cards))
        elif HandEvaluator.is_two_pair(cards):
            return (HandRank.TWO_PAIR, HandEvaluator.get_two_pair_values(cards))
        elif HandEvaluator.is_one_pair(cards):
            return (HandRank.ONE_PAIR, HandEvaluator.get_one_pair_values(cards))
        else:
            return (HandRank.HIGH_CARD, HandEvaluator.get_high_card_values(cards))
    
    @staticmethod
    def get_rank_counts(cards: List[Card]) -> dict:
        """获取每个等级的数量"""
        counts = {}
        for card in cards:
            counts[card.rank.value] = counts.get(card.rank.value, 0) + 1
        return counts
    
    @staticmethod
    def is_flush(cards: List[Card]) -> bool:
        """是否是同花"""
        suits = [card.suit for card in cards]
        return len(set(suits)) == 1
    
    @staticmethod
    def is_straight(cards: List[Card]) -> bool:
        """是否是顺子"""
        ranks = sorted([card.rank.value for card in cards])
        # 检查普通顺子
        if ranks[-1] - ranks[0] == 4 and len(set(ranks)) == 5:
            return True
        # 检查A-2-3-4-5 (轮顺)
        if ranks == [2, 3, 4, 5, 14]:
            return True
        return False
    
    @staticmethod
    def is_one_pair(cards: List[Card]) -> bool:
        """是否是一对"""
        counts = HandEvaluator.get_rank_counts(cards)
        return list(counts.values()).count(2) == 1
    
    @staticmethod
    def is_two_pair(cards: List[Card]) -> bool:
        """是否是两对"""
        counts = HandEvaluator.get_rank_counts(cards)
        return list(counts.values()).count(2) == 2
    
    @staticmethod
    def is_three_of_a_kind(cards: List[Card]) -> bool:
        """是否是三条"""
        counts = HandEvaluator.get_rank_counts(cards)
        return 3 in counts.values()
    
    @staticmethod
    def is_full_house(cards: List[Card]) -> bool:
        """是否是葫芦（三条+一对）"""
        counts = HandEvaluator.get_rank_counts(cards)
        values = sorted(counts.values())
        return values == [2, 3]
    
    @staticmethod
    def is_four_of_a_kind(cards: List[Card]) -> bool:
        """是否是四条"""
        counts = HandEvaluator.get_rank_counts(cards)
        return 4 in counts.values()
    
    @staticmethod
    def is_straight_flush(cards: List[Card]) -> bool:
        """是否是顺子同花"""
        return HandEvaluator.is_straight(cards) and HandEvaluator.is_flush(cards)
    
    @staticmethod
    def is_royal_flush(cards: List[Card]) -> bool:
        """是否是皇家同花顺"""
        if not HandEvaluator.is_straight_flush(cards):
            return False
        ranks = sorted([card.rank.value for card in cards])
        return ranks == [10, 11, 12, 13, 14]
    
    @staticmethod
    def get_straight_high_card(cards: List[Card]) -> List[int]:
        """获取顺子的最高牌"""
        ranks = sorted([card.rank.value for card in cards])
        if ranks == [2, 3, 4, 5, 14]:  # 轮顺，最高是5
            return [5]
        return [ranks[-1]]
    
    @staticmethod
    def get_high_card_values(cards: List[Card]) -> List[int]:
        """获取最高牌的值"""
        return sorted([card.rank.value for card in cards], reverse=True)
    
    @staticmethod
    def get_one_pair_values(cards: List[Card]) -> List[int]:
        """获取一对的值"""
        counts = HandEvaluator.get_rank_counts(cards)
        pair_rank = [rank for rank, count in counts.items() if count == 2][0]
        kickers = sorted([rank for rank in counts.keys() if rank != pair_rank], reverse=True)
        return [pair_rank] + kickers
    
    @staticmethod
    def get_two_pair_values(cards: List[Card]) -> List[int]:
        """获取两对的值"""
        counts = HandEvaluator.get_rank_counts(cards)
        pairs = sorted([rank for rank, count in counts.items() if count == 2], reverse=True)
        kicker = [rank for rank, count in counts.items() if count == 1][0]
        return pairs + [kicker]
    
    @staticmethod
    def get_three_of_a_kind_values(cards: List[Card]) -> List[int]:
        """获取三条的值"""
        counts = HandEvaluator.get_rank_counts(cards)
        three_rank = [rank for rank, count in counts.items() if count == 3][0]
        kickers = sorted([rank for rank in counts.keys() if rank != three_rank], reverse=True)
        return [three_rank] + kickers
    
    @staticmethod
    def get_full_house_values(cards: List[Card]) -> List[int]:
        """获取葫芦的值"""
        counts = HandEvaluator.get_rank_counts(cards)
        three_rank = [rank for rank, count in counts.items() if count == 3][0]
        pair_rank = [rank for rank, count in counts.items() if count == 2][0]
        return [three_rank, pair_rank]
    
    @staticmethod
    def get_four_of_a_kind_values(cards: List[Card]) -> List[int]:
        """获取四条的值"""
        counts = HandEvaluator.get_rank_counts(cards)
        four_rank = [rank for rank, count in counts.items() if count == 4][0]
        kicker = [rank for rank in counts.keys() if rank != four_rank][0]
        return [four_rank, kicker]
    
    @staticmethod
    def get_flush_values(cards: List[Card]) -> List[int]:
        """获取同花的值"""
        return sorted([card.rank.value for card in cards], reverse=True)
