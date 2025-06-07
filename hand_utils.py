# hand_utils.py

# 169通りのスターティングハンドを定義（"AKs", "AQo", など）
all_starting_hands = [
    f"{r1}{r2}s" if i < j else f"{r2}{r1}o" if i > j else f"{r1}{r2}"
    for i, r1 in enumerate("AKQJT98765432")
    for j, r2 in enumerate("AKQJT98765432")
    if i <= j
]

# 例: "AKs" → ["Ah", "Kh"]
def convert_hand_to_cards(hand_notation):
    ranks = "AKQJT98765432"
    suits = ['h', 'd', 'c', 's']
    r1, r2 = hand_notation[0], hand_notation[1]
    suited = hand_notation.endswith('s')
    offsuit = hand_notation.endswith('o')
    
    if suited:
        return [r1 + 'h', r2 + 'h']
    elif offsuit:
        return [r1 + 'h', r2 + 'd']  # 違うスート
    else:
        return [r1 + 'h', r2 + 'd'] if r1 != r2 else [r1 + 'h', r1 + 'd']
