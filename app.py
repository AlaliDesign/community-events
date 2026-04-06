import streamlit as st
import pandas as pd
from datetime import datetime
import os

# --- 1. إعدادات الصفحة ---
st.set_page_config(page_title="مناسبات آل علي", layout="centered", page_icon="logo.png")

# --- 2. التنسيق المتطور (توسيط وتكبير الشعار) ---
st.markdown("""
    <style>
    .main { background-color: #080808; }
    
    /* تنسيق الحاوية لتوسيط الشعار تماماً */
    .logo-wrapper {
        display: flex;
        justify-content: center;
        align-items: center;
        padding: 20px 0;
    }
    
    .centered-logo {
        width: 150px !important; /* حجم أكبر وواضح */
        border-radius: 10px;
    }

    .main-title { 
        color: #D4AF37; 
        text-align: center; 
        font-size: 1.5em !important; /* تكبير العنوان قليلاً */
        font-weight: bold;
        margin-top: 10px;
        margin-bottom: 25px;
    }
    
    [data-testid="stMetric"] {
        background-color: #fdfdfd; 
        border: 1px solid #D4AF37;
        padding: 10px !important;
        border-radius: 8px;
        text-align: center;
    }
    
    .stButton>button { 
        border-radius: 10px; border: 1.5px solid #D4AF37; 
        background-color: #1a1a1a; color: #D4AF37; 
        font-weight: bold; width: 100%; height: 3.5em;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 3. وظائف البيانات ---
EXCEL_FILE = 'names.xlsx'
CSV_RESULTS = 'community_events_results.csv'

def load_names():
    if os.path.exists(EXCEL_FILE):
        try:
            df = pd.read_excel(EXCEL_FILE)
            return sorted(df.iloc[:, 0].dropna().unique().tolist())
        except: return []
    return []

def save_names(names_list):
    df = pd.DataFrame(names_list, columns=['الاسم'])
    df.to_excel(EXCEL_FILE, index=False)

def load_results():
    if os.path.exists(CSV_RESULTS):
        try: return pd.read_csv(CSV_RESULTS, encoding='utf-8-sig')
        except: return pd.DataFrame(columns=['الاسم', 'الحالة', 'الوقت'])
    return pd.DataFrame(columns=['الاسم', 'الحالة', 'الوقت'])

if 'input_key' not in st.session_state:
    st.session_state.input_key = 0

# --- 4. عرض الشعار والعنوان في المنتصف ---

# عرض الشعار باستخدام كود HTML لضمان التوسيط الكامل
# ملاحظة: تأكد من وجود ملف باسم logo.png في نفس المجلد على GitHub
if os.path.exists("logo.png"):
    st.image("logo.png", width=150) # استخدام الدالة المباشرة أضمن للظهور
else:
    st.markdown("<h1 style='text-align:center;'>⚜️</h1>", unsafe_allow_html=True)

st.markdown("<div class='main-title'>مناسبات جماعة آل علي بالرياض</div>", unsafe_allow_html=True)

# --- باقي الكود البرمجي (كما هو لضمان استقرار الإضافة والحذف) ---
if 'names' not in st.session_state:
    st.session_state.names = load_names()

names_list = st.session_state.names

if names_list:
    selected_name = st.selectbox("🔍 ابحث عن اسمك:", options=["-- اختر من القائمة --"] + names_list)

    if selected_name != "-- اختر من القائمة --":
        col1, col2 = st.columns(2)
        with col1:
            if st.button("✅ حضور"):
                res = load_results()
                new_row = pd.DataFrame({'الاسم': [selected_name], 'الحالة': ['حاضر'], 'الوقت': [datetime.now().strftime("%I:%M %p")]})
                pd.concat([res[res['الاسم'] != selected_name], new_row], ignore_index=True).to_csv(CSV_RESULTS, index=False, encoding='utf-8-sig')
                st.success("تم التأكيد")
                st.rerun()
        with col2:
            if st.button("❌ اعتذار"):
                res = load_results()
                new_row = pd.DataFrame({'الاسم': [selected_name], 'الحالة': ['معتذر'], 'الوقت': [datetime.now().strftime("%I:%M %p")]})
                pd.concat([res[res['الاسم'] != selected_name], new_row], ignore_index=True).to_csv(CSV_RESULTS, index=False, encoding='utf-8-sig')
                st.warning("تم تسجيل الاعتذار")
                st.rerun()

st.divider()
df_final = load_results()
if not df_final.empty:
    c1, c2, c3 = st.columns(3)
    with c1: st.metric("المسجلين", len(df_final))
    with c2: st.metric("✅ حاضر", len(df_final[df_final['الحالة'] == 'حاضر']))
    with c3: st.metric("❌ معتذر", len(df_final[df_final['الحالة'] == 'معتذر']))

with st.expander("⚙️ إعدادات الإدارة"):
    admin_pass = st.text_input("الرقم السري:", type="password")
    if admin_pass == "1234":
        tab1, tab2, tab3 = st.tabs(["➕ إضافة", "🗑️ حذف", "🧹 تصفير"])
        with tab1:
            new_person = st.text_input("الاسم الجديد:", key=f"ins_{st.session_state.input_key}")
            if st.button("حفظ"):
                if new_person:
                    clean_n = new_person.strip()
                    if clean_n not in st.session_state.names:
                        st.session_state.names.append(clean_n)
                        save_names(sorted(st.session_state.names))
                        st.session_state.input_key += 1
                        st.rerun()
        with tab2:
            to_del = st.selectbox("حذف:", options=["-- اختر --"] + st.session_state.names)
            if st.button("تأكيد الحذف"):
                if to_del != "-- اختر --":
                    st.session_state.names.remove(to_del)
                    save_names(st.session_state.names)
                    st.rerun()
        with tab3:
            if st.button("تصفير الكل"):
                if os.path.exists(CSV_RESULTS): os.remove(CSV_RESULTS)
                st.rerun()

st.markdown("<p style='text-align:center; color:#555; font-size:0.8em;'>تصميم: أبو فيصل للعقارات 2026</p>", unsafe_allow_html=True)