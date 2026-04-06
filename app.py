import streamlit as st
import pandas as pd
from datetime import datetime
import os

# --- 1. إعدادات الصفحة ---
st.set_page_config(page_title="مناسبات آل علي", layout="centered", page_icon="logo.png")

# --- 2. التنسيق (Mobile Optimized) ---
st.markdown("""
    <style>
    .main { background-color: #080808; }
    .main-title { color: #D4AF37; text-align: center; font-size: 1.3em !important; font-weight: bold; padding: 5px; margin-bottom: 15px; }
    [data-testid="stMetric"] { background-color: #fdfdfd; border: 1px solid #D4AF37; padding: 5px !important; border-radius: 8px; }
    [data-testid="stMetricValue"] { color: #1a1a1a !important; font-size: 1.1em !important; font-weight: bold !important; }
    .stButton>button { border-radius: 10px; border: 1.5px solid #D4AF37; background-color: #1a1a1a; color: #D4AF37; font-weight: bold; width: 100%; height: 3.2em; }
    </style>
    """, unsafe_allow_html=True)

# --- 3. وظائف البيانات ---
EXCEL_FILE = 'names.xlsx'
CSV_RESULTS = 'community_events_results.csv'

def load_names():
    if os.path.exists(EXCEL_FILE):
        df = pd.read_excel(EXCEL_FILE)
        return sorted(df.iloc[:, 0].dropna().unique().tolist())
    return []

def save_names(names_list):
    df = pd.DataFrame(names_list, columns=['الاسم'])
    df.to_excel(EXCEL_FILE, index=False)

def load_results():
    if os.path.exists(CSV_RESULTS):
        try: return pd.read_csv(CSV_RESULTS, encoding='utf-8-sig')
        except: return pd.DataFrame(columns=['الاسم', 'الحالة', 'الوقت'])
    return pd.DataFrame(columns=['الاسم', 'الحالة', 'الوقت'])

# دالة مسح حقل الإضافة
def clear_text():
    st.session_state["new_name_input"] = ""

# --- 4. واجهة التطبيق الرئيسية ---
if os.path.exists("logo.png"):
    col_logo, _ = st.columns([1, 3])
    with col_logo: st.image("logo.png", width=65)

st.markdown("<div class='main-title'>⚜️ مناسبات جماعة آل علي بالرياض ⚜️</div>", unsafe_allow_html=True)

names_list = load_names()

if names_list:
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

# --- 6. مركز تحكم الإدارة (تحديث: ميزة تفريغ الحقل) ---
st.write("---")
with st.expander("⚙️ إعدادات الإدارة المتطورة"):
    admin_pass = st.text_input("أدخل الرقم السري للإدارة:", type="password")
    
    if admin_pass == "1234":
        tab1, tab2, tab3 = st.tabs(["➕ إضافة اسم", "🗑️ حذف اسم", "🧹 تصفير"])
        
        with tab1:
            # استخدام key و Session State لتفريغ الحقل
            new_person = st.text_input("اكتب الاسم الجديد بالكامل:", key="new_name_input")
            if st.button("حفظ الاسم الجديد"):
                if new_person and new_person not in names_list:
                    names_list.append(new_person)
                    save_names(names_list)
                    st.success(f"تمت إضافة {new_person}")
                    # هنا نقوم بتفريغ الحقل ثم إعادة التشغيل
                    st.session_state["new_name_input"] = "" 
                    st.rerun()
                elif new_person in names_list:
                    st.warning("الاسم موجود مسبقاً!")
        
        with tab2:
            name_to_del = st.selectbox("اختر الاسم المراد حذفه نهائياً:", options=["-- اختر --"] + names_list)
            if st.button("تأكيد حذف الاسم"):
                if name_to_del != "-- اختر --":
                    names_list.remove(name_to_del)
                    save_names(names_list)
                    st.error(f"تم حذف {name_to_del}")
                    st.rerun()
                    
        with tab3:
            if st.button("🗑️ تصفير قائمة الحضور الحالية"):
                if os.path.exists(CSV_RESULTS):
                    os.remove(CSV_RESULTS)
                    st.success("تم التصفير بنجاح")
                    st.rerun()
    elif admin_pass != "":
        st.error("الرقم السري خطأ")

st.markdown("<p style='text-align:center; color:#555; font-size:0.7em;'>تصميم وبرمجة: أبو فيصل للعقارات 2026</p>", unsafe_allow_html=True)