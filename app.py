import streamlit as st
import pandas as pd
from datetime import datetime
import os

# 1. إعدادات الواجهة الملكية
st.set_page_config(page_title="نظام مناسبات الجماعة", layout="centered")

st.markdown("""
    <style>
    .main { background-color: #000000; }
    h1 { color: #D4AF37; text-align: center; border-bottom: 2px solid #D4AF37; padding-bottom: 10px; }
    .stButton>button { border-radius: 20px; border: 1px solid #D4AF37; font-weight: bold; height: 3em; }
    </style>
    """, unsafe_allow_html=True)

st.markdown("<h1>⚜️ نظام مناسبات الجماعة ⚜️</h1>", unsafe_allow_html=True)

# 2. رفع ملف الأسماء يدوياً (لحل مشكلة عدم العثور على الملف)
uploaded_file = st.file_uploader("📂 فضلاً قم برفع ملف الأسماء (Excel) من هنا:", type=["xlsx"])
csv_output = 'community_events.csv'

if uploaded_file:
    try:
        df_excel = pd.read_excel(uploaded_file)
        names_list = df_excel.iloc[:, 0].dropna().unique().tolist()
        
        # قراءة أو إنشاء ملف النتائج
        if os.path.exists(csv_output):
            df_results = pd.read_csv(csv_output, encoding='utf-8-sig')
        else:
            df_results = pd.DataFrame(columns=['الاسم', 'الحالة', 'التاريخ'])

        # 3. واجهة الاختيار والتسجيل
        if names_list:
            selected_name = st.selectbox("👤 اختر اسمك من القائمة:", options=["-- اختر اسماً --"] + names_list)
            
            if selected_name != "-- اختر اسماً --":
                c1, c2 = st.columns(2)
                with c1:
                    if st.button("✅ سأحضر", use_container_width=True):
                        new_data = pd.DataFrame({'الاسم': [selected_name], 'الحالة': ['حاضر'], 'التاريخ': [datetime.now().strftime("%Y-%m-%d %H:%M")]})
                        df_results = pd.concat([df_results[df_results['الاسم'] != selected_name], new_data], ignore_index=True)
                        df_results.to_csv(csv_output, index=False, encoding='utf-8-sig')
                        st.success("تم تسجيل حضورك")
                        st.rerun()
                with c2:
                    if st.button("❌ أعتذر", use_container_width=True):
                        new_data = pd.DataFrame({'الاسم': [selected_name], 'الحالة': ['معتذر'], 'التاريخ': [datetime.now().strftime("%Y-%m-%d %H:%M")]})
                        df_results = pd.concat([df_results[df_results['الاسم'] != selected_name], new_data], ignore_index=True)
                        df_results.to_csv(csv_output, index=False, encoding='utf-8-sig')
                        st.warning("تم تسجيل اعتذارك")
                        st.rerun()

        # 4. عرض النتائج بالأسفل
        st.divider()
        if not df_results.empty:
            st.subheader("📊 كشف المسجلين")
            st.dataframe(df_results, use_container_width=True, hide_index=True)
        
    except Exception as e:
        st.error(f"حدث خطأ في قراءة الملف: {e}")
else:
    st.info("💡 يرجى رفع ملف الإكسل (community_events.xlsx) لكي تظهر قائمة الأسماء.")