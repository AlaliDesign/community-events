import streamlit as st
import pandas as pd
from datetime import datetime
import os

# --- 1. إعدادات الصفحة والشعار (متناسب مع الجوال) ---
st.set_page_config(
    page_title="مناسبات آل علي", 
    layout="centered", 
    page_icon="logo.png" 
)

# --- 2. التنسيق المتطور (Mobile Friendly) ---
st.markdown("""
    <style>
    .main { background-color: #080808; }
    .main-title { color: #D4AF37; text-align: center; font-size: 1.3em !important; font-weight: bold; padding: 5px; margin-bottom: 15px; }
    [data-testid="stMetric"] { background-color: #fdfdfd; border: 1px solid #D4AF37; padding: 5px !important; border-radius: 8px; }
    [data-testid="stMetricValue"] { color: #1a1a1a !important; font-size: 1.1em !important; font-weight: bold !important; }
    [data-testid="stMetricLabel"] { color: #444 !important; font-size: 0.75em !important; }
    .stButton>button { border-radius: 10px; border: 1.5px solid #D4AF37; background-color: #1a1a1a; color: #D4AF37; font-weight: bold; width: 100%; height: 3.2em; font-size: 0.9em; }
    </style>
    """, unsafe_allow_html=True)

# --- 3. وظائف معالجة البيانات ---
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
if os.path.exists("logo.png"):
    col_logo, _ = st.columns([1, 3])
    with col_logo: st.image("logo.png", width=65)

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

    # --- 5. قسم النتائج والإحصائيات ---
    st.divider()
    df_final = load_results()
    
    if not df_final.empty:
        c1, c2, c3 = st.columns(3)
        with c1: st.metric("المسجلين", len(df_final))
        with c2: st.metric("✅ حاضر", len(df_final[df_final['الحالة'] == 'حاضر']))
        with c3: st.metric("❌ معتذر", len(df_final[df_final['الحالة'] == 'معتذر']))

        with st.expander("👁️ عرض كشف الأسماء"):
            st.dataframe(df_final, use_container_width=True, hide_index=True)
            csv_data = df_final.to_csv(index=False).encode('utf-8-sig')
            st.download_button("📥 تحميل التقرير (Excel)", data=csv_data, file_name="report.csv")

        # --- 6. مركز التحكم المقفل برقم سري ---
        st.write("---")
        with st.expander("⚙️ إعدادات الإدارة"):
            password = st.text_input("أدخل الرقم السري للتصفير:", type="password")
            
            # يمكنك تغيير الرقم السري من هنا (بدل 1234)
            if password == "1234":
                st.warning("⚠️ أنت الآن في وضع الإدارة. الضغط على الزر أدناه سيحذف جميع البيانات.")
                if st.button("🗑️ تأكيد تصفير المناسبة"):
                    if os.path.exists(CSV_RESULTS):
                        os.remove(CSV_RESULTS)
                        st.success("تم تصفير البيانات بنجاح!")
                        st.rerun()
            elif password != "":
                st.error("الرقم السري غير صحيح!")
    else:
        st.info("💡 بانتظار بدء تسجيل الحضور للمناسبة.")
else:
    st.error("ملف names.xlsx غير موجود.")

st.markdown("<p style='text-align:center; color:#555; font-size:0.7em; margin-top:30px;'>تصميم وبرمجة: أبو فيصل للعقارات 2026</p>", unsafe_allow_html=True)