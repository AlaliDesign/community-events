import streamlit as st
import pandas as pd
from datetime import datetime, date
import os
import json
import urllib.parse
from ummalqura.hijri_date import HijriDate
from PIL import Image

# --- 1. إعدادات الصفحة والأيقونة ---
icon_path = 'logo.png'
image_url = "https://i.ibb.co/Pv2TzzCj/logo.png"

if os.path.exists(icon_path):
    try:
        img = Image.open(icon_path)
        st.set_page_config(page_title="مناسبات جماعة آل علي", page_icon=img)
    except:
        st.set_page_config(page_title="مناسبات جماعة آل علي", page_icon="⚔️")
else:
    st.set_page_config(page_title="مناسبات جماعة آل علي", page_icon="⚔️")

st.markdown(f'<link rel="apple-touch-icon" href="{image_url}">', unsafe_allow_html=True)

# --- 2. وظائف البيانات ---
def load_data():
    names = []
    if os.path.exists('names.xlsx'):
        try:
            df = pd.read_excel('names.xlsx')
            names = sorted(df.iloc[:, 0].dropna().astype(str).unique().tolist())
        except: pass
    
    results = pd.DataFrame(columns=['الاسم', 'الحالة', 'الوقت'])
    if os.path.exists('results.csv'):
        try: 
            results = pd.read_csv('results.csv', encoding='utf-8-sig')
        except: pass
        
    settings = {"title": "مناسبات جماعة آل علي في الرياض", "h_date": "لم يحدد", "time": "حدد الوقت", "location": "حدد الموقع", "map_url": ""}
    if os.path.exists('settings.json'):
        try:
            with open('settings.json', 'r', encoding='utf-8') as f:
                saved = json.load(f)
                settings.update(saved)
        except: pass
    return names, results, settings

# --- 3. التنسيق (CSS) ---
st.markdown("""
    <style>
    #MainMenu, footer, header {visibility: hidden;}
    .stApp { background-color: #FDFCF0; }
    .main .block-container {
        border: 2px solid #D4AF37; padding: 15px !important; 
        border-radius: 15px; background-color: #ffffff;
        max-width: 95% !important; margin: auto;
    }
    .event-card {
        background-color: #FFFDF5; border: 1px double #D4AF37;
        border-radius: 12px; padding: 15px; margin: 10px 0; text-align: center;
    }
    div.stLinkButton > a {
        background-color: #D4AF37 !important; color: white !important;
        border-radius: 10px !important; width: 100% !important; display: block !important;
        font-weight: bold !important; text-decoration: none !important;
    }
    .stButton>button { 
        border-radius: 10px; border: 2px solid #D4AF37; 
        background-color: #1a1a1a; color: #D4AF37; font-weight: bold; width: 100%;
    }
    </style>
    """, unsafe_allow_html=True)

all_names, df_results, settings = load_data()

# --- 4. واجهة العرض ---
col_l, col_m, col_r = st.columns([1, 1.5, 1])
with col_m:
    if os.path.exists(icon_path):
        st.image(icon_path, use_column_width=True)
    else:
        st.markdown("<div style='text-align:center; font-size:40px;'>🌴⚔️</div>", unsafe_allow_html=True)

st.markdown("<h3 style='text-align:center; color:#1a1a1a; font-weight:bold;'>مناسبات جماعة آل علي في الرياض</h3>", unsafe_allow_html=True)

# العدادات
h_count = len(df_results[df_results['الحالة'] == 'حاضر'])
m_count = len(df_results[df_results['الحالة'] == 'معتذر'])
t_count = len(all_names)

st.markdown(f"""
    <div style="display: flex; justify-content: space-between; gap: 10px; margin-bottom: 20px;">
        <div style="background-color: #28a745; color: white; padding: 15px; border-radius: 10px; flex: 1; text-align: center;">
            <div style="font-size: 0.9em;">الحاضرين</div>
            <div style="font-size: 1.5em; font-weight: bold;">{h_count}</div>
        </div>
        <div style="background-color: #dc3545; color: white; padding: 15px; border-radius: 10px; flex: 1; text-align: center;">
            <div style="font-size: 0.9em;">المعتذرين</div>
            <div style="font-size: 1.5em; font-weight: bold;">{m_count}</div>
        </div>
        <div style="background-color: #1a1a1a; color: #D4AF37; padding: 15px; border-radius: 10px; flex: 1; text-align: center; border: 1px solid #D4AF37;">
            <div style="font-size: 0.9em;">الإجمالي</div>
            <div style="font-size: 1.5em; font-weight: bold;">{t_count}</div>
        </div>
    </div>
""", unsafe_allow_html=True)

st.markdown(f"""
    <div class="event-card">
        <p style="font-size:1.2em;">📅 <b>التاريخ الهجري:</b> {settings['h_date']}</p>
        <p style="font-size:1.1em;">⏰ <b>الوقت:</b> {settings['time']} | 📍 <b>الموقع:</b> {settings['location']}</p>
    </div>
""", unsafe_allow_html=True)

