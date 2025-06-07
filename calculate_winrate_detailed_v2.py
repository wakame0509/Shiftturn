import eval7
import random
from flop_generator import generate_flops_by_type
from opponent_hands_25_range import opponent_hand_combos

def simulate_winrate_for_turn_card(hero_hand, flop_type, num_trials=1000):
    results = []
    flop_candidates = generate_flops_by_type(hero_hand, flop_type)

    for _ in range(num_trials):
        flop = random.choice(flop_candidates)
        community = flop.copy()
        deck = eval7.Deck()

        used = set(hero_hand + flop)
        for card in used:
            deck.cards.remove(eval7.Card(card))

        turn_results = []

        for turn in deck.cards:
            board = flop + [str(turn)]
            hero = [eval7.Card(c) for c in hero_hand]
            turn_card = str(turn)

            wins = 0
            total = 0
            for opp_hand in random.sample(opponent_hand_combos, 50):  # サンプリング数は調整可
                if any(c in board + hero_hand for c in opp_hand):
                    continue

                opp = [eval7.Card(c) for c in opp_hand]
                community_cards = [eval7.Card(c) for c in board]

                hero_hand_val = eval7.evaluate(hero + community_cards)
                opp_hand_val = eval7.evaluate(opp + community_cards)

                if hero_hand_val > opp_hand_val:
                    wins += 1
                elif hero_hand_val == opp_hand_val:
                    wins += 0.5
                total += 1

            if total == 0:
                continue

            winrate = 100 * wins / total
            preflop_wr = get_preflop_winrate(hero_hand)
            shift = winrate - preflop_wr
            turn_results.append({"flop": flop, "turn": turn_card, "winrate": winrate, "shift": shift})

        results.extend(turn_results)

    return results

def get_preflop_winrate(hero_hand):
    from preflop_winrate_dict import preflop_winrates
    from utils import format_hand
    hand_str = format_hand(hero_hand[0], hero_hand[1])
    return preflop_winrates.get(hand_str, 50.0)
