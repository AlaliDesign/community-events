import streamlit as st
import pandas as pd
from datetime import datetime
import os

# --- إعدادات ثابتة للمناسبة (عدلها حسب الحاجة) ---
DATE_OF_EVENT = "الجمعة، 15 مايو 2026"
TIME_OF_EVENT = "08:00 مساءً"
LOCATION_URL = "https://maps.google.com/?q=24.7136,46.6753" # ضع رابط قوقل ماب هنا
# -----------------------------------------------

st.set_page_config(page_title="نظام مناسبات الجماعة", layout="centered")

# التنسيق الملكي المطور
st.markdown(f"""
    <style>
    .main {{ background-color: #000000; }}
    h1 {{ color: #D4AF37; text-align: center; text-shadow: 2px 2px 5px #000; }}
    .event-card {{
        background-color: #1a1a1a;
        border: 1px solid #D4AF37;
        padding: 20px;
        border-radius: 15px;
        text-align: center;
        margin-bottom: 25px;
    }}
    .event-info {{ color: #ffffff; font-size: 1.1em; margin: 5px 0; }}
    .stButton>button {{ 
        border-radius: 12px; border: 2px solid #D4AF37; 
        background-color: #1a1a1a; color: #D4AF37; font-weight: bold; width: 100%;
    }}
    .stButton>button:hover {{ background-color: #D4AF37; color: #000; }}
    </style>
    """, unsafe_allow_html=True)

st.markdown("<h1>⚜️ نظام مناسبات الجماعة ⚜️</h1>", unsafe_allow_html=True)

# 1. بطاقة تفاصيل المناسبة
st.markdown(f"""
    <div class="event-card">
        <h3 style="color: #D4AF37; margin-top: 0;">تفاصيل المناسبة</h3>
        <p class="event-info">📅 <b>التاريخ:</b> {DATE_OF_EVENT}</p>
        <p class="event-info">⏰ <b>الوقت:</b> {TIME_OF_EVENT}</p>
        <br>
        <a href="{LOCATION_URL}" target="_blank" style="text-decoration: none;">
            <button style="background-color: #D4AF37; color: black; border: none; padding: 10px 20px; border-radius: 10px; font-weight: bold; cursor: pointer; width: 80%;">
                📍 عرض موقع المناسبة (Google Maps)
            </button>
        </a>
    </div>
    """, unsafe_allow_html=True)

# 2. إعداد الملفات
EXCEL_FILE = 'names.xlsx'
CSV_RESULTS = 'community_events_results.csv'

def load_names():
    if os.path.exists(EXCEL_FILE):
        df = pd.read_excel(EXCEL_FILE)
        return df.iloc[:, 0].dropna().unique().tolist()
    return []

names_list = load_names()
df_results = pd.read_csv(CSV_RESULTS, encoding='utf-8-sig') if os.path.exists(CSV_RESULTS) else pd.DataFrame(columns=['الاسم', 'الحالة', 'وقت التسجيل'])

# 3. واجهة التسجيل
if not names_list:
    st.error("⚠️ يرجى رفع ملف names.xlsx")
else:
    selected_name = st.selectbox("👤 اختر اسمك لتأكيد الحضور:", options=["-- اختر اسماً --"] + names_list)

    if selected_name != "-- اختر اسماً --":
        col1, col2 = st.columns(2)
        with col1:
            if st.button("✅ سأحضر"):
                new_data = pd.DataFrame({'الاسم': [selected_name], 'الحالة': ['حاضر/تأكيد'], 'وقت التسجيل': [datetime.now().strftime("%Y-%m-%d %I:%M %p")]})
                df_results = pd.concat([df_results[df_results['الاسم'] != selected_name], new_data], ignore_index=True)
                df_results.to_csv(CSV_RESULTS, index=False, encoding='utf-8-sig')
                st.success("تم تأكيد حضورك، حياك الله!")
                st.rerun()
        with col2:
            if st.button("❌ أعتذر"):
                new_data = pd.DataFrame({'الاسم': [selected_name], 'الحالة': ['معتذر'], 'وقت التسجيل': [datetime.now().strftime("%Y-%m-%d %I:%M %p")]})
                df_results = pd.concat([df_results[df_results['الاسم'] != selected_name], new_data], ignore_index=True)
                df_results.to_csv(CSV_RESULTS, index=False, encoding='utf-8-sig')
                st.warning("تم تسجيل اعتذارك.")
                st.rerun()

# 4. عرض الكشف (اختياري)
st.divider()
with st.expander("📊 كشف حضور المناسبة"):
    st.dataframe(df_results, use_container_width=True, hide_index=True)

st.markdown("<p style='text-align: center; color: #555; font-size: 0.8em;'>تصميم وبرمجة: أبو فيصل للعقارات</p>", unsafe_allow_html=True)