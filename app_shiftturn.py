import streamlit as st
from calculate_winrate_detailed_v2 import simulate_shift_turn_with_ranking
from flop_generator import generate_flops_by_type
from opponent_hands_25_range import opponent_hand_combos
from hand_group_definitions import all_starting_hands
import pandas as pd
import datetime

st.title("ShiftTurn 勝率変動分析ツール")

# 自分のハンド選択（169通り）
hand = st.selectbox("自分のハンドを選択", all_starting_hands)

# フロップタイプ選択
flop_type = st.selectbox(
    "フロップタイプを選択",
    ["ミドルペア＋2同スート", "ローカードドライ", "ハイカード＋2同スート", "オーバーカード", "2枚連続", "ミドル＆コネクター", "ハンドと無関係"]
)

# 使用するフロップの数を選択
num_flops = st.selectbox("使用するフロップの数", [10, 20, 30])

# モンテカルロの回数（1フロップに対してターン枚数分）
mc_trials = st.selectbox("各フロップに対するモンテカルロ回数", [1000, 5000, 10000])

if st.button("勝率変動を計算"):
    st.write("計算中...")
    flops = generate_flops_by_type(hand, flop_type, num_flops)
    result_df = simulate_shift_turn_with_ranking(hand, flops, opponent_hand_combos, mc_trials)

    st.subheader("勝率変動ランキング")
    st.dataframe(result_df)

    # 保存処理
    now = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"shift_turn_{hand}_{flop_type}_{now}.csv".replace(" ", "_")
    result_df.to_csv(filename, index=False)
    st.success(f"CSVとして保存されました: {filename}")
