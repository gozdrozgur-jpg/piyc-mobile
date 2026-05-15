import streamlit as st
import numpy as np

# 1. Sayfa Ayarları
st.set_page_config(page_title="PIYC Elite 6x6", layout="centered")

# --- CSS: MOBİL UYUMLU GÖRÜNÜM VE KONTRAST ---
st.markdown("""
<style>
    .stApp { background-color: #0e1117; }
    [data-testid="stHorizontalBlock"] {
        display: flex !important;
        flex-direction: row !important;
        flex-wrap: nowrap !important;
        gap: 2px !important;
        justify-content: center !important;
    }
    [data-testid="column"] {
        flex: 1 1 0 !important;
        min-width: 0 !important;
    }
    .stButton > button {
        width: 100% !important;
        aspect-ratio: 1 / 1 !important;
        height: auto !important;
        font-size: 22px !important;
        font-weight: 800 !important;
        color: #ffffff !important;
        background-color: #262730 !important;
        border: 1px solid #444 !important;
    }
</style>
""", unsafe_allow_html=True)

# 2. Oyun Hafızası
if 'board' not in st.session_state:
    st.session_state.board = np.zeros((6, 6), dtype=int)
    st.session_state.turn = 1
    st.session_state.game_over = False
    st.session_state.winner = None

def check_move(board, row, col, val):
    if val in board[row, :] or val in board[:, col]:
        return False
    return True

def can_move_anywhere(board):
    for r in range(6):
        for c in range(6):
            if board[r, c] == 0:
                for v in range(1, 7):
                    if check_move(board, r, c, v):
                        return True
    return False

# 3. Başlık ve Sayı Seçimi
st.title("🔢 PIYC: 6x6 Elite")

# Rakam seçimi (Varsayılan olarak 1 seçili gelir)
selected_num = st.pills("Rakam Seç:", [1, 2, 3, 4, 5, 6], selection_mode="single", default=1)

if not st.session_state.game_over:
    st.write(f"Sıra: **Oyuncu {st.session_state.turn}**")
else:
    st.success(f"🏆 Kazanan: Oyuncu {st.session_state.winner}")

# 4. Oyun Tahtası (Buradaki döngü yapısı label hatasını çözer)
for r in range(6):
    cols = st.columns(6)
    for c in range(6):
        with cols[c]:
            # Değişkenleri burada net bir şekilde tanımlıyoruz
            current_val = st.session_state.board[r, c]
            button_label = str(int(current_val)) if current_val != 0 else " "
            
            if st.button(button_label, key=f"b_{r}_{c}", disabled=st.session_state.game_over):
                # Hata engelleyici kontrol
                if selected_num is not None:
                    if current_val == 0:
                        if check_move(st.session_state.board, r, c, selected_num):
                            st.session_state.board[r, c] = selected_num
                            next_player = 2 if st.session_state.turn == 1 else 1
                            
                            if not can_move_anywhere(st.session_state.board):
                                st.session_state.game_over = True
                                st.session_state.winner = st.session_state.turn
                            else:
                                st.session_state.turn = next_player
                            st.rerun()
                        else:
                            st.toast(f"Çakışma: {selected_num}", icon="❌")
                else:
                    st.warning("Lütfen bir sayı seçin!")

# 5. Alt Bölüm
st.divider()
if st.button("🔄 Yeni Oyun"):
    st.session_state.board = np.zeros((6, 6), dtype=int)
    st.session_state.turn = 1
    st.session_state.game_over = False
    st.rerun()
