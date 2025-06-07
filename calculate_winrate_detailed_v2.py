# calculate_winrate_detailed_v2.py

import eval7
import random
from collections import defaultdict
from extract_features import extract_features_for_turn
from hand_group_definitions import classify_hand
from tqdm import tqdm

def evaluate_hand(cards):
    hand = eval7.Hand(cards)
    return hand.evaluate()

def simulate_shift_turn_with_ranking(hero_cards, flop_list, opponent_hand_combos):
    shift_results = defaultdict(float)
    total_shift = 0
    total_count = 0

    for flop in flop_list:
        used = set(hero_cards + flop)
        deck = [card for card in eval7.Deck() if str(card) not in used]
        turn_cards = [str(card) for card in deck]

        for turn in turn_cards:
            board4 = flop + [turn]
            hero_full = hero_cards + board4

            hero_score = evaluate_hand(hero_full)

            wins = 0
            ties = 0
            losses = 0

            for opp in opponent_hand_combos:
                if any(card in board4 or card in hero_cards for card in opp):
                    continue

                opp_full = opp + board4
                opp_score = evaluate_hand(opp_full)

                if hero_score > opp_score:
                    wins += 1
                elif hero_score == opp_score:
                    ties += 1
                else:
                    losses += 1

            total = wins + ties + losses
            if total == 0:
                continue

            winrate = (wins + ties * 0.5) / total * 100
            preflop_winrate = 50  # 仮値、必要なら変更
            diff = winrate - preflop_winrate

            shift_results[turn] += diff
            total_shift += diff
            total_count += 1

    if total_count == 0:
        return 0.0, [], []

    avg_total = total_shift / total_count
    average_shifts = list(shift_results.items())
    average_shifts.sort(key=lambda x: x[1], reverse=True)

    top10 = average_shifts[:10]
    worst10 = average_shifts[-10:]

    return avg_total, top10, worst10
