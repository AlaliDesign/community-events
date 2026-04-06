import streamlit as st
import pandas as pd
from datetime import datetime
import os

# --- 1. إعدادات الصفحة ---
st.set_page_config(page_title="مناسبات آل علي", layout="centered", page_icon="logo.png")

# --- 2. التنسيق المتطور (توسيط الشعار، دائرة مثالية، برواز، وراحة العين) ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Amiri&family=Tajawal:wght@400;700&display=swap');

    /* تغيير خلفية التطبيق للون كريمي مريح للعين */
    .stApp {
        background-color: #F5F5DC; 
    }
    
    /* تصميم البرواز الملكي المتجاوب مع الجوال */
    .main .block-container {
        border: 2px solid #D4AF37;
        padding: 20px !important;
        border-radius: 15px;
        background-color: #ffffff;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
        margin: 10px auto;
        max-width: 95% !important;
    }

    /* البسملة */
    .bismillah {
        font-family: 'Amiri', serif;
        font-size: 2em;
        color: #1a1a1a;
        text-align: center;
        margin-bottom: 5px;
    }

    /* --- التوسيط القسري للشعار وجعله دائرة مثالية --- */
    .centered-logo-container {
        display: flex;
        justify-content: center; /* توسيط أفقي */
        align-items: center;    /* توسيط عمودي إذا لزم الأمر */
        width: 100%;
        margin: 15px 0;
    }

    /* تنسيق الشعار ليكون دائرة مثالية */
    .circular-logo {
        width: 160px !important;  /* عرض ثابت */
        height: 160px !important; /* طول ثابت مطابق للعرض */
        border-radius: 50% !important; /* جعل الزوايا دائرة كاملة */
        border: 4px solid #D4AF37 !important; /* إطار ذهبي فخم */
        object-fit: cover !important; /* ضمان عدم تمدد الصورة بالداخل */
        box-shadow: 0 5px 15px rgba(0,0,0,0.2) !important;
    }

    /* العنوان الرئيسي */
    .main-title { 
        color: #D4AF37; 
        text-align: center; 
        font-size: 1.4em !important; 
        font-family: 'Tajawal', sans-serif;
        font-weight: bold;
        margin-bottom: 25px;
        border-bottom: 2px solid #eee;
        padding-bottom: 10px;
    }
    
    /* تنسيق العدادات الإحصائية للجوال */
    [data-testid="stMetric"] {
        background-color: #FFFDF5; 
        border: 1px solid #D4AF37;
        border-radius: 10px;
        text-align: center;
    }
    
    [data-testid="stMetricValue"] { color: #1a1a1a !important; font-size: 1.3em !important; font-weight: bold !important; }

    /* أزرار الحضور */
    .stButton>button { 
        border-radius: 10px; border: 2px solid #D4AF37; 
        background-color: #1a1a1a; color: #D4AF37; 
        font-weight: bold; width: 100%; height: 3.5em;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 3. إدارة البيانات ---
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

# --- 4. واجهة العرض ---

st.markdown("<div class='bismillah'>بِسْمِ اللهِ الرَّحْمٰنِ الرَّحِيْمِ</div>", unsafe_allow_html=True)

# التوسيط المطلق والدائرة المثالية للشعار
if os.path.exists("logo.png"):
    st.markdown("""
        <div class="centered-logo-container">
            <img src="app/static/logo.png" class="circular-logo" alt="Logo">
        </div>
        """, unsafe_allow_html=True)
else:
    # خيار بديل في حال لم يرفع الملف بعد
    st.markdown("<h1 style='text-align:center;'>⚜️</h1>", unsafe_allow_html=True)

st.markdown("<div class='main-title'>مناسبات جماعة آل علي بالرياض</div>", unsafe_allow_html=True)

# تحميل الأسماء في الذاكرة لتكون القائمة دائماً محدثة
if 'names' not in st.session_state:
    st.session_state.names = load_names()

names_list = st.session_state.names

# --- 5. حقل البحث وتسجيل الحضور ---
if names_list:
    selected_name = st.selectbox("🔍 ابحث عن اسمك:", options=["-- اختر من القائمة --"] + names_list)

    if selected_name != "-- اختر من القائمة --":
        col1, col2 = st.columns(2)
        with col1:
            if st.button("✅ تأكيد الحضور"):
                res = load_results()
                # إضافة تسجيل الحضور مع استبعاد الاعتذار السابق إن وجد
                new_row = pd.DataFrame({'الاسم': [selected_name], 'الحالة': ['حاضر'], 'الوقت': [datetime.now().strftime("%I:%M %p")]})
                pd.concat([res[res['الاسم'] != selected_name], new_row], ignore_index=True).to_csv(CSV_RESULTS, index=False, encoding='utf-8-sig')
                st.success(f"تم تأكيد حضورك يا {selected_name.split()[0]}")
                st.rerun()
        with col2:
            if st.button("❌ تقديم اعتذار"):
                res = load_results()
                # إضافة تسجيل الاعتذار مع استبعاد الحضور السابق إن وجد
                new_row = pd.DataFrame({'الاسم': [selected_name], 'الحالة': ['معتذر'], 'الوقت': [datetime.now().strftime("%I:%M %p")]})
                pd.concat([res[res['الاسم'] != selected_name], new_row], ignore_index=True).to_csv(CSV_RESULTS, index=False, encoding='utf-8-sig')
                st.warning("تم تسجيل اعتذارك")
                st.rerun()

st.divider()

# --- 6. إحصائيات الفرز العام ---
df_results = load_results()
total_all = len(names_list)
total_present = len(df_results[df_results['الحالة'] == 'حاضر'])
total_absent = len(df_results[df_results['الحالة'] == 'معتذر'])

st.markdown("<h3 style='color:#D4AF37; text-align:center;'>📊 إحصائيات الفرز العام</h3>", unsafe_allow_html=True)

# الصف الأول: الإجماليات
c1, c2 = st.columns(2)
with c1: st.metric("إجمالي القائمة", total_all)
with c2: st.metric("إجمالي المتفاعلين", len(df_results))

# الصف الثاني: التفاصيل
c3, c4 = st.columns(2)
with c3: st.metric("✅ عدد الحاضرين", total_present)
with c4: st.metric("❌ عدد المعتذرين", total_absent)

# --- 7. لوحة التحكم للإدارة ---
with st.expander("⚙️ لوحة تحكم المشرف"):
    admin_pass = st.text_input("أدخل الرقم السري للإدارة:", type="password")
    
    if admin_pass == "1234":
        tab1, tab2, tab3 = st.tabs(["➕ إضافة اسم", "🗑️ حذف اسم", "🧹 تصفير"])
        
        with tab1:
            # استخدام المفتاح الديناميكي لتفريغ الحقل بعد الإضافة
            new_person = st.text_input("الاسم الجديد بالكامل:", key=f"ins_{st.session_state.input_key}")
            
            if st.button("حفظ وإضافة الاسم"):
                if new_person:
                    clean_name = new_person.strip()
                    if clean_name not in st.session_state.names:
                        st.session_state.names.append(clean_name)
                        st.session_state.names = sorted(st.session_state.names)
                        save_names(st.session_state.names)
                        st.session_state.input_key += 1
                        st.rerun()
        
        with tab2:
            name_to_del = st.selectbox("حذف اسم من القائمة الرئيسية:", options=["-- اختر --"] + st.session_state.names)
            if st.button("تأكيد الحذف"):
                if name_to_del != "-- اختر --":
                    st.session_state.names.remove(name_to_del)
                    save_names(st.session_state.names)
                    st.rerun()
                    
        with tab3:
            if st.button("🗑️ تصفير قائمة الحضور للمناسبة القادمة"):
                if os.path.exists(CSV_RESULTS):
                    os.remove(CSV_RESULTS)
                    st.rerun()

st.markdown("<p style='text-align:center; color:#888; font-size:0.8em; margin-top:30px;'>تصميم وبرمجة: أبو فيصل للعقارات 2026</p>", unsafe_allow_html=True)