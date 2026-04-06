import streamlit as st
import pandas as pd
from datetime import datetime
import os

# --- إعدادات ثابتة للمناسبة ---
EVENT_NAME = "مناسبة الجماعة الكبرى"
DATE_OF_EVENT = "الجمعة، 15 مايو 2026"
TIME_OF_EVENT = "08:00 مساءً"
LOCATION_URL = "https://maps.app.goo.gl/xxxx" # ضع رابط الخريطة هنا
# -----------------------------------------------

st.set_page_config(page_title="نظام مناسبات الجماعة", layout="centered", page_icon="⚜️")

# التنسيق الملكي مع إضافة كود لجعل الواجهة تبدو كتطبيق جوال
st.markdown(f"""
    <style>
    .main {{ background-color: #000000; }}
    [data-testid="stHeader"] {{ background: rgba(0,0,0,0); }}
    
    /* رسالة إرشادية للتثبيت */
    .install-hint {{
        background-color: #D4AF37;
        color: #000;
        padding: 10px;
        border-radius: 10px;
        text-align: center;
        font-weight: bold;
        margin-bottom: 20px;
        font-size: 0.9em;
        border: 2px solid #fff;
    }}

    .event-card {{
        background-color: #1a1a1a;
        border: 2px solid #D4AF37;
        padding: 20px;
        border-radius: 20px;
        text-align: center;
        box-shadow: 0 4px 15px rgba(212, 175, 55, 0.3);
    }}
    
    .stButton>button {{ 
        border-radius: 15px; border: 2px solid #D4AF37; 
        background-color: #1a1a1a; color: #D4AF37; 
        font-weight: bold; width: 100%; height: 3.5em;
    }}
    </style>
    """, unsafe_allow_html=True)

# رسالة "تثبيت التطبيق" تظهر في الأعلى
with st.container():
    st.markdown("""
        <div class="install-hint">
        📱 لجعل البرنامج تطبيقاً ثابتاً على جوالك:<br>
        <b>للأيفون:</b> اضغط سهم المشاركة ثم "إضافة للشاشة الرئيسية"<br>
        <b>للأندرويد:</b> اضغط النقاط الثلاث ثم "تثبيت التطبيق"
        </div>
    """, unsafe_allow_html=True)

st.markdown(f"<h1 style='color:#D4AF37; text-align:center;'>⚜️ {EVENT_NAME} ⚜️</h1>", unsafe_allow_html=True)

# بطاقة المناسبة
st.markdown(f"""
    <div class="event-card">
        <p style="color: #D4AF37; font-size: 1.2em; margin-bottom: 5px;">📅 {DATE_OF_EVENT}</p>
        <p style="color: #ffffff; margin-bottom: 15px;">⏰ {TIME_OF_EVENT}</p>
        <a href="{LOCATION_URL}" target="_blank" style="text-decoration: none;">
            <button style="background-color: #D4AF37; color: black; border: none; padding: 12px; border-radius: 12px; font-weight: bold; width: 90%; cursor: pointer;">
                📍 موقع المجلس (قوقل ماب)
            </button>
        </a>
    </div>
    """, unsafe_allow_html=True)

# بقية الكود (الأسماء والتسجيل) كما هي...
EXCEL_FILE = 'names.xlsx'
CSV_RESULTS = 'community_events_results.csv'

if os.path.exists(EXCEL_FILE):
    df_names = pd.read_excel(EXCEL_FILE)
    names_list = df_names.iloc[:, 0].dropna().unique().tolist()
    
    st.write("###")
    selected_name = st.selectbox("👤 اختر اسمك لتأكيد الحضور:", options=["-- اختر اسماً --"] + names_list)

    if selected_name != "-- اختر اسماً --":
        col1, col2 = st.columns(2)
        # (هنا تضع أكواد أزرار الحضور والاعتذار التي استخدمناها سابقاً)
        with col1:
             if st.button("✅ تأكيد الحضور"):
                 st.success("تم التسجيل يا أبا فيصل!") # مثال
        with col2:
             if st.button("❌ اعتذار"):
                 st.warning("تم تسجيل الاعتذار")

# التوقيع
st.markdown("<br><p style='text-align: center; color: #D4AF37; font-size: 0.8em; opacity: 0.6;'>تصميم وبرمجة: صقر العقارات 2026</p>", unsafe_allow_html=True)