from typing import List, Dict, Tuple, Optional
from card import Card
from player import Player, GameRound, PlayerAction
from hand_evaluator import HandEvaluator
import itertools

class PokerGame:
    """德州扑克游戏主类（5人游戏）"""
    
    def __init__(self, player_names: List[str], initial_chips: int = 1000, small_blind: int = 10, big_blind: int = 20):
        """
        初始化游戏
        参数:
            player_names: 玩家名称列表（必须是5个）
            initial_chips: 初始筹码
            small_blind: 小盲注
            big_blind: 大盲注
        """
        if len(player_names) != 5:
            raise ValueError("德州扑克必须是5个玩家")
        
        self.players: List[Player] = [
            Player(i, player_names[i], initial_chips) 
            for i in range(5)
        ]
        self.small_blind = small_blind
        self.big_blind = big_blind
        self.current_round: Optional[GameRound] = None
        self.round_number = 0
        self.game_over = False
    
    def start_new_round(self):
        """开始新一轮游戏"""
        # 检查游戏是否结束
        active_players = [p for p in self.players if p.chips > 0]
        if len(active_players) == 1:
            self.game_over = True
            return
        
        self.round_number += 1
        
        # 轮转Button位置
        button_position = (self.round_number - 1) % 5
        
        self.current_round = GameRound(self.players, self.small_blind, self.big_blind)
        self.current_round.button_position = button_position
        self.current_round.small_blind_position = (button_position + 1) % 5
        self.current_round.big_blind_position = (button_position + 2) % 5
        self.current_round.current_player_index = (button_position + 3) % 5
        
        self.current_round.setup_round()
    
    def player_action(self, player_index: int, action: PlayerAction, amount: int = 0) -> bool:
        """
        玩家执行操作
        返回: 操作是否成功
        """
        if not self.current_round:
            return False
        
        player = self.players[player_index]
        
        if action == PlayerAction.FOLD:
            player.fold()
        elif action == PlayerAction.CHECK:
            if player.current_bet < self.current_round.current_bet_level:
                return False  # 不能过牌，有更高的下注
        elif action == PlayerAction.CALL:
            call_amount = self.current_round.current_bet_level - player.current_bet
            bet_amount = player.place_bet(call_amount)
            self.current_round.pot += bet_amount
        elif action == PlayerAction.RAISE:
            if amount <= self.current_round.current_bet_level:
                return False  # 加注金额必须高于当前下注
            
            total_bet_needed = amount
            current_debt = total_bet_needed - player.current_bet
            bet_amount = player.place_bet(current_debt)
            self.current_round.pot += bet_amount
            self.current_round.current_bet_level = amount
        elif action == PlayerAction.ALL_IN:
            bet_amount = player.place_bet(player.chips)
            self.current_round.pot += bet_amount
            if bet_amount > self.current_round.current_bet_level - player.current_bet:
                self.current_round.current_bet_level = player.current_bet
        
        return True
    
    def get_best_five_cards(self, hole_cards: List[Card], community_cards: List[Card]) -> Tuple[List[Card], Tuple]:
        """
        从7张牌中获取最好的5张牌组合
        返回: (最好的5张牌, (手牌等级, 比较值))
        """
        all_cards = hole_cards + community_cards
        best_hand = None
        best_rank = None
        best_values = None
        
        # 获取所有5张牌的组合
        for five_cards in itertools.combinations(all_cards, 5):
            rank, values = HandEvaluator.evaluate_hand(list(five_cards))
            
            if best_rank is None:
                best_hand = list(five_cards)
                best_rank = rank
                best_values = values
            else:
                # 比较两个手牌
                if rank.value > best_rank.value:
                    best_hand = list(five_cards)
                    best_rank = rank
                    best_values = values
                elif rank.value == best_rank.value:
                    # 同等级，比较具体值
                    if values > best_values:
                        best_hand = list(five_cards)
                        best_rank = rank
                        best_values = values
        
        return best_hand, (best_rank, best_values)
    
    def determine_winners(self) -> List[Tuple[Player, List[Card], Tuple]]:
        """
        确定获胜者
        返回: [(玩家, 最好的5张牌, (手牌等级, 比较值)), ...]
        """
        if not self.current_round:
            return []
        
        # 获取未弃牌的玩家
        active_players = [p for p in self.players if not p.is_folded]
        
        if len(active_players) == 1:
            # 只有一个玩家未弃牌，他赢了
            return [(active_players[0], active_players[0].hole_cards, (None, None))]
        
        # 评估每个玩家的手牌
        player_hands: List[Tuple[Player, List[Card], Tuple]] = []
        for player in active_players:
            best_hand, rank_info = self.get_best_five_cards(
                player.hole_cards,
                self.current_round.community_cards
            )
            player_hands.append((player, best_hand, rank_info))
        
        # 排序，最好的手牌在前面
        player_hands.sort(key=lambda x: (x[2][0].value, x[2][1]), reverse=True)
        
        # 检查是否有并列
        winners = [player_hands[0]]
        if len(player_hands) > 1:
            for i in range(1, len(player_hands)):
                if player_hands[i][2] == player_hands[0][2]:
                    winners.append(player_hands[i])
                else:
                    break
        
        return winners
    
    def end_round(self):
        """结束当前一轮"""
        winners = self.determine_winners()
        
        # 分配底池
        if winners:
            share = self.current_round.pot // len(winners)
            remainder = self.current_round.pot % len(winners)
            
            for i, (winner, _, _) in enumerate(winners):
                chips_won = share + (1 if i == 0 else 0)  # 余数分配给第一个赢家
                winner.chips += chips_won
        
        return winners
    
    def get_game_state(self) -> dict:
        """获取完整游戏状态"""
        if not self.current_round:
            return {
                "round_number": self.round_number,
                "game_over": self.game_over,
                "players": [{"name": p.name, "chips": p.chips} for p in self.players]
            }
        
        return {
            "round_number": self.round_number,
            "game_over": self.game_over,
            "current_round": self.current_round.get_game_state(),
            "small_blind": self.small_blind,
            "big_blind": self.big_blind
        }
    
    def is_betting_round_complete(self) -> bool:
        """检查下注轮是否完成"""
        if not self.current_round:
            return False
        
        active_players = [p for p in self.players if not p.is_folded and not p.is_all_in]
        
        if len(active_players) <= 1:
            return True  # 只有0或1个玩家还在游戏中
        
        # 检查是否所有玩家都跟注了当前下注或已全压
        current_bet = self.current_round.current_bet_level
        for player in active_players:
            if player.current_bet < current_bet:
                return False
        
        return True
