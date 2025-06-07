import eval7
from collections import defaultdict
from extract_features import extract_features_for_turn  # 修正済みインポート

def simulate_winrate(hero_cards, board, opponent_hands):
    hero_hand = [eval7.Card(card) for card in hero_cards]
    board_cards = [eval7.Card(card) for card in board]
    hero_score = evaluate_hand(hero_hand + board_cards)

    wins = 0
    ties = 0
    total = 0

    for opp in opponent_hands:
        opp_hand = [eval7.Card(opp[0]), eval7.Card(opp[1])]
        opp_score = evaluate_hand(opp_hand + board_cards)
        if hero_score > opp_score:
            wins += 1
        elif hero_score == opp_score:
            ties += 1
        total += 1

    return (wins + ties / 2) / total if total > 0 else 0

def evaluate_hand(cards):
    hand = eval7.Hand(cards)
    hand_type = hand.evaluate()
    return hand_type

def simulate_shift_turn_average(hero_cards, flop_list, opponent_hands):
    turn_winrates = []

    for flop in flop_list:
        used = set(hero_cards + flop)
        deck = [str(c) for c in eval7.Deck() if str(c) not in used]
        for turn_card in deck:
            board = flop + [turn_card]
            winrate = simulate_winrate(hero_cards, board, opponent_hands)
            turn_winrates.append(winrate)

    return sum(turn_winrates) / len(turn_winrates)

def simulate_shift_turn_with_ranking(hero_cards, flop_list, opponent_hands):
    turn_shifts = defaultdict(list)

    for flop in flop_list:
        used = set(hero_cards + flop)
        turn_cards = [str(c) for c in eval7.Deck() if str(c) not in used]

        base_winrate = simulate_winrate(hero_cards, flop, opponent_hands)

        for turn in turn_cards:
            full_board = flop + [turn]
            winrate = simulate_winrate(hero_cards, full_board, opponent_hands)
            delta = winrate - base_winrate
            features = extract_features_for_turn(hero_cards, flop, turn)
            turn_shifts[turn].append((delta, features))

    average_shifts = []
    for card, data in turn_shifts.items():
        avg = sum(d for d, _ in data) / len(data)
        features = data[0][1]  # 最初の特徴量を使用
        average_shifts.append((card, avg, features))

    average_shifts.sort(key=lambda x: x[1], reverse=True)
    top10 = average_shifts[:10]
    worst10 = average_shifts[-10:]
    avg_total = sum(x[1] for x in average_shifts) / len(average_shifts)

    return avg_total, top10, worst10
