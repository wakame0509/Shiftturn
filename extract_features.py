# extract_features.py

def extract_features_for_turn(flop, turn, hero_hand):
    features = []

    ranks = '23456789TJQKA'
    flop_ranks = [card[0] for card in flop]
    flop_suits = [card[1] for card in flop]
    turn_rank = turn[0]
    turn_suit = turn[1]

    # Set完成（フロップでワンペア→ターンでセット）
    if any(flop_ranks.count(rank) == 2 and turn_rank == rank for rank in flop_ranks):
        features.append("Set完成")

    # フラッシュ完成
    all_suits = flop_suits + [turn_suit]
    for suit in 'hdcs':
        if all_suits.count(suit) >= 5:
            features.append("Flush完成")
            break

    # ストレート完成（かなり単純なチェック）
    all_ranks = flop_ranks + [turn_rank]
    unique_ranks = sorted(set([ranks.index(r) for r in all_ranks]))
    for i in range(len(unique_ranks) - 4 + 1):
        if unique_ranks[i+4] - unique_ranks[i] == 4:
            features.append("Straight完成")
            break

    # オーバーカード出現（ターンがフロップの最高位より高い）
    flop_max = max([ranks.index(r) for r in flop_ranks])
    turn_idx = ranks.index(turn_rank)
    if turn_idx > flop_max:
        features.append("Overcard出現")

    # ノーヒット（ターンがフロップのランクと重複なし）
    if turn_rank not in flop_ranks:
        features.append("NoPair")

    return features
