from typing import List, Dict
from collections import defaultdict
import eval7

RANKS = '23456789TJQKA'
SUITS = 'cdhs'

def get_deck(exclude: List[str]) -> List[str]:
    return [r + s for r in RANKS for s in SUITS if r + s not in exclude]

def classify_feature(card: str, hand: List[str], board: List[str]) -> str:
    all_cards = hand + board + [card]
    ranks = [c[0] for c in all_cards]
    rank_counts = defaultdict(int)
    for r in ranks:
        rank_counts[r] += 1

    if rank_counts[card[0]] == 3:
        return "セット完成"
    elif card[0] not in ranks and RANKS.index(card[0]) > max([RANKS.index(r[0]) for r in hand]):
        return "オーバーカード"
    else:
        return "その他"

def simulate_shift_turn_with_ranking(
    hand: List[str], flop: List[str], opponent_combos: List[List[str]]
) -> Dict[str, any]:
    deck = get_deck(hand + flop)
    results = []

    for turn_card in deck:
        full_board = flop + [turn_card]
        hero = [eval7.Card(c) for c in hand]
        board_eval = [eval7.Card(c) for c in full_board]

        hero_wins = 0
        total = 0
        for opp in opponent_combos:
            if turn_card in opp or any(c in full_board for c in opp):
                continue
            opp_eval = [eval7.Card(c) for c in opp]
            hero_score = eval7.evaluate(hero + board_eval)
            opp_score = eval7.evaluate(opp_eval + board_eval)
            if hero_score > opp_score:
                hero_wins += 1
            elif hero_score == opp_score:
                hero_wins += 0.5
            total += 1

        if total == 0:
            continue
        winrate = hero_wins / total
        results.append({
            "card": turn_card,
            "winrate": winrate,
            "feature": classify_feature(turn_card, hand, flop)
        })

    results.sort(key=lambda x: x["winrate"], reverse=True)
    top_5 = results[:5]
    bottom_5 = results[-5:]

    return {
        "top": top_5,
        "bottom": bottom_5,
        "average_shift": sum(r["winrate"] for r in results) / len(results) - 0.5,
    }
