# 5人德州扑克游戏

一个完整的Python实现的5人德州扑克游戏引擎。

## 项目结构

```
poker/
├── card.py              # 扑克牌类定义
├── hand_evaluator.py    # 手牌评估器
├── player.py            # 玩家和游戏轮次
├── game.py              # 主游戏引擎
├── example.py           # 游戏示例脚本
└── README.md            # 本文件
```

## 功能特性

✅ 完整的德州扑克规则实现
- 标准手牌排名（从高牌到皇家同花顺）
- 正确的盲注和轮转系统
- 支持全压功能
- 自动最佳手牌评估

✅ 5人游戏支持
- 自动轮转按钮位置
- 正确的盲注计算
- 并列获胜处理

✅ 灵活的游戏流程
- 支持自定义初始筹码
- 可配置的小/大盲注
- 完整的游戏状态查询

## 快速开始

### 基本使用

```python
from game import PokerGame
from player import PlayerAction

# 创建游戏（5个玩家，初始1000筹码）
game = PokerGame(
    player_names=["Alice", "Bob", "Charlie", "David", "Eve"],
    initial_chips=1000,
    small_blind=10,
    big_blind=20
)

# 开始新一轮
game.start_new_round()

# 玩家操作
game.player_action(0, PlayerAction.CALL)  # 玩家0跟注
game.player_action(1, PlayerAction.RAISE, 50)  # 玩家1加注到50
game.player_action(2, PlayerAction.FOLD)  # 玩家2弃牌

# 发翻牌
game.current_round.flop()

# 结束一轮，确定赢家
winners = game.end_round()
for winner, best_hand, (hand_rank, values) in winners:
    print(f"{winner.name} 获胜!")
```

### 运行示例游戏

```bash
cd poker
python example.py
```

## 核心类说明

### Card（扑克牌）
代表一张扑克牌。

```python
from card import Card, Suit, Rank

card = Card(Suit.HEARTS, Rank.ACE)
print(card)  # A♥
```

### Deck（牌堆）
管理52张牌的标准牌堆。

```python
from card import Deck

deck = Deck()
deck.shuffle()
card = deck.draw()
```

### Player（玩家）
代表游戏中的一个玩家。

```python
from player import Player

player = Player(0, "Alice", 1000)
player.place_bet(50)  # 下注50
```

### GameRound（游戏轮次）
管理单一轮次的游戏状态。

```python
from player import GameRound

round = GameRound(players, small_blind=10, big_blind=20)
round.setup_round()  # 初始化
round.flop()  # 发翻牌
round.turn()  # 发转牌
round.river()  # 发河牌
```

### HandEvaluator（手牌评估器）
评估5张牌的手牌等级。

```python
from hand_evaluator import HandEvaluator

best_hand, (rank, values) = HandEvaluator.evaluate_hand(cards)
print(f"手牌类型: {rank.name}")
```

### PokerGame（主游戏）
完整的游戏管理。

```python
from game import PokerGame

game = PokerGame(player_names, initial_chips=1000)
game.start_new_round()

# 进行下注
winners = game.end_round()
```

## 玩家操作（PlayerAction）

- **FOLD**: 弃牌 - 退出当前轮次
- **CHECK**: 过牌 - 不下注但继续游戏（仅当没有更高下注时）
- **CALL**: 跟注 - 跟随当前最高下注
- **RAISE**: 加注 - 增加下注额度
- **ALL_IN**: 全压 - 投入所有筹码

## 手牌等级（从低到高）

1. **HIGH_CARD** - 高牌
2. **ONE_PAIR** - 一对
3. **TWO_PAIR** - 两对
4. **THREE_OF_A_KIND** - 三条
5. **STRAIGHT** - 顺子
6. **FLUSH** - 同花
7. **FULL_HOUSE** - 葫芦（三条+一对）
8. **FOUR_OF_A_KIND** - 四条
9. **STRAIGHT_FLUSH** - 顺子同花
10. **ROYAL_FLUSH** - 皇家同花顺（10-J-Q-K-A同花）

## 游戏流程

1. **初始化**: 创建5个玩家，分配初始筹码
2. **开始一轮**: 
   - 轮转按钮位置
   - 计算小盲注和大盲注位置
   - 发两张底牌
3. **前翻牌下注轮**: 从大盲注后的玩家开始
4. **翻牌**: 发3张公牌，继续下注
5. **转牌**: 再发1张公牌，继续下注
6. **河牌**: 最后发1张公牌，继续下注
7. **摊牌**: 比较手牌，分配底池
8. **重复**: 进行下一轮

## 算法说明

### 手牌评估
使用组合算法从7张牌（2张底牌 + 5张公牌）中找出最好的5张牌组合。

### 手牌比较
按等级排序，相同等级按具体数值比较（如两个都是一对，比较对牌大小，再比较踢脚牌）。

### 并列处理
多个玩家手牌相同时，等分底池。

## 拓展建议

- 添加GUI界面（使用Tkinter或PyQt）
- 实现不同难度的AI对手
- 添加游戏统计和分析
- 支持网络多人游戏
- 添加游戏重放功能
- 支持不同的下注结构（无限制、底池限制等）

## 许可证

MIT

## 贡献

欢迎提交问题和拉取请求！
