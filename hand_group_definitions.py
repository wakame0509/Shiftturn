def classify_hand(hand_str):
    """
    ハンド文字列（例: "AKs", "TT", "QJo"）をグループ名に分類
    """
    pairs = ['AA', 'KK', 'QQ', 'JJ', 'TT', '99', '88', '77', '66', '55', '44', '33', '22']
    high_cards = ['A', 'K', 'Q', 'J', 'T']
    connectors = ['AK', 'KQ', 'QJ', 'JT', 'T9', '98', '87', '76', '65', '54']

    if hand_str in pairs:
        rank = hand_str[0]
        if rank in ['A', 'K', 'Q']:
            return 'High Pair'
        elif rank in ['J', 'T', '9']:
            return 'Middle Pair'
        else:
            return 'Low Pair'

    offsuit = hand_str.endswith('o')
    suited = hand_str.endswith('s')
    offsuit_or_suited = offsuit or suited

    base = hand_str[:2]

    if base in connectors and suited:
        return 'Suited Connector'
    if base in connectors and offsuit:
        return 'Offsuit Connector'
    if base[0] in high_cards and base[1] in high_cards:
        return 'Broadway'
    if suited:
        return 'Other Suited'
    if offsuit:
        return 'Other Offsuit'
    return 'Other'
