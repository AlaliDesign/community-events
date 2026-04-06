import streamlit as st
import pandas as pd
from datetime import datetime
import os
from PIL import Image

# --- 1. إعدادات الصفحة واللوجو ---
icon_path = 'logo.png'
# وضعنا إعداد الصفحة في أول سطر لتجنب أي أخطاء
try:
    if os.path.exists(icon_path):
        img = Image.open(icon_path)
        st.set_page_config(page_title="مناسبات جماعة آل علي", page_icon=img, layout="centered")
    else:
        st.set_page_config(page_title="مناسبات جماعة آل علي", page_icon="⚔️", layout="centered")
except:
    st.set_page_config(page_title="مناسبات جماعة آل علي", page_icon="⚔️", layout="centered")

# --- 2. وظائف إدارة البيانات ---
def load_data():
    # تحميل النتائج (سجل الحضور)
    results = pd.DataFrame(columns=['الاسم', 'الحالة', 'الوقت'])
    if os.path.exists('results.csv'):
        try: 
            results = pd.read_csv('results.csv', encoding='utf-8-sig')
        except: pass
        
    # تحميل إعدادات المناسبة
    settings = {"h_date": "1447-10-18", "time": "الحضور من 4 العصر", "location": "الرياض", "map_url": ""}
    if os.path.exists('settings.json'):
        try:
            with open('settings.json', 'r', encoding='utf-8') as f:
                import json
                settings.update(json.load(f))
        except: pass
    return results, settings

df_results, settings = load_data()

# --- 3. التنسيق الجمالي (CSS) ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700&display=swap');
    html, body, [class*="css"] { font-family: 'Cairo', sans-serif; text-align: right; }
    #MainMenu, footer, header {visibility: hidden;}
    .stApp { background-color: #FDFCF0; }
    .main .block-container {
        border: 2px solid #D4AF37; padding: 20px !important; 
        border-radius: 20px; background-color: #ffffff;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
    }
    .stButton>button { 
        border-radius: 12px; border: 2px solid #D4AF37; 
        background-color: #1a1a1a; color: #D4AF37; font-weight: bold; width: 100%;
        height: 3em; transition: 0.3s;
    }
    .stButton>button:hover { background-color: #D4AF37; color: white; }
    </style>
    """, unsafe_allow_html=True)

# --- 4. واجهة العرض الرئيسية ---
col_logo = st.columns([1, 2, 1])
with col_logo[1]:
    if os.path.exists(icon_path):
        st.image(icon_path, use_container_width=True)
    else:
        st.markdown("<h1 style='text-align:center;'>🌴⚔️</h1>", unsafe_allow_html=True)

st.markdown("<h2 style='text-align:center; color:#1a1a1a; margin-bottom:0;'>مناسبات جماعة آل علي</h2>", unsafe_allow_html=True)
st.markdown("<p style='text-align:center; color:#D4AF37; font-weight:bold;'>الرياض</p>", unsafe_allow_html=True)

# العدادات العلوية
h_count = len(df_results[df_results['الحالة'] == 'حاضر'])
m_count = len(df_results[df_results['الحالة'] == 'معتذر'])

st.markdown(f"""
    <div style="display: flex; justify-content: space-between; gap: 10px; margin: 20px 0; direction: rtl;">
        <div style="background: linear-gradient(135deg, #28a745, #218838); color: white; padding: 15px; border-radius: 15px; flex: 1; text-align: center;">
            <small>الحاضرين</small><br><b style="font-size: 1.5em;">{h_count}</b>
        </div>
        <div style="background: linear-gradient(135deg, #dc3545, #c82333); color: white; padding: 15px; border-radius: 15px; flex: 1; text-align: center;">
            <small>المعتذرين</small><br><b style="font-size: 1.5em;">{m_count}</b>
        </div>
    </div>
""", unsafe_allow_html=True)

# كليشة بيانات المناسبة
st.markdown(f"""
    <div style="background-color: #FFFDF5; border: 1px double #D4AF37; border-radius: 15px; padding: 20px; text-align: center; margin-bottom: 20px; direction: rtl;">
        <p style="font-size:1.2em; margin:5px;">📅 <b>التاريخ:</b> {settings['h_date']}</p>
        <p style="font-size:1.1em; margin:5px;">⏰ <b>الوقت:</b> {settings['time']}</p>
        <p style="font-size:1.1em; margin:5px;">📍 <b>الموقع:</b> {settings['location']}</p>
    </div>
""", unsafe_allow_html=True)

if settings['map_url']:
    st.link_button("📍 موقع المناسبة (خرائط جوجل)", settings['map_url'], use_container_width=True)

# --- 5. منطقة تسجيل الحضور (فكرة أبا فيصل: القاعدة الفاضية) ---
st.divider()
st.subheader("📝 سجل حضورك")

name_input = st.text_input("👤 اكتب اسمك الكريم للتسجيل:", placeholder="مثال: فلان بن فلان آل علي")

if name_input:
    name_clean = name_input.strip()
    
    # التحقق من عدم التكرار
    check_exist = df_results[df_results['الاسم'] == name_clean]
    
    if not check_exist.empty:
        st.warning(f"⚠️ الاسم '{name_clean}' مسجل مسبقاً كـ ({check_exist.iloc[0]['الحالة']})")
    else:
        st.info(f"مرحباً بك يا {name_clean}، يرجى اختيار الحالة:")
        c1, col_gap, c2 = st.columns([2, 0.5, 2])
        with c1:
            if st.button("✅ تأكيد الحضور"):
                new_row = pd.DataFrame({'الاسم': [name_clean], 'الحالة': ['حاضر'], 'الوقت': [datetime.now().strftime("%I:%M %p")]})
                df_updated = pd.concat([df_results, new_row], ignore_index=True)
                df_updated.to_csv('results.csv', index=False, encoding='utf-8-sig')
                st.success("تم تسجيل حضورك بنجاح")
                import time
                time.sleep(1)
                st.rerun()
        with c2:
            if st.button("❌ اعتذار"):
                new_row = pd.DataFrame({'الاسم': [name_clean], 'الحالة': ['معتذر'], 'الوقت': [datetime.now().strftime("%I:%M %p")]})
                df_updated = pd.concat([df_results, new_row], ignore_index=True)
                df_updated.to_csv('results.csv', index=False, encoding='utf-8-sig')
                st.warning("تم تسجيل اعتذارك")
                import time
                time.sleep(1)
                st.rerun()

# --- 6. عرض القائمة للجميع (حل مشكلة AttributeError) ---
if not df_results.empty:
    st.divider()
    st.markdown("### 📋 قائمة المسجلين")
    
    def color_status(val):
        color = '#ccffcc' if val == 'حاضر' else '#ffcccc'
        return f'background-color: {color}'

    # معالجة الخطأ البرمجي حسب نسخة Pandas
    try:
        styled_df = df_results[['الاسم', 'الحالة', 'الوقت']].style.map(color_status, subset=['الحالة'])
    except AttributeError:
        styled_df = df_results[['الاسم', 'الحالة', 'الوقت']].style.applymap(color_status, subset=['الحالة'])

    st.dataframe(styled_df, use_container_width=True, hide_index=True)

# --- 7. لوحة التحكم (مخفية للمنظم) ---
with st.expander("⚙️ إعدادات"):
    pw = st.text_input("كلمة المرور", type="password")
    if pw == "1234":
        if st.button("🧹 تصفير السجل بالكامل"):
            if os.path.exists('results.csv'): os.remove('results.csv')
            st.rerun()
        
        st.markdown("---")
        new_h = st.text_input("تحديث التاريخ:", value=settings['h_date'])
        new_m = st.text_input("تحديث رابط الخريطة:", value=settings['map_url'])
        if st.button("💾 حفظ الإعدادات"):
            import json
            with open('settings.json', 'w', encoding='utf-8') as f:
                json.dump({"h_date":new_h, "time":settings['time'], "location":settings['location'], "map_url":new_m}, f, ensure_ascii=False)
            st.rerun()

st.markdown("<br><p style='text-align:center; color:#aaa; font-size:0.8em;'>تصميم محمد العلالي - صقر العقارات 2026</p>", unsafe_allow_html=True)