import streamlit as st
import pandas as pd
from datetime import datetime
import os

# --- 1. إعدادات الصفحة ---
st.set_page_config(page_title="مناسبات آل علي", layout="centered", page_icon="logo.png")

# --- 2. التنسيق الملكي المريح للعين ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Amiri&family=Tajawal:wght@400;700&display=swap');
    .stApp { background-color: #F5F5DC; }
    .main .block-container {
        border: 2px solid #D4AF37;
        padding: 20px !important;
        border-radius: 15px;
        background-color: #ffffff;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
        margin: 10px auto;
        max-width: 95% !important;
    }
    .bismillah { font-family: 'Amiri', serif; font-size: 2em; color: #1a1a1a; text-align: center; margin-bottom: 5px; }
    .logo-wrapper { display: flex; justify-content: center; width: 100%; margin-bottom: 10px; }
    .logo-wrapper img { width: 170px !important; height: auto; }
    .main-title { color: #D4AF37; text-align: center; font-size: 1.4em !important; font-family: 'Tajawal', sans-serif; font-weight: bold; margin-bottom: 25px; }
    [data-testid="stMetric"] { background-color: #FFFDF5; border: 1px solid #D4AF37; border-radius: 10px; text-align: center; }
    .stButton>button { border-radius: 10px; border: 2px solid #D4AF37; background-color: #1a1a1a; color: #D4AF37; font-weight: bold; width: 100%; height: 3.5em; }
    </style>
    """, unsafe_allow_html=True)

# --- 3. إدارة البيانات ---
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

if os.path.exists("logo.png"):
    st.markdown('<div class="logo-wrapper">', unsafe_allow_html=True)
    st.image("logo.png", width=170)
    st.markdown('</div>', unsafe_allow_html=True)

st.markdown("<div class='main-title'>مناسبات جماعة آل علي بالرياض</div>", unsafe_allow_html=True)

if 'names' not in st.session_state:
    st.session_state.names = load_names()
names_list = st.session_state.names

# --- 5. حقل البحث وتسجيل الحضور ---
if names_list:
    st.markdown("<p style='text-align:right; font-weight:bold; color:#555;'>🔍 ابحث عن اسمك في القائمة:</p>", unsafe_allow_html=True)
    selected_name = st.selectbox("", options=["-- اختر من هنا أو اكتب اسمك للبحث --"] + names_list, label_visibility="collapsed")

    if selected_name != "-- اختر من هنا أو اكتب اسمك للبحث --":
        col1, col2 = st.columns(2)
        with col1:
            if st.button("✅ تأكيد الحضور"):
                res = load_results()
                new_row = pd.DataFrame({'الاسم': [selected_name], 'الحالة': ['حاضر'], 'الوقت': [datetime.now().strftime("%I:%M %p")]})
                pd.concat([res[res['الاسم'] != selected_name], new_row], ignore_index=True).to_csv(CSV_RESULTS, index=False, encoding='utf-8-sig')
                st.success("تم تأكيد حضورك")
                st.rerun()
        with col2:
            if st.button("❌ تقديم اعتذار"):
                res = load_results()
                new_row = pd.DataFrame({'الاسم': [selected_name], 'الحالة': ['معتذر'], 'الوقت': [datetime.now().strftime("%I:%M %p")]})
                pd.concat([res[res['الاسم'] != selected_name], new_row], ignore_index=True).to_csv(CSV_RESULTS, index=False, encoding='utf-8-sig')
                st.warning("تم تسجيل اعتذارك")
                st.rerun()

st.divider()

# --- 6. الإحصائيات ---
df_results = load_results()
total_all = len(names_list)
total_done = len(df_results)
st.markdown("<h3 style='color:#D4AF37; text-align:center;'>📊 إحصائيات الفرز العام</h3>", unsafe_allow_html=True)
c1, c2 = st.columns(2)
with c1: st.metric("إجمالي القائمة", total_all)
with c2: st.metric("إجمالي المتفاعلين", total_done)

# --- 7. لوحة التحكم (تعديل منع التكرار هنا) ---
with st.expander("⚙️ لوحة تحكم المشرف"):
    admin_pass = st.text_input("كلمة المرور:", type="password")
    if admin_pass == "1234":
        tab1, tab2, tab3 = st.tabs(["➕ إضافة", "🗑️ حذف", "🧹 تصفير"])
        with tab1:
            new_p = st.text_input("أدخل الاسم لإضافته:", key=f"ins_{st.session_state.input_key}")
            if st.button("حفظ الاسم الجديد"):
                if new_p:
                    clean_n = new_p.strip()
                    # التحقق الذكي من وجود الاسم مسبقاً
                    if clean_n in st.session_state.names:
                        st.error(f"⚠️ تنبيه: الاسم ({clean_n}) مضاف مسبقاً في القائمة!")
                    else:
                        st.session_state.names.append(clean_n)
                        st.session_state.names = sorted(st.session_state.names)
                        save_names(st.session_state.names)
                        st.session_state.input_key += 1
                        st.success(f"✅ تم حفظ {clean_n} بنجاح")
                        st.rerun()
        with tab2:
            to_del = st.selectbox("اختر اسماً لحذفه:", options=["-- اختر --"] + st.session_state.names)
            if st.button("حذف نهائي"):
                if to_del != "-- اختر --":
                    st.session_state.names.remove(to_del)
                    save_names(st.session_state.names)
                    st.rerun()
        with tab3:
            if st.button("تفريغ كشف الحضور"):
                if os.path.exists(CSV_RESULTS): os.remove(CSV_RESULTS)
                st.rerun()

st.markdown("<p style='text-align:center; color:#888; font-size:0.8em; margin-top:30px;'>تصميم وبرمجة: أبو فيصل للعقارات 2026</p>", unsafe_allow_html=True)