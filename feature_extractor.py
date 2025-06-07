def extract_flop_features(hero_str, flop_cards):
    """
    フロップ特徴量（ShiftFlop用）を抽出（省略版）
    """
    # 必要に応じて定義（既存ロジック使用）
    return "Coming soon"

def extract_turn_features(hero_str, flop, turn):
    """
    ターン特徴量を抽出
    """
    features = []

    ranks = [c[0] for c in flop + [turn]]
    suits = [c[1] for c in flop + [turn]]

    # セット完成（例：88 + 8がターンで落ちる）
    if hero_str[0] == hero_str[1] and hero_str[0] in ranks:
        features.append("Set Completed")

    # フラッシュドロー完成（スートが4枚揃う）
    for s in 'hdcs':
        if suits.count(s) == 4:
            features.append("Flush Draw Possible")
        if suits.count(s) >= 5:
            features.append("Flush Completed")

    # ストレートドロー完成（例：5678 + 9）
    rank_map = {'2':2, '3':3, '4':4, '5':5, '6':6, '7':7,
                '8':8, '9':9, 'T':10, 'J':11, 'Q':12, 'K':13, 'A':14}
    values = sorted(set(rank_map[r] for r in ranks))
    for i in range(len(values) - 3):
        if values[i+3] - values[i] == 3:
            features.append("Straight Possible")

    # オーバーカード出現
    hole_ranks = [hero_str[0], hero_str[1]]
    overcards = [r for r in ranks if r > max(hole_ranks)]
    if overcards:
        features.append("Overcard on Turn")

    return ", ".join(features) if features else "None"
