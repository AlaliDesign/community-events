import streamlit as st
import pandas as pd
from datetime import datetime
from PIL import Image
import os

# --- 1. إعدادات الصفحة ---
st.set_page_config(page_title="مناسبات آل علي", layout="centered", page_icon="logo.png")

# --- 2. التنسيق الملكي المطور (إخفاء الشعار الافتراضي + دائرة الشعار) ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Amiri&family=Tajawal:wght@400;700&display=swap');
    
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}

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

    .bismillah { font-family: 'Amiri', serif; font-size: 2.2em; color: #1a1a1a; text-align: center; margin-bottom: 10px; }
    
    /* تنسيق حاوية الشعار لضمان التوسط */
    .logo-container {
        display: flex;
        justify-content: center;
        margin-bottom: 20px;
    }

    .main-title { 
        color: #D4AF37; 
        text-align: center; 
        font-size: 1.5em !important; 
        font-family: 'Tajawal', sans-serif;
        font-weight: bold;
        margin-bottom: 25px;
    }
    
    [data-testid="stMetric"] {
        background-color: #FFFDF5; 
        border: 1px solid #D4AF37;
        border-radius: 10px;
        text-align: center;
    }

    .stButton>button { 
        border-radius: 10px; border: 2px solid #D4AF37; 
        background-color: #1a1a1a; color: #D4AF37; 
        font-weight: bold; width: 100%; height: 3.5em;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 3. وظيفة عرض الشعار الدائري بشكل مضمون ---
def display_circular_logo(image_path):
    if os.path.exists(image_path):
        img = Image.open(image_path)
        # عرض الصورة باستخدام Streamlit مع تنسيق CSS للدائرة
        st.markdown('<div class="logo-container">', unsafe_allow_html=True)
        st.image(img, width=150) # سيتم تحويلها لدائرة عبر التنسيق أدناه
        st.markdown("""
            <style>
            /* استهداف الصورة المرفوعة داخل الحاوية */
            [data-testid="stImage"] img {
                border-radius: 50%;
                border: 3px solid #D4AF37;
                box-shadow: 0 4px 8px rgba(0,0,0,0.2);
            }
            </style>
            </div>
            """, unsafe_allow_html=True)

# --- 4. إدارة البيانات ---
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

# --- 5. واجهة العرض ---
st.markdown("<div class='bismillah'>بِسْمِ اللهِ الرَّحْمٰنِ الرَّحِيْمِ</div>", unsafe_allow_html=True)

# استدعاء دالة عرض الشعار
display_circular_logo("logo.png")

st.markdown("<div class='main-title'>مناسبات جماعة آل علي بالرياض</div>", unsafe_allow_html=True)

if 'names' not in st.session_state:
    st.session_state.names = load_names()
names_list = st.session_state.names

# --- 6. حقل البحث وتسجيل الحضور ---
if names_list:
    selected_name = st.selectbox("🔍 ابحث عن اسمك لتسجيل الحضور:", options=["-- اختر من القائمة --"] + names_list)

    if selected_name != "-- اختر من القائمة --":
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

# --- 7. إحصائيات الفرز العام ---
df_results = load_results()
total_all = len(names_list)
total_present = len(df_results[df_results['الحالة'] == 'حاضر'])
total_absent = len(df_results[df_results['الحالة'] == 'معتذر'])

st.markdown("<h3 style='color:#D4AF37; text-align:center;'>📊 إحصائيات الفرز العام</h3>", unsafe_allow_html=True)

c1, c2, c3 = st.columns(3)
with c1: st.metric("إجمالي القائمة", total_all)
with c2: st.metric("✅ حاضر", total_present)
with c3: st.metric("❌ معتذر", total_absent)

# --- 8. لوحة التحكم ---
with st.expander("⚙️ لوحة تحكم المشرف"):
    admin_pass = st.text_input("كلمة المرور:", type="password")
    if admin_pass == "1234":
        tab1, tab2, tab3 = st.tabs(["➕ إضافة", "🗑️ حذف", "🧹 تصفير"])
        with tab1:
            new_p = st.text_input("أدخل الاسم الجديد:", key=f"ins_{st.session_state.input_key}")
            if st.button("حفظ الاسم"):
                if new_p and new_p.strip() not in st.session_state.names:
                    st.session_state.names.append(new_p.strip())
                    st.session_state.names = sorted(st.session_state.names)
                    save_names(st.session_state.names)
                    st.session_state.input_key += 1
                    st.success("✅ تم الحفظ")
                    st.rerun()
        with tab2:
            to_del = st.selectbox("حذف اسم:", options=["-- اختر --"] + st.session_state.names)
            if st.button("تأكيد الحذف"):
                if to_del != "-- اختر --":
                    st.session_state.names.remove(to_del)
                    save_names(st.session_state.names)
                    st.rerun()
        with tab3:
            if st.button("تصفير القائمة"):
                if os.path.exists(CSV_RESULTS): os.remove(CSV_RESULTS)
                st.rerun()

st.markdown("<p style='text-align:center; color:#888; font-size:0.8em; margin-top:30px;'>تصميم وبرمجة: أبو فيصل للعقارات 2026</p>", unsafe_allow_html=True)