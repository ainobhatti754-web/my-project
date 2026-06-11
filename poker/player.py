from typing import List, Optional
from enum import Enum
from card import Card, Deck

class PlayerAction(Enum):
    """玩家行动"""
    FOLD = "弃牌"
    CHECK = "过牌"
    CALL = "跟注"
    RAISE = "加注"
    ALL_IN = "全压"

class Player:
    """玩家类"""
    def __init__(self, player_id: int, name: str, initial_chips: int):
        self.player_id = player_id
        self.name = name
        self.chips = initial_chips
        self.hole_cards: List[Card] = []
        self.current_bet = 0
        self.total_bet_this_round = 0
        self.is_folded = False
        self.is_all_in = False
    
    def receive_card(self, card: Card):
        """接收一张牌"""
        self.hole_cards.append(card)
    
    def clear_hand(self):
        """清空手牌"""
        self.hole_cards = []
    
    def place_bet(self, amount: int) -> int:
        """下注，返回实际下注额"""
        if amount >= self.chips:
            actual_bet = self.chips
            self.chips = 0
            self.is_all_in = True
        else:
            actual_bet = amount
            self.chips -= amount
        
        self.current_bet += actual_bet
        self.total_bet_this_round += actual_bet
        return actual_bet
    
    def reset_bet(self):
        """重置当前下注"""
        self.current_bet = 0
    
    def reset_round(self):
        """重置一轮"""
        self.current_bet = 0
        self.total_bet_this_round = 0
        self.is_folded = False
        self.is_all_in = False
    
    def fold(self):
        """弃牌"""
        self.is_folded = True
    
    def is_active(self) -> bool:
        """是否还在游戏中"""
        return not self.is_folded and self.chips > 0
    
    def can_act(self) -> bool:
        """是否可以行动"""
        return not self.is_folded and not self.is_all_in
    
    def __str__(self):
        status = []
        if self.is_folded:
            status.append("已弃牌")
        if self.is_all_in:
            status.append("全压")
        status_str = f" [{', '.join(status)}]" if status else ""
        return f"{self.name}: {self.chips}筹码{status_str}"

class GameRound:
    """游戏一轮"""
    def __init__(self, players: List[Player], small_blind: int, big_blind: int):
        self.players = players
        self.small_blind = small_blind
        self.big_blind = big_blind
        self.deck = Deck()
        self.community_cards: List[Card] = []
        self.current_bet_level = 0
        self.pot = 0
        self.button_position = 0
        self.small_blind_position = 1
        self.big_blind_position = 2
        self.current_player_index = 3  # 第一个行动的玩家
    
    def setup_round(self):
        """设置一轮游戏"""
        # 清空所有玩家的状态
        for player in self.players:
            player.clear_hand()
            player.reset_round()
        
        # 洗牌
        self.deck.shuffle()
        self.community_cards = []
        self.pot = 0
        self.current_bet_level = self.big_blind
        
        # 发盲注
        self.post_blinds()
        
        # 发底牌
        for _ in range(2):
            for player in self.players:
                player.receive_card(self.deck.draw())
    
    def post_blinds(self):
        """发盲注"""
        # 小盲注
        small_blind_bet = self.players[self.small_blind_position].place_bet(self.small_blind)
        self.pot += small_blind_bet
        
        # 大盲注
        big_blind_bet = self.players[self.big_blind_position].place_bet(self.big_blind)
        self.pot += big_blind_bet
    
    def get_next_active_player(self, start_index: int) -> Optional[int]:
        """获取下一个还在游戏中的玩家索引"""
        for i in range(len(self.players)):
            player_index = (start_index + i) % len(self.players)
            if self.players[player_index].can_act():
                return player_index
        return None
    
    def get_active_players_count(self) -> int:
        """获取还在游戏中的玩家数"""
        return sum(1 for player in self.players if not player.is_folded)
    
    def flop(self):
        """翻牌（发3张社区牌）"""
        self.deck.draw()  # 烧一张牌
        for _ in range(3):
            self.community_cards.append(self.deck.draw())
    
    def turn(self):
        """转牌（发第4张社区牌）"""
        self.deck.draw()  # 烧一张牌
        self.community_cards.append(self.deck.draw())
    
    def river(self):
        """河牌（发第5张社区牌）"""
        self.deck.draw()  # 烧一张牌
        self.community_cards.append(self.deck.draw())
    
    def get_game_state(self) -> dict:
        """获取游戏状态"""
        return {
            "pot": self.pot,
            "community_cards": [str(card) for card in self.community_cards],
            "current_bet_level": self.current_bet_level,
            "players": [
                {
                    "id": player.player_id,
                    "name": player.name,
                    "chips": player.chips,
                    "current_bet": player.current_bet,
                    "hole_cards": [str(card) for card in player.hole_cards] if not player.is_folded else [],
                    "is_folded": player.is_folded,
                    "is_all_in": player.is_all_in
                }
                for player in self.players
            ]
        }
