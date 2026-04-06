import streamlit as st
import pandas as pd
from datetime import datetime, date
import os
import json
import urllib.parse
from ummalqura.hijri_date import HijriDate

# --- 1. إدارة البيانات ---
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
        
    settings = {"title": "مناسبات آل علي", "h_date": "1447-10-20", "time": "08:30 PM", "location": "الرياض", "map_url": ""}
    if os.path.exists('settings.json'):
        try:
            with open('settings.json', 'r', encoding='utf-8') as f: settings = json.load(f)
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
        font-weight: bold !important;
    }
    .stButton>button { 
        border-radius: 10px; border: 2px solid #D4AF37; 
        background-color: #1a1a1a; color: #D4AF37; font-weight: bold; width: 100%;
    }
    input { font-size: 16px !important; }
    </style>
    """, unsafe_allow_html=True)

all_names, df_results, settings = load_data()

# --- 3. معالجة التاريخ والتحقق من صلاحية المناسبة ---
today_g = date.today()
is_active = False
g_date_final = today_g

try:
    # تحويل الهجري المكتوب (1447-10-25) لميلادي للمقارنة
    hy, hm, hd = map(int, settings['h_date'].split('-'))
    g_date_final = HijriDate(hy, hm, hd).get_georgiandate()
    if g_date_final >= today_g:
        is_active = True
except:
    is_active = True # نشطة في حال الخطأ بالتنسيق

# --- 4. عرض الواجهة ---
if is_active:
    st.markdown(f"<h3 style='text-align:center; color:#D4AF37;'>{settings['title']}</h3>", unsafe_allow_html=True)
    
    st.markdown(f"""
        <div class="event-card">
            <p style="font-size:1.2em;">📅 <b>التاريخ الهجري:</b> {settings['h_date']}</p>
            <p>⏰ <b>الوقت:</b> {settings['time']} | 📍 <b>الموقع:</b> {settings['location']}</p>
        </div>
    """, unsafe_allow_html=True)
    
    # رابط التذكير الصوتي
    g_str = g_date_final.strftime('%Y%m%d')
    t_q = urllib.parse.quote(settings['title'])
    cal_url = f"https://www.google.com/calendar/render?action=TEMPLATE&text={t_q}&dates={g_str}T170000Z/{g_str}T210000Z&details=تذكير+بالمناسبة"
    
    st.link_button("🔔 أضف تذكير بجوالك (تنبيه صوتي)", cal_url, use_container_width=True)
    
    if settings['map_url']:
        st.link_button("📍 موقع المناسبة (خرائط جوجل)", settings['map_url'], use_container_width=True)

    st.divider()
    st.markdown("### 📝 سجل حضورك")
    search = st.text_input("🔍 ابحث عن اسمك:", placeholder="اكتب أول حروف...")
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
    st.markdown("<br><br><h2 style='text-align:center; color:#D4AF37;'>نلقاكم على خير في مناسبات قادمة</h2>", unsafe_allow_html=True)
    st.markdown("<p style='text-align:center; color:#888;'>لا توجد مناسبات نشطة حالياً.</p>", unsafe_allow_html=True)

# --- 5. الإحصائيات والكشف ---
st.divider()
st.markdown("<h4 style='text-align:center;'>📊 الإحصائيات</h4>", unsafe_allow_html=True)
col1, col2, col3 = st.columns(3)
with col1: st.metric("المسجلين", len(all_names))
with col2: st.metric("حاضر ✅", len(df_results[df_results['الحالة'] == 'حاضر']))
with col3: st.metric("معتذر ❌", len(df_results[df_results['الحالة'] == 'معتذر']))

if not df_results.empty:
    with st.expander("📋 عرض كشف الأسماء"):
        st.dataframe(df_results.sort_values(by='الوقت', ascending=False), use_container_width=True, hide_index=True)

# --- 6. لوحة التحكم ---
with st.expander("⚙️ لوحة التحكم"):
    if st.text_input("كلمة المرور", type="password") == "1234":
        if st.button("تصفير السجل لمناسبة جديدة"):
            if os.path.exists('results.csv'): os.remove('results.csv')
            st.rerun()
        st.write("---")
        nt = st.text_input("عنوان المناسبة", value=settings['title'])
        nh = st.text_input("التاريخ الهجري (مثال: 1447-10-25)", value=settings['h_date'])
        
        try:
            hy_i, hm_i, hd_i = map(int, nh.split('-'))
            conv_g = HijriDate(hy_i, hm_i, hd_i).get_georgiandate()
            st.info(f"📅 يوافق بالميلادي: {conv_g}")
            if conv_g < today_g: st.error("⚠️ التاريخ قديم، ستختفي المناسبة!")
        except: st.warning("اكتب التاريخ هكذا: 1447-10-25")

        nw = st.text_input("الوقت", value=settings['time'])
        nl = st.text_input("الموقع", value=settings['location'])
        nm = st.text_input("رابط الخريطة", value=settings['map_url'])
        
        if st.button("حفظ ونشر المناسبة"):
            with open('settings.json', 'w', encoding='utf-8') as f:
                json.dump({"title":nt, "h_date":nh, "time":nw, "location":nl, "map_url":nm}, f, ensure_ascii=False)
            st.rerun()

st.markdown("<p style='text-align:center; color:#888; font-size:0.7em;'>محمد العلالي - صقر العقارات 2026</p>", unsafe_allow_html=True)