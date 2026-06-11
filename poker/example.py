"""
5人德州扑克游戏示例
"""

from game import PokerGame
from player import PlayerAction
import random

def print_game_state(game):
    """打印游戏状态"""
    print("\n" + "="*60)
    print(f"第 {game.round_number} 轮")
    print("="*60)
    
    state = game.get_game_state()
    
    if "current_round" in state:
        current_round = state["current_round"]
        print(f"\n底池: {current_round['pot']} 筹码")
        
        if current_round["community_cards"]:
            print(f"公牌: {' '.join(current_round['community_cards'])}")
        
        print("\n玩家状态:")
        for player_state in current_round["players"]:
            hole_cards = " ".join(player_state["hole_cards"]) if player_state["hole_cards"] else "已弃牌"
            print(f"  {player_state['name']}: {player_state['chips']}筹码 | 下注: {player_state['current_bet']} | 手牌: {hole_cards}")

def simple_ai_action(game, player_index):
    """简单AI决策"""
    player = game.players[player_index]
    current_round = game.current_round
    
    if not player.can_act():
        return
    
    # 随机选择行动
    current_bet_needed = current_round.current_bet_level - player.current_bet
    
    if current_bet_needed == 0:
        # 可以过牌或加注
        action = random.choice([PlayerAction.CHECK, PlayerAction.RAISE])
        if action == PlayerAction.RAISE:
            raise_amount = current_round.current_bet_level + 20
            game.player_action(player_index, action, raise_amount)
        else:
            game.player_action(player_index, action)
    else:
        # 需要跟注或弃牌或加注
        if random.random() < 0.7:  # 70%的概率跟注
            game.player_action(player_index, PlayerAction.CALL)
        else:
            game.player_action(player_index, PlayerAction.FOLD)

def play_betting_round(game, round_name):
    """进行一轮下注"""
    print(f"\n--- {round_name} ---")
    
    current_player_index = game.current_round.current_player_index
    
    while not game.is_betting_round_complete():
        next_player = game.current_round.get_next_active_player(current_player_index)
        if next_player is None:
            break
        
        current_player_index = next_player
        player = game.players[current_player_index]
        
        if not player.can_act():
            continue
        
        print(f"\n{player.name} 的行动...")
        simple_ai_action(game, current_player_index)
        
        current_player_index = (current_player_index + 1) % 5

def play_single_round(game):
    """玩一轮完整的游戏"""
    game.start_new_round()
    print_game_state(game)
    
    # Pre-flop
    play_betting_round(game, "前翻牌下注轮")
    
    if game.current_round.get_active_players_count() <= 1:
        winners = game.end_round()
        print_winners(winners)
        return
    
    # Flop
    game.current_round.flop()
    print_game_state(game)
    
    for player in game.players:
        player.reset_bet()
    game.current_round.current_bet_level = 0
    
    play_betting_round(game, "翻牌下注轮")
    
    if game.current_round.get_active_players_count() <= 1:
        winners = game.end_round()
        print_winners(winners)
        return
    
    # Turn
    game.current_round.turn()
    print_game_state(game)
    
    for player in game.players:
        player.reset_bet()
    game.current_round.current_bet_level = 0
    
    play_betting_round(game, "转牌下注轮")
    
    if game.current_round.get_active_players_count() <= 1:
        winners = game.end_round()
        print_winners(winners)
        return
    
    # River
    game.current_round.river()
    print_game_state(game)
    
    for player in game.players:
        player.reset_bet()
    game.current_round.current_bet_level = 0
    
    play_betting_round(game, "河牌下注轮")
    
    # Showdown
    winners = game.end_round()
    print_winners(winners)

def print_winners(winners):
    """打印赢家"""
    print("\n" + "-"*60)
    print("摊牌结果:")
    for winner, best_hand, (hand_rank, values) in winners:
        print(f"  {winner.name} 获胜！最好的手牌: {' '.join(str(card) for card in best_hand)}")
        print(f"    手牌类型: {hand_rank.name if hand_rank else '无'}")

def main():
    """主函数"""
    print("欢迎来到5人德州扑克游戏！")
    
    player_names = ["Alice", "Bob", "Charlie", "David", "Eve"]
    game = PokerGame(player_names, initial_chips=1000, small_blind=10, big_blind=20)
    
    # 玩几轮游戏
    for _ in range(5):
        if game.game_over:
            break
        
        try:
            play_single_round(game)
        except Exception as e:
            print(f"发生错误: {e}")
            break
        
        input("\n按Enter继续下一轮...")
    
    # 打印最终结果
    print("\n" + "="*60)
    print("游戏结束！最终筹码统计：")
    print("="*60)
    for player in game.players:
        print(f"{player.name}: {player.chips} 筹码")

if __name__ == "__main__":
    main()
