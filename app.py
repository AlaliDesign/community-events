import streamlit as st
import pandas as pd
from datetime import datetime
import os

# --- 1. إعدادات الصفحة ---
st.set_page_config(page_title="مناسبات آل علي", layout="centered", page_icon="logo.png")

# --- 2. التنسيق الجمالي (البرواز والخطوط) ---
st.markdown("""
    <style>
    /* استيراد خط النسخ العربي */
    @import url('https://fonts.googleapis.com/css2?family=Amiri&family=Tajawal:wght@400;700&display=swap');

    .main { 
        background-color: #f9f9f9; 
    }
    
    /* تصميم البرواز المحيط بالتطبيق */
    .block-container {
        border: 3px double #D4AF37;
        padding: 30px !important;
        border-radius: 20px;
        background-color: white;
        box-shadow: 0 10px 25px rgba(0,0,0,0.1);
        margin-top: 20px;
        margin-bottom: 20px;
    }

    /* تنسيق البسملة */
    .bismillah {
        font-family: 'Amiri', serif;
        font-size: 2.2em;
        color: #1a1a1a;
        text-align: center;
        margin-bottom: 10px;
        font-weight: bold;
    }

    /* توسيط وتكبير الشعار */
    .logo-box {
        display: flex;
        justify-content: center;
        margin-bottom: 15px;
    }
    .logo-box img {
        width: 180px !important;
        height: auto;
    }

    /* العنوان الرئيسي */
    .main-title { 
        color: #D4AF37; 
        text-align: center; 
        font-size: 1.6em !important; 
        font-family: 'Tajawal', sans-serif;
        font-weight: bold;
        margin-bottom: 30px;
        border-bottom: 2px solid #eee;
        padding-bottom: 10px;
    }
    
    /* تنسيق العدادات الإحصائية */
    [data-testid="stMetric"] {
        background-color: #fff9e6; 
        border: 1px solid #D4AF37;
        padding: 15px !important;
        border-radius: 12px;
        text-align: center;
        box-shadow: 2px 2px 5px rgba(0,0,0,0.05);
    }
    
    [data-testid="stMetricValue"] { color: #1a1a1a !important; font-size: 1.4em !important; font-weight: bold !important; }

    /* أزرار الحضور */
    .stButton>button { 
        border-radius: 12px; border: 2px solid #D4AF37; 
        background-color: #1a1a1a; color: white; 
        font-weight: bold; width: 100%; height: 3.8em;
        transition: 0.3s;
    }
    .stButton>button:hover {
        background-color: #D4AF37;
        color: black;
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

# --- 4. واجهة العرض (البسملة والشعار) ---

# البسملة بخط نسخ مرتب
st.markdown("<div class='bismillah'>بِسْمِ اللهِ الرَّحْمٰنِ الرَّحِيْمِ</div>", unsafe_allow_html=True)

# عرض الشعار في المنتصف
if os.path.exists("logo.png"):
    st.markdown('<div class="logo-box">', unsafe_allow_html=True)
    st.image("logo.png", width=180)
    st.markdown('</div>', unsafe_allow_html=True)
else:
    st.markdown("<h1 style='text-align:center;'>⚜️</h1>", unsafe_allow_html=True)

st.markdown("<div class='main-title'>مناسبات جماعة آل علي بالرياض</div>", unsafe_allow_html=True)

# تحميل الأسماء
if 'names' not in st.session_state:
    st.session_state.names = load_names()
names_list = st.session_state.names

# --- 5. تسجيل الحضور ---
if names_list:
    selected_name = st.selectbox("🔍 ابحث عن اسمك لتسجيل الحضور:", options=["-- اختر من القائمة --"] + names_list)

    if selected_name != "-- اختر من القائمة --":
        col1, col2 = st.columns(2)
        with col1:
            if st.button("✅ تأكيد الحضور"):
                res = load_results()
                new_row = pd.DataFrame({'الاسم': [selected_name], 'الحالة': ['حاضر'], 'الوقت': [datetime.now().strftime("%I:%M %p")]})
                pd.concat([res[res['الاسم'] != selected_name], new_row], ignore_index=True).to_csv(CSV_RESULTS, index=False, encoding='utf-8-sig')
                st.success("تم تأكيد حضورك، حياك الله")
                st.rerun()
        with col2:
            if st.button("❌ تقديم اعتذار"):
                res = load_results()
                new_row = pd.DataFrame({'الاسم': [selected_name], 'الحالة': ['معتذر'], 'الوقت': [datetime.now().strftime("%I:%M %p")]})
                pd.concat([res[res['الاسم'] != selected_name], new_row], ignore_index=True).to_csv(CSV_RESULTS, index=False, encoding='utf-8-sig')
                st.warning("تم تسجيل اعتذارك، نراك في مناسبات قادمة")
                st.rerun()

st.write("") 
st.divider()

# --- 6. إحصائيات الفرز العام (عادت للظهور) ---
df_results = load_results()
total_in_list = len(names_list)
total_responded = len(df_results)

st.markdown("<h3 style='color:#D4AF37; text-align:center; font-family:Tajawal;'>📊 إحصائيات الفرز العام</h3>", unsafe_allow_html=True)

# عرض العدادات بشكل مرتب وجمالي
c1, c2 = st.columns(2)
with c1: st.metric("إجمالي القائمة", total_in_list)
with c2: st.metric("إجمالي المتفاعلين", total_responded)

c3, c4 = st.columns(2)
with c3: st.metric("✅ عدد الحاضرين", len(df_results[df_results['الحالة'] == 'حاضر']))
with c4: st.metric("❌ عدد المعتذرين", len(df_results[df_results['الحالة'] == 'معتذر']))

# --- 7. الإدارة ---
with st.expander("⚙️ لوحة تحكم المشرف"):
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
            to_del = st.selectbox("اختر للحذف:", options=["-- اختر --"] + st.session_state.names)
            if st.button("تأكيد الحذف"):
                if to_del != "-- اختر --":
                    st.session_state.names.remove(to_del)
                    save_names(st.session_state.names)
                    st.rerun()
        with tab3:
            if st.button("تصفير الكشف"):
                if os.path.exists(CSV_RESULTS): os.remove(CSV_RESULTS)
                st.rerun()

st.markdown("<p style='text-align:center; color:#888; font-size:0.8em; margin-top:50px;'>تصميم وبرمجة: أبو فيصل للعقارات 2026</p>", unsafe_allow_html=True)