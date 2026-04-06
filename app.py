import streamlit as st
import pandas as pd
from datetime import datetime
import os

# --- 1. إعدادات الصفحة ---
st.set_page_config(page_title="مناسبات آل علي", layout="centered", page_icon="logo.png")

# --- 2. التنسيق (التوسيط القسري وتكبير الشعار) ---
st.markdown("""
    <style>
    .main { background-color: #080808; }
    
    /* حاوية الشعار لضمان التوسط وتكبير الحجم */
    .logo-container {
        display: flex;
        justify-content: center; /* توسيط أفقي */
        align-items: center;    /* توسيط عمودي */
        width: 100%;
        padding: 20px 0;
    }
    
    .logo-container img {
        width: 180px !important; /* تكبير الشعار ليكون واضحاً جداً */
        height: auto;
        display: block;
        margin-left: auto;
        margin-right: auto;
    }

    .main-title { 
        color: #D4AF37; 
        text-align: center; 
        font-size: 1.6em !important; 
        font-weight: bold;
        margin-top: 10px;
        margin-bottom: 25px;
        text-shadow: 1px 1px 2px black;
    }
    
    /* تنسيق العدادات */
    [data-testid="stMetric"] {
        background-color: #fdfdfd; 
        border: 1px solid #D4AF37;
        padding: 12px !important;
        border-radius: 10px;
        text-align: center;
    }
    
    [data-testid="stMetricValue"] { color: #1a1a1a !important; font-size: 1.3em !important; font-weight: bold !important; }

    .stButton>button { 
        border-radius: 12px; border: 2px solid #D4AF37; 
        background-color: #1a1a1a; color: #D4AF37; 
        font-weight: bold; width: 100%; height: 3.8em;
    }
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

if 'input_key' not in st.session_state:
    st.session_state.input_key = 0

# --- 4. عرض الشعار (النسخة المكبرة والمتوسطة) ---

# استخدام HTML لضمان التوسط المطلق وتجاوز إعدادات ستريمليت الافتراضية
if os.path.exists("logo.png"):
    st.markdown(f"""
        <div class="logo-container">
            <img src="https://raw.githubusercontent.com/{st.secrets.get('GITHUB_USER', 'YourUser')}/{st.secrets.get('REPO_NAME', 'YourRepo')}/main/logo.png" alt="Logo">
        </div>
        """, unsafe_allow_html=True)
    # في حال لم يعمل الرابط أعلاه، نستخدم الطريقة التقليدية كاحتياط
    st.image("logo.png", width=180) 
else:
    st.markdown("<h1 style='text-align:center;'>⚜️</h1>", unsafe_allow_html=True)

st.markdown("<div class='main-title'>مناسبات جماعة آل علي بالرياض</div>", unsafe_allow_html=True)

# تحميل الأسماء
if 'names' not in st.session_state:
    st.session_state.names = load_names()

names_list = st.session_state.names

# --- 5. تسجيل الحضور ---
if names_list:
    selected_name = st.selectbox("🔍 ابحث عن اسمك لتسجيل الحضور:", options=["-- اختر من القائمة --"] + names_list)

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
                st.warning("تم تسجيل الاعتذار")
                st.rerun()

st.divider()

# --- 6. الإحصائيات الشاملة ---
df_results = load_results()
total_in_list = len(names_list)
total_responded = len(df_results)

st.markdown("<h3 style='color:#D4AF37; text-align:center;'>📊 إحصائيات الفرز العام</h3>", unsafe_allow_html=True)

c1, c2 = st.columns(2)
with c1: st.metric("إجمالي الأسماء المضافة", total_in_list)
with c2: st.metric("إجمالي من سجلوا", total_responded)

c3, c4 = st.columns(2)
with c3: st.metric("✅ عدد الحضور", len(df_results[df_results['الحالة'] == 'حاضر']))
with c4: st.metric("❌ عدد المعتذرين", len(df_results[df_results['الحالة'] == 'معتذر']))

# --- 7. مركز تحكم الإدارة ---
with st.expander("⚙️ إعدادات الإدارة"):
    admin_pass = st.text_input("الرقم السري للإدارة:", type="password")
    if admin_pass == "1234":
        tab1, tab2, tab3 = st.tabs(["➕ إضافة شخص", "🗑️ حذف شخص", "🧹 تصفير الكشف"])
        with tab1:
            new_person = st.text_input("الاسم الكامل:", key=f"ins_{st.session_state.input_key}")
            if st.button("حفظ وإضافة"):
                if new_person:
                    clean_n = new_person.strip()
                    if clean_n not in st.session_state.names:
                        st.session_state.names.append(clean_n)
                        save_names(sorted(st.session_state.names))
                        st.session_state.input_key += 1
                        st.success(f"تمت إضافة {clean_n} للقائمة")
                        st.rerun()
        with tab2:
            to_del = st.selectbox("اختر الاسم لحذفه:", options=["-- اختر --"] + st.session_state.names)
            if st.button("تأكيد الحذف النهائي"):
                if to_del != "-- اختر --":
                    st.session_state.names.remove(to_del)
                    save_names(st.session_state.names)
                    st.rerun()
        with tab3:
            if st.button("تصفير كشف الحضور الحالي"):
                if os.path.exists(CSV_RESULTS): 
                    os.remove(CSV_RESULTS)
                    st.rerun()

st.markdown("<p style='text-align:center; color:#555; font-size:0.85em; margin-top:50px;'>تصميم وبرمجة: أبو فيصل للعقارات 2026</p>", unsafe_allow_html=True)