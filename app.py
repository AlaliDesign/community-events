import streamlit as st
import pandas as pd
from datetime import datetime
import os
import json
import urllib.parse
from ummalqura.hijri_date import HijriDate
from PIL import Image

# --- 1. إعدادات الصفحة ---
icon_path = 'logo.png'
# محاولة تحميل اللوجو المرفق
if os.path.exists(icon_path):
    try:
        img = Image.open(icon_path)
        st.set_page_config(page_title="مناسبات جماعة آل علي", page_icon=img, layout="centered")
    except:
        st.set_page_config(page_title="مناسبات جماعة آل علي", page_icon="⚔️")
else:
    st.set_page_config(page_title="مناسبات جماعة آل علي", page_icon="⚔️")

# --- 2. وظائف إدارة البيانات ---
def load_data():
    names = []
    if os.path.exists('names.xlsx'):
        try:
            # قراءة العمود الأول فقط وتجاهل الهيدر إذا لزم الأمر
            df_names = pd.read_excel('names.xlsx', header=None)
            names = sorted(df_names[0].dropna().astype(str).unique().tolist())
        except: pass
    
    results = pd.DataFrame(columns=['الاسم', 'الحالة', 'الوقت'])
    if os.path.exists('results.csv'):
        try: 
            results = pd.read_csv('results.csv', encoding='utf-8-sig')
        except: pass
        
    settings = {"h_date": "1447-10-18", "time": "الحضور من 4 العصر", "location": "استراحة رانديفو", "map_url": ""}
    if os.path.exists('settings.json'):
        try:
            with open('settings.json', 'r', encoding='utf-8') as f:
                settings.update(json.load(f))
        except: pass
    return names, results, settings

