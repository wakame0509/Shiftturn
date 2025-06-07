import streamlit as st
import pandas as pd
from calculate_winrate_detailed_v2 import simulate_shift_turn_with_ranking
from flop_generator import generate_flops_by_type
from hand_utils import all_starting_hands
import os

st.title("ShiftTurn 勝率変動分析（ターン）")

# 自分のハンドを選択（169通り）
hand = st.selectbox("自分のハンドを選択", all_starting_hands)

# フロップタイプ選択
flop_type = st.selectbox(
    "フロップタイプを選択",
    ["High Card", "Paired", "Monotone", "Two Tone", "Straight Possible", "Flush Possible", "Connected"]
)

# フロップ枚数を選択（10, 20, 30）
flop_count = st.selectbox("使用するフロップの数を選択", [10, 20, 30])

# 自分のハンドのカード（仮スート）
rank1, rank2 = hand[0], hand[1]
suits = ['h', 'd'] if rank1 != rank2 else ['h', 's']
hero_cards = [rank1 + suits[0], rank2 + suits[1]]

# 保存先フォルダ（任意。Renderなどでは注意）
output_dir = "results"
os.makedirs(output_dir, exist_ok=True)

# 実行ボタン
if st.button("ShiftTurn を実行"):
    with st.spinner("計算中..."):
        flop_list = generate_flops_by_type(hero_cards, flop_type, count=flop_count)
        avg_shift, top10, worst10 = simulate_shift_turn_with_ranking(hero_cards, flop_list)

    # 結果表示
    st.success("計算完了！")
    st.write(f"平均勝率変動：{avg_shift:.2f}%")

    # トップ10 表示
    st.subheader("トップ10（勝率上昇）")
    for card, delta, features in top10:
        st.write(f"{card}: {delta:+.2f}%, 特徴: {features}")

    # ワースト10 表示
    st.subheader("ワースト10（勝率下降）")
    for card, delta, features in worst10:
        st.write(f"{card}: {delta:+.2f}%, 特徴: {features}")

    # 結果保存
    df_top = pd.DataFrame(top10, columns=["カード", "変動値", "特徴量"])
    df_top["カテゴリ"] = "Top10"
    df_worst = pd.DataFrame(worst10, columns=["カード", "変動値", "特徴量"])
    df_worst["カテゴリ"] = "Worst10"
    df_all = pd.concat([df_top, df_worst], ignore_index=True)
    df_all["ハンド"] = hand
    df_all["フロップタイプ"] = flop_type

    # CSV保存
    filename = f"{output_dir}/shiftturn_{hand}_{flop_type}_{flop_count}flops.csv"
    df_all.to_csv(filename, index=False)
    st.success(f"結果を保存しました：{filename}")
