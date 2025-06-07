# shift_river_utils.py

import random
from itertools import combinations

ranks = '23456789TJQKA'
suits = 'hdcs'

def generate_all_flops():
    """デッキからすべてのフロップ（3枚）を生成"""
    deck = [r + s for r in ranks for s in suits]
    return list(combinations(deck, 3))

def generate_flops_by_type(hero_cards, flop_type, count=10):
    """指定されたフロップタイプに合致するフロップを指定数ランダム抽出"""
    all_flops = generate_all_flops()

    def classify_flop(flop):
        ranks_only = [card[0] for card in flop]
        suits_only = [card[1] for card in flop]

        unique_ranks = set(ranks_only)
        unique_suits = set(suits_only)

        is_connected = max([ord(r) for r in ranks_only]) - min([ord(r) for r in ranks_only]) <= 4
        is_suited = len(unique_suits) == 1
        is_rainbow = len(unique_suits) == 3
        is_paired = len(unique_ranks) == 2 or len(unique_ranks) == 1

        if is_paired:
            return "Paired"
        elif is_suited:
            return "Suited"
        elif is_connected:
            return "Connected"
        elif is_rainbow:
            return "Rainbow"
        else:
            return "Other"

    # 対象タイプに一致するフロップ候補
    matched = [f for f in all_flops if classify_flop(f) == flop_type and not any(c in f for c in hero_cards)]

    # ランダムに指定数抽出
    return random.sample(matched, min(count, len(matched)))
