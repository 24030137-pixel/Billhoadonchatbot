import streamlit as st
from datetime import datetime
from io import BytesIO
import unicodedata
import re
import os

# =========================================================
# CẤU HÌNH TRANG
# =========================================================

st.set_page_config(
    page_title="Lucky Tea",
    page_icon="🧋",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# =========================================================
# CSS GIAO DIỆN
# =========================================================

st.markdown(
    """
    <style>
    .main { padding-top: 1rem; }

    .lucky-title {
        text-align: center;
        font-size: 42px;
        font-weight: 800;
        margin-top: 10px;
        margin-bottom: 0px;
    }

    .lucky-subtitle {
        text-align: center;
        font-size: 17px;
        margin-bottom: 20px;
    }

    .total-box {
        padding: 20px;
        border-radius: 15px;
        text-align: center;
        border: 2px solid rgba(128,128,128,0.35);
        margin-top: 15px;
        margin-bottom: 15px;
    }

    .total-title { font-size: 18px; font-weight: 600; }
    .total-money { font-size: 32px; font-weight: 800; }

    .bill-number {
        text-align: center;
        font-size: 23px;
        font-weight: 700;
        margin-bottom: 15px;
    }

    div.stButton > button {
        border-radius: 10px;
        font-weight: 600;
        min-height: 45px;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# =========================================================
# DỮ LIỆU MENU
# ---------------------------------------------------------
# price : giá size M
# sold  : số ly đã bán (dùng để xếp hạng bán chạy - bạn tự sửa)
# new   : True nếu là món mới
# tags  : đặc điểm để chatbot lọc theo sở thích
# desc  : mô tả ngắn chatbot sẽ nói
# =========================================================

DRINK_INFO = {
    "Trà sữa truyền thống": {
        "price": 25000, "sold": 950, "new": False,
        "tags": ["tra sua", "beo", "ngot"],
        "desc": "Vị cổ điển, béo nhẹ, dễ uống."
    },
    "Trà sữa trân châu":
