import streamlit as st
import pandas as pd
import random
from calculate_winrate_detailed_v2 import simulate_shift_turn_with_ranking
from flop_generator import generate_flops_by_type
from opponent_hand_combos import opponent_hand_combos
from hand_utils import all_starting_hands, convert_hand_to_cards

st.title("ShiftTurn 勝率変動シミュレーター")

# 自分のハンド選択（169通り）
hand_str = st.selectbox("自分のハンドを選択", all_starting_hands)
hero_cards = convert_hand_to_cards(hand_str)

# フロップタイプ選択
flop_type = st.selectbox("フロップタイプを選択", [
    "High Card", "Pair", "Two Tone", "Monotone", "Connected", "Low", "Ace High"
])

# フロップ枚数選択（10, 20, 30枚）
flop_count = st.selectbox("使用するフロップ枚数", [10, 20, 30])

# スタートボタン
if st.button("ShiftTurnを実行"):
    st.write("計算中です... 少々お待ちください。")

    # フロップ生成
    flop_list = generate_flops_by_type(hero_cards, flop_type, count=flop_count)

    # 勝率変動の数え上げ処理
    avg_shift, top10, worst10 = simulate_shift_turn_with_ranking(
        hero_cards, flop_list, opponent_hand_combos
    )

    # 結果表示
    st.subheader("平均勝率変動")
    st.write(f"{avg_shift:.2f}%")

    st.subheader("勝率上昇ランキング（Top 10）")
    st.dataframe(pd.DataFrame(top10, columns=["ターンカード", "変動量", "特徴量"]))

    st.subheader("勝率下降ランキング（Worst 10）")
    st.dataframe(pd.DataFrame(worst10, columns=["ターンカード", "変動量", "特徴量"]))

    # 保存用CSVダウンロード
    df_all = pd.DataFrame(top10 + worst10, columns=["ターンカード", "変動量", "特徴量"])
    csv = df_all.to_csv(index=False).encode("utf-8")
    st.download_button("CSVをダウンロード", data=csv, file_name="shiftturn_result.csv", mime="text/csv")