# --- 3. التنسيق الجمالي (CSS) ---
st.markdown("""
    <style>
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

all_names, df_results, settings = load_data()

# --- 4. واجهة العرض الرئيسية ---
col_logo = st.columns([1, 2, 1])
with col_logo[1]:
    if os.path.exists(icon_path):
        st.image(icon_path, use_container_width=True)
    else:
        st.markdown("<h1 style='text-align:center;'>🌴⚔️</h1>", unsafe_allow_html=True)

st.markdown("<h2 style='text-align:center; color:#1a1a1a; margin-bottom:0;'>مناسبات جماعة آل علي</h2>", unsafe_allow_html=True)
st.markdown("<p style='text-align:center; color:#D4AF37; font-weight:bold;'>الرياض</p>", unsafe_allow_html=True)

# العدادات الملونة
h_count = len(df_results[df_results['الحالة'] == 'حاضر'])
m_count = len(df_results[df_results['الحالة'] == 'معتذر'])

st.markdown(f"""
    <div style="display: flex; justify-content: space-between; gap: 10px; margin: 20px 0;">
        <div style="background: linear-gradient(135deg, #28a745, #218838); color: white; padding: 15px; border-radius: 15px; flex: 1; text-align: center;">
            <small>الحاضرين</small><br><b style="font-size: 1.5em;">{h_count}</b>
        </div>
        <div style="background: linear-gradient(135deg, #dc3545, #c82333); color: white; padding: 15px; border-radius: 15px; flex: 1; text-align: center;">
            <small>المعتذرين</small><br><b style="font-size: 1.5em;">{m_count}</b>
        </div>
        <div style="background: #1a1a1a; color: #D4AF37; padding: 15px; border-radius: 15px; flex: 1; text-align: center; border: 1px solid #D4AF37;">
            <small>الإجمالي</small><br><b style="font-size: 1.5em;">{len(all_names)}</b>
        </div>
    </div>
""", unsafe_allow_html=True)

# كليشة المناسبة
st.markdown(f"""
    <div style="background-color: #FFFDF5; border: 1px double #D4AF37; border-radius: 15px; padding: 20px; text-align: center; margin-bottom: 20px;">
        <p style="font-size:1.2em; margin:5px;">📅 <b>التاريخ:</b> {settings['h_date']}</p>
        <p style="font-size:1.1em; margin:5px;">⏰ <b>الوقت:</b> {settings['time']}</p>
        <p style="font-size:1.1em; margin:5px;">📍 <b>الموقع:</b> {settings['location']}</p>
    </div>
""", unsafe_allow_html=True)

if settings['map_url']:
    st.link_button("📍 موقع المناسبة (خرائط جوجل)", settings['map_url'], use_container_width=True)

# --- 5. منطقة تسجيل الحضور ---
st.divider()
st.subheader("📝 سجل حضورك")

if not all_names:
    st.warning("⚠️ القائمة فارغة حالياً، يرجى إضافة الأسماء من لوحة التحكم.")
else:
    search = st.text_input("🔍 ابحث عن اسمك:", placeholder="اكتب اسمك للبحث...")
    filtered = [n for n in all_names if search in n] if search else all_names
    selected = st.selectbox("اختر الاسم:", options=["-- اختر اسمك --"] + filtered)

    if selected != "-- اختر اسمك --":
        c1, c2 = st.columns(2)
        with c1:
            if st.button("✅ تأكيد الحضور"):
                new_row = pd.DataFrame({'الاسم': [selected], 'الحالة': ['حاضر'], 'الوقت': [datetime.now().strftime("%I:%M %p")]})
                df_final = pd.concat([df_results[df_results['الاسم'] != selected], new_row], ignore_index=True)
                df_final.to_csv('results.csv', index=False, encoding='utf-8-sig')
                st.success("تم تسجيل حضورك بنجاح")
                st.rerun()
        with c2:
            if st.button("❌ اعتذار"):
                new_row = pd.DataFrame({'الاسم': [selected], 'الحالة': ['معتذر'], 'الوقت': [datetime.now().strftime("%I:%M %p")]})
                df_final = pd.concat([df_results[df_results['الاسم'] != selected], new_row], ignore_index=True)
                df_final.to_csv('results.csv', index=False, encoding='utf-8-sig')
                st.warning("تم تسجيل اعتذارك")
                st.rerun()

# --- 6. جدول النتائج ---
if not df_results.empty:
    st.divider()
    st.markdown("### 📋 قائمة المسجلين")
    def style_status(val):
        if val == 'معتذر': return 'background-color: #ffcccc; color: #990000; font-weight: bold;'
        return 'background-color: #ccffcc; color: #006600;'
    
    st.dataframe(df_results[['الاسم', 'الحالة', 'الوقت']].style.map(style_status, subset=['الحالة']), 
                 use_container_width=True, hide_index=True)

# --- 7. لوحة التحكم ---
st.write("")
with st.expander("⚙️ إعدادات الإدارة"):
    pw = st.text_input("كلمة المرور", type="password")
    if pw == "1234":
        st.markdown("#### 👥 إدارة القائمة")
        
        # إضافة اسم
        new_n = st.text_input("أضف اسم جديد:")
        if st.button("➕ إضافة للقائمة"):
            if new_n and new_n not in all_names:
                all_names.append(new_n)
                # حفظ في ملف أكسل مع التأكد من الصيغة الصحيحة
                pd.DataFrame(all_names).to_excel('names.xlsx', index=False, header=False, engine='openpyxl')
                st.success(f"تمت إضافة {new_n}")
                st.rerun()
            elif new_n in all_names:
                st.error("الاسم موجود مسبقاً!")

        # حذف اسم
        if all_names:
            to_del = st.selectbox("حذف اسم من القائمة:", options=["-- اختر اسم للحذف --"] + all_names)
            if st.button("🗑️ حذف الاسم المختارة"):
                if to_del != "-- اختر اسم للحذف --":
                    all_names.remove(to_del)
                    pd.DataFrame(all_names).to_excel('names.xlsx', index=False, header=False, engine='openpyxl')
                    st.error(f"تم حذف {to_del}")
                    st.rerun()

        st.divider()
        st.markdown("#### 📅 تحديث بيانات المناسبة")
        new_h = st.text_input("التاريخ الهجري:", value=settings['h_date'])
        new_t = st.text_input("الوقت:", value=settings['time'])
        new_l = st.text_input("الموقع:", value=settings['location'])
        new_m = st.text_input("رابط الخرائط:", value=settings['map_url'])
        
        if st.button("💾 حفظ الإعدادات"):
            with open('settings.json', 'w', encoding='utf-8') as f:
                json.dump({"h_date":new_h, "time":new_t, "location":new_l, "map_url":new_m}, f, ensure_ascii=False)
            st.success("تم التحديث!")
            st.rerun()

        if st.button("🧹 تصفير سجل الحضور"):
            if os.path.exists('results.csv'): 
                os.remove('results.csv')
                st.rerun()

st.markdown("<p style='text-align:center; color:#aaa; font-size:0.8em; margin-top:50px;'>تصميم محمد العلالي - صقر العقارات 2026</p>", unsafe_allow_html=True)