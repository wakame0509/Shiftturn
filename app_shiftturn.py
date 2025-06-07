import streamlit as st
import pandas as pd
from calculate_winrate_detailed_v2 import simulate_shift_turn_average
from opponent_hand_combos import opponent_hand_combos
from flop_generator import generate_flops_by_type
from hand_utils import all_starting_hands

st.title("ShiftTurn 勝率変動分析ツール（数え上げ法）")

# 自分のハンド選択
hand = st.selectbox("自分のハンドを選択", all_starting_hands)

# フロップタイプ選択
flop_type = st.selectbox("フロップタイプを選択", [
    "Low Dry", "Middle Connected", "High Wet", "One Pair", "Monotone", "Overcards", "Random"
])

# フロップの数（10/20/30）
flop_count = st.selectbox("使用するフロップ数", [10, 20, 30])

# 実行ボタン
if st.button("ShiftTurn 勝率変動を計算"):
    st.write("フロップ生成中...")
    flop_list = generate_flops_by_type(flop_type, count=flop_count)

    st.write("計算中（ターンカードの数え上げ処理）...")
    df = simulate_shift_turn_average(hand, flop_list, opponent_hand_combos)

    st.write("計算結果（Top10 & Worst10 勝率変動）:")
    st.dataframe(df)

    # CSV保存
    csv = df.to_csv(index=False).encode('utf-8')
    st.download_button("CSVとしてダウンロード", csv, file_name=f"shiftturn_{hand}_{flop_type}.csv", mime='text/csv')
