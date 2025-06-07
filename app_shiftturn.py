import streamlit as st
from calculate_winrate_detailed_v2 import simulate_shift_turn_with_ranking

st.title("ShiftTurn 勝率変動分析")

# 169通りのスターティングハンドを直接定義
all_starting_hands = []
ranks = "AKQJT98765432"
for i, r1 in enumerate(ranks):
    for j, r2 in enumerate(ranks):
        if i < j:
            all_starting_hands.append(r1 + r2 + "s")  # スーテッド
            all_starting_hands.append(r1 + r2 + "o")  # オフスート
        elif i == j:
            all_starting_hands.append(r1 + r2)        # ペア

# 自分のハンドを選択
hand = st.selectbox("自分のハンドを選択", all_starting_hands)

# フロップタイプの選択
flop_type = st.selectbox("フロップタイプを選択", [
    "High Card + Suited", "No Pair + Dry", "Connected + Suited",
    "Low + Rainbow", "Paired + Suited", "Ace High", "Broadway"
])

# 使用するフロップ数を選択
num_flops = st.selectbox("使用するフロップ数", [10, 20, 30])

# 計算ボタン
if st.button("ShiftTurnを実行"):
    with st.spinner("計算中..."):
        result_df = simulate_shift_turn_with_ranking(hand, flop_type, num_flops)
        st.success("計算完了！")

        # 平均勝率変動の表示
        avg_shift = result_df["shift"].mean()
        st.write(f"平均勝率変動: {avg_shift:.2f}%")

        # トップ10
        st.subheader("勝率上昇 トップ10")
        st.dataframe(result_df.sort_values(by="shift", ascending=False).head(10))

        # ワースト10
        st.subheader("勝率下降 ワースト10")
        st.dataframe(result_df.sort_values(by="shift").head(10))
