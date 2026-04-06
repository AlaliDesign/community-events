import streamlit as st
import pandas as pd
from datetime import datetime
import os

# --- 1. إعدادات الصفحة ---
st.set_page_config(page_title="مناسبات آل علي", layout="centered", page_icon="logo.png")

# --- 2. التنسيق الملكي المريح للعين وإخفاء شعار المنصة ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Amiri&family=Tajawal:wght@400;700&display=swap');
    
    /* إخفاء شعار Streamlit والقوائم الافتراضية */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}

    /* خلفية مريحة للعين */
    .stApp { background-color: #F5F5DC; }
    
    /* البرواز الملكي المتجاوب */
    .main .block-container {
        border: 2px solid #D4AF37;
        padding: 20px !important;
        border-radius: 15px;
        background-color: #ffffff;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
        margin: 10px auto;
        max-width: 95% !important;
    }

    .bismillah { font-family: 'Amiri', serif; font-size: 2em; color: #1a1a1a; text-align: center; margin-bottom: 5px; }
    
    .logo-wrapper { display: flex; justify-content: center; width: 100%; margin-bottom: 10px; }
    .logo-wrapper img { width: 170px !important; height: auto; }

    .main-title { 
        color: #D4AF37; 
        text-align: center; 
        font-size: 1.4em !important; 
        font-family: 'Tajawal', sans-serif;
        font-weight: bold;
        margin-bottom: 25px;
    }
    
    /* تنسيق العدادات */
    [data-testid="stMetric"] {
        background-color: #FFFDF5; 
        border: 1px solid #D4AF37;
        border-radius: 10px;
        text-align: center;
    }

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

if os.path.exists("logo.png"):
    st.markdown('<div class="logo-wrapper">', unsafe_allow_html=True)
    st.image("logo.png", width=170)
    st.markdown('</div>', unsafe_allow_html=True)

st.markdown("<div class='main-title'>مناسبات جماعة آل علي بالرياض</div>", unsafe_allow_html=True)

if 'names' not in st.session_state:
    st.session_state.names = load_names()
names_list = st.session_state.names

# --- 5. حقل البحث وتسجيل الحضور ---
if names_list:
    st.markdown("<p style='text-align:right; font-weight:bold; color:#555;'>🔍 ابحث عن اسمك في القائمة:</p>", unsafe_allow_html=True)
    selected_name = st.selectbox("", options=["-- اختر من هنا أو اكتب اسمك للبحث --"] + names_list, label_visibility="collapsed")

    if selected_name != "-- اختر من هنا أو اكتب اسمك للبحث --":
        col1, col2 = st.columns(2)
        with col1:
            if st.button("✅ تأكيد الحضور"):
                res = load_results()
                new_row = pd.DataFrame({'الاسم': [selected_name], 'الحالة': ['حاضر'], 'الوقت': [datetime.now().strftime("%I:%M %p")]})
                pd.concat([res[res['الاسم'] != selected_name], new_row], ignore_index=True).to_csv(CSV_RESULTS, index=False, encoding='utf-8-sig')
                st.success("تم تأكيد حضورك")
                st.rerun()
        with col2:
            if st.button("❌ تقديم اعتذار"):
                res = load_results()
                new_row = pd.DataFrame({'الاسم': [selected_name], 'الحالة': ['معتذر'], 'الوقت': [datetime.now().strftime("%I:%M %p")]})
                pd.concat([res[res['الاسم'] != selected_name], new_row], ignore_index=True).to_csv(CSV_RESULTS, index=False, encoding='utf-8-sig')
                st.warning("تم تسجيل اعتذارك")
                st.rerun()

st.divider()

# --- 6. إحصائيات الفرز العام (إعادة العدادات المفقودة) ---
df_results = load_results()
total_all = len(names_list)
total_done = len(df_results)
total_present = len(df_results[df_results['الحالة'] == 'حاضر'])
total_absent = len(df_results[df_results['الحالة'] == 'معتذر'])

st.markdown("<h3 style='color:#D4AF37; text-align:center;'>📊 إحصائيات الفرز العام</h3>", unsafe_allow_html=True)

# الصف الأول: الإجماليات
c1, c2 = st.columns(2)
with c1: st.metric("إجمالي القائمة", total_all)
with c2: st.metric("إجمالي المتفاعلين", total_done)

# الصف الثاني: التفاصيل (التي كانت مختفية)
c3, c4 = st.columns(2)
with c3: st.metric("✅ عدد الحاضرين", total_present)
with c4: st.metric("❌ عدد المعتذرين", total_absent)

# --- 7. لوحة التحكم ---
with st.expander("⚙️ لوحة تحكم المشرف"):
    admin_pass = st.text_input("كلمة المرور:", type="password")
    if admin_pass == "1234":
        tab1, tab2, tab3 = st.tabs(["➕ إضافة", "🗑️ حذف", "🧹 تصفير"])
        with tab1:
            new_p = st.text_input("أدخل الاسم الجديد:", key=f"ins_{st.session_state.input_key}")
            if st.button("حفظ الاسم"):
                if new_p:
                    clean_n = new_p.strip()
                    if clean_n in st.session_state.names:
                        st.error("⚠️ الاسم موجود مسبقاً!")
                    else:
                        st.session_state.names.append(clean_n)
                        st.session_state.names = sorted(st.session_state.names)
                        save_names(st.session_state.names)
                        st.session_state.input_key += 1
                        st.success("✅ تم الحفظ بنجاح")
                        st.rerun()
        with tab2:
            to_del = st.selectbox("اختر اسماً لحذفه:", options=["-- اختر --"] + st.session_state.names)
            if st.button("تأكيد الحذف"):
                if to_del != "-- اختر --":
                    st.session_state.names.remove(to_del)
                    save_names(st.session_state.names)
                    st.rerun()
        with tab3:
            if st.button("تصفير كشف المناسبة"):
                if os.path.exists(CSV_RESULTS): os.remove(CSV_RESULTS)
                st.rerun()

st.markdown("<p style='text-align:center; color:#888; font-size:0.8em; margin-top:30px;'>تصميم وبرمجة: أبو فيصل للعقارات 2026</p>", unsafe_allow_html=True)import streamlit as st
import pandas as pd
from datetime import datetime
import os

# --- 1. إعدادات الصفحة والشعار (متوافق مع الجوال) ---
st.set_page_config(
    page_title="مناسبات آل علي", 
    layout="centered", 
    page_icon="logo.png"
)

# --- 2. التنسيق الملكي (Mobile First - مع تحويل الشعار لدائري) ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Amiri&family=Tajawal:wght@400;700&display=swap');
    
    /* إخفاء شعار Streamlit والقوائم الافتراضية لظهور احترافي */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}

    /* خلفية مريحة للعين */
    .stApp { background-color: #F5F5DC; }
    
    /* البرواز الملكي المتجاوب */
    .main .block-container {
        border: 2px solid #D4AF37;
        padding: 20px !important;
        border-radius: 15px;
        background-color: #ffffff;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
        margin: 10px auto;
        max-width: 95% !important;
    }

    .bismillah { font-family: 'Amiri', serif; font-size: 2em; color: #1a1a1a; text-align: center; margin-bottom: 5px; }
    
    /* --- تنسيق الشعار الدائري الملكي في المنتصف --- */
    .logo-frame {
        display: flex;
        justify-content: center; /* التوسط المطلق */
        margin-top: 10px;
        margin-bottom: 20px;
    }
    .community-logo {
        width: 150px !important; /* حجم متوازن ومناسب للجوال */
        height: 150px !important;
        border-radius: 50%; /* تحويل المربع لدائرة كاملة */
        border: 4px solid #D4AF37; /* إطار ذهبي فخم حول الدائرة */
        object-fit: cover; /* لضمان عدم تمدد الصورة داخل الدائرة */
        box-shadow: 0 5px 15px rgba(0,0,0,0.2); /* ظل لإعطاء عمق */
    }

    .main-title { 
        color: #D4AF37; 
        text-align: center; 
        font-size: 1.4em !important; 
        font-family: 'Tajawal', sans-serif;
        font-weight: bold;
        margin-bottom: 25px;
        line-height: 1.4;
    }
    
    /* تنسيق العدادات الإحصائية للجوال */
    [data-testid="stMetric"] {
        background-color: #FFFDF5; 
        border: 1px solid #D4AF37;
        padding: 8px !important;
        border-radius: 8px;
        text-align: center;
    }
    
    [data-testid="stMetricValue"] { color: #1a1a1a !important; font-size: 1.25em !important; font-weight: bold !important; }
    [data-testid="stMetricLabel"] { color: #444 !important; font-size: 0.8em !important; }

    /* أزرار الحضور - ارتفاع مناسب للإبهام على الجوال */
    .stButton>button { 
        border-radius: 10px; border: 1.5px solid #D4AF37; 
        background-color: #1a1a1a; color: #D4AF37; 
        font-weight: bold; width: 100%; height: 3.5em;
        font-size: 0.9em;
    }
    
    /* رسالة النجاح والتحذير مصغرة للجوال */
    .stAlert { padding: 5px !important; font-size: 0.85em !important; }
    </style>
    """, unsafe_allow_html=True)

# --- 3. وظائف معالجة البيانات ---
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

# تهيئة الذاكرة للمفتاح الديناميكي
if 'input_key' not in st.session_state:
    st.session_state.input_key = 0

# --- 4. واجهة التطبيق الرئيسية ---
st.markdown("<div class='bismillah'>بِسْمِ اللهِ الرَّحْمٰنِ الرَّحِيْمِ</div>", unsafe_allow_html=True)

# عرض الشعار الدائري المحاط بالإطار الذهبي في المنتصف
if os.path.exists("logo.png"):
    st.markdown(f"""
    <div class="logo-frame">
        <img src="app/static/logo.png" class="community-logo">
    </div>
    """, unsafe_allow_html=True)
else:
    # خيار بديل في حال لم يرفع الملف بعد
    st.markdown("<h1 style='text-align:center;'>⚜️</h1>", unsafe_allow_html=True)

# العنوان بالكليشة المطلوبة
st.markdown("<div class='main-title'>مناسبات جماعة آل علي بالرياض</div>", unsafe_allow_html=True)

# تحميل الأسماء في الذاكرة لتكون القائمة دائماً محدثة
if 'names' not in st.session_state:
    st.session_state.names = load_names()

names_list = st.session_state.names

if names_list:
    selected_name = st.selectbox("🔍 ابحث عن اسمك في القائمة:", options=["-- اختر من هنا أو اكتب اسمك للبحث --"] + names_list, label_visibility="collapsed")

    if selected_name != "-- اختر من هنا أو اكتب اسمك للبحث --":
        col1, col2 = st.columns(2)
        with col1:
            if st.button("✅ تأكيد الحضور"):
                res = load_results()
                # إضافة تسجيل الحضور مع استبعاد الاعتذار السابق إن وجد
                new_row = pd.DataFrame({'الاسم': [selected_name], 'الحالة': ['حاضر'], 'الوقت': [datetime.now().strftime("%I:%M %p")]})
                pd.concat([res[res['الاسم'] != selected_name], new_row], ignore_index=True).to_csv(CSV_RESULTS, index=False, encoding='utf-8-sig')
                st.success(f"تم التأكيد يا {selected_name}")
                st.rerun()
        with col2:
            if st.button("❌ تقديم اعتذار"):
                res = load_results()
                # إضافة تسجيل الاعتذار مع استبعاد الحضور السابق إن وجد
                new_row = pd.DataFrame({'الاسم': [selected_name], 'الحالة': ['معتذر'], 'الوقت': [datetime.now().strftime("%I:%M %p")]})
                pd.concat([res[res['الاسم'] != selected_name], new_row], ignore_index=True).to_csv(CSV_RESULTS, index=False, encoding='utf-8-sig')
                st.warning("تم تسجيل اعتذارك بنجاح")
                st.rerun()

# --- 5. قسم النتائج والإحصائيات للمشرف ---
st.divider()
df_final = load_results()

if not df_final.empty:
    st.markdown("<h3 style='color:#D4AF37; text-align:center;'>📊 إحصائيات المناسبة</h3>", unsafe_allow_html=True)
    # عدادات الحضور (تظهر في صف واحد على الجوال)
    c1, c2, c3 = st.columns(3)
    with c1: st.metric("المسجلين", len(df_final))
    with c2: st.metric("✅ حاضر", len(df_final[df_final['الحالة'] == 'حاضر']))
    with c3: st.metric("❌ معتذر", len(df_final[df_final['الحالة'] == 'معتذر']))

    # استعراض الكشف
    with st.expander("👁️ عرض كشف الأسماء التفصيلي"):
        st.dataframe(df_final, use_container_width=True, hide_index=True)
        csv_data = df_final.to_csv(index=False).encode('utf-8-sig')
        st.download_button("📥 تحميل التقرير النهائي للمشرف", data=csv_data, file_name="report.csv")

# --- 6. مركز تحكم الإدارة (الإصدار العبقري للتفريغ) ---
st.write("---")
with st.expander("⚙️ إعدادات الإدارة المتطورة"):
    admin_pass = st.text_input("أدخل الرقم السري للإدارة:", type="password")
    
    if admin_pass == "1234":
        tab1, tab2, tab3 = st.tabs(["➕ إضافة اسم", "🗑️ حذف اسم", "🧹 تصفير"])
        
        with tab1:
            # هنا نستخدم المفتاح المتغير input_key لضمان التفريغ القاطع
            new_person = st.text_input("الاسم الجديد بالكامل:", key=f"ins_{st.session_state.input_key}")
            
            if st.button("حفظ الاسم الجديد"):
                # تنظيف النص من المسافات الزائدة
                clean_name = new_person.strip()
                if clean_name and clean_name not in st.session_state.names:
                    # 1. تحديث القائمة في الذاكرة أولاً
                    st.session_state.names.append(clean_name)
                    st.session_state.names = sorted(st.session_state.names)
                    
                    # 2. الحفظ الفعلي في ملف الإكسل
                    save_names(st.session_state.names)
                    
                    # 3. تحديث مفتاح الحقل للتفريغ الديناميكي
                    st.session_state.input_key += 1
                    
                    st.success(f"تمت إضافة {clean_name}")
                    st.rerun()
                elif clean_name in st.session_state.names:
                    st.warning("الاسم موجود مسبقاً!")
        
        with tab2:
            name_to_del = st.selectbox("حذف اسم نهائياً من القائمة الأساسية:", options=["-- اختر --"] + st.session_state.names)
            if st.button("تأكيد حذف الاسم"):
                if name_to_del != "-- اختر --":
                    st.session_state.names.remove(name_to_del)
                    save_names(st.session_state.names)
                    st.error(f"تم حذف {name_to_del} من القائمة")
                    st.rerun()
                    
        with tab3:
            if st.button("🗑️ تصفير قائمة الحضور للمناسبة القادمة"):
                if os.path.exists(CSV_RESULTS):
                    os.remove(CSV_RESULTS)
                    st.success("تم تصفير البيانات بنجاح!")
                    st.rerun()
    elif admin_pass != "":
        st.error("الرقم السري غير صحيح!")

st.markdown("<p style='text-align:center; color:#555; font-size:0.7em; margin-top:30px;'>تصميم وبرمجة: أبو فيصل للعقارات 2026</p>", unsafe_allow_html=True)