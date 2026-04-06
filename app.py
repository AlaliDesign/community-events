import streamlit as st
import pandas as pd
from datetime import datetime, date
import os
import json
import urllib.parse
from ummalqura.hijri_date import HijriDate

# --- 1. إدارة البيانات بدقة ---
def load_data():
    names = []
    if os.path.exists('names.xlsx'):
        try:
            df = pd.read_excel('names.xlsx')
            names = sorted(df.iloc[:, 0].dropna().astype(str).unique().tolist())
        except: pass
    
    results = pd.DataFrame(columns=['الاسم', 'الحالة', 'الوقت'])
    if os.path.exists('results.csv'):
        try: results = pd.read_csv('results.csv', encoding='utf-8-sig')
        except: pass
        
    # الإعدادات الافتراضية
    settings = {"title": "مناسبات آل علي", "h_date": str(date.today()), "time": "08:30 PM", "location": "الرياض", "map_url": ""}
    
    if os.path.exists('settings.json'):
        try:
            with open('settings.json', 'r', encoding='utf-8') as f:
                saved_settings = json.load(f)
                # دمج الإعدادات القديمة مع الجديدة لضمان عدم حدوث KeyError
                settings.update(saved_settings)
        except: pass
    return names, results, settings

# --- 2. التصميم الملكي ---
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
    }
    </style>
    """, unsafe_allow_html=True)

all_names, df_results, settings = load_data()

# التأكد من وجود h_date لتجنب الخطأ
current_h_date = settings.get('h_date', '1447-01-01')

# --- 3. معالجة التاريخ والتحقق ---
today_g = date.today()
is_active = False
g_date_final = today_g

try:
    hy, hm, hd = map(int, current_h_date.split('-'))
    g_date_final = HijriDate(hy, hm, hd).get_georgiandate()
    if g_date_final >= today_g:
        is_active = True
except:
    is_active = True

# --- 4. العرض ---
if is_active:
    st.markdown(f"<h3 style='text-align:center; color:#D4AF37;'>{settings['title']}</h3>", unsafe_allow_html=True)
    st.markdown(f"""
        <div class="event-card">
            <p style="font-size:1.2em;">📅 <b>التاريخ الهجري:</b> {current_h_date}</p>
            <p>⏰ <b>الوقت:</b> {settings['time']} | 📍 <b>الموقع:</b> {settings['location']}</p>
        </div>
    """, unsafe_allow_html=True)
    
    g_str = g_date_final.strftime('%Y%m%d')
    t_q = urllib.parse.quote(settings['title'])
    cal_url = f"https://www.google.com/calendar/render?action=TEMPLATE&text={t_q}&dates={g_str}T170000Z/{g_str}T210000Z"
    st.link_button("🔔 أضف تذكير صوتي بجوالك", cal_url, use_container_width=True)
    
    if settings['map_url']:
        st.link_button("📍 موقع المناسبة (خرائط جوجل)", settings['map_url'], use_container_width=True)

    st.divider()
    st.markdown("### 📝 سجل حضورك")
    search = st.text_input("🔍 ابحث عن اسمك:", placeholder="اكتب اسمك...")
    opts = [n for n in all_names if search in n] if search else all_names
    selected = st.selectbox("اختر اسمك من القائمة:", options=["-- اختر --"] + opts)

    if selected != "-- اختر --":
        c1, c2 = st.columns(2)
        with c1:
            if st.button("✅ تأكيد الحضور"):
                new = pd.DataFrame({'الاسم': [selected], 'الحالة': ['حاضر'], 'الوقت': [datetime.now().strftime("%I:%M %p")]})
                pd.concat([df_results[df_results['الاسم'] != selected], new], ignore_index=True).to_csv('results.csv', index=False, encoding='utf-8-sig')
                st.success("تم تسجيل حضورك")
                st.rerun()
        with c2:
            if st.button("❌ اعتذار"):
                new = pd.DataFrame({'الاسم': [selected], 'الحالة': ['معتذر'], 'الوقت': [datetime.now().strftime("%I:%M %p")]})
                pd.concat([df_results[df_results['الاسم'] != selected], new], ignore_index=True).to_csv('results.csv', index=False, encoding='utf-8-sig')
                st.warning("تم تسجيل اعتذارك")
                st.rerun()
else:
    st.markdown("<h2 style='text-align:center; color:#D4AF37;'>نلقاكم على خير في مناسبات قادمة</h2>", unsafe_allow_html=True)

# --- 5. الإحصائيات ---
st.divider()
st.markdown("<h4 style='text-align:center;'>📊 الإحصائيات</h4>", unsafe_allow_html=True)
col1, col2, col3 = st.columns(3)
with col1: st.metric("المسجلين", len(all_names))
with col2: st.metric("حاضر ✅", len(df_results[df_results['الحالة'] == 'حاضر']))
with col3: st.metric("معتذر ❌", len(df_results[df_results['الحالة'] == 'معتذر']))

# --- 6. لوحة التحكم ---
with st.expander("⚙️ لوحة التحكم"):
    if st.text_input("كلمة المرور", type="password") == "1234":
        if st.button("تصفير السجل"):
            if os.path.exists('results.csv'): os.remove('results.csv')
            st.rerun()
        st.write("---")
        nt = st.text_input("عنوان المناسبة", value=settings['title'])
        nh = st.text_input("التاريخ الهجري (1447-10-25)", value=current_h_date)
        nw = st.text_input("الوقت", value=settings['time'])
        nl = st.text_input("الموقع", value=settings['location'])
        nm = st.text_input("رابط الخريطة", value=settings['map_url'])
        
        if st.button("حفظ ونشر"):
            with open('settings.json', 'w', encoding='utf-8') as f:
                json.dump({"title":nt, "h_date":nh, "time":nw, "location":nl, "map_url":nm}, f, ensure_ascii=False)
            st.rerun()

st.markdown("<p style='text-align:center; color:#888; font-size:0.7em;'>محمد العلالي - صقر العقارات 2026</p>", unsafe_allow_html=True)