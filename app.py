import streamlit as st
import pandas as pd
from datetime import datetime
import os

# --- 1. إعدادات الصفحة والملفات ---
EVENT_NAME = "مناسبة الجماعة الكبرى"
EXCEL_FILE = 'names.xlsx'
CSV_RESULTS = 'community_events_results.csv'

st.set_page_config(page_title=EVENT_NAME, layout="centered", page_icon="⚜️")

# --- 2. التنسيق المطور للوضوح العالي ---
st.markdown("""
    <style>
    /* الخلفية العامة */
    .main { background-color: #080808; }
    h1 { color: #D4AF37; text-align: center; padding-bottom: 20px; }
    
    /* تنسيق بطاقات الإحصائيات بألوان فاتحة وواضحة */
    [data-testid="stMetric"] {
        background-color: #f8f9fa; /* لون خلفية فاتح جداً */
        border: 2px solid #D4AF37;
        padding: 15px;
        border-radius: 15px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    
    /* جعل أرقام الإحصائيات غامقة وواضحة */
    [data-testid="stMetricValue"] {
        color: #1a1a1a !important;
        font-weight: bold !important;
    }
    
    /* اسم الإحصائية (Label) */
    [data-testid="stMetricLabel"] {
        color: #444 !important;
        font-weight: bold !important;
    }

    /* تنسيق الأزرار */
    .stButton>button { 
        border-radius: 12px; border: 2px solid #D4AF37; 
        background-color: #1a1a1a; color: #D4AF37; 
        font-weight: bold; width: 100%; height: 3.5em;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 3. وظيفة جلب البيانات ---
def load_results():
    if os.path.exists(CSV_RESULTS):
        try:
            return pd.read_csv(CSV_RESULTS, encoding='utf-8-sig')
        except:
            return pd.DataFrame(columns=['الاسم', 'الحالة', 'الوقت'])
    return pd.DataFrame(columns=['الاسم', 'الحالة', 'الوقت'])

# --- 4. واجهة المستخدم ---
st.markdown(f"<h1>⚜️ {EVENT_NAME} ⚜️</h1>", unsafe_allow_html=True)

if os.path.exists(EXCEL_FILE):
    df_names = pd.read_excel(EXCEL_FILE)
    names_list = sorted(df_names.iloc[:, 0].dropna().unique().tolist())
    
    selected_name = st.selectbox("🔍 ابحث عن اسمك في القائمة:", options=["-- اختر اسمك --"] + names_list)

    if selected_name != "-- اختر اسمك --":
        col1, col2 = st.columns(2)
        with col1:
            if st.button("✅ تأكيد الحضور"):
                res = load_results()
                new_row = pd.DataFrame({'الاسم': [selected_name], 'الحالة': ['حاضر'], 'الوقت': [datetime.now().strftime("%I:%M %p")]})
                pd.concat([res[res['الاسم'] != selected_name], new_row], ignore_index=True).to_csv(CSV_RESULTS, index=False, encoding='utf-8-sig')
                st.success("تم تسجيل حضورك بنجاح")
                st.rerun()
        with col2:
            if st.button("❌ اعتذار"):
                res = load_results()
                new_row = pd.DataFrame({'الاسم': [selected_name], 'الحالة': ['معتذر'], 'الوقت': [datetime.now().strftime("%I:%M %p")]})
                pd.concat([res[res['الاسم'] != selected_name], new_row], ignore_index=True).to_csv(CSV_RESULTS, index=False, encoding='utf-8-sig')
                st.warning("تم تسجيل اعتذارك")
                st.rerun()

    # --- 5. لوحة الإحصائيات بالألوان الجديدة ---
    st.divider()
    df_final = load_results()
    
    if not df_final.empty:
        st.markdown("<h3 style='color:#D4AF37; text-align:center;'>📊 ملخص التسجيل</h3>", unsafe_allow_html=True)
        c1, c2, c3 = st.columns(3)
        with c1:
            st.metric("المسجلين", len(df_final))
        with c2:
            st.metric("✅ حاضر", len(df_final[df_final['الحالة'] == 'حاضر']))
        with c3:
            st.metric("❌ معتذر", len(df_final[df_final['الحالة'] == 'معتذر']))

        with st.expander("👁️ عرض كشف الأسماء"):
            st.dataframe(df_final, use_container_width=True, hide_index=True)
            csv = df_final.to_csv(index=False).encode('utf-8-sig')
            st.download_button("📥 تحميل التقرير النهائي", data=csv, file_name="report.csv")
else:
    st.error("تنبيه: ملف names.xlsx غير موجود في المجلد.")

st.markdown("<br><p style='text-align:center; color:#555;'>تصميم وبرمجة: أبو فيصل للعقارات 2026</p>", unsafe_allow_html=True)