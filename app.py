import streamlit as st
import pandas as pd
from datetime import datetime
import os

# --- إعدادات ثابتة ---
EVENT_NAME = "مناسبة الجماعة الكبرى"
EXCEL_FILE = 'names.xlsx'
CSV_RESULTS = 'community_events_results.csv'

st.set_page_config(page_title=EVENT_NAME, layout="centered", page_icon="⚜️")

# 1. التنسيق الملكي (أبو فيصل)
st.markdown("""
    <style>
    .main { background-color: #000000; }
    .stSelectbox label { color: #D4AF37 !important; font-size: 1.2em; }
    .stButton>button { border-radius: 12px; border: 2px solid #D4AF37; background-color: #1a1a1a; color: #D4AF37; font-weight: bold; width: 100%; }
    </style>
    """, unsafe_allow_html=True)

# 2. وظيفة جلب البيانات (محدثة لضمان القراءة الصحيحة)
def load_results():
    if os.path.exists(CSV_RESULTS):
        try:
            # قراءة الملف مع التأكد من الترميز العربي
            return pd.read_csv(CSV_RESULTS, encoding='utf-8-sig')
        except:
            return pd.DataFrame(columns=['الاسم', 'الحالة', 'الوقت'])
    return pd.DataFrame(columns=['الاسم', 'الحالة', 'الوقت'])

# 3. تحميل قائمة الأسماء من الإكسل
if os.path.exists(EXCEL_FILE):
    df_names = pd.read_excel(EXCEL_FILE)
    names_list = sorted(df_names.iloc[:, 0].dropna().unique().tolist())
else:
    st.error("⚠️ ملف names.xlsx غير موجود!")
    names_list = []

st.markdown(f"<h1 style='text-align:center; color:#D4AF37;'>⚜️ {EVENT_NAME} ⚜️</h1>", unsafe_allow_html=True)

# 4. واجهة الاختيار والبحث
selected_name = st.selectbox("🔍 ابحث عن اسمك:", options=["-- اختر اسمك --"] + names_list)

if selected_name != "-- اختر اسمك --":
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("✅ تأكيد الحضور"):
            # جلب البيانات الحالية أولاً
            current_results = load_results()
            new_entry = pd.DataFrame({
                'الاسم': [selected_name], 
                'الحالة': ['حاضر'], 
                'الوقت': [datetime.now().strftime("%I:%M %p")]
            })
            # تحديث أو إضافة الاسم
            updated_df = pd.concat([current_results[current_results['الاسم'] != selected_name], new_entry], ignore_index=True)
            updated_df.to_csv(CSV_RESULTS, index=False, encoding='utf-8-sig')
            
            st.success(f"تم تسجيل حضورك يا {selected_name}")
            st.rerun() # إجبار التطبيق على التحديث فوراً

    with col2:
        if st.button("❌ اعتذار"):
            current_results = load_results()
            new_entry = pd.DataFrame({
                'الاسم': [selected_name], 
                'الحالة': ['معتذر'], 
                'الوقت': [datetime.now().strftime("%I:%M %p")]
            })
            updated_df = pd.concat([current_results[current_results['الاسم'] != selected_name], new_entry], ignore_index=True)
            updated_df.to_csv(CSV_RESULTS, index=False, encoding='utf-8-sig')
            
            st.warning("تم تسجيل اعتذارك.")
            st.rerun() # إجبار التطبيق على التحديث فوراً

# 5. عرض النتائج (محدثة)
st.divider()
df_final = load_results() # قراءة الملف مرة أخرى بعد التحديث

if not df_final.empty:
    with st.expander("📊 استعراض كشف المسجلين (محدث فورياً)"):
        # عرض الجدول بشكل مرتب
        st.dataframe(df_final, use_container_width=True, hide_index=True)
        
        # زر التحميل للتأكيد
        csv = df_final.to_csv(index=False).encode('utf-8-sig')
        st.download_button("📥 تحميل الكشف (CSV)", data=csv, file_name="results.csv", mime="text/csv")
else:
    st.info("لم يتم تسجيل أي حضور حتى الآن.")

st.markdown("<p style='text-align:center; color:#555;'>تصميم: أبو فيصل للعقارات 2026</p>", unsafe_allow_html=True)