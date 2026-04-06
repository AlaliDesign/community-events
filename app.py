import streamlit as st
import pandas as pd
from datetime import datetime
import os
import json
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

# --- 2. وظائف إدارة البيانات ---
if 'has_voted' not in st.session_state:
    st.session_state.has_voted = False

def load_data():
    # تحميل النتائج
    results = pd.DataFrame(columns=['الاسم', 'الحالة', 'الوقت'])
    if os.path.exists('results.csv'):
        try: results = pd.read_csv('results.csv', encoding='utf-8-sig')
        except: pass
    
    # تحميل أو إنشاء الإعدادات (الكليشة)
    default_settings = {
        "h_date": "لم يحدد", 
        "time": "لم يحدد", 
        "location": "الرياض", 
        "map_url": ""
    }
    
    if os.path.exists('settings.json'):
        try:
            with open('settings.json', 'r', encoding='utf-8') as f:
                content = json.load(f)
                default_settings.update(content)
        except: pass
    else:
        # إنشاء ملف إعدادات افتراضي إذا لم يكن موجوداً
        with open('settings.json', 'w', encoding='utf-8') as f:
            json.dump(default_settings, f, ensure_ascii=False)
            
    return results, default_settings

df_results, settings = load_data()

# --- 3. التنسيق الجمالي (CSS) ---
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
    .stButton>button { border-radius: 12px; font-weight: bold; width: 100%; height: 3em; border: 2px solid #D4AF37; background-color: #1a1a1a; color: #D4AF37; }
    .stButton>button:hover { background-color: #D4AF37; color: white; }
    /* تنسيق الكليشة */
    .klisha-box {
        background-color: #FFFDF5; border: 2px double #D4AF37; 
        border-radius: 15px; padding: 20px; text-align: center; 
        margin-bottom: 25px; box-shadow: inset 0 0 10px rgba(212,175,55,0.1);
    }
    </style>
    """, unsafe_allow_html=True)

# --- 4. واجهة العرض (الكليشة والعدادات) ---
col_logo = st.columns([1, 2, 1])
with col_logo[1]:
    if os.path.exists(icon_path):
        st.image(icon_path, use_container_width=True)
    else:
        st.markdown("<h1 style='text-align:center;'>🌴⚔️</h1>", unsafe_allow_html=True)

st.markdown("<h2 style='text-align:center; color:#1a1a1a; margin-top:0;'>مناسبات جماعة آل علي</h2>", unsafe_allow_html=True)
st.markdown("<p style='text-align:center; color:#D4AF37; font-weight:bold; font-size:1.2em;'>الرياض</p>", unsafe_allow_html=True)

# العدادات
h_count = len(df_results[df_results['الحالة'] == 'حاضر'])
m_count = len(df_results[df_results['الحالة'] == 'معتذر'])

st.markdown(f"""
    <div style="display: flex; justify-content: space-around; margin: 20px 0; gap: 10px; direction: rtl;">
        <div style="background: linear-gradient(135deg, #28a745, #218838); color: white; padding: 15px; border-radius: 15px; flex: 1; text-align: center; border: 1px solid #1e7e34;">
            <small>الحاضرين</small><br><b style="font-size: 1.5em;">{h_count}</b>
        </div>
        <div style="background: linear-gradient(135deg, #dc3545, #c82333); color: white; padding: 15px; border-radius: 15px; flex: 1; text-align: center; border: 1px solid #bd2130;">
            <small>المعتذرين</small><br><b style="font-size: 1.5em;">{m_count}</b>
        </div>
    </div>
""", unsafe_allow_html=True)

# عرض الكليشة (بيانات المناسبة)
st.markdown(f"""
    <div class="klisha-box">
        <p style="font-size:1.3em; margin:8px; color:#1a1a1a;">📅 <b>التاريخ:</b> {settings['h_date']}</p>
        <p style="font-size:1.2em; margin:8px; color:#1a1a1a;">⏰ <b>الوقت:</b> {settings['time']}</p>
        <p style="font-size:1.2em; margin:8px; color:#1a1a1a;">📍 <b>الموقع:</b> {settings['location']}</p>
    </div>
""", unsafe_allow_html=True)

if settings['map_url'] and settings['map_url'].startswith("http"):
    st.link_button("📍 موقع المناسبة (خرائط جوجل)", settings['map_url'], use_container_width=True)

# --- 5. منطقة تسجيل الحضور ---
st.divider()

if st.session_state.has_voted:
    st.success("✅ بيّض الله وجهك، تم استلام تسجيلك بنجاح.")
    st.info("نظام الحماية: لقد سجلت مسبقاً من هذا الجهاز.")
else:
    st.subheader("📝 سجل حضورك")
    u_name = st.text_input("👤 أدخل اسمك الثلاثي/الرباعي:", placeholder="اكتب اسمك هنا...")

    if u_name:
        name_clean = u_name.strip()
        if name_clean in df_results['الاسم'].values:
            st.warning(f"⚠️ الاسم '{name_clean}' مسجل مسبقاً في القائمة.")
        else:
            col1, col2 = st.columns(2)
            with col1:
                if st.button("✅ تأكيد الحضور"):
                    new_entry = pd.DataFrame({'الاسم': [name_clean], 'الحالة': ['حاضر'], 'الوقت': [datetime.now().strftime("%I:%M %p")]})
                    pd.concat([df_results, new_entry], ignore_index=True).to_csv('results.csv', index=False, encoding='utf-8-sig')
                    st.session_state.has_voted = True
                    st.rerun()
            with col2:
                if st.button("❌ اعتذار"):
                    new_entry = pd.DataFrame({'الاسم': [name_clean], 'الحالة': ['معتذر'], 'الوقت': [datetime.now().strftime("%I:%M %p")]})
                    pd.concat([df_results, new_entry], ignore_index=True).to_csv('results.csv', index=False, encoding='utf-8-sig')
                    st.session_state.has_voted = True
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

# --- 7. لوحة الإدارة ---
st.write("")
with st.expander("⚙️ إعدادات الإدارة"):
    admin_pw = st.text_input("كلمة المرور", type="password", key="admin_pw")
    if admin_pw == "1234":
        st.markdown("#### 📅 تحديث الكليشة (بيانات المناسبة)")
        new_h = st.text_input("التاريخ الهجري:", value=settings['h_date'])
        new_t = st.text_input("الوقت:", value=settings['time'])
        new_l = st.text_input("الموقع:", value=settings['location'])
        new_m = st.text_input("رابط الخرائط:", value=settings['map_url'])
        
        if st.button("💾 حفظ البيانات"):
            with open('settings.json', 'w', encoding='utf-8') as f:
                json.dump({"h_date":new_h, "time":new_t, "location":new_l, "map_url":new_m}, f, ensure_ascii=False)
            st.success("✅ تم تحديث الكليشة بنجاح!")
            st.rerun()

        st.divider()
        if st.button("🧹 تصفير السجل بالكامل"):
            if os.path.exists('results.csv'): os.remove('results.csv')
            st.session_state.has_voted = False
            st.rerun()

st.markdown("<p style='text-align:center; color:#aaa; font-size:0.8em; margin-top:30px;'>تصميم محمد العلالي</p>", unsafe_allow_html=True)