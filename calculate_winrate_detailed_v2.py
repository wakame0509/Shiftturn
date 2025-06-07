import eval7
import random
from extract_features import extract_features_for_turn
from hand_utils import convert_hand_to_cards

def calculate_winrate(hero, board, opponent_range, iters=1000):
    hero_hand = [eval7.Card(card) for card in hero]
    board_cards = [eval7.Card(card) for card in board]
    deck = [card for card in eval7.Deck() if card not in hero_hand + board_cards]

    wins = 0
    for _ in range(iters):
        deck_copy = deck[:]
        random.shuffle(deck_copy)

        opp_hand = [eval7.Card(card) for card in random.choice(opponent_range)]
        remaining = [card for card in deck_copy if card not in opp_hand][:5 - len(board_cards)]
        full_board = board_cards + remaining

        hero_hand_eval = hero_hand + full_board
        opp_hand_eval = opp_hand + full_board

        hero_value = eval7.evaluate(hero_hand_eval)
        opp_value = eval7.evaluate(opp_hand_eval)

        if hero_value > opp_value:
            wins += 1
        elif hero_value == opp_value:
            wins += 0.5

    return wins / iters

def simulate_shift_turn_with_ranking(hero_hand_str, flop_list, opponent_range):
    hero_cards = convert_hand_to_cards(hero_hand_str)
    average_shifts = []
    all_ranked = []

    for flop in flop_list:
        used = set(hero_cards + flop)
        deck = [card for card in eval7.Deck() if card not in used]

        shift_data = []
        for turn in deck:
            board = flop + [turn]
            winrate = calculate_winrate(hero_cards, board, opponent_range)
            features = extract_features_for_turn(hero_cards, board)
            shift_data.append(((flop, turn), winrate, features))

        if shift_data:
            total_shift = sum(w for _, w, _ in shift_data)
            avg = total_shift / len(shift_data)
            average_shifts.append(((flop,), avg))

            sorted_shift = sorted(shift_data, key=lambda x: x[1], reverse=True)
            top10 = sorted_shift[:10]
            worst10 = sorted_shift[-10:]
            all_ranked.append(((flop,), top10, worst10))

    if average_shifts:
        avg_total = sum(x[1] for x in average_shifts) / len(average_shifts)
    else:
        avg_total = 0.0
        top10, worst10 = [], []

    # 平均勝率 + トップ10・ワースト10（最後のフロップから）
    return avg_total, top10, worst10
