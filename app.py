import streamlit as st
import pandas as pd
from datetime import datetime
import os
import json

# --- 1. تحميل البيانات ---
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
        
    if os.path.exists('settings.json'):
        try:
            with open('settings.json', 'r', encoding='utf-8') as f: settings = json.load(f)
        except: settings = {"title": "مناسبات آل علي", "date": "-", "time": "-", "location": "-", "map_url": ""}
    else:
        settings = {"title": "مناسبات آل علي", "date": "-", "time": "-", "location": "-", "map_url": ""}
            
    return names, results, settings

# --- 2. التنسيق البرمجي (تحسين رؤية العناصر) ---
st.markdown("""
    <style>
    #MainMenu, footer, header {visibility: hidden;}
    .stApp { background-color: #FDFCF0; }
    .main .block-container {
        border: 2px solid #D4AF37; padding: 15px !important; 
        border-radius: 15px; background-color: #ffffff;
        max-width: 95% !important; margin: auto;
    }
    /* تكبير الخط للحقول لضمان فتح كيبورد الجوال */
    input { font-size: 16px !important; }
    
    /* تنسيق مربعات الإحصائيات */
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
    </style>
    """, unsafe_allow_html=True)

all_names, df_results, settings = load_data()

# --- 3. الواجهة العلوية ---
st.markdown(f"<h3 style='text-align:center; color:#D4AF37;'>{settings['title']}</h3>", unsafe_allow_html=True)

st.markdown(f"""
    <div style="background-color: #FFFDF5; border: 1px double #D4AF37; border-radius: 10px; padding: 10px; text-align: center; margin-bottom: 15px;">
        <p style="margin:2px;">📅 <b>التاريخ:</b> {settings['date']} | ⏰ <b>الوقت:</b> {settings['time']}</p>
        <a href="{settings['map_url']}" target="_blank" style="color:#D4AF37; font-weight:bold; text-decoration:none;">📍 فتح الموقع في الخرائط</a>
    </div>
""", unsafe_allow_html=True)

# --- 4. محرك البحث (الحل الجذري للجوال) ---
st.markdown("### 📝 سجل حضورك")

# حقل نصي عادي (يجبر الجوال على فتح الكيبورد)
search_term = st.text_input("🔍 ابحث عن اسمك هنا (اكتب أول حروف):", placeholder="اكتب اسمك...")

# فلترة القائمة بناءً على ما يكتبه المستخدم
filtered_options = [n for n in all_names if search_term in n] if search_term else all_names

# القائمة المنسدلة تظهر النتائج المفلترة فقط
selected_name = st.selectbox(
    "اختر اسمك الصحيح من القائمة أدناه:",
    options=["-- اختر --"] + filtered_options,
    index=0
)

if selected_name != "-- اختر --":
    st.info(f"الاسم المختار: {selected_name}")
    col1, col2 = st.columns(2)
    with col1:
        if st.button("✅ تأكيد الحضور"):
            new_data = pd.DataFrame({'الاسم': [selected_name], 'الحالة': ['حاضر'], 'الوقت': [datetime.now().strftime("%I:%M %p")]})
            updated_df = pd.concat([df_results[df_results['الاسم'] != selected_name], new_data], ignore_index=True)
            updated_df.to_csv('results.csv', index=False, encoding='utf-8-sig')
            st.success("تم تسجيل حضورك")
            st.rerun()
    with col2:
        if st.button("❌ اعتذار"):
            new_data = pd.DataFrame({'الاسم': [selected_name], 'الحالة': ['معتذر'], 'الوقت': [datetime.now().strftime("%I:%M %p")]})
            updated_df = pd.concat([df_results[df_results['الاسم'] != selected_name], new_data], ignore_index=True)
            updated_df.to_csv('results.csv', index=False, encoding='utf-8-sig')
            st.warning("تم تسجيل الاعتذار")
            st.rerun()

st.divider()

# --- 5. الإحصائيات (تظهر دائماً بوضوح) ---
st.markdown("<h4 style='text-align:center;'>📊 الإحصائيات</h4>", unsafe_allow_html=True)
c1, c2, c3 = st.columns(3)
with c1: st.metric("المسجلين", len(all_names))
with c2: st.metric("حاضر ✅", len(df_results[df_results['الحالة'] == 'حاضر']))
with c3: st.metric("معتذر ❌", len(df_results[df_results['الحالة'] == 'معتذر']))

# --- 6. لوحة التحكم ---
with st.expander("⚙️ الإدارة"):
    if st.text_input("كلمة المرور", type="password") == "1234":
        if st.button("تصفير السجل"):
            if os.path.exists('results.csv'): os.remove('results.csv')
            st.rerun()
        
        # تعديل البيانات
        st.write("تعديل تفاصيل المناسبة:")
        new_title = st.text_input("العنوان", value=settings['title'])
        new_date = st.text_input("التاريخ", value=settings['date'])
        new_time = st.text_input("الوقت", value=settings['time'])
        new_loc = st.text_input("الموقع", value=settings['location'])
        new_map = st.text_input("الرابط", value=settings['map_url'])
        if st.button("حفظ"):
            with open('settings.json', 'w', encoding='utf-8') as f:
                json.dump({"title":new_title, "date":new_date, "time":new_time, "location":new_loc, "map_url":new_map}, f, ensure_ascii=False)
            st.rerun()

st.markdown("<p style='text-align:center; color:#888; font-size:0.7em;'>صقر العقارات 2026</p>", unsafe_allow_html=True)