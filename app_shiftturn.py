import streamlit as st
from calculate_winrate_detailed_v2 import simulate_winrate_for_turn_card
from utils import expand_hand_to_specific_cards, format_flop
from feature_extractor import extract_turn_features
from preflop_winrate_dict import preflop_winrates

st.title("ShiftTurn 勝率変動ランキング")
st.write("指定のハンドとフロップに対して、ターンでどのカードが来た時に勝率がどう変化するかを分析します。")

# --- ハンド選択 ---
hand_options = list(preflop_winrates.keys())
hero_hand_name = st.selectbox("ヒーローのハンドを選択", hand_options)

# --- フロップタイプ選択 ---
flop_type = st.selectbox("フロップタイプを選択", [
    "High Card Rainbow",
    "Paired Board",
    "Suited Two Tone",
    "Connected Low",
    "1 Hit + 2 Flush Draw",
    "No Hit",
    "Straight Possible"
])

# --- モンテカルロ試行回数 ---
num_trials = st.selectbox("モンテカルロ試行回数", [1000, 10000, 50000, 100000])

# --- 実行ボタン ---
if st.button("ShiftTurn を実行"):
    with st.spinner("計算中..."):
        hero_cards = expand_hand_to_specific_cards(hero_hand_name)

        # 勝率シミュレーション
        results = simulate_winrate_for_turn_card(
            hero_cards, flop_type, num_trials=num_trials
        )

        st.subheader("ターンカードによる勝率変動（トップ10）")

        results_sorted = sorted(results, key=lambda x: abs(x["shift"]), reverse=True)[:10]
        for res in results_sorted:
            turn_card = res["turn"]
            shift = res["shift"]
            wr = res["winrate"]
            features = extract_turn_features("".join(hero_cards), res["flop"], turn_card)
            flop_str = format_flop(res["flop"])
            st.markdown(f"""
                <div class='report'>
                <b>Flop:</b> {flop_str}  
                <b>Turn:</b> {turn_card}  
                <b>Winrate:</b> {wr:.1f}%  
                <b>Shift:</b> {shift:+.2f}%  
                <b>Features:</b> {features}
                </div>
            """, unsafe_allow_html=True)
