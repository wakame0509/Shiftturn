import eval7
import random
from collections import defaultdict
from feature_extractor import extract_turn_feature

def evaluate_hand_vs_range(hero, board, opponent_hand_combos):
    hero_wins = 0
    villain_wins = 0
    ties = 0

    for opp in opponent_hand_combos:
        opp_cards = [eval7.Card(c) for c in opp]
        all_cards = hero + board + opp_cards
        if len(set(all_cards)) < len(all_cards):
            continue

        hero_eval = eval7.evaluate(hero, board)
        opp_eval = eval7.evaluate(opp_cards, board)

        if hero_eval > opp_eval:
            hero_wins += 1
        elif hero_eval < opp_eval:
            villain_wins += 1
        else:
            ties += 1

    total = hero_wins + villain_wins + ties
    if total == 0:
        return 0
    return (hero_wins + 0.5 * ties) / total

def simulate_shift_turn_with_ranking(hero_hand, flop_list, opponent_hand_combos, num_sample=10):
    all_turns = [card for card in eval7.Deck() if card not in hero_hand]

    total_shift = 0
    turn_stats = defaultdict(list)

    sampled_flops = random.sample(flop_list, min(num_sample, len(flop_list)))

    for flop in sampled_flops:
        board3 = [eval7.Card(c) for c in flop]
        used_cards = set(hero_hand + board3)

        for turn_card in all_turns:
            if turn_card in used_cards:
                continue
            board4 = board3 + [turn_card]

            winrate = evaluate_hand_vs_range(hero_hand, board4, opponent_hand_combos)
            key = turn_card.__str__()
            turn_stats[key].append(winrate)

    averaged = {k: sum(v)/len(v) for k, v in turn_stats.items() if v}
    average_shift = sum(averaged.values()) / len(averaged) if averaged else 0

    # ランキング処理
    top10 = sorted(averaged.items(), key=lambda x: -x[1])[:10]
    bottom10 = sorted(averaged.items(), key=lambda x: x[1])[:10]

    top10_detailed = []
    bottom10_detailed = []

    for card, win in top10:
        feat = extract_turn_feature(hero_hand, card)
        top10_detailed.append({"card": card, "winrate": win, "feature": feat})

    for card, win in bottom10:
        feat = extract_turn_feature(hero_hand, card)
        bottom10_detailed.append({"card": card, "winrate": win, "feature": feat})

    return {
        "average_shift": average_shift,
        "top10": top10_detailed,
        "bottom10": bottom10_detailed
    }
