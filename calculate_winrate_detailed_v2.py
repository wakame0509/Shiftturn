import eval7
from opponent_hands_25_range import opponent_hand_combos

def evaluate_hand(hand, board):
    full_hand = hand + board
    full_eval = [eval7.Card(c) for c in full_hand]
    return eval7.evaluate(full_eval)

def simulate_winrate_vs_opponent(hero_cards, board):
    hero = [eval7.Card(c) for c in hero_cards]
    board_cards = [eval7.Card(c) for c in board]

    wins = 0
    ties = 0
    total = 0

    for opp_combo in opponent_hand_combos:
        if any(c in hero_cards + board for c in opp_combo):
            continue

        opp = [eval7.Card(c) for c in opp_combo]

        hero_val = eval7.evaluate(hero + board_cards)
        opp_val = eval7.evaluate(opp + board_cards)

        if hero_val > opp_val:
            wins += 1
        elif hero_val == opp_val:
            ties += 1
        total += 1

    if total == 0:
        return 0.0
    return (wins + ties * 0.5) / total

def simulate_shift_turn(hero_cards, flop_cards):
    """
    ターンカードごとに 1枚ずつ全て追加し、数え上げ法で勝率を計算（高速・正確）
    """
    all_cards = [r + s for r in '23456789TJQKA' for s in 'cdhs']
    used = set(hero_cards + flop_cards)
    turn_candidates = [c for c in all_cards if c not in used]

    results = []

    for turn_card in turn_candidates:
        board = flop_cards + [turn_card]
        winrate = simulate_winrate_vs_opponent(hero_cards, board)
        results.append({
            "flop": flop_cards,
            "turn": turn_card,
            "winrate": round(winrate * 100, 2),
            "shift": 0.0  # プリフロップ勝率と比較はアプリ側で
        })

    return results
