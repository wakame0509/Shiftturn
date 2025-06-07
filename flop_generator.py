# flop_generator.py

import random
from itertools import combinations

RANK_ORDER = {'2': 2, '3': 3, '4': 4, '5': 5, '6': 6,
              '7': 7, '8': 8, '9': 9, 'T': 10,
              'J': 11, 'Q': 12, 'K': 13, 'A': 14}

def classify_flop(flop):
    suits = [card[1] for card in flop]
    ranks = [card[0] for card in flop]
    rank_values = [RANK_ORDER[r] for r in ranks]

    is_monotone = suits.count(suits[0]) == 3
    is_two_tone = len(set(suits)) == 2
    is_rainbow = len(set(suits)) == 3
    is_connected = max(rank_values) - min(rank_values) <= 4

    if is_monotone and is_connected:
        return 'Connected Monotone'
    elif is_rainbow and is_connected:
        return 'Connected Rainbow'
    elif is_two_tone and is_connected:
        return 'Connected Two-tone'
    elif is_monotone:
        return 'Monotone'
    elif is_rainbow:
        return 'Rainbow'
    elif is_two_tone:
        return 'Two-tone'
    else:
        return 'Other'

def generate_all_flops(hero_cards):
    deck = [r + s for r in '23456789TJQKA' for s in 'cdhs']
    used = set(hero_cards)
    deck = [card for card in deck if card not in used]
    return list(combinations(deck, 3))

def generate_flops_by_type(hero_cards, flop_type, count=10):
    all_flops = generate_all_flops(hero_cards)
    matched = [f for f in all_flops if classify_flop(f) == flop_type]
    if len(matched) <= count:
        return matched
    return random.sample(matched, count)
