import streamlit as st
import pandas as pd
from datetime import datetime
import os

# --- 1. إعدادات الصفحة والشعار (متناسب مع الجوال) ---
st.set_page_config(
    page_title="مناسبات آل علي", 
    layout="centered", 
    page_icon="logo_clean.png" # اعتماد الشعار الجديد والمفرغ
)

# --- 2. التنسيق (Mobile First - مع إزالة الخلفية البيضاء للشعار) ---
st.markdown("""
    <style>
    .main { background-color: #080808; }
    
    /* تنسيق الشعار الملكي الكبير والمتوسط (برمجياً) */
    .logo-frame {
        display: flex;
        justify-content: center; /* التوسط المطلق */
        margin-top: 20px;
        margin-bottom: 5px;
        filter: drop-shadow(2px 2px 3px rgba(0,0,0,0.3)); /* ظل لتوضيح الشعار المفرغ */
    }
    .コミュニティ-logo {
        width: 170px !important; /* حجم كبير وواضح */
        background-color: transparent !important; /* إزالة أي خلفية بيضاء */
        mix-blend-mode: multiply; /* دمج الألوان الغامقة للشعار مع الخلفية */
    }

    /* العنوان الرئيسي المحدث */
    .community-title { 
        color: #D4AF37; 
        text-align: center; 
        font-size: 1.5em !important; 
        font-weight: bold;
        margin-bottom: 25px;
        line-height: 1.4;
    }
    
    /* تنسيق العدادات (Mobile Optimized) */
    [data-testid="stMetric"] {
        background-color: #fdfdfd; 
        border: 1px solid #D4AF37;
        padding: 8px !important;
        border-radius: 8px;
        text-align: center;
    }
    
    [data-testid="stMetricValue"] { color: #1a1a1a !important; font-size: 1.25em !important; font-weight: bold !important; }
    [data-testid="stMetricLabel"] { color: #444 !important; font-size: 0.8em !important; }

    /* أزرار الحضور - ارتفاع مناسب للإبهام */
    .stButton>button { 
        border-radius: 10px; border: 1.5px solid #D4AF37; 
        background-color: #1a1a1a; color: #D4AF37; 
        font-weight: bold; width: 100%; height: 3.5em;
        font-size: 0.9em;
    }
    
    /* رسالة النجاح والتحذير مصغرة לגوال */
    .stAlert { padding: 5px !important; font-size: 0.85em !important; }
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

# تهيئة الذاكرة للمفتاح الديناميكي
if 'input_key' not in st.session_state:
    st.session_state.input_key = 0

# --- 4. واجهة التطبيق الرئيسية ---

# عرض الشعار الجديد والمفرغ (يجب أن ترفعه باسم logo_clean.png)
if os.path.exists("logo_clean.png"):
    st.markdown(f"""
    <div class="logo-frame">
        <img src="app/static/logo_clean.png" class="community-logo">
    </div>
    """, unsafe_allow_html=True)
else:
    # خيار بديل في حال لم يرفع الملف بعد
    st.markdown("<h1 style='text-align:center;'>⚜️</h1>", unsafe_allow_html=True)

# العنوان بالكليشة المطلوبة
st.markdown("<div class='community-title'>مناسبات جماعة آل علي بالرياض</div>", unsafe_allow_html=True)

# تحميل الأسماء في الذاكرة لتكون القائمة دائماً محدثة
if 'names' not in st.session_state:
    st.session_state.names = load_names()

names_list = st.session_state.names

if names_list:
    selected_name = st.selectbox("🔍 ابحث عن اسمك لتسجيل الحضور:", options=["-- اختر من القائمة --"] + names_list)

    if selected_name != "-- اختر من القائمة --":
        col1, col2 = st.columns(2)
        with col1:
            if st.button("✅ تأكيد الحضور"):
                res = load_results()
                # إضافة تسجيل الحضور مع استبعاد الاعتذار السابق إن وجد
                new_row = pd.DataFrame({'الاسم': [selected_name], 'الحالة': ['حاضر'], 'الوقت': [datetime.now().strftime("%I:%M %p")]})
                pd.concat([res[res['الاسم'] != selected_name], new_row], ignore_index=True).to_csv(CSV_RESULTS, index=False, encoding='utf-8-sig')
                st.success(f"تم التأكيد")
                st.rerun()
        with col2:
            if st.button("❌ اعتذار"):
                res = load_results()
                # إضافة تسجيل الاعتذار مع استبعاد الحضور السابق إن وجد
                new_row = pd.DataFrame({'الاسم': [selected_name], 'الحالة': ['معتذر'], 'الوقت': [datetime.now().strftime("%I:%M %p")]})
                pd.concat([res[res['الاسم'] != selected_name], new_row], ignore_index=True).to_csv(CSV_RESULTS, index=False, encoding='utf-8-sig')
                st.warning("تم التسجيل")
                st.rerun()

# --- 5. قسم النتائج والإحصائيات (Mobile Friendly) ---
st.divider()
df_final = load_results()

if not df_final.empty:
    st.markdown("<h3 style='color:#D4AF37; text-align:center;'>📊 ملخص المناسبة</h3>", unsafe_allow_html=True)
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
                    st.error(f"تم حذف {name_to_del}")
                    st.rerun()
                    
        with tab3:
            if st.button("🗑️ تصفير قائمة الحضور للمناسبة القادمة"):
                if os.path.exists(CSV_RESULTS):
                    os.remove(CSV_RESULTS)
                    st.success("تم التصفير")
                    st.rerun()
    elif admin_pass != "":
        st.error("الرقم السري غير صحيح!")

st.markdown("<p style='text-align:center; color:#555; font-size:0.7em; margin-top:30px;'>تصميم وبرمجة: أبو فيصل للعقارات 2026</p>", unsafe_allow_html=True)