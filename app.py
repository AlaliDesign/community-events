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
        try:
            df = pd.read_excel(EXCEL_FILE)
            return sorted(df.iloc[:, 0].dropna().unique().tolist())
        except: return []
    return []

def save_names(names_list):
    df = pd.DataFrame(names_list, columns=['الاسم'])
    df.to_excel(EXCEL_FILE, index=False)

def load_results():
    if os.path.exists(CSV_RESULTS):
        try: return pd.read_csv(CSV_RESULTS, encoding='utf-8-sig')
        except: return pd.DataFrame(columns=['الاسم', 'الحالة', 'الوقت'])
    return pd.DataFrame(columns=['الاسم', 'الحالة', 'الوقت'])

# --- 4. تهيئة الذاكرة (Session State) ---
if 'names' not in st.session_state:
    st.session_state.names = load_names()
if 'input_key' not in st.session_state:
    st.session_state.input_key = 0 # هذا هو المفتاح السحري للتفريغ

# --- 5. واجهة التطبيق ---
if os.path.exists("logo.png"):
    col_logo, _ = st.columns([1, 3])
    with col_logo: st.image("logo.png", width=65)

st.markdown("<div class='main-title'>⚜️ مناسبات جماعة آل علي بالرياض ⚜️</div>", unsafe_allow_html=True)

names_list = st.session_state.names

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

st.divider()
df_final = load_results()

if not df_final.empty:
    c1, c2, c3 = st.columns(3)
    with c1: st.metric("المسجلين", len(df_final))
    with c2: st.metric("✅ حاضر", len(df_final[df_final['الحالة'] == 'حاضر']))
    with c3: st.metric("❌ معتذر", len(df_final[df_final['الحالة'] == 'معتذر']))
    with st.expander("👁️ عرض الكشف"):
        st.dataframe(df_final, use_container_width=True, hide_index=True)

# --- 6. مركز تحكم الإدارة (الإصدار العبقري للتفريغ) ---
st.write("---")
with st.expander("⚙️ إعدادات الإدارة"):
    admin_pass = st.text_input("رقم الإدارة السري:", type="password")
    
    if admin_pass == "1234":
        tab1, tab2, tab3 = st.tabs(["➕ إضافة", "🗑️ حذف", "🧹 تصفير"])
        
        with tab1:
            # هنا نستخدم المفتاح المتغير input_key لضمان التفريغ
            new_person = st.text_input("الاسم الجديد:", key=f"ins_{st.session_state.input_key}")
            
            if st.button("حفظ الآن"):
                if new_person and new_person not in st.session_state.names:
                    st.session_state.names.append(new_person)
                    save_names(st.session_state.names)
                    # تغيير المفتاح فوراً لمسح الحقل
                    st.session_state.input_key += 1 
                    st.success(f"تمت إضافة {new_person}")
                    st.rerun()
                elif new_person in st.session_state.names:
                    st.warning("موجود مسبقاً!")
        
        with tab2:
            name_to_del = st.selectbox("حذف اسم:", options=["-- اختر --"] + st.session_state.names)
            if st.button("تأكيد الحذف"):
                if name_to_del != "-- اختر --":
                    st.session_state.names.remove(name_to_del)
                    save_names(st.session_state.names)
                    st.rerun()
                    
        with tab3:
            if st.button("🗑️ تصفير الحضور"):
                if os.path.exists(CSV_RESULTS):
                    os.remove(CSV_RESULTS)
                    st.rerun()