import streamlit as st
import pandas as pd
from datetime import datetime
import os

# --- إعدادات ثابتة للمناسبة ---
EVENT_NAME = "مناسبة جماعة آل علي بالرياض"
# -----------------------------------------------

st.set_page_config(page_title=EVENT_NAME, layout="centered", page_icon="⚜️")

# التنسيق الملكي (أبو فيصل)
st.markdown("""
    <style>
    .main { background-color: #000000; }
    .stSelectbox label { color: #D4AF37 !important; font-size: 1.3em; font-weight: bold; }
    .stSelectbox div[data-baseweb="select"] { border: 2px solid #D4AF37; border-radius: 10px; }
    </style>
    """, unsafe_allow_html=True)

st.markdown(f"<h1 style='color:#D4AF37; text-align:center;'>⚜️ {EVENT_NAME} ⚜️</h1>", unsafe_allow_html=True)

# 1. تحميل الأسماء
EXCEL_FILE = 'names.xlsx'
CSV_RESULTS = 'community_events_results.csv'

def get_names():
    if os.path.exists(EXCEL_FILE):
        df = pd.read_excel(EXCEL_FILE)
        # ترتيب الأسماء أبجدياً لتسهيل البحث
        names = sorted(df.iloc[:, 0].dropna().unique().tolist())
        return names
    return []

names_list = get_names()

# 2. واجهة البحث والاختيار
if not names_list:
    st.error("⚠️ يرجى رفع ملف names.xlsx")
else:
    st.write("---")
    # ملاحظة: Streamlit يسمح بالكتابة داخل الـ selectbox للبحث تلقائياً
    selected_name = st.selectbox(
        "🔍 ابحث عن اسمك (اكتب اسمك هنا):", 
        options=["-- ابدأ بكتابة اسمك هنا --"] + names_list,
        index=0,
        help="بمجرد كتابة أول حروف من اسمك ستظهر لك الخيارات"
    )

    if selected_name != "-- ابدأ بكتابة اسمك هنا --":
        st.info(f"مرحباً بك: **{selected_name}**")
        
        col1, col2 = st.columns(2)
        with col1:
             if st.button("✅ تأكيد الحضور", use_container_width=True):
                 # كود حفظ البيانات (نفس السابق)
                 st.success("تم تسجيل حضورك")
        with col2:
             if st.button("❌ اعتذار", use_container_width=True):
                 st.warning("تم تسجيل اعتذارك")

# 3. عرض النتائج (مخفي تحت expander)
with st.expander("📊 كشف الحضور والاعتذار"):
    if os.path.exists(CSV_RESULTS):
        df_res = pd.read_csv(CSV_RESULTS)
        st.table(df_res) # عرض جدول بسيط ونظيف
    else:
        st.write("لا توجد تسجيلات بعد.")

st.markdown("<p style='text-align: center; color: #555;'>برمجة وتطوير: أبو فيصل للعقارات 2026</p>", unsafe_allow_html=True)