import streamlit as st
import numpy as np

# Sayfa Ayarları
st.set_page_config(page_title="PIYC 6x6", layout="centered")

# --- GELİŞMİŞ MOBİL OYUN CSS ---
st.markdown("""
<style>
    /* Ekranın sağa sola kaymasını engelle */
    .main .block-container {
        padding: 10px !important;
        max-width: 100% !important;
    }

    /* SAYI SEÇİM PANELİNİ ÜSTE SABİTLE (Sticky) */
    div[data-testid="stWidgetLabel"] { display: none; } /* Etiketi gizle yer kazandır */
    
    div[data-row-widget="true"] {
        position: sticky;
        top: 0;
        z-index: 1000;
        background-color: #0e1117;
        padding: 10px 0;
        border-bottom: 1px solid #333;
    }

    /* 6x6 IZGARA ZORLAMASI */
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

    /* BUTONLAR (Kare Formu) */
    .stButton > button {
        width: 100% !important;
        aspect-ratio: 1 / 1 !important; /* Kare yap */
        height: auto !important;
        padding: 0 !important;
        font-size: clamp(12px, 4vw, 20px) !important; /* Ekran boyutuna göre yazı tipi */
        line-height: 1 !important;
        border-radius: 4px !important;
        background-color: #262730 !important;
    }

    /* Mobilde alt boşlukları temizle */
    footer {display: none !important;}
    #MainMenu {display: none !important;}
</style>
""", unsafe_allow_html=True)

# 1. Oyun Hafızası
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

# 2. Üst Panel (Sabitlenmiş Sayı Seçimi)
st.write("### PIYC 6x6")
selected_num = st.select_slider("Rakam Seç:", options=[1, 2, 3, 4, 5, 6], value=1)

if not st.session_state.game_over:
    st.caption(f"Sıra: Oyuncu {st.session_state.turn}")
else:
    st.success(f"🏆 Kazanan: Oyuncu {st.session_state.winner}")

# 3. Oyun Tahtası
for r in range(6):
    cols = st.columns(6)
    for c in range(6):
        with cols[c]:
            val = st.session_state.board[r, c]
            label = str(int(val)) if val != 0 else " "
            
            if st.button(label, key=f"b_{r}_{c}", disabled=st.session_state.game_over):
                if val == 0:
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
                        st.toast(f"Hata: {selected_num}", icon="❌")

# 4. Alt Kontroller
if st.button("🔄 Yeni Oyun"):
    st.session_state.board = np.zeros((6, 6), dtype=int)
    st.session_state.turn = 1
    st.session_state.game_over = False
    st.rerun()
