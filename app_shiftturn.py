# app_shiftturn.py

import streamlit as st
from calculate_winrate_detailed_v2 import simulate_shift_turn_with_ranking
from hand_utils import all_starting_hands, convert_hand_to_cards
from opponent_hand_combos import opponent_hand_combos
from flop_generator import generate_flops_by_type

st.title("ShiftTurn 勝率変動分析ツール")

# 自分のハンド選択（169通り）
hand = st.selectbox("自分のハンドを選択", all_starting_hands)
hero_cards = convert_hand_to_cards(hand)

# フロップタイプ選択
flop_type = st.selectbox("フロップタイプを選択", [
    "Rainbow Low", "Rainbow Broadways", "Monotone",
    "Connected", "Paired", "Two-tone", "Mixed"
])

# フロップ枚数選択（10, 20, 30）
flop_count = st.selectbox("使用するフロップ数", [10, 20, 30])

# スタートボタン
if st.button("ShiftTurnを実行"):
    with st.spinner("計算中..."):
        flop_list = generate_flops_by_type(hero_cards, flop_type, flop_count)
        avg_shift, top10, worst10 = simulate_shift_turn_with_ranking(
            hero_cards, flop_list, opponent_hand_combos
        )

        st.write(f"平均勝率変動: {avg_shift:.2f}%")

        st.subheader("トップ10（勝率上昇）")
        for card, shift in top10:
            st.write(f"{card} → {shift:+.2f}%")

        st.subheader("ワースト10（勝率下降）")
        for card, shift in worst10:
            st.write(f"{card} → {shift:+.2f}%")
