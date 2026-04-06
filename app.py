import streamlit as st
import pandas as pd
from datetime import datetime
import os
import base64

# --- 1. إعدادات الصفحة ---
st.set_page_config(page_title="مناسبات آل علي", layout="centered", page_icon="logo.png")

# --- 2. بيانات المناسبة (عدلها من هنا مباشرة) ---
EVENT_INFO = {
    "title": "مناسبات جماعة آل علي بالرياض",
    "date": "يوم الجمعة: 2026/05/15م",
    "time": "الساعة 8:00 مساءً",
    "location_name": "استراحة الفخامة - الرياض",
    "map_url": "https://maps.google.com" # ضع رابط قوقل ماب هنا
}

# --- 3. وظائف النظام ---
def get_image_base64(path):
    if os.path.exists(path):
        with open(path, "rb") as img_file:
            return base64.b64encode(img_file.read()).decode()
    return None

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

# --- 4. التنسيق الملكي (CSS) ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Amiri&family=Tajawal:wght@400;700&display=swap');
    #MainMenu, footer, header {visibility: hidden;}
    .stApp { background-color: #F5F5DC; }
    
    /* برواز الصفحة الرئيسي */
    .main .block-container {
        border: 2px solid #D4AF37;
        padding: 5px 15px !important; 
        border-radius: 15px;
        background-color: #ffffff;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
        margin: 5px auto;
    }

    .bismillah { font-family: 'Amiri', serif; font-size: 2.2em; color: #1a1a1a; text-align: center; margin-bottom: 0px; }
    
    .logo-frame { display: flex; justify-content: center; align-items: center; margin: -10px 0 5px 0; }
    .circular-logo { width: 250px !important; height: 250px !important; border-radius: 50%; object-fit: cover; }

    .main-title { color: #D4AF37; text-align: center; font-size: 1.6em !important; font-family: 'Tajawal', sans-serif; font-weight: bold; margin-top: -10px; }

    /* بطاقة تفاصيل المناسبة */
    .event-card {
        background-color: #FFFDF5;
        border: 1px double #D4AF37;
        border-radius: 15px;
        padding: 15px;
        margin: 10px 0;
        text-align: center;
    }
    .event-info { font-family: 'Tajawal', sans-serif; color: #1a1a1a; font-size: 1.1em; margin: 5px 0; }
    .map-btn {
        background-color: #D4AF37; color: white !important; padding: 5px 15px; 
        border-radius: 20px; text-decoration: none; display: inline-block; 
        margin-top: 10px; font-weight: bold;
    }

    [data-testid="stMetric"] { background-color: #FFFDF5; border: 1px solid #D4AF37; border-radius: 10px; text-align: center; }
    .stButton>button { border-radius: 12px; border: 2px solid #D4AF37; background-color: #1a1a1a; color: #D4AF37; font-weight: bold; width: 100%; }
    </style>
    """, unsafe_allow_html=True)

# --- 5. واجهة العرض العلوية (الهوية والدعوة) ---
st.markdown("<div class='bismillah'>بِسْمِ اللهِ الرَّحْمٰنِ الرَّحِيْمِ</div>", unsafe_allow_html=True)

img_b64 = get_image_base64("logo.png")
if img_b64:
    st.markdown(f'<div class="logo-frame"><img src="data:image/png;base64,{img_b64}" class="circular-logo"></div>', unsafe_allow_html=True)

st.markdown(f"<div class='main-title'>{EVENT_INFO['title']}</div>", unsafe_allow_html=True)

# عرض تفاصيل المناسبة (التاريخ والموقع)
st.markdown(f"""
    <div class="event-card">
        <div class="event-info">📅 <b>التاريخ:</b> {EVENT_INFO['date']}</div>
        <div class="event-info">⏰ <b>الوقت:</b> {EVENT_INFO['time']}</div>
        <div class="event-info">📍 <b>الموقع:</b> {EVENT_INFO['location_name']}</div>
        <a href="{EVENT_INFO['map_url']}" target="_blank" class="map-btn">📍 موقع المناسبة (Google Maps)</a>
    </div>
""", unsafe_allow_html=True)

# --- 6. نظام تسجيل الحضور ---
if 'names' not in st.session_state:
    st.session_state.names = load_names()
    st.session_state.input_key = 0

names_list = st.session_state.names

if names_list:
    selected_name = st.selectbox("🔍 ابحث عن اسمك لتأكيد حضورك أو اعتذارك:", options=["-- اختر الاسم --"] + names_list)

    if selected_name != "-- اختر الاسم --":
        col1, col2 = st.columns(2)
        with col1:
            if st.button("✅ تأكيد الحضور"):
                res = load_results()
                new_row = pd.DataFrame({'الاسم': [selected_name], 'الحالة': ['حاضر'], 'الوقت': [datetime.now().strftime("%I:%M %p")]})
                pd.concat([res[res['الاسم'] != selected_name], new_row], ignore_index=True).to_csv(CSV_RESULTS, index=False, encoding='utf-8-sig')
                st.success(f"تم تسجيل حضورك يا {selected_name}")
                st.rerun()
        with col2:
            if st.button("❌ تقديم اعتذار"):
                res = load_results()
                new_row = pd.DataFrame({'الاسم': [selected_name], 'الحالة': ['معتذر'], 'الوقت': [datetime.now().strftime("%I:%M %p")]})
                pd.concat([res[res['الاسم'] != selected_name], new_row], ignore_index=True).to_csv(CSV_RESULTS, index=False, encoding='utf-8-sig')
                st.warning(f"تم تسجيل اعتذارك يا {selected_name}")
                st.rerun()

st.divider()

# --- 7. الإحصائيات العامة ---
df_results = load_results()
total_all = len(names_list)
total_present = len(df_results[df_results['الحالة'] == 'حاضر'])
total_absent = len(df_results[df_results['الحالة'] == 'معتذر'])

st.markdown("<h3 style='color:#D4AF37; text-align:center;'>📊 إحصائيات الحضور</h3>", unsafe_allow_html=True)
c1, c2, c3 = st.columns(3)
with c1: st.metric("إجمالي المسجلين", total_all)
with c2: st.metric("حاضر", total_present)
with c3: st.metric("معتذر", total_absent)

# --- 8. لوحة التحكم (للمشرف فقط) ---
with st.expander("⚙️ لوحة تحكم المشرف"):
    admin_pass = st.text_input("كلمة المرور:", type="password")
    if admin_pass == "1234":
        tab1, tab2, tab3 = st.tabs(["➕ إضافة اسم", "🗑️ حذف اسم", "🧹 تصفير البيانات"])
        with tab1:
            new_p = st.text_input("أدخل الاسم الكامل:", key=f"ins_{st.session_state.input_key}")
            if st.button("حفظ الآن"):
                if new_p and new_p.strip() not in st.session_state.names:
                    st.session_state.names.append(new_p.strip())
                    save_names(sorted(st.session_state.names))
                    st.session_state.input_key += 1
                    st.rerun()
        with tab2:
            to_del = st.selectbox("اختر الاسم المراد حذفه:", options=["-- اختر --"] + st.session_state.names)
            if st.button("تأكيد حذف الاسم"):
                if to_del != "-- اختر --":
                    st.session_state.names.remove(to_del)
                    save_names(st.session_state.names)
                    st.rerun()
        with tab3:
            st.warning("تحذير: هذا الخيار سيحذف جميع سجلات الحضور والاعتذار!")
            if st.button("تصفير جميع البيانات"):
                if os.path.exists(CSV_RESULTS): os.remove(CSV_RESULTS)
                st.rerun()

st.markdown("<p style='text-align:center; color:#888; font-size:0.8em; margin-top:30px;'>تصميم وبرمجة: محمد العلالي - أبو فيصل للعقارات 2026</p>", unsafe_allow_html=True)