# -*- coding: utf-8 -*-
"""
Created on Thu May 14 09:46:24 2026

@author: User
"""

import streamlit as st
import numpy as np

# Sayfa Yapılandırması
st.set_page_config(page_title="PIYC Elite 6x6", layout="centered")

# --- MOBİL UYUMLU CSS (IZGARA ZORLAMASI) ---
st.markdown("""
    <style>
    /* Sütunların mobilde alt alta gelmesini engelle, yan yana tut */
    [data-testid="column"] {
        width: calc(16.6% - 5px) !important;
        flex: 1 1 calc(16.6% - 5px) !important;
        min-width: calc(16.6% - 5px) !important;
    }
    
    /* Buton boyutlarını telefon ekranı için optimize et */
    .stButton>button {
        height: 55px !important; 
        width: 100% !important; 
        font-size: 18px !important; 
        font-weight: bold !important;
        padding: 0px !important;
        margin: 2px 0px !important;
    }
    
    /* Konteynır boşluklarını daralt */
    .block-container {
        padding-top: 1rem !important;
        padding-left: 0.5rem !important;
        padding-right: 0.5rem !important;
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

# 3. Başlık ve Durum
st.title("🔢 PIYC: 6x6 Elite")

if not st.session_state.game_over:
    st.write(f"Sıradaki: **Oyuncu {st.session_state.turn}**")
else:
    st.success(f"🏆 Kazanan: **Oyuncu {st.session_state.winner}**")

# 4. Rakam Seçimi
selected_num = st.pills("Seç:", [1, 2, 3, 4, 5, 6], selection_mode="single", default=1)

# 5. 6x6 Izgara (Mobil Uyumlu)
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
                        st.toast(f"Hata: {selected_num} çakışıyor!", icon="❌")

# Reset
if st.button("🔄 Yeni Oyun"):
    del st.session_state.board
    st.rerun()