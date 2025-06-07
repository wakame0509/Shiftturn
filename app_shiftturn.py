import streamlit as st
import eval7
import random
import csv
import os
from collections import defaultdict

# 自分のハンド定義（169通り）
all_starting_hands = [
    f"{r1}{s1} {r2}{s2}"
    for r1 in "AKQJT98765432"
    for r2 in "AKQJT98765432"
    for s1 in "shdc"
    for s2 in "shdc"
    if r1 + s1 != r2 + s2
]

# フロップタイプ選択
flop_types = ["Rainbow", "Two Tone", "Monotone", "Connected", "Paired", "Dry", "Wet"]

# opponent_hand_combos（静的な25%レンジの代表スート付き208通り）
from opponent_hand_combos import opponent_hand_combos

# タイトル
st.title("ShiftTurn 勝率変動計算（特徴量＋ランキング付き）")

# ハンド選択
hero_hand_str = st.selectbox("自分のハンドを選択", all_starting_hands)

# フロップタイプ選択
flop_type = st.selectbox("フロップタイプを選択", flop_types)

# フロップ数選択（10, 20, 30）
flop_count = st.selectbox("使用するフロップの枚数を選択", [10, 20, 30])

# CSV保存ON/OFF
save_csv = st.checkbox("CSVで結果を保存", value=True)

# 実行ボタン
if st.button("ShiftTurnを計算"):
    hero_cards = hero_hand_str.split()

    # フロップ生成
    from flop_generator import generate_flops_by_type
    flop_list = generate_flops_by_type(hero_cards, flop_type)
    random.shuffle(flop_list)
    flop_list = flop_list[:flop_count]

    # ShiftTurn実行
    from calculate_winrate_detailed_v2 import simulate_shift_turn_with_ranking
    avg_shift, top10, worst10 = simulate_shift_turn_with_ranking(hero_cards, flop_list, opponent_hand_combos)

    st.markdown(f"### 平均勝率変動: {avg_shift:.4f}")

    # トップ10表示
    st.markdown("### Top 10 勝率上昇カード")
    for card, delta, features in top10:
        st.write(f"{card}: +{delta:.4f}, 特徴: {', '.join(features)}")

    # ワースト10表示
    st.markdown("### Worst 10 勝率下降カード")
    for card, delta, features in worst10:
        st.write(f"{card}: {delta:.4f}, 特徴: {', '.join(features)}")

    # 保存処理
    if save_csv:
        filename = f"shiftturn_{hero_hand_str.replace(' ', '')}_{flop_type}_{flop_count}.csv"
        with open(filename, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["Card", "Delta", "Features"])
            for card, delta, features in top10 + worst10:
                writer.writerow([card, delta, ";".join(features)])
        st.success(f"結果をCSVに保存しました：{filename}")
