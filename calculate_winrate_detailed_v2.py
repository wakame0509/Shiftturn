import eval7
from collections import defaultdict
import pandas as pd
from itertools import combinations
import random

def get_all_turn_cards(used_cards):
    full_deck = [eval7.Card(str_rank + suit) for str_rank in "23456789TJQKA" for suit in "shdc"]
    return [card for card in full_deck if card not in used_cards]

def evaluate_vs_opponent(hero_hand, board, opponent_combos):
    hero = [eval7.Card(c) for c in hero_hand]
    board_cards = [eval7.Card(c) for c in board]
    hero_hand_full = hero + board_cards
    hero_val = eval7.evaluate(hero_hand_full)

    wins, ties, total = 0, 0, 0
    for opp in opponent_combos:
        opp_cards = [eval7.Card(c) for c in opp]
        if set(hero) & set(opp_cards):
            continue
        opp_hand_full = opp_cards + board_cards
        opp_val = eval7.evaluate(opp_hand_full)
        if hero_val > opp_val:
            wins += 1
        elif hero_val == opp_val:
            ties += 1
        total += 1

    return (wins + 0.5 * ties) / total if total else 0.0

def simulate_shift_turn_average(hand, flop_list, opponent_combos):
    from hand_utils import expand_hand  # ※別ファイルで定義されたハンド展開関数を使う想定

    hero_hands = expand_hand(hand)  # [[Ah, Kh], [Ad, Kd], ...] など
    results = []

    for flop_str in flop_list:
        flop = flop_str.split()
        for hero in hero_hands:
            base_board = flop.copy()
            used = set(hero + flop)
            turn_cards = get_all_turn_cards([eval7.Card(c) for c in used])
            base_winrates = {}
            for turn in turn_cards:
                board = flop + [str(turn)]
                winrate = evaluate_vs_opponent(hero, board, opponent_combos)
                base_winrates[str(turn)] = winrate
            avg_winrate = sum(base_winrates.values()) / len(base_winrates)
            shift_diffs = {card: (wr - avg_winrate) for card, wr in base_winrates.items()}
            sorted_shifts = sorted(shift_diffs.items(), key=lambda x: x[1], reverse=True)
            top10 = sorted_shifts[:10]
            bottom10 = sorted_shifts[-10:]
            for card, diff in top10 + bottom10:
                results.append({
                    "Flop": " ".join(flop),
                    "HeroHand": f"{hero[0]} {hero[1]}",
                    "Card": card,
                    "Diff": round(diff * 100, 2)
                })

    return pd.DataFrame(results)
