import streamlit as st
import pandas as pd
from datetime import datetime
import os
import base64
import json

# --- 1. إعدادات الصفحة ---
st.set_page_config(page_title="مناسبات آل علي", layout="centered")

# --- 2. وظائف الملفات (تأكد من وجودها) ---
SETTINGS_FILE = 'settings.json'
NAMES_FILE = 'names.xlsx'
RESULTS_FILE = 'results.csv'

def load_settings():
    if os.path.exists(SETTINGS_FILE):
        with open(SETTINGS_FILE, 'r', encoding='utf-8') as f: return json.load(f)
    return {"title": "مناسبات آل علي", "date": "لم يحدد", "time": "لم يحدد", "location": "لم يحدد", "map_url": ""}

def load_names():
    if os.path.exists(NAMES_FILE):
        try: return sorted(pd.read_excel(NAMES_FILE).iloc[:, 0].dropna().astype(str).unique().tolist())
        except: return []
    return []

def load_results():
    if os.path.exists(RESULTS_FILE):
        try: return pd.read_csv(RESULTS_FILE, encoding='utf-8-sig')
        except: return pd.DataFrame(columns=['الاسم', 'الحالة', 'الوقت'])
    return pd.DataFrame(columns=['الاسم', 'الحالة', 'الوقت'])

# --- 3. التنسيق الملكي المحسن (وضوح المربعات) ---
st.markdown("""
    <style>
    #MainMenu, footer, header {visibility: hidden;}
    .stApp { background-color: #FDFCF0; }
    
    .main .block-container {
        border: 2px solid #D4AF37; padding: 20px !important; 
        border-radius: 15px; background-color: #ffffff;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1); margin: auto;
    }
    
    /* تنسيق مربعات الإحصائيات (العداد الكلي) */
    [data-testid="stMetric"] {
        background-color: #FFFDF5 !important;
        border: 1px solid #D4AF37 !important;
        border-radius: 10px !important;
        padding: 10px !important;
        text-align: center !important;
    }
    [data-testid="stMetricLabel"] { color: #1a1a1a !important; font-size: 1.1em !important; font-weight: bold !important; }
    [data-testid="stMetricValue"] { color: #D4AF37 !important; }

    .event-card {
        background-color: #FFFDF5; border: 1px double #D4AF37;
        border-radius: 12px; padding: 15px; margin: 10px 0; text-align: center;
    }
    
    .stButton>button { 
        border-radius: 10px; border: 2px solid #D4AF37; 
        background-color: #1a1a1a; color: #D4AF37; 
        font-weight: bold; width: 100%; height: 3.5em;
    }
    </style>
    """, unsafe_allow_html=True)

# استدعاء البيانات الحالية
current_settings = load_settings()
all_names = load_names()
df_results = load_results()

# --- 4. واجهة العرض ---
st.markdown("<h2 style='text-align:center;'>بِسْمِ اللهِ الرَّحْمٰنِ الرَّحِيْمِ</h2>", unsafe_allow_html=True)
st.markdown(f"<h3 style='text-align:center; color:#D4AF37;'>{current_settings['title']}</h3>", unsafe_allow_html=True)

st.markdown(f"""
    <div class="event-card">
        <p>📅 <b>التاريخ:</b> {current_settings['date']} | ⏰ <b>الوقت:</b> {current_settings['time']}</p>
        <p>📍 <b>الموقع:</b> {current_settings['location']}</p>
        <a href="{current_settings['map_url']}" target="_blank" style="color:#D4AF37; font-weight:bold;">📍 فتح الموقع في الخرائط</a>
    </div>
""", unsafe_allow_html=True)

st.divider()

# --- 5. نظام البحث والتسجيل ---
st.markdown("### 📝 سجل حضورك")

# حقل البحث
search_query = st.text_input("🔍 ابحث عن اسمك هنا أولاً:", placeholder="اكتب اسمك...")

# فلترة الأسماء
if search_query:
    filtered_names = [n for n in all_names if search_query in n]
else:
    filtered_names = all_names

# اختيار الاسم من القائمة المفلترة
selected_user = st.selectbox("👇 ثم اختر اسمك من القائمة أدناه:", options=["-- اختر --"] + filtered_names)

if selected_user != "-- اختر --":
    col1, col2 = st.columns(2)
    with col1:
        if st.button("✅ تأكيد الحضور"):
            new_row = pd.DataFrame({'الاسم': [selected_user], 'الحالة': ['حاضر'], 'الوقت': [datetime.now().strftime("%I:%M %p")]})
            # دمج البيانات مع حذف القديم لنفس الاسم لمنع التكرار
            updated_df = pd.concat([df_results[df_results['الاسم'] != selected_user], new_row], ignore_index=True)
            updated_df.to_csv(RESULTS_FILE, index=False, encoding='utf-8-sig')
            st.success(f"تم تسجيل حضورك يا {selected_user}")
            st.rerun()
    with col2:
        if st.button("❌ تقديم اعتذار"):
            new_row = pd.DataFrame({'الاسم': [selected_user], 'الحالة': ['معتذر'], 'الوقت': [datetime.now().strftime("%I:%M %p")]})
            updated_df = pd.concat([df_results[df_results['الاسم'] != selected_user], new_row], ignore_index=True)
            updated_df.to_csv(RESULTS_FILE, index=False, encoding='utf-8-sig')
            st.warning("تم تسجيل اعتذارك")
            st.rerun()

st.divider()

# --- 6. الإحصائيات (التي كانت لا تظهر) ---
st.markdown("<h3 style='text-align:center; color:#1a1a1a;'>📊 الإحصائيات الحالية</h3>", unsafe_allow_html=True)
c1, c2, c3 = st.columns(3)
with c1: st.metric("إجمالي الأسماء", len(all_names))
with c2: st.metric("حاضر ✅", len(df_results[df_results['الحالة'] == 'حاضر']))
with c3: st.metric("معتذر ❌", len(df_results[df_results['الحالة'] == 'معتذر']))

# --- 7. لوحة التحكم ---
with st.expander("⚙️ لوحة تحكم المشرف"):
    pw = st.text_input("كلمة المرور:", type="password")
    if pw == "1234":
        t1, t2 = st.tabs(["إدارة المناسبة", "تصفير السجل"])
        with t1:
            # نموذج لتغيير البيانات
            new_t = st.text_input("العنوان:", value=current_settings['title'])
            new_d = st.text_input("التاريخ:", value=current_settings['date'])
            new_time = st.text_input("الوقت:", value=current_settings['time'])
            new_l = st.text_input("الموقع:", value=current_settings['location'])
            new_m = st.text_input("رابط الخريطة:", value=current_settings['map_url'])
            if st.button("حفظ الإعدادات"):
                with open(SETTINGS_FILE, 'w', encoding='utf-8') as f:
                    json.dump({"title":new_t, "date":new_d, "time":new_time, "location":new_l, "map_url":new_m}, f, ensure_ascii=False)
                st.rerun()
        with t2:
            if st.button("مسح جميع تسجيلات الحضور"):
                if os.path.exists(RESULTS_FILE): os.remove(RESULTS_FILE)
                st.rerun()

st.markdown("<p style='text-align:center; color:#888; font-size:0.7em;'>صقر العقارات 2026</p>", unsafe_allow_html=True)