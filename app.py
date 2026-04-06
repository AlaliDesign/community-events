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

# --- 3. وظائف إدارة البيانات ---
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

# --- 4. التنسيق الملكي (CSS) ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Amiri&family=Tajawal:wght@400;700&display=swap');
    #MainMenu, footer, header {visibility: hidden;}
    .stApp { background-color: #F5F5DC; }
    .main .block-container {
        border: 2px solid #D4AF37; padding: 10px 20px !important; 
        border-radius: 15px; background-color: #ffffff;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1); margin: 10px auto;
    }
    .bismillah { font-family: 'Amiri', serif; font-size: 2.2em; color: #1a1a1a; text-align: center; }
    .logo-frame { display: flex; justify-content: center; margin: -10px 0 10px 0; }
    .circular-logo { width: 220px !important; height: 220px !important; border-radius: 50%; object-fit: cover; border: 2px solid #D4AF37; }
    .main-title { color: #D4AF37; text-align: center; font-size: 1.7em !important; font-family: 'Tajawal', sans-serif; font-weight: bold; }
    .event-card {
        background-color: #FFFDF5; border: 1px double #D4AF37;
        border-radius: 15px; padding: 15px; margin: 15px 0; text-align: center;
    }
    .event-info { font-family: 'Tajawal', sans-serif; color: #1a1a1a; font-size: 1.1em; margin: 5px 0; }
    .map-btn {
        background-color: #D4AF37; color: white !important; padding: 8px 20px; 
        border-radius: 20px; text-decoration: none; display: inline-block; 
        margin-top: 10px; font-weight: bold; font-size: 0.9em;
    }
    [data-testid="stMetric"] { background-color: #FFFDF5; border: 1px solid #D4AF37; border-radius: 10px; }
    .stButton>button { border-radius: 10px; border: 2px solid #D4AF37; background-color: #1a1a1a; color: #D4AF37; font-weight: bold; width: 100%; }
    </style>
    """, unsafe_allow_html=True)

# تحضير البيانات
if 'names' not in st.session_state:
    st.session_state.names = load_names()
    st.session_state.input_key = 0

current_settings = load_settings()

# --- 5. واجهة العرض الرئيسية ---
st.markdown("<div class='bismillah'>بِسْمِ اللهِ الرَّحْمٰنِ الرَّحِيْمِ</div>", unsafe_allow_html=True)

img_b64 = get_image_base64("logo.png")
if img_b64:
    st.markdown(f'<div class="logo-frame"><img src="data:image/png;base64,{img_b64}" class="circular-logo"></div>', unsafe_allow_html=True)

st.markdown(f"<div class='main-title'>{current_settings['title']}</div>", unsafe_allow_html=True)

# عرض بطاقة المناسبة
st.markdown(f"""
    <div class="event-card">
        <div class="event-info">📅 <b>التاريخ:</b> {current_settings['date']}</div>
        <div class="event-info">⏰ <b>الوقت:</b> {current_settings['time']}</div>
        <div class="event-info">📍 <b>الموقع:</b> {current_settings['location']}</div>
        {"<a href='"+current_settings['map_url']+"' target='_blank' class='map-btn'>📍 موقع المناسبة (خرائط جوجل)</a>" if current_settings['map_url'] else ""}
    </div>
""", unsafe_allow_html=True)

# --- 6. حقل البحث وتسجيل الحضور ---
st.subheader("📝 تسجيل الحضور والاعتذار")
selected_name = st.selectbox(
    "ابحث عن اسمك في القائمة:",
    options=["-- ابدأ بكتابة اسمك هنا --"] + st.session_state.names,
    index=0,
    help="اكتب اسمك للبحث بسرعة"
)

if selected_name != "-- ابدأ بكتابة اسمك هنا --":
    col1, col2 = st.columns(2)
    with col1:
        if st.button("✅ تأكيد الحضور"):
            res = load_results()
            new_row = pd.DataFrame({'الاسم': [selected_name], 'الحالة': ['حاضر'], 'الوقت': [datetime.now().strftime("%I:%M %p")]})
            pd.concat([res[res['الاسم'] != selected_name], new_row], ignore_index=True).to_csv(CSV_RESULTS, index=False, encoding='utf-8-sig')
            st.success(f"حياك الله يا {selected_name}، تم تسجيل حضورك")
            st.rerun()
    with col2:
        if st.button("❌ تقديم اعتذار"):
            res = load_results()
            new_row = pd.DataFrame({'الاسم': [selected_name], 'الحالة': ['معتذر'], 'الوقت': [datetime.now().strftime("%I:%M %p")]})
            pd.concat([res[res['الاسم'] != selected_name], new_row], ignore_index=True).to_csv(CSV_RESULTS, index=False, encoding='utf-8-sig')
            st.warning(f"تم قبول اعتذارك يا {selected_name}، نراك في مناسبات قادمة")
            st.rerun()

st.divider()

# --- 7. الإحصائيات ---
df_results = load_results()
total_all = len(st.session_state.names)
total_present = len(df_results[df_results['الحالة'] == 'حاضر'])
total_absent = len(df_results[df_results['الحالة'] == 'معتذر'])

c1, c2, c3 = st.columns(3)
with c1: st.metric("المسجلين", total_all)
with c2: st.metric("حاضر", total_present)
with c3: st.metric("معتذر", total_absent)

# --- 8. لوحة التحكم المتقدمة ---
with st.expander("⚙️ لوحة تحكم المشرف"):
    password = st.text_input("كلمة المرور:", type="password")
    if password == "1234":
        t1, t2, t3, t4 = st.tabs(["📅 إعدادات المناسبة", "➕ إضافة أسماء", "🗑️ إدارة الأسماء", "🧹 تصفير"])
        
        with t1:
            st.write("تعديل بيانات الدعوة")
            new_title = st.text_input("عنوان المناسبة:", value=current_settings['title'])
            new_date = st.text_input("التاريخ (مثلاً: الجمعة 20 مايو):", value=current_settings['date'])
            new_time = st.text_input("الوقت (مثلاً: 8:00 مساءً):", value=current_settings['time'])
            new_loc = st.text_input("اسم الموقع:", value=current_settings['location'])
            new_map = st.text_input("رابط جوجل ماب:", value=current_settings['map_url'])
            if st.button("حفظ إعدادات المناسبة"):
                save_settings({"title": new_title, "date": new_date, "time": new_time, "location": new_loc, "map_url": new_map})
                st.success("تم تحديث بيانات المناسبة بنجاح!")
                st.rerun()

        with t2:
            new_name = st.text_input("أضف اسماً جديداً للقائمة:", key=f"add_{st.session_state.input_key}")
            if st.button("إضافة الآن"):
                if new_name and new_name.strip() not in st.session_state.names:
                    st.session_state.names.append(new_name.strip())
                    save_names(sorted(st.session_state.names))
                    st.session_state.input_key += 1
                    st.rerun()
        
        with t3:
            del_name = st.selectbox("اختر اسماً لحذفه:", options=["-- اختر --"] + st.session_state.names)
            if st.button("حذف الاسم"):
                if del_name != "-- اختر --":
                    st.session_state.names.remove(del_name)
                    save_names(st.session_state.names)
                    st.rerun()

        with t4:
            if st.button("مسح سجل الحضور والاعتذار"):
                if os.path.exists(CSV_RESULTS): os.remove(CSV_RESULTS)
                st.success("تم تصفير السجل بنجاح")
                st.rerun()

st.markdown("<p style='text-align:center; color:#888; font-size:0.8em; margin-top:30px;'>تصميم: محمد العلالي - صقر العقارات 2026</p>", unsafe_allow_html=True)