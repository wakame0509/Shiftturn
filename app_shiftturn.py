import streamlit as st
import os
import pandas as pd
from datetime import datetime
from calculate_winrate_detailed_v2 import simulate_shift_turn
from feature_extractor import extract_turn_features
from preflop_winrate_dict import preflop_winrates
from utils import expand_hand_to_specific_cards, format_flop
from flop_generator import generate_flops_by_type

# ---- スタイル適用 ----
with open("style.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

st.title("ShiftTurn 勝率変動ランキング")
st.write("指定したハンドとフロップに対して、ターンで落ちるカードによる勝率変動と特徴量を分析します。")

# 入力：ヒーローのハンドとフロップタイプ
hand_options = list(preflop_winrates.keys())
hero_hand_name = st.selectbox("ヒーローのハンドを選択", hand_options)

flop_type = st.selectbox("フロップタイプを選択", [
    "High Card Rainbow",
    "Paired Board",
    "Suited Two Tone",
    "Connected Low",
    "1 Hit + 2 Flush Draw",
    "No Hit",
    "Straight Possible"
])

# フロップの選択肢（タイプに合った候補を自動生成）
flop_candidates = generate_flops_by_type(hero_hand_name, flop_type)
selected_flop = st.selectbox("フロップを選択", flop_candidates, format_func=format_flop)

# 実行ボタン
if st.button("ShiftTurn 勝率分析実行"):
    st.write("計算中...（ターンカード全枚数について数え上げ実行）")

    hero_hand = expand_hand_to_specific_cards(hero_hand_name)
    flop_cards = selected_flop

    results = simulate_shift_turn(hero_hand, flop_cards)

    # 特徴量を抽出してDataFrameに追加
    for row in results:
        row["features"] = extract_turn_features(row, hero_hand, flop_cards)

    df = pd.DataFrame(results)
    df_sorted = df.sort_values("shift", ascending=False)

    st.subheader("勝率変動ランキング（ターンカード別）")
    st.dataframe(df_sorted[["turn", "winrate", "shift", "features"]].reset_index(drop=True))

    # --- CSV保存 ---
    os.makedirs("results/shiftturn", exist_ok=True)
    flop_str = "".join([card for card in flop_cards])
    filename = f"results/shiftturn/{hero_hand_name}_{flop_type}_{flop_str}.csv"
    df_sorted.to_csv(filename, index=False)

    st.success(f"結果を保存しました：{filename}")
