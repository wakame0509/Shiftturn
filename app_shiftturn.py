import streamlit as st
from calculate_winrate_detailed_v2 import simulate_shift_turn
from feature_extractor import extract_turn_features
from preflop_winrate_dict import preflop_winrates
from utils import expand_hand_to_specific_cards, format_flop
from flop_generator import generate_flops_by_type

# ---- スタイル読み込み ----
with open("style.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# ---- タイトル ----
st.title("ShiftTurn 勝率変動ランキング")
st.write("指定のハンドとフロップに対して、ターンでどのカードが来た時に勝率がどう変化するかを数え上げ法で分析します。")

# ---- 入力 ----
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

# ---- 実行ボタン ----
if st.button("ShiftTurn を実行"):
    with st.spinner("ターンカード別の勝率を計算中..."):
        hero_cards = expand_hand_to_specific_cards(hero_hand_name)
        flop_list = generate_flops_by_type(hero_cards, flop_type)
        flop = flop_list[0]  # 固定フロップで評価（高速化）

        results = simulate_shift_turn(hero_cards, flop)
        preflop_wr = preflop_winrates[hero_hand_name]

        for r in results:
            r["shift"] = round(r["winrate"] - preflop_wr, 2)

        results_sorted = sorted(results, key=lambda x: abs(x["shift"]), reverse=True)[:10]

        st.subheader("ターンカードによる勝率変動（トップ10）")

        for res in results_sorted:
            flop_str = format_flop(res["flop"])
            turn = res["turn"]
            shift = res["shift"]
            winrate = res["winrate"]
            features = extract_turn_features("".join(hero_cards), res["flop"], turn)

            st.markdown(f"""
            <div class='report'>
            <b>Flop:</b> {flop_str}<br>
            <b>Turn:</b> {turn}<br>
            <b>Winrate:</b> {winrate:.2f}%<br>
            <b>Shift:</b> {shift:+.2f}%<br>
            <b>Features:</b> {features}
            </div>
            """, unsafe_allow_html=True)
