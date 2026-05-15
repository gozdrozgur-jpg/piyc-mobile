import streamlit as st
import numpy as np

# Sayfa Ayarları
st.set_page_config(page_title="PIYC Elite 6x6", layout="centered")

# --- YÜKSEK KONTRAST VE GÖRÜNÜRLÜK CSS ---
st.markdown("""
<style>
    /* Ana Arka Plan */
    .stApp { background-color: #0e1117; }

    /* IZGARA ZORLAMASI (Dikeyde yan yana tutar) */
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

    /* TAHTA BUTONLARI (Okunabilir Rakamlar) */
    .stButton > button {
        width: 100% !important;
        aspect-ratio: 1 / 1 !important;
        height: auto !important;
        padding: 0 !important;
        font-size: 22px !important; /* Rakamları büyüttük */
        font-weight: 800 !important; /* Kalınlaştırdık */
        border-radius: 4px !important;
        background-color: #262730 !important; /* Koyu gri arka plan */
        color: #ffffff !important; /* PARLAK BEYAZ RAKAMLAR */
        border: 1px solid #444 !important;
    }
    
    /* Üzerine gelince veya basınca renk değişimi */
    .stButton > button:active, .stButton > button:focus {
        color: #FF4B4B !important;
        border-color: #FF4B4B !important;
    }

    /* SAYI SEÇİM PANELİ (Pills) Görünümü */
    div[data-testid="stWidgetLabel"] p {
        color: #ffffff !important;
        font-size: 18px !important;
        font-weight: bold !important;
    }
    
    /* Seçili olan sayının belirgin olması için */
    button[data-testid="stBaseButton-secondary"] {
        border-radius: 8px !important;
    }
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

# 2. Üst Panel (Görünür Sayı Seçimi)
st.title("🔢 PIYC: 6x6 Elite")

# Sürgü yerine yan yana duran büyük butonlar (Pills)
selected_num = st.pills("Koymak istediğin rakamı seç:", [1, 2, 3, 4, 5, 6], selection_mode="single", default=1)

if not st.session_state.game_over:
    st.markdown(f"**Sıra:** Oyuncu {st.session_state.turn}")
else:
    st.success(f"🏆 Kazanan: Oyuncu {st.session_state.winner}")

# 3. Oyun Tahtası
if st.button(label, key=f"b_{r}_{c}", disabled=st.session_state.game_over):
                # GÜVENLİK KONTROLÜ: selected_num None ise işlemi yapma
                if selected_num is None:
                    st.warning("Lütfen önce bir rakam seçin!")
                elif val == 0:
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
                        st.toast(f"Hata: {selected_num} çakışıyor!", icon="❌")

# 4. Alt Kontroller
st.divider()
if st.button("🔄 Yeni Oyun Başlat"):
    st.session_state.board = np.zeros((6, 6), dtype=int)
    st.session_state.turn = 1
    st.session_state.game_over = False
    st.rerun()
