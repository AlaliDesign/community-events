import streamlit as st
import pandas as pd
from datetime import datetime
import os
import json

# --- 1. إعدادات وبرمجة الوظائف ---
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
        
    settings = {"title": "مناسبات آل علي", "date": "-", "time": "-", "location": "-", "map_url": ""}
    if os.path.exists('settings.json'):
        try:
            with open('settings.json', 'r', encoding='utf-8') as f: settings = json.load(f)
        except: pass
            
    return names, results, settings

# --- 2. تنسيق الواجهة الملكي ---
st.markdown("""
    <style>
    #MainMenu, footer, header {visibility: hidden;}
    .stApp { background-color: #FDFCF0; }
    .main .block-container {
        border: 2px solid #D4AF37; padding: 20px !important; 
        border-radius: 15px; background-color: #ffffff;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1); margin: auto; max-width: 95% !important;
    }
    /* تنسيق العدادات لتظهر بوضوح */
    div[data-testid="stMetric"] {
        background-color: #FFFDF5 !important;
        border: 2px solid #D4AF37 !important;
        border-radius: 15px !important;
        padding: 15px !important;
    }
    .stButton>button { 
        border-radius: 10px; border: 2px solid #D4AF37; 
        background-color: #1a1a1a; color: #D4AF37; 
        font-weight: bold; width: 100%; height: 3.8em;
    }
    </style>
    """, unsafe_allow_html=True)

# تحميل البيانات
all_names, df_results, settings = load_data()

# --- 3. عرض الهوية والمناسبة ---
st.markdown("<h2 style='text-align:center;'>بِسْمِ اللهِ الرَّحْمٰنِ الرَّحِيْمِ</h2>", unsafe_allow_html=True)
st.markdown(f"<h3 style='text-align:center; color:#D4AF37;'>{settings['title']}</h3>", unsafe_allow_html=True)

st.markdown(f"""
    <div style="background-color: #FFFDF5; border: 1px double #D4AF37; border-radius: 12px; padding: 15px; text-align: center; margin-bottom: 20px;">
        <p>📅 <b>التاريخ:</b> {settings['date']} | ⏰ <b>الوقت:</b> {settings['time']}</p>
        <p>📍 <b>الموقع:</b> {settings['location']}</p>
        <a href="{settings['map_url']}" target="_blank" style="color:#D4AF37; font-weight:bold; text-decoration:none;">📍 اضغط هنا لفتح الخريطة</a>
    </div>
""", unsafe_allow_html=True)

# --- 4. محرك البحث الذكي (تم حل المشكلة هنا) ---
st.markdown("### 🔍 ابحث عن اسمك وسجل حضورك")

# استخدام حقل واحد فقط للبحث والاختيار (هذا الحقل يدعم البحث التلقائي بالاسم)
selected_name = st.selectbox(
    "اكتب اسمك هنا للبحث والاختيار مباشرة:",
    options=["-- اختر اسمك من القائمة --"] + all_names,
    index=0,
    help="ابدأ بكتابة حروف اسمك وسوف يظهر لك فوراً"
)

# لا تظهر الأزرار إلا إذا تم اختيار اسم فعلي
if selected_name != "-- اختر اسمك من القائمة --":
    st.info(f"الاسم المختار: **{selected_name}**")
    c1, c2 = st.columns(2)
    with c1:
        if st.button("✅ تأكيد الحضور"):
            new_row = pd.DataFrame({'الاسم': [selected_name], 'الحالة': ['حاضر'], 'الوقت': [datetime.now().strftime("%I:%M %p")]})
            # تحديث السجل ومنع التكرار
            final_df = pd.concat([df_results[df_results['الاسم'] != selected_name], new_row], ignore_index=True)
            final_df.to_csv('results.csv', index=False, encoding='utf-8-sig')
            st.success("تم تسجيل حضورك بنجاح")
            st.balloons()
            st.rerun()
    with c2:
        if st.button("❌ تقديم اعتذار"):
            new_row = pd.DataFrame({'الاسم': [selected_name], 'الحالة': ['معتذر'], 'الوقت': [datetime.now().strftime("%I:%M %p")]})
            final_df = pd.concat([df_results[df_results['الاسم'] != selected_name], new_row], ignore_index=True)
            final_df.to_csv('results.csv', index=False, encoding='utf-8-sig')
            st.warning("تم تسجيل اعتذارك")
            st.rerun()

st.divider()

# --- 5. الإحصائيات (تظهر دائماً) ---
st.markdown("<h3 style='text-align:center;'>📊 إحصائيات المناسبة</h3>", unsafe_allow_html=True)
col_a, col_b, col_c = st.columns(3)
with col_a: st.metric("المسجلين", len(all_names))
with col_b: st.metric("حاضر ✅", len(df_results[df_results['الحالة'] == 'حاضر']))
with col_c: st.metric("معتذر ❌", len(df_results[df_results['الحالة'] == 'معتذر']))

# --- 6. لوحة التحكم ---
with st.expander("⚙️ لوحة التحكم (للمشرف)"):
    if st.text_input("كلمة المرور", type="password") == "1234":
        if st.button("تصفير سجل الحضور بالكامل"):
            if os.path.exists('results.csv'): os.remove('results.csv')
            st.rerun()
        
        st.write("--- تعديل بيانات المناسبة ---")
        t_title = st.text_input("العنوان", value=settings['title'])
        t_date = st.text_input("التاريخ", value=settings['date'])
        t_time = st.text_input("الوقت", value=settings['time'])
        t_loc = st.text_input("الموقع", value=settings['location'])
        t_map = st.text_input("رابط الخريطة", value=settings['map_url'])
        if st.button("حفظ التعديلات"):
            with open('settings.json', 'w', encoding='utf-8') as f:
                json.dump({"title":t_title, "date":t_date, "time":t_time, "location":t_loc, "map_url":t_map}, f, ensure_ascii=False)
            st.rerun()

st.markdown("<p style='text-align:center; color:#888; font-size:0.8em;'>صقر العقارات 2026</p>", unsafe_allow_html=True)