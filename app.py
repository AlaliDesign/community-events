import streamlit as st
import pandas as pd
from datetime import datetime
import os

# --- 1. إعدادات الصفحة ---
st.set_page_config(page_title="مناسبات آل علي", layout="centered", page_icon="logo.png")

# --- 2. التنسيق المتطور (لراحة العين والتوافق مع الجوال) ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Amiri&family=Tajawal:wght@400;700&display=swap');

    /* تغيير خلفية التطبيق للون كريمي مريح للعين */
    .stApp {
        background-color: #F5F5DC; 
    }
    
    /* تصميم البرواز الملكي المتجاوب مع الجوال */
    .main .block-container {
        border: 2px solid #D4AF37;
        padding: 20px !important;
        border-radius: 15px;
        background-color: #ffffff; /* محتوى البطاقة أبيض صافي */
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
        margin: 10px auto;
        max-width: 95% !important; /* ضمان ظهور البرواز في الجوال */
    }

    /* البسملة */
    .bismillah {
        font-family: 'Amiri', serif;
        font-size: 1.8em;
        color: #1a1a1a;
        text-align: center;
        margin-bottom: 5px;
    }

    /* التوسيط المطلق للشعار وتعديل المقاس */
    .centered-logo-wrapper {
        display: flex;
        justify-content: center;
        align-items: center;
        width: 100%;
        margin: 10px 0;
    }
    .centered-logo-wrapper img {
        width: 160px !important; /* مقاس متوازن للجوال والكمبيوتر */
        height: auto;
    }

    /* العنوان */
    .main-title { 
        color: #D4AF37; 
        text-align: center; 
        font-size: 1.3em !important; 
        font-family: 'Tajawal', sans-serif;
        font-weight: bold;
        margin-bottom: 20px;
    }
    
    /* العدادات */
    [data-testid="stMetric"] {
        background-color: #FFFDF5; 
        border: 1px solid #D4AF37;
        border-radius: 10px;
        text-align: center;
    }

    /* الأزرار */
    .stButton>button { 
        border-radius: 10px; border: 2px solid #D4AF37; 
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

# --- 4. واجهة العرض ---

st.markdown("<div class='bismillah'>بِسْمِ اللهِ الرَّحْمٰنِ الرَّحِيْمِ</div>", unsafe_allow_html=True)

# التوسيط المطلق للشعار باستخدام HTML و CSS
if os.path.exists("logo.png"):
    st.markdown("""
        <div class="centered-logo-wrapper">
            <img src="https://raw.githubusercontent.com/mohammad-alali/community-events/main/logo.png" onerror="this.src='app/static/logo.png'">
        </div>
        """, unsafe_allow_html=True)
else:
    st.markdown("<h1 style='text-align:center;'>⚜️</h1>", unsafe_allow_html=True)

st.markdown("<div class='main-title'>مناسبات جماعة آل علي بالرياض</div>", unsafe_allow_html=True)

# تحميل الأسماء
if 'names' not in st.session_state:
    st.session_state.names = load_names()
names_list = st.session_state.names

# --- 5. تسجيل الحضور ---
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
                st.warning("تم التسجيل")
                st.rerun()

st.divider()

# --- 6. إحصائيات الفرز العام ---
df_results = load_results()
total_in_list = len(names_list)
total_responded = len(df_results)

st.markdown("<h3 style='color:#D4AF37; text-align:center;'>📊 إحصائيات الفرز العام</h3>", unsafe_allow_html=True)

c1, c2 = st.columns(2)
with c1: st.metric("إجمالي القائمة", total_in_list)
with c2: st.metric("إجمالي المتفاعلين", total_responded)

c3, c4 = st.columns(2)
with c3: st.metric("✅ الحضور", len(df_results[df_results['الحالة'] == 'حاضر']))
with c4: st.metric("❌ المعتذرين", len(df_results[df_results['الحالة'] == 'معتذر']))

# --- 7. الإدارة ---
with st.expander("⚙️ لوحة التحكم"):
    admin_pass = st.text_input("الرقم السري:", type="password")
    if admin_pass == "1234":
        tab1, tab2, tab3 = st.tabs(["➕ إضافة", "🗑️ حذف", "🧹 تصفير"])
        with tab1:
            new_p = st.text_input("الاسم الجديد:", key=f"ins_{st.session_state.input_key}")
            if st.button("حفظ"):
                if new_p:
                    clean_n = new_p.strip()
                    if clean_n not in st.session_state.names:
                        st.session_state.names.append(clean_n)
                        save_names(sorted(st.session_state.names))
                        st.session_state.input_key += 1
                        st.rerun()
        with tab2:
            to_del = st.selectbox("حذف اسم:", options=["-- اختر --"] + st.session_state.names)
            if st.button("تأكيد"):
                if to_del != "-- اختر --":
                    st.session_state.names.remove(to_del)
                    save_names(st.session_state.names)
                    st.rerun()
        with tab3:
            if st.button("تصفير الكشف"):
                if os.path.exists(CSV_RESULTS): os.remove(CSV_RESULTS)
                st.rerun()

st.markdown("<p style='text-align:center; color:#888; font-size:0.8em; margin-top:30px;'>تصميم وبرمجة: أبو فيصل للعقارات 2026</p>", unsafe_allow_html=True)