import streamlit as st
import pandas as pd
import io
from calculate_winrate_detailed_v2 import simulate_shift_turn_average
from flop_generator import generate_flops_by_type
from hand_range_matrix import all_169_hands

st.title("ShiftTurn 勝率変動シミュレーター（平均処理）")

# 自分のハンド（169通り）選択
hand = st.selectbox("自分のハンドを選択", all_169_hands)

# フロップタイプ選択
flop_type = st.selectbox("フロップタイプを選択", [
    "High Card Rainbow",
    "One Pair",
    "Flush Draw",
    "Straight Draw",
    "Connected Low",
    "Paired Board",
    "Dry Lowcard"
])

# 抽出回数の選択（最大50通り）
num_samples = st.select_slider(
    "毎試行のランダム抽出枚数（フロップ）",
    options=[5, 10, 15, 20, 25, 30, 35, 40, 45, 50],
    value=10
)

start = st.button("ShiftTurn 勝率計算スタート")

if start:
    with st.spinner("フロップを生成中..."):
        flop_candidates = generate_flops_by_type(flop_type, hand)

    if len(flop_candidates) < num_samples:
        st.warning(f"候補が {len(flop_candidates)} 通りしかありません。")
    else:
        with st.spinner("勝率変動を計算中（数え上げ×平均処理）..."):
            df_result = simulate_shift_turn_average(
                hand=hand,
                flop_list=flop_candidates,
                num_samples=num_samples
            )

        st.success("計算完了！")
        st.dataframe(df_result)

        # CSV保存処理
        csv = io.StringIO()
        df_result.to_csv(csv, index=False)
        csv.seek(0)
        filename = f"{hand}_shiftturn_{flop_type.replace(' ', '_')}.csv"

        st.download_button(
            label="CSVをダウンロード",
            data=csv,
            file_name=filename,
            mime="text/csv"
        )
