import streamlit as st
import pandas as pd
from datetime import datetime
import os
import json

# --- 1. تحميل ومعالجة البيانات ---
def load_data():
    names = []
    if os.path.exists('names.xlsx'):
        try:
            df = pd.read_excel('names.xlsx')
            names = sorted(df.iloc[:, 0].dropna().astype(str).unique().tolist())
        except: pass
    
    results = pd.DataFrame(columns=['الاسم', 'الحالة', 'الوقت'])
    if os.path.exists('results.csv'):
        try: 
            results = pd.read_csv('results.csv', encoding='utf-8-sig')
        except: pass
        
    settings = {"title": "مناسبات آل علي", "date": "-", "time": "-", "location": "-", "map_url": ""}
    if os.path.exists('settings.json'):
        try:
            with open('settings.json', 'r', encoding='utf-8') as f: settings = json.load(f)
        except: pass
            
    return names, results, settings

# --- 2. التنسيق المرئي ---
st.markdown("""
    <style>
    #MainMenu, footer, header {visibility: hidden;}
    .stApp { background-color: #FDFCF0; }
    .main .block-container {
        border: 2px solid #D4AF37; padding: 15px !important; 
        border-radius: 15px; background-color: #ffffff;
        max-width: 95% !important; margin: auto;
    }
    div[data-testid="stMetric"] {
        background-color: #FFFDF5 !important;
        border: 1px solid #D4AF37 !important;
        border-radius: 10px !important;
        padding: 10px !important;
        text-align: center !important;
    }
    .stButton>button { 
        border-radius: 10px; border: 2px solid #D4AF37; 
        background-color: #1a1a1a; color: #D4AF37; 
        font-weight: bold; width: 100%; height: 3.5em;
    }
    /* تنسيق الجدول */
    .styled-table { margin: 10px 0; font-size: 0.9em; font-family: sans-serif; min-width: 100%; }
    </style>
    """, unsafe_allow_html=True)

all_names, df_results, settings = load_data()

# --- 3. عرض تفاصيل المناسبة ---
st.markdown(f"<h3 style='text-align:center; color:#D4AF37;'>{settings['title']}</h3>", unsafe_allow_html=True)
st.markdown(f"""
    <div style="background-color: #FFFDF5; border: 1px double #D4AF37; border-radius: 10px; padding: 10px; text-align: center; margin-bottom: 15px;">
        <p style="margin:2px;">📅 <b>التاريخ:</b> {settings['date']} | ⏰ <b>الوقت:</b> {settings['time']}</p>
        <p style="margin:2px;">📍 <b>الموقع:</b> {settings['location']}</p>
        <a href="{settings['map_url']}" target="_blank" style="color:#D4AF37; font-weight:bold; text-decoration:none;">📍 فتح الموقع في الخرائط</a>
    </div>
""", unsafe_allow_html=True)

# --- 4. تسجيل الحضور (متوافق مع الجوال) ---
st.markdown("### 📝 سجل حضورك")
search_term = st.text_input("🔍 ابحث عن اسمك هنا:", placeholder="اكتب اسمك...")
filtered_options = [n for n in all_names if search_term in n] if search_term else all_names
selected_name = st.selectbox("اختر اسمك من القائمة:", options=["-- اختر --"] + filtered_options)

if selected_name != "-- اختر --":
    c1, c2 = st.columns(2)
    with c1:
        if st.button("✅ تأكيد الحضور"):
            new_data = pd.DataFrame({'الاسم': [selected_name], 'الحالة': ['حاضر'], 'الوقت': [datetime.now().strftime("%I:%M %p")]})
            updated_df = pd.concat([df_results[df_results['الاسم'] != selected_name], new_data], ignore_index=True)
            updated_df.to_csv('results.csv', index=False, encoding='utf-8-sig')
            st.success("تم تسجيل حضورك")
            st.rerun()
    with c2:
        if st.button("❌ اعتذار"):
            new_data = pd.DataFrame({'الاسم': [selected_name], 'الحالة': ['معتذر'], 'الوقت': [datetime.now().strftime("%I:%M %p")]})
            updated_df = pd.concat([df_results[df_results['الاسم'] != selected_name], new_data], ignore_index=True)
            updated_df.to_csv('results.csv', index=False, encoding='utf-8-sig')
            st.warning("تم تسجيل الاعتذار")
            st.rerun()

st.divider()

# --- 5. الإحصائيات ---
st.markdown("<h4 style='text-align:center;'>📊 إحصائيات سريعة</h4>", unsafe_allow_html=True)
c1, c2, c3 = st.columns(3)
with c1: st.metric("المسجلين", len(all_names))
with c2: st.metric("حاضر ✅", len(df_results[df_results['الحالة'] == 'حاضر']))
with c3: st.metric("معتذر ❌", len(df_results[df_results['الحالة'] == 'معتذر']))

# --- 6. عرض كشف الأسماء (هذا الجزء الذي طلبته) ---
st.divider()
st.markdown("<h4 style='text-align:center; color:#1a1a1a;'>📋 كشف الحضور والاعتذار</h4>", unsafe_allow_html=True)

if not df_results.empty:
    # ترتيب الجدول ليظهر الأحدث أولاً
    display_df = df_results.copy()
    display_df = display_df.sort_values(by='الوقت', ascending=False)
    
    # تحسين عرض الجدول
    st.dataframe(display_df, use_container_width=True, hide_index=True)
else:
    st.info("لا يوجد تسجيلات حتى الآن.")

# --- 7. لوحة التحكم ---
with st.expander("⚙️ الإدارة"):
    if st.text_input("كلمة المرور", type="password") == "1234":
        if st.button("تصفير السجل بالكامل"):
            if os.path.exists('results.csv'): os.remove('results.csv')
            st.rerun()
        
        st.write("--- تعديل بيانات المناسبة ---")
        new_title = st.text_input("العنوان", value=settings['title'])
        new_date = st.text_input("التاريخ", value=settings['date'])
        new_time = st.text_input("الوقت", value=settings['time'])
        new_loc = st.text_input("الموقع", value=settings['location'])
        new_map = st.text_input("الرابط", value=settings['map_url'])
        if st.button("حفظ التعديلات"):
            with open('settings.json', 'w', encoding='utf-8') as f:
                json.dump({"title":new_title, "date":new_date, "time":new_time, "location":new_loc, "map_url":new_map}, f, ensure_ascii=False)
            st.rerun()

st.markdown("<p style='text-align:center; color:#888; font-size:0.7em; margin-top:20px;'>محمد العلالي - صقر العقارات 2026</p>", unsafe_allow_html=True)