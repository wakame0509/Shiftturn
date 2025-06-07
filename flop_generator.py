import itertools
import random

ranks = '23456789TJQKA'
suits = 'hdcs'

def generate_flops_by_type(hero_cards, flop_type):
    """
    フロップタイプに応じたフロップ候補全通りを生成
    """
    all_cards = [r + s for r in ranks for s in suits]
    used = set(hero_cards)
    deck = [c for c in all_cards if c not in used]

    flop_combos = []

    for flop in itertools.combinations(deck, 3):
        if is_flop_type(flop, flop_type):
            flop_combos.append(list(flop))

    return flop_combos

def is_flop_type(flop, flop_type):
    """
    各フロップが指定されたタイプに合致するかを判定
    """
    ranks_in_flop = [card[0] for card in flop]
    suits_in_flop = [card[1] for card in flop]

    unique_ranks = set(ranks_in_flop)
    unique_suits = set(suits_in_flop)

    if flop_type == "High Card Rainbow":
        return len(unique_ranks) == 3 and len(unique_suits) == 3

    elif flop_type == "Paired Board":
        return len(unique_ranks) == 2

    elif flop_type == "Suited Two Tone":
        return any(suits_in_flop.count(suit) == 2 for suit in unique_suits)

    elif flop_type == "Connected Low":
        values = sorted([rank_to_value(r) for r in ranks_in_flop])
        return values[2] - values[0] <= 4 and max(values) <= 9

    elif flop_type == "1 Hit + 2 Flush Draw":
        return len(unique_ranks) == 3 and any(suits_in_flop.count(s) == 2 for s in unique_suits)

    elif flop_type == "No Hit":
        return True  # 任意の3枚（とりあえず条件なし）

    elif flop_type == "Straight Possible":
        values = sorted([rank_to_value(r) for r in ranks_in_flop])
        return values[2] - values[0] == 2 or values[2] - values[0] == 3

    return False

def rank_to_value(r):
    return {'2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7,
            '8': 8, '9': 9, 'T': 10, 'J': 11, 'Q': 12, 'K': 13, 'A': 14}[r]
