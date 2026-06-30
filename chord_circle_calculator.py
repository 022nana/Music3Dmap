import streamlit as st
import math

# 1. 24個のコードの定義（五度圏＋平行調の並び順）
CHORD_SEQUENCE = [
    "C", "Em", "G", "Bm", "D", "F#m", "A", "C#m", "E", "G#m", "B", "D#m",
    "F#", "Bbm", "Db", "Fm", "Ab", "Cm", "Eb", "Gm", "Bb", "Dm", "F", "Am"
]

st.set_page_config(page_title="Chord Circle Calculator", layout="wide")

st.title("🎵 24コード・サークル計算ツール (Web版)")
st.write("五度圏に平行調を挿入した24個のコードを円状に配置し、調性空間上の距離を数値化・計算するツールです。")

# 2. サイドバーでのコントロール（基準設定と回転）
st.sidebar.header("⚙️ コントロールパネル")

# 基準コードの選択
base_chord = st.sidebar.selectbox("1. 基準コードを選択 (値 = 0.0)", CHORD_SEQUENCE, index=0)

# 中華テーブル風の回転角度調整（スライダーでテーブルをくるくる回す感覚を再現）
rotation_step = st.sidebar.slider("🔄 テーブルを回転させる (ステップ移動)", -12, 12, 0)

st.sidebar.markdown("---")
st.sidebar.write("💡 **仕様・計算規則**")
st.sidebar.write("- 基準コードが `0.0` となります。")
st.sidebar.write("- 隣り合うコード間の距離は `0.5` です。")
st.sidebar.write("- 最短ルート（時計回り・反時計回り）で計算するため、絶対値の上限は `6.0` に制限されます。")

# 3. メイン画面：計算エリア (□ → □)
col_calc, col_space = st.columns([2, 1])

with col_calc:
    st.subheader("🧮 コード差分計算")
    
    col1, col_arrow, col2 = st.columns([2, 1, 2])
    
    with col1:
        chord1 = st.selectbox("始点コード (□)", CHORD_SEQUENCE, index=0) # デフォルト C
    with col_arrow:
        st.markdown("<h2 style='text-align: center; margin-top: 10px;'>→</h2>", unsafe_allow_html=True)
    with col2:
        chord2 = st.selectbox("終点コード (□)", CHORD_SEQUENCE, index=1) # デフォルト Em

# 4. 計算ロジック
def get_shortest_distance(name_from, name_to):
    idx_from = CHORD_SEQUENCE.index(name_from)
    idx_to = CHORD_SEQUENCE.index(name_to)
    
    diff_steps = idx_to - idx_from
    if diff_steps > 12:
        diff_steps -= 24
    elif diff_steps < -12:
        diff_steps += 24
        
    return diff_steps * 0.5

def format_sign(val):
    if val > 0:
        return f"+{val:.1f}"
    elif val < 0:
        return f"{val:.1f}"
    else:
        return "0.0"

# 各種数値の計算
val_c1 = get_shortest_distance(base_chord, chord1)
val_c2 = get_shortest_distance(base_chord, chord2)
diff_between = get_shortest_distance(chord1, chord2)

# 結果の表示
with col_calc:
    st.markdown("### 📊 計算結果")
    st.info(f"🔹 **始点 {chord1} の値** (基準 {base_chord} から): `{format_sign(val_c1)}`\n"
            f"🔸 **終点 {chord2} の値** (基準 {base_chord} から): `{format_sign(val_c2)}`")
    
    # メインのフォーマット表示
    st.markdown(
        f"<div style='background-color: #e1f5fe; padding: 20px; border-radius: 10px; text-align: center; border-left: 5px solid #0288d1;'>"
        f"<h2 style='color: #01579b; margin: 0;'>{chord1} ➔ {chord2} ： {format_sign(diff_between)}</h2>"
        f"</div>", 
        unsafe_allow_html=True
    )

# 5. 円状図形（SVGによる描画）の作成
st.markdown("---")
st.subheader("🎡 コード・サークル盤面 (中華テーブル風)")
st.write("※サイドバーの「テーブルを回転させる」スライダーを動かすと、盤面全体がスムーズに回転します。")

# SVGを使った美しい円盤の描画
svg_size = 500
cx, cy = svg_size / 2, svg_size / 2
r = svg_size * 0.35

num_chords = len(CHORD_SEQUENCE)
svg_elements = []

# 背景の大きな円（テーブルの縁）
svg_elements.append(f'<circle cx="{cx}" cy="{cy}" r="{r}" stroke="#333333" stroke-width="3" fill="#fcfcfc" />')

for i, name in enumerate(CHORD_SEQUENCE):
    effective_index = (i + rotation_step) % num_chords
    base_angle = (2 * math.pi * effective_index / num_chords) - (math.pi / 2)
    
    x = cx + r * math.cos(base_angle)
    y = cy + r * math.sin(base_angle)
    
    svg_elements.append(f'<circle cx="{x}" cy="{y}" r="5" fill="#ff4b4b" />')
    
    tx = cx + (r + 32) * math.cos(base_angle)
    ty = cy + (r + 32) * math.sin(base_angle) + 5
    
    font_weight = "normal"
    fill_color = "#333333"
    font_size = "13px"
    display_name = name
    
    if name == base_chord:
        font_weight = "bold"
        fill_color = "#7b1fa2"  # 基準は紫
        font_size = "15px"
        display_name = f"【{name}】(0.0)"
    elif name == chord1:
        font_weight = "bold"
        fill_color = "#0288d1"  # 始点は青
        font_size = "15px"
    elif name == chord2:
        font_weight = "bold"
        fill_color = "#388e3c"  # 終点は緑
        font_size = "15px"
        
    svg_elements.append(
        f'<text x="{tx}" y="{ty}" text-anchor="middle" font-family="sans-serif" '
        f'font-size="{font_size}" font-weight="{font_weight}" fill="{fill_color}">{display_name}</text>'
    )

svg_code = f'<svg width="100%" height="{svg_size}" viewBox="0 0 {svg_size} {svg_size}" xmlns="http://www.w3.org/2000/svg">{"".join(svg_elements)}</svg>'
st.components.v1.html(svg_code, height=svg_size)
