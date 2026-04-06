import streamlit as st
import pandas as pd
from datetime import datetime
import os

# --- 1. إعدادات الصفحة والملفات ---
EVENT_NAME = "مناسبة الجماعة الكبرى"
EXCEL_FILE = 'names.xlsx'
CSV_RESULTS = 'community_events_results.csv'

st.set_page_config(page_title=EVENT_NAME, layout="centered", page_icon="⚜️")

# --- 2. التنسيق الملكي ---
st.markdown("""
    <style>
    .main { background-color: #000000; }
    h1 { color: #D4AF37; text-align: center; }
    .stButton>button { border-radius: 12px; border: 2px solid #D4AF37; background-color: #1a1a1a; color: #D4AF37; font-weight: bold; width: 100%; height: 3em; }
    .stMetric { background-color: #1a1a1a; padding: 15px; border-radius: 10px; border: 1px solid #333; }
    </style>
    """, unsafe_allow_html=True)

# --- 3. وظائف جلب البيانات ---
def load_results():
    if os.path.exists(CSV_RESULTS):
        try:
            return pd.read_csv(CSV_RESULTS, encoding='utf-8-sig')
        except:
            return pd.DataFrame(columns=['الاسم', 'الحالة', 'الوقت'])
    return pd.DataFrame(columns=['الاسم', 'الحالة', 'الوقت'])

# --- 4. واجهة المستخدم ---
st.markdown(f"<h1>⚜️ {EVENT_NAME} ⚜️</h1>", unsafe_allow_html=True)

# تحميل الأسماء من الإكسل
if os.path.exists(EXCEL_FILE):
    df_names = pd.read_excel(EXCEL_FILE)
    names_list = sorted(df_names.iloc[:, 0].dropna().unique().tolist())
    
    selected_name = st.selectbox("🔍 ابحث عن اسمك:", options=["-- اختر اسمك من القائمة --"] + names_list)

    if selected_name != "-- اختر اسمك من القائمة --":
        col1, col2 = st.columns(2)
        with col1:
            if st.button("✅ تأكيد الحضور"):
                res = load_results()
                new_row = pd.DataFrame({'الاسم': [selected_name], 'الحالة': ['حاضر'], 'الوقت': [datetime.now().strftime("%I:%M %p")]})
                pd.concat([res[res['الاسم'] != selected_name], new_row], ignore_index=True).to_csv(CSV_RESULTS, index=False, encoding='utf-8-sig')
                st.success("تم تسجيل حضورك")
                st.rerun()
        with col2:
            if st.button("❌ اعتذار"):
                res = load_results()
                new_row = pd.DataFrame({'الاسم': [selected_name], 'الحالة': ['معتذر'], 'الوقت': [datetime.now().strftime("%I:%M %p")]})
                pd.concat([res[res['الاسم'] != selected_name], new_row], ignore_index=True).to_csv(CSV_RESULTS, index=False, encoding='utf-8-sig')
                st.warning("تم تسجيل اعتذارك")
                st.rerun()

    # --- 5. لوحة الإحصائيات (العدادات) ---
    st.divider()
    df_final = load_results()
    
    if not df_final.empty:
        c1, c2, c3 = st.columns(3)
        with c1:
            st.metric("المسجلين", len(df_final))
        with c2:
            st.metric("✅ حاضر", len(df_final[df_final['الحالة'] == 'حاضر']))
        with c3:
            st.metric("❌ معتذر", len(df_final[df_final['الحالة'] == 'معتذر']))

        with st.expander("📊 كشف الأسماء التفصيلي"):
            st.dataframe(df_final, use_container_width=True, hide_index=True)
            csv = df_final.to_csv(index=False).encode('utf-8-sig')
            st.download_button("📥 تحميل التقرير (Excel/CSV)", data=csv, file_name="report.csv")
else:
    st.error("ملف names.xlsx غير موجود")

st.markdown("<p style='text-align:center; color:#555; margin-top:50px;'>تصميم وبرمجة: أبو فيصل للعقارات 2026</p>", unsafe_allow_html=True)