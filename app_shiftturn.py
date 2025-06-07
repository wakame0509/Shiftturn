import streamlit as st
from calculate_winrate_detailed_v2 import simulate_shift_turn_with_ranking
from opponent_hands_25_range import opponent_hand_combos
from utils import generate_flops_by_type, parse_hand

st.title("ShiftTurn 勝率変動ランキング")

# 自分のハンド（169通り）
ranks = "23456789TJQKA"
hands = []
for r in ranks:
    hands.append(r + r)
for i, r1 in enumerate(ranks):
    for j, r2 in enumerate(ranks):
        if i < j:
            hands.append(r1 + r2 + "s")
            hands.append(r1 + r2 + "o")

hand_str = st.selectbox("自分のハンドを選択", hands)

# フロップタイプ選択
flop_type = st.selectbox("フロップタイプを選択", [
    "ミドルペア + 同スート2枚",
    "トップヒット + スート2枚",
    "ローカードドライ",
    "2枚連続 + 1枚ブランク",
    "スート3枚（フラッシュボード）",
    "ミドルストレートボード",
    "ハイカード + バラバラ"
])

# 試行数（ターンは数え上げなので無視）
num_flops = st.slider("1回の試行ごとのフロップ抽出数", 5, 50, 10)

if st.button("計算開始"):
    try:
        hero_hand = parse_hand(hand_str)
        flops = generate_flops_by_type(flop_type)
        result = simulate_shift_turn_with_ranking(hero_hand, flops, opponent_hand_combos, num_sample=10)

        st.subheader("平均勝率変動")
        st.write(f"{result['average_shift']:+.2%}")

        st.subheader("トップ10（勝率上昇）")
        for item in result["top10"]:
            st.write(f"{item['card']} - {item['winrate']:.2%} ({item['feature']})")

        st.subheader("ワースト10（勝率下降）")
        for item in result["bottom10"]:
            st.write(f"{item['card']} - {item['winrate']:.2%} ({item['feature']})")

    except Exception as e:
        st.error(f"エラーが発生しました: {e}")