if settings['h_date'] != "لم يحدد":
    try:
        hy, hm, hd = map(int, settings['h_date'].split('-'))
        g_date = HijriDate(hy, hm, hd).get_georgiandate()
        g_str = g_date.strftime('%Y%m%d')
        t_q = urllib.parse.quote("مناسبات جماعة آل علي")
        cal_url = f"https://www.google.com/calendar/render?action=TEMPLATE&text={t_q}&dates={g_str}T170000Z/{g_str}T210000Z"
        st.link_button("🔔 أضف تذكير صوتي بجوالك", cal_url, use_container_width=True)
    except: pass

if settings['map_url']:
    st.link_button("📍 موقع المناسبة (خرائط جوجل)", settings['map_url'], use_container_width=True)

# --- 5. سجل الحضور ---
st.divider()
st.markdown("### 📝 سجل حضورك")

if not all_names:
    st.info("ℹ️ القائمة فارغة. أضف أسماء من لوحة التحكم.")
    selected = st.text_input("أو اكتب اسمك يدوياً هنا:")
else:
    search = st.text_input("🔍 ابحث عن اسمك:", placeholder="اكتب اسمك هنا...")
    opts = [n for n in all_names if search in n] if search else all_names
    selected = st.selectbox("اختر اسمك من القائمة:", options=["-- اختر --"] + opts)

if selected and selected != "-- اختر --":
    ca, cb = st.columns(2)
    with ca:
        if st.button("✅ تأكيد الحضور"):
            new = pd.DataFrame({'الاسم': [selected], 'الحالة': ['حاضر'], 'الوقت': [datetime.now().strftime("%I:%M %p")]})
            final_df = pd.concat([df_results[df_results['الاسم'] != selected], new], ignore_index=True)
            final_df.to_csv('results.csv', index=False, encoding='utf-8-sig')
            st.success(f"تم تسجيل حضورك")
            st.rerun()
    with cb:
        if st.button("❌ اعتذار"):
            new = pd.DataFrame({'الاسم': [selected], 'الحالة': ['معتذر'], 'الوقت': [datetime.now().strftime("%I:%M %p")]})
            final_df = pd.concat([df_results[df_results['الاسم'] != selected], new], ignore_index=True)
            final_df.to_csv('results.csv', index=False, encoding='utf-8-sig')
            st.warning(f"تم تسجيل اعتذارك")
            st.rerun()

# --- 6. عرض الجدول ---
st.divider()
if not df_results.empty:
    st.markdown("### 📋 قائمة الحضور والاعتذار")
    def color_status(val):
        if val == 'معتذر': return 'background-color: #ffcccc; color: #990000; font-weight: bold;'
        return 'background-color: #ccffcc; color: #006600;'
    styled_df = df_results[['الاسم', 'الحالة', 'الوقت']].style.map(color_status, subset=['الحالة'])
    st.dataframe(styled_df, use_container_width=True, hide_index=True)

# --- 7. لوحة التحكم (إضافة وحذف الأسماء) ---
with st.expander("⚙️ لوحة التحكم وإدارة الأسماء"):
    pw = st.text_input("كلمة المرور", type="password", key="admin_pw")
    if pw == "1234":
        # قسم إدارة ملف الأسماء
        st.subheader("👥 إدارة قائمة الأسماء (names.xlsx)")
        col_add, col_del = st.columns(2)
        
        with col_add:
            new_name = st.text_input("أضف اسم جديد للقائمة:")
            if st.button("➕ إضافة اسم"):
                if new_name and new_name not in all_names:
                    all_names.append(new_name)
                    pd.DataFrame(all_names).to_excel('names.xlsx', index=False, header=False)
                    st.success(f"تمت إضافة {new_name}")
                    st.rerun()
        
        with col_del:
            if all_names:
                name_to_del = st.selectbox("اختر اسم لحذفه:", options=all_names)
                if st.button("🗑️ حذف الاسم"):
                    all_names.remove(name_to_del)
                    pd.DataFrame(all_names).to_excel('names.xlsx', index=False, header=False)
                    st.error(f"تم حذف {name_to_del}")
                    st.rerun()

        st.divider()
        # قسم إعدادات المناسبة
        st.subheader("📅 إعدادات المناسبة")
        nh = st.text_input("التاريخ الهجري (1447-10-25)", value=settings['h_date'])
        nw = st.text_input("الوقت", value=settings['time'])
        nl = st.text_input("الموقع", value=settings['location'])
        nm = st.text_input("رابط الخريطة", value=settings['map_url'])
        
        if st.button("💾 حفظ ونشر المناسبة"):
            with open('settings.json', 'w', encoding='utf-8') as f:
                json.dump({"title":"مناسبات جماعة آل علي في الرياض", "h_date":nh, "time":nw, "location":nl, "map_url":nm}, f, ensure_ascii=False)
            st.success("تم الحفظ!")
            st.rerun()

        if st.button("🧹 تصفير سجل الحضور (لمناسبة جديدة)"):
            if os.path.exists('results.csv'): 
                os.remove('results.csv')
                st.rerun()

st.markdown("<p style='text-align:center; color:#888; font-size:0.7em;'>محمد العلالي - صقر العقارات 2026</p>", unsafe_allow_html=True)