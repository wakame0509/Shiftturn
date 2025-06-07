# hand_group_definitions.py

hand_groups = {
    "High Pair": ["AA", "KK", "QQ", "JJ"],
    "Middle Pair": ["TT", "99", "88", "77"],
    "Low Pair": ["66", "55", "44", "33", "22"],
    "Ace High": ["AKo", "AQo", "AJo", "ATo", "AKs", "AQs", "AJs", "ATs"],
    "Broadway": ["KQo", "KJo", "QJo", "JTo", "KQs", "KJs", "QJs", "JTs"],
    "Suited Connectors": ["T9s", "98s", "87s", "76s", "65s", "54s"],
    "Suited One Gap": ["97s", "86s", "75s", "64s", "53s", "42s"],
    "Offsuit Connectors": ["T9o", "98o", "87o", "76o", "65o"],
    "Offsuit One Gap": ["97o", "86o", "75o", "64o", "53o"],
    "Low Suited": ["43s", "32s"],
    "Low Offsuit": ["43o", "32o"],
    "Other": []  # その他はここに追加
}
