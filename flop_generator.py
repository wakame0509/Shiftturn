import random
from itertools import combinations
from eval7 import Card

def generate_flops_by_type(flop_type, count=10):
    """
    指定されたフロップタイプに一致するフロップをランダムに count 個返す。
    """
    ranks = "23456789TJQKA"
    suits = "cdhs"
    all_cards = [Card(r + s) for r in ranks for s in suits]
    all_flops = list(combinations(all_cards, 3))

    def classify_flop(flop):
        ranks = sorted([c.rank for c in flop])
        suits = [c.suit for c in flop]
        unique_suits = set(suits)

        if len(set(ranks)) == 1:
            return 'Paired'
        if len(unique_suits) == 1:
            return 'Monotone'
        if len(unique_suits) == 3:
            return 'Rainbow'
        if 'A' in ranks:
            return 'Ace High'
        if set(ranks).issubset({'T', 'J', 'Q', 'K', 'A'}):
            return 'Broadway'
        if max([ord(r) for r in ranks]) - min([ord(r) for r in ranks]) <= 4:
            return 'Connected'
        if max([ord(r) for r in ranks]) <= ord('7'):
            return 'Low Dry'
        return 'Other'

    matched = [f for f in all_flops if classify_flop(f) == flop_type]
    random.shuffle(matched)
    return matched[:count]
