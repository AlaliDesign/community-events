import streamlit as st
import pandas as pd
from datetime import datetime
import os

# 1. إعدادات الواجهة الملكية (تنسيق أبو فيصل الخاص)
st.set_page_config(page_title="نظام مناسبات الجماعة", layout="centered")

st.markdown("""
    <style>
    /* الخلفية والخطوط العامة */
    .main { background-color: #000000; }
    body { color: #D4AF37; }
    
    /* العنوان الرئيسي بلمسة ذهبية */
    h1 { 
        color: #D4AF37; 
        text-align: center; 
        border-bottom: 2px solid #D4AF37; 
        padding-bottom: 10px; 
        text-shadow: 2px 2px 5px #000;
        font-family: 'Arial';
    }
    
    /* تنسيق الأزرار */
    .stButton>button { 
        border-radius: 15px; 
        border: 2px solid #D4AF37; 
        background-color: #1a1a1a; 
        color: #D4AF37; 
        font-weight: bold; 
        height: 3.5em;
        width: 100%;
        transition: 0.3s;
    }
    .stButton>button:hover { 
        background-color: #D4AF37; 
        color: #000; 
        box-shadow: 0 0 15px #D4AF37;
    }

    /* تنسيق الجداول والقوائم */
    .stSelectbox label { color: #D4AF37 !important; font-size: 1.2em; }
    .stDataFrame { border: 1px solid #D4AF37; border-radius: 10px; }
    </style>
    """, unsafe_allow_html=True)

st.markdown("<h1>⚜️ نظام مناسبات الجماعة ⚜️</h1>", unsafe_allow_html=True)

# 2. تعريف الملفات (تأكد من وجود names.xlsx في نفس المجلد)
EXCEL_FILE = 'names.xlsx'
CSV_RESULTS = 'community_events_results.csv'

# وظيفة لتحميل البيانات وتجنب مشاكل الذاكرة التخزينية
def load_data():
    if os.path.exists(EXCEL_FILE):
        df_excel = pd.read_excel(EXCEL_FILE)
        # جلب الأسماء من العمود الأول وحذف الفراغات
        return df_excel.iloc[:, 0].dropna().unique().tolist()
    else:
        return []

names_list = load_data()

# 3. التحقق من وجود ملف النتائج أو إنشاؤه
if os.path.exists(CSV_RESULTS):
    df_results = pd.read_csv(CSV_RESULTS, encoding='utf-8-sig')
else:
    df_results = pd.DataFrame(columns=['الاسم', 'الحالة', 'التاريخ'])

# 4. واجهة المستخدم
if not names_list:
    st.error("⚠️ لم يتم العثور على ملف الأسماء (names.xlsx). يرجى التأكد من رفعه في المجلد الرئيسي.")
else:
    st.write("###")
    selected_name = st.selectbox("👤 فضلاً، اختر اسمك من القائمة:", options=["-- اختر اسماً --"] + names_list)

    if selected_name != "-- اختر اسماً --":
        st.write(f"مرحباً بك يا **{selected_name}**، يرجى تأكيد حضورك للمناسبة:")
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("✅ سأحضر"):
                new_entry = pd.DataFrame({
                    'الاسم': [selected_name], 
                    'الحالة': ['حاضر'], 
                    'التاريخ': [datetime.now().strftime("%Y-%m-%d %I:%M %p")]
                })
                # تحديث الحالة إذا كان الاسم موجوداً مسبقاً أو إضافة جديد
                df_results = pd.concat([df_results[df_results['الاسم'] != selected_name], new_entry], ignore_index=True)
                df_results.to_csv(CSV_RESULTS, index=False, encoding='utf-8-sig')
                st.success(f"تم تسجيل حضورك بنجاح يا {selected_name}")
                st.balloons()
                st.rerun()

        with col2:
            if st.button("❌ أعتذر"):
                new_entry = pd.DataFrame({
                    'الاسم': [selected_name], 
                    'الحالة': ['معتذر'], 
                    'التاريخ': [datetime.now().strftime("%Y-%m-%d %I:%M %p")]
                })
                df_results = pd.concat([df_results[df_results['الاسم'] != selected_name], new_entry], ignore_index=True)
                df_results.to_csv(CSV_RESULTS, index=False, encoding='utf-8-sig')
                st.warning("تم تسجيل اعتذارك، نراك في مناسبات قادمة بإذن الله.")
                st.rerun()

# 5. عرض كشف النتائج (للمسؤول أو للاطلاع العام)
st.divider()
if not df_results.empty:
    with st.expander("📊 استعراض كشف المسجلين حالياً"):
        st.dataframe(df_results, use_container_width=True, hide_index=True)
        
        # زر لتحميل النتائج بصيغة CSV في أي وقت
        csv = df_results.to_csv(index=False).encode('utf-8-sig')
        st.download_button(
            label="📥 تحميل الكشف النهائي (CSV)",
            data=csv,
            file_name=f'results_{datetime.now().strftime("%Y%m%d")}.csv',
            mime='text/csv',
        )

# التوقيع الخاص بك (بصمة أبو فيصل)
st.markdown("<br><p style='text-align: center; color: #555;'>تصميم وبرمجة: أبو فيصل للعقارات</p>", unsafe_allow_html=True)