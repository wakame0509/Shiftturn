import random

suits = ['h', 'd', 'c', 's']

def expand_hand_to_specific_cards(hand_name):
    """
    "AKs" → ["Ah", "Kh"] のようにスート付き2枚に展開（ランダム）
    """
    if len(hand_name) == 2:  # ペア
        rank = hand_name[0]
        s1, s2 = random.sample(suits, 2)
        return [rank + s1, rank + s2]
    
    r1, r2, suited = hand_name[0], hand_name[1], hand_name[2]
    if suited == 's':
        s = random.choice(suits)
        return [r1 + s, r2 + s]
    elif suited == 'o':
        while True:
            s1, s2 = random.sample(suits, 2)
            if s1 != s2:
                return [r1 + s1, r2 + s2]
    else:
        raise ValueError(f"Invalid hand notation: {hand_name}")

def format_flop(flop_cards):
    """
    ["7h", "Qd", "Td"] → "7h Qd Td" のように文字列へ整形
    """
    return " ".join(flop_cards)

def format_hand(card1, card2):
    """
    ["Ah", "Kh"] → "AhKh"
    """
    return card1 + card2
