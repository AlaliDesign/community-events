import streamlit as st
import pandas as pd
from datetime import datetime
import os
from PIL import Image

# --- 1. إعدادات الصفحة ---
icon_path = 'logo.png'
try:
    if os.path.exists(icon_path):
        img = Image.open(icon_path)
        st.set_page_config(page_title="مناسبات جماعة آل علي", page_icon=img, layout="centered")
    else:
        st.set_page_config(page_title="مناسبات جماعة آل علي", page_icon="⚔️", layout="centered")
except:
    st.set_page_config(page_title="مناسبات جماعة آل علي", page_icon="⚔️", layout="centered")

# --- 2. وظائف إدارة البيانات والبصمة الرقمية ---
# استخدام خاصية session_state كبصمة مؤقتة للجلسة
if 'has_voted' not in st.session_state:
    st.session_state.has_voted = False

def load_results():
    if os.path.exists('results.csv'):
        try: return pd.read_csv('results.csv', encoding='utf-8-sig')
        except: return pd.DataFrame(columns=['الاسم', 'الحالة', 'الوقت'])
    return pd.DataFrame(columns=['الاسم', 'الحالة', 'الوقت'])

df_results = load_results()

# --- 3. التنسيق الجمالي ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700&display=swap');
    html, body, [class*="css"] { font-family: 'Cairo', sans-serif; text-align: right; direction: rtl; }
    #MainMenu, footer, header {visibility: hidden;}
    .stApp { background-color: #FDFCF0; }
    .main .block-container {
        border: 2px solid #D4AF37; padding: 20px !important; 
        border-radius: 20px; background-color: #ffffff;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
    }
    .stButton>button { border-radius: 12px; font-weight: bold; width: 100%; height: 3em; }
    </style>
    """, unsafe_allow_html=True)

# --- 4. واجهة العرض الرئيسية ---
st.markdown("<h2 style='text-align:center;'>مناسبات جماعة آل علي</h2>", unsafe_allow_html=True)

# عدادات الحضور
h_count = len(df_results[df_results['الحالة'] == 'حاضر'])
m_count = len(df_results[df_results['الحالة'] == 'معتذر'])

st.markdown(f"""
    <div style="display: flex; justify-content: space-around; margin: 20px 0; gap: 10px;">
        <div style="background: #28a745; color: white; padding: 15px; border-radius: 15px; flex: 1; text-align: center;">
            <small>الحاضرين</small><br><b style="font-size: 1.5em;">{h_count}</b>
        </div>
        <div style="background: #dc3545; color: white; padding: 15px; border-radius: 15px; flex: 1; text-align: center;">
            <small>المعتذرين</small><br><b style="font-size: 1.5em;">{m_count}</b>
        </div>
    </div>
""", unsafe_allow_html=True)

# --- 5. منطقة تسجيل الحضور (الحماية من التلاعب) ---
st.divider()

# القفل البرمجي: إذا سجل الشخص، تختفي الحقول
if st.session_state.has_voted:
    st.success("✅ بيّض الله وجهك، تم استلام تسجيلك بنجاح.")
    st.info("نظام الحماية: تم تسجيل دخولك مسبقاً من هذا الجهاز.")
else:
    st.subheader("📝 سجل حضورك")
    u_name = st.text_input("👤 أدخل اسمك الثلاثي/الرباعي:", placeholder="اكتب اسمك هنا...")

    if u_name:
        name_clean = u_name.strip()
        
        # 1. منع تكرار نفس الاسم في القاعدة
        if name_clean in df_results['الاسم'].values:
            st.warning(f"⚠️ الاسم '{name_clean}' مسجل مسبقاً في القائمة.")
        else:
            col1, col2 = st.columns(2)
            with col1:
                if st.button("✅ تأكيد الحضور"):
                    new_entry = pd.DataFrame({'الاسم': [name_clean], 'الحالة': ['حاضر'], 'الوقت': [datetime.now().strftime("%I:%M %p")]})
                    pd.concat([df_results, new_entry], ignore_index=True).to_csv('results.csv', index=False, encoding='utf-8-sig')
                    st.session_state.has_voted = True # قفل الجهاز فوراً
                    st.rerun()
            with col2:
                if st.button("❌ اعتذار"):
                    new_entry = pd.DataFrame({'الاسم': [name_clean], 'الحالة': ['معتذر'], 'الوقت': [datetime.now().strftime("%I:%M %p")]})
                    pd.concat([df_results, new_entry], ignore_index=True).to_csv('results.csv', index=False, encoding='utf-8-sig')
                    st.session_state.has_voted = True # قفل الجهاز فوراً
                    st.rerun()

# --- 6. عرض القائمة للجميع ---
if not df_results.empty:
    st.divider()
    st.markdown("### 📋 قائمة المسجلين")
    
    def style_row(val):
        return f'background-color: {"#ccffcc" if val == "حاضر" else "#ffcccc"}'

    try:
        styled_df = df_results[['الاسم', 'الحالة', 'الوقت']].style.map(style_row, subset=['الحالة'])
    except:
        styled_df = df_results[['الاسم', 'الحالة', 'الوقت']].style.applymap(style_row, subset=['الحالة'])

    st.dataframe(styled_df, use_container_width=True, hide_index=True)

# --- 7. لوحة التحكم (للمنظم) ---
with st.expander("⚙️ إعدادات الإدارة"):
    if st.text_input("كلمة مرور الإدارة", type="password") == "1234":
        if st.button("🧹 تصفير السجل (بدء مناسبة جديدة)"):
            if os.path.exists('results.csv'): os.remove('results.csv')
            st.session_state.has_voted = False
            st.rerun()

st.markdown("<p style='text-align:center; color:#aaa; font-size:0.8em; margin-top:30px;'>تصميم محمد العلالي - صقر العقارات 2026</p>", unsafe_allow_html=True)