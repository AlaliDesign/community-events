import streamlit as st
import pandas as pd
from datetime import datetime
import os
import base64
import json

# --- 1. إعدادات الصفحة ---
st.set_page_config(page_title="مناسبات آل علي", layout="centered", page_icon="logo.png")

# --- 2. ملفات النظام ---
EXCEL_FILE = 'names.xlsx'
CSV_RESULTS = 'community_events_results.csv'
SETTINGS_FILE = 'settings.json'

# --- 3. وظائف النظام ---
def load_settings():
    if os.path.exists(SETTINGS_FILE):
        with open(SETTINGS_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {
        "title": "مناسبات جماعة آل علي بالرياض",
        "date": "حدد التاريخ",
        "time": "حدد الوقت",
        "location": "حدد الموقع",
        "map_url": ""
    }

def save_settings(settings):
    with open(SETTINGS_FILE, 'w', encoding='utf-8') as f:
        json.dump(settings, f, ensure_ascii=False, indent=4)

def get_image_base64(path):
    if os.path.exists(path):
        with open(path, "rb") as img_file:
            return base64.b64encode(img_file.read()).decode()
    return None

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

# --- 4. التنسيق الملكي المحسن (لحل مشاكل الجوال) ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Amiri&family=Tajawal:wght@400;700&display=swap');
    
    /* إخفاء القوائم الافتراضية */
    #MainMenu, footer, header {visibility: hidden;}
    
    .stApp { background-color: #F5F5DC; }
    
    /* تحسين البرواز والحواف */
    .main .block-container {
        border: 2px solid #D4AF37; padding: 15px !important; 
        border-radius: 15px; background-color: #ffffff;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1); margin: 5px auto;
        max-width: 95% !important;
    }
    
    .bismillah { font-family: 'Amiri', serif; font-size: 2.2em; color: #1a1a1a; text-align: center; margin-bottom: 10px; }
    .logo-frame { display: flex; justify-content: center; margin-bottom: 10px; }
    .circular-logo { width: 200px !important; height: 200px !important; border-radius: 50%; object-fit: cover; border: 2px solid #D4AF37; }
    .main-title { color: #D4AF37; text-align: center; font-size: 1.5em !important; font-family: 'Tajawal', sans-serif; font-weight: bold; }
    
    /* بطاقة الدعوة */
    .event-card {
        background-color: #FFFDF5; border: 1px double #D4AF37;
        border-radius: 12px; padding: 12px; margin: 10px 0; text-align: center;
    }
    .event-info { font-family: 'Tajawal', sans-serif; color: #1a1a1a; font-size: 1.0em; margin: 3px 0; }
    .map-btn {
        background-color: #D4AF37; color: white !important; padding: 6px 15px; 
        border-radius: 20px; text-decoration: none; display: inline-block; 
        margin-top: 8px; font-weight: bold; font-size: 0.85em;
    }
    
    /* تحسين ظهور الحقول على الجوال */
    input, select, .stSelectbox {
        font-size: 16px !important; /* يمنع الزووم التلقائي في الآيفون */
    }
    
    .stButton>button { 
        border-radius: 10px; border: 2px solid #D4AF37; 
        background-color: #1a1a1a; color: #D4AF37; 
        font-weight: bold; width: 100%; height: 3.5em;
    }
    </style>
    """, unsafe_allow_html=True)

# تحضير البيانات
if 'names' not in st.session_state:
    st.session_state.names = load_names()
    st.session_state.input_key = 0

current_settings = load_settings()

# --- 5. واجهة العرض ---
st.markdown("<div class='bismillah'>بِسْمِ اللهِ الرَّحْمٰنِ الرَّحِيْمِ</div>", unsafe_allow_html=True)

img_b64 = get_image_base64("logo.png")
if img_b64:
    st.markdown(f'<div class="logo-frame"><img src="data:image/png;base64,{img_b64}" class="circular-logo"></div>', unsafe_allow_html=True)

st.markdown(f"<div class='main-title'>{current_settings['title']}</div>", unsafe_allow_html=True)

st.markdown(f"""
    <div class="event-card">
        <div class="event-info">📅 <b>التاريخ:</b> {current_settings['date']}</div>
        <div class="event-info">⏰ <b>الوقت:</b> {current_settings['time']}</div>
        <div class="event-info">📍 <b>الموقع:</b> {current_settings['location']}</div>
        {"<a href='"+current_settings['map_url']+"' target='_blank' class='map-btn'>📍 خرائط جوجل</a>" if current_settings['map_url'] else ""}
    </div>
""", unsafe_allow_html=True)

# --- 6. اختيار الاسم (البحث) ---
st.write("### 🔍 ابحث عن اسمك")
# استخدام selectbox مع ميزة البحث المفعلة افتراضياً
selected_name = st.selectbox(
    "اختر من القائمة (يمكنك كتابة اسمك للبحث):",
    options=["-- اختر الاسم --"] + st.session_state.names,
    index=0
)

# إذا لم يجد اسمه، نترك له خيار الإضافة اليدوية (اختياري)
if selected_name == "-- اختر الاسم --":
    st.info("💡 إذا لم تجد اسمك، يمكنك إضافته من لوحة التحكم بالأسفل أو التواصل مع المنظم.")

if selected_name != "-- اختر الاسم --":
    st.success(f"الاسم المختار: {selected_name}")
    col1, col2 = st.columns(2)
    with col1:
        if st.button("✅ تأكيد الحضور"):
            res = load_results()
            new_row = pd.DataFrame({'الاسم': [selected_name], 'الحالة': ['حاضر'], 'الوقت': [datetime.now().strftime("%I:%M %p")]})
            pd.concat([res[res['الاسم'] != selected_name], new_row], ignore_index=True).to_csv(CSV_RESULTS, index=False, encoding='utf-8-sig')
            st.balloons()
            st.success("تم الحفظ بنجاح")
            st.rerun()
    with col2:
        if st.button("❌ تقديم اعتذار"):
            res = load_results()
            new_row = pd.DataFrame({'الاسم': [selected_name], 'الحالة': ['معتذر'], 'الوقت': [datetime.now().strftime("%I:%M %p")]})
            pd.concat([res[res['الاسم'] != selected_name], new_row], ignore_index=True).to_csv(CSV_RESULTS, index=False, encoding='utf-8-sig')
            st.warning("تم تسجيل الاعتذار")
            st.rerun()

st.divider()

# --- 7. الإحصائيات ---
df_results = load_results()
total_present = len(df_results[df_results['الحالة'] == 'حاضر'])
total_absent = len(df_results[df_results['الحالة'] == 'معتذر'])

c1, c2, c3 = st.columns(3)
with c1: st.metric("المسجلين", len(st.session_state.names))
with c2: st.metric("حاضر", total_present)
with c3: st.metric("معتذر", total_absent)

# --- 8. لوحة التحكم ---
with st.expander("⚙️ الإدارة"):
    pw = st.text_input("كلمة المرور:", type="password")
    if pw == "1234":
        t1, t2, t3 = st.tabs(["📅 الإعدادات", "👥 الأسماء", "📊 السجل"])
        with t1:
            new_title = st.text_input("العنوان:", value=current_settings['title'])
            new_date = st.text_input("التاريخ:", value=current_settings['date'])
            new_time = st.text_input("الوقت:", value=current_settings['time'])
            new_loc = st.text_input("الموقع:", value=current_settings['location'])
            new_map = st.text_input("رابط الخريطة:", value=current_settings['map_url'])
            if st.button("حفظ التغييرات"):
                save_settings({"title": new_title, "date": new_date, "time": new_time, "location": new_loc, "map_url": new_map})
                st.rerun()
        with t2:
            n_name = st.text_input("إضافة اسم جديد:")
            if st.button("إضافة"):
                if n_name and n_name not in st.session_state.names:
                    st.session_state.names.append(n_name.strip())
                    save_names(sorted(st.session_state.names))
                    st.rerun()
            del_n = st.selectbox("حذف اسم:", options=["-- اختر --"] + st.session_state.names)
            if st.button("حذف"):
                if del_n != "-- اختر --":
                    st.session_state.names.remove(del_n)
                    save_names(st.session_state.names)
                    st.rerun()
        with t3:
            if st.button("تصفير سجل الحضور"):
                if os.path.exists(CSV_RESULTS): os.remove(CSV_RESULTS)
                st.rerun()
            st.dataframe(df_results)

st.markdown("<p style='text-align:center; color:#888; font-size:0.8em; margin-top:20px;'>محمد العلالي - صقر العقارات 2026</p>", unsafe_allow_html=True)