import streamlit as st
import pandas as pd
from datetime import datetime
import os

# --- 1. إعدادات الصفحة والشعار ---
st.set_page_config(
    page_title="مناسبات آل علي", 
    layout="centered", 
    page_icon="logo.png" 
)

# --- 2. التنسيق المتناسب مع الجوال (Mobile Optimized) ---
st.markdown("""
    <style>
    .main { background-color: #080808; }
    
    /* تصغير العنوان ليناسب شاشة الجوال */
    .main-title { 
        color: #D4AF37; 
        text-align: center; 
        font-size: 1.4em !important; /* حجم خط أصغر للجوال */
        font-weight: bold;
        padding: 10px 5px;
        line-height: 1.4;
    }
    
    /* تنسيق بطاقات الإحصائيات - حجم مرن */
    [data-testid="stMetric"] {
        background-color: #fdfdfd; 
        border: 1px solid #D4AF37;
        padding: 10px !important;
        border-radius: 10px;
    }
    
    /* تصغير أرقام العدادات لتظهر في صف واحد بالعرض */
    [data-testid="stMetricValue"] { 
        color: #1a1a1a !important; 
        font-size: 1.1em !important; /* تصغير الرقم قليلاً */
        font-weight: bold !important; 
    }
    [data-testid="stMetricLabel"] { 
        color: #444 !important; 
        font-size: 0.8em !important; /* تصغير المسمى */
    }

    /* أزرار الحضور - ارتفاع مناسب للإبهام */
    .stButton>button { 
        border-radius: 10px; border: 1.5px solid #D4AF37; 
        background-color: #1a1a1a; color: #D4AF37; 
        font-weight: bold; width: 100%; height: 3em;
        font-size: 0.9em;
    }
    
    /* تصغير حجم خانة البحث */
    .stSelectbox label { font-size: 0.9em !important; color: #D4AF37 !important; }
    </style>
    """, unsafe_allow_html=True)

# --- 3. وظائف البيانات ---
EXCEL_FILE = 'names.xlsx'
CSV_RESULTS = 'community_events_results.csv'

def load_results():
    if os.path.exists(CSV_RESULTS):
        try:
            return pd.read_csv(CSV_RESULTS, encoding='utf-8-sig')
        except:
            return pd.DataFrame(columns=['الاسم', 'الحالة', 'الوقت'])
    return pd.DataFrame(columns=['الاسم', 'الحالة', 'الوقت'])

# --- 4. واجهة التطبيق ---
# عرض الشعار بحجم صغير يتناسب مع الجوال
if os.path.exists("logo.png"):
    col_logo, _ = st.columns([1, 4])
    with col_logo:
        st.image("logo.png", width=70)

# العنوان بالكليشة الجديدة والحجم المصغر
st.markdown("<div class='main-title'>⚜️ مناسبات جماعة آل علي بالرياض ⚜️</div>", unsafe_allow_html=True)

if os.path.exists(EXCEL_FILE):
    df_names = pd.read_excel(EXCEL_FILE)
    names_list = sorted(df_names.iloc[:, 0].dropna().unique().tolist())
    
    selected_name = st.selectbox("🔍 ابحث عن اسمك:", options=["-- اختر من القائمة --"] + names_list)

    if selected_name != "-- اختر من القائمة --":
        col1, col2 = st.columns(2)
        with col1:
            if st.button("✅ حضور"):
                res = load_results()
                new_row = pd.DataFrame({'الاسم': [selected_name], 'الحالة': ['حاضر'], 'الوقت': [datetime.now().strftime("%I:%M %p")]})
                pd.concat([res[res['الاسم'] != selected_name], new_row], ignore_index=True).to_csv(CSV_RESULTS, index=False, encoding='utf-8-sig')
                st.success("تم التأكيد")
                st.rerun()
        with col2:
            if st.button("❌ اعتذار"):
                res = load_results()
                new_row = pd.DataFrame({'الاسم': [selected_name], 'الحالة': ['معتذر'], 'الوقت': [datetime.now().strftime("%I:%M %p")]})
                pd.concat([res[res['الاسم'] != selected_name], new_row], ignore_index=True).to_csv(CSV_RESULTS, index=False, encoding='utf-8-sig')
                st.warning("تم الاعتذار")
                st.rerun()

    # --- 5. ملخص الحضور (مصغر للجوال) ---
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

        with st.expander("👁️ كشف الأسماء"):
            st.dataframe(df_final, use_container_width=True, hide_index=True)
            csv = df_final.to_csv(index=False).encode('utf-8-sig')
            st.download_button("📥 تحميل التقرير", data=csv, file_name="report.csv")
else:
    st.error("تنبيه: ملف names.xlsx غير موجود.")

st.markdown("<p style='text-align:center; color:#555; font-size:0.7em;'>تصميم وبرمجة: أبو فيصل للعقارات 2026</p>", unsafe_allow_html=True)