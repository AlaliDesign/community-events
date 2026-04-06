import streamlit as st
import pandas as pd
from datetime import datetime
import os
import json
import urllib.parse

# --- 1. وظائف البيانات ---
def load_data():
    names = []
    if os.path.exists('names.xlsx'):
        try:
            df = pd.read_excel('names.xlsx')
            names = sorted(df.iloc[:, 0].dropna().astype(str).unique().tolist())
        except: pass
    
    results = pd.DataFrame(columns=['الاسم', 'الحالة', 'الوقت'])
    if os.path.exists('results.csv'):
        try: results = pd.read_csv('results.csv', encoding='utf-8-sig')
        except: pass
        
    settings = {"title": "مناسبات آل علي", "date": "2026-05-15", "time": "08:00 PM", "location": "الرياض", "map_url": ""}
    if os.path.exists('settings.json'):
        try:
            with open('settings.json', 'r', encoding='utf-8') as f: settings = json.load(f)
        except: pass
    return names, results, settings

# --- 2. التنسيق الملكي المحسن ---
st.markdown("""
    <style>
    #MainMenu, footer, header {visibility: hidden;}
    .stApp { background-color: #FDFCF0; }
    .main .block-container {
        border: 2px solid #D4AF37; padding: 15px !important; 
        border-radius: 15px; background-color: #ffffff;
        max-width: 95% !important; margin: auto;
    }
    /* تنسيق زر التذكير الجديد */
    .reminder-link {
        display: block;
        background-color: #D4AF37;
        color: white !important;
        text-align: center;
        padding: 15px;
        text-decoration: none;
        border-radius: 10px;
        font-weight: bold;
        font-size: 1.1em;
        margin: 15px 0;
        box-shadow: 0 4px 8px rgba(0,0,0,0.1);
    }
    .reminder-link:hover { background-color: #B8860B; }
    
    .event-card {
        background-color: #FFFDF5; border: 1px double #D4AF37;
        border-radius: 12px; padding: 15px; margin: 10px 0; text-align: center;
    }
    div[data-testid="stMetric"] {
        background-color: #FFFDF5 !important; border: 1px solid #D4AF37 !important;
        border-radius: 10px !important; padding: 10px !important;
    }
    .stButton>button { 
        border-radius: 10px; border: 2px solid #D4AF37; 
        background-color: #1a1a1a; color: #D4AF37; 
        font-weight: bold; width: 100%; height: 3.5em;
    }
    </style>
    """, unsafe_allow_html=True)

all_names, df_results, settings = load_data()

# --- 3. واجهة العرض ---
st.markdown(f"<h3 style='text-align:center; color:#D4AF37;'>{settings['title']}</h3>", unsafe_allow_html=True)

# تحضير رابط التقويم
title_q = urllib.parse.quote(settings['title'])
date_q = settings['date'].replace("-", "")
loc_q = urllib.parse.quote(settings['location'])
cal_url = f"https://www.google.com/calendar/render?action=TEMPLATE&text={title_q}&dates={date_q}T170000Z/{date_q}T210000Z&details=ننتظركم+بكل+حب&location={loc_q}"

st.markdown(f"""
    <div class="event-card">
        <p style="font-size:1.1em;">📅 <b>التاريخ:</b> {settings['date']} | ⏰ <b>الوقت:</b> {settings['time']}</p>
        <p>📍 <b>الموقع:</b> {settings['location']}</p>
        
        <a href="{cal_url}" target="_blank" class="reminder-link">🔔 أضف تذكير (تنبيه صوتي بجوالك)</a>
        
        <a href="{settings['map_url']}" target="_blank" style="color:#D4AF37; font-weight:bold; text-decoration:none;">📍 فتح الخريطة</a>
    </div>
""", unsafe_allow_html=True)

# --- 4. تسجيل الحضور ---
st.markdown("### 📝 سجل حضورك")
search_term = st.text_input("🔍 ابحث عن اسمك هنا:", placeholder="اكتب اسمك...")
filtered = [n for n in all_names if search_term in n] if search_term else all_names
selected = st.selectbox("اختر اسمك من القائمة:", options=["-- اختر --"] + filtered)

if selected != "-- اختر --":
    c1, c2 = st.columns(2)
    with c1:
        if st.button("✅ تأكيد الحضور"):
            new_row = pd.DataFrame({'الاسم': [selected], 'الحالة': ['حاضر'], 'الوقت': [datetime.now().strftime("%I:%M %p")]})
            pd.concat([df_results[df_results['الاسم'] != selected], new_row], ignore_index=True).to_csv('results.csv', index=False, encoding='utf-8-sig')
            st.success("تم تسجيل حضورك")
            st.rerun()
    with c2:
        if st.button("❌ اعتذار"):
            new_row = pd.DataFrame({'الاسم': [selected], 'الحالة': ['معتذر'], 'الوقت': [datetime.now().strftime("%I:%M %p")]})
            pd.concat([df_results[df_results['الاسم'] != selected], new_row], ignore_index=True).to_csv('results.csv', index=False, encoding='utf-8-sig')
            st.warning("تم تسجيل اعتذارك")
            st.rerun()

st.divider()

# --- 5. الإحصائيات والكشف ---
c1, c2, c3 = st.columns(3)
with c1: st.metric("المسجلين", len(all_names))
with c2: st.metric("حاضر ✅", len(df_results[df_results['الحالة'] == 'حاضر']))
with c3: st.metric("معتذر ❌", len(df_results[df_results['الحالة'] == 'معتذر']))

st.markdown("<h4 style='text-align:center;'>📋 كشف الأسماء</h4>", unsafe_allow_html=True)
if not df_results.empty:
    st.dataframe(df_results.sort_values(by='الوقت', ascending=False), use_container_width=True, hide_index=True)

# --- 6. لوحة التحكم ---
with st.expander("⚙️ الإدارة"):
    if st.text_input("كلمة المرور", type="password") == "1234":
        if st.button("مسح السجل"):
            if os.path.exists('results.csv'): os.remove('results.csv')
            st.rerun()
        st.write("--- تعديل المناسبة ---")
        nt = st.text_input("العنوان", value=settings['title'])
        nd = st.text_input("التاريخ (مثال: 2026-05-20)", value=settings['date'])
        nw = st.text_input("الوقت", value=settings['time'])
        nl = st.text_input("الموقع", value=settings['location'])
        nm = st.text_input("رابط الخريطة", value=settings['map_url'])
        if st.button("حفظ التعديلات"):
            with open('settings.json', 'w', encoding='utf-8') as f:
                json.dump({"title":nt, "date":nd, "time":nw, "location":nl, "map_url":nm}, f, ensure_ascii=False)
            st.rerun()

st.markdown("<p style='text-align:center; color:#888; font-size:0.7em;'>محمد العلالي - صقر العقارات 2026</p>", unsafe_allow_html=True)