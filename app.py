import streamlit as st
import pandas as pd
from datetime import datetime
import os
import base64
import json

# --- 1. إعدادات الصفحة ---
st.set_page_config(page_title="مناسبات آل علي", layout="centered")

# --- 2. وظائف البيانات ---
def load_settings():
    if os.path.exists('settings.json'):
        try:
            with open('settings.json', 'r', encoding='utf-8') as f: return json.load(f)
        except: pass
    return {"title": "مناسبات جماعة آل علي", "date": "قريباً", "time": "8:00 مساءً", "location": "الرياض", "map_url": ""}

def save_settings(s):
    with open('settings.json', 'w', encoding='utf-8') as f: json.dump(s, f, ensure_ascii=False, indent=4)

def load_names():
    if os.path.exists('names.xlsx'):
        try:
            df = pd.read_excel('names.xlsx')
            return sorted(df.iloc[:, 0].dropna().unique().tolist())
        except: return []
    return []

def save_names(n):
    pd.DataFrame(n, columns=['الاسم']).to_excel('names.xlsx', index=False)

# --- 3. التنسيق الملكي ---
st.markdown("""
    <style>
    #MainMenu, footer, header {visibility: hidden;}
    .stApp { background-color: #F5F5DC; }
    .main .block-container {
        border: 2px solid #D4AF37; padding: 15px !important; 
        border-radius: 15px; background-color: #ffffff;
        max-width: 95% !important; margin: auto;
    }
    input { font-size: 16px !important; }
    .stButton>button { 
        border-radius: 10px; border: 2px solid #D4AF37; 
        background-color: #1a1a1a; color: #D4AF37; 
        font-weight: bold; width: 100%; height: 3.5em;
    }
    .event-card {
        background-color: #FFFDF5; border: 1px double #D4AF37;
        border-radius: 12px; padding: 12px; margin: 10px 0; text-align: center;
    }
    </style>
    """, unsafe_allow_html=True)

# استدعاء البيانات
if 'names' not in st.session_state:
    st.session_state.names = load_names()
    st.session_state.input_key = 0

current_settings = load_settings()

# --- 4. واجهة العرض ---
st.markdown("<h2 style='text-align:center; color:#1a1a1a;'>بِسْمِ اللهِ الرَّحْمٰنِ الرَّحِيْمِ</h2>", unsafe_allow_html=True)
st.markdown(f"<h3 style='text-align:center; color:#D4AF37;'>{current_settings['title']}</h3>", unsafe_allow_html=True)

st.markdown(f"""
    <div class="event-card">
        <p>📅 <b>التاريخ:</b> {current_settings['date']}</p>
        <p>⏰ <b>الوقت:</b> {current_settings['time']}</p>
        <p>📍 <b>الموقع:</b> {current_settings['location']}</p>
        <a href="{current_settings['map_url']}" target="_blank" style="color:#D4AF37; font-weight:bold; text-decoration:none;">📍 اضغط لفتح الموقع في الخرائط</a>
    </div>
""", unsafe_allow_html=True)

# --- 5. نظام البحث والقائمة المدمج ---
st.write("### 📝 سجل حضورك")

# حقل البحث (يفتح لوحة المفاتيح فوراً)
search_input = st.text_input("🔍 ابحث عن اسمك هنا أولاً:", placeholder="اكتب اسمك للبحث...")

# فلترة الأسماء بناءً على البحث
if search_input:
    filtered_list = [n for n in st.session_state.names if search_input in n]
else:
    filtered_list = st.session_state.names

# عرض القائمة المنسدلة (دائماً موجودة)
selected_name = st.selectbox(
    "ثم اختر اسمك من هذه القائمة:",
    options=["-- اختر الاسم --"] + filtered_list,
    index=0
)

if selected_name != "-- اختر الاسم --":
    col1, col2 = st.columns(2)
    with col1:
        if st.button("✅ تأكيد الحضور"):
            res = pd.read_csv('results.csv') if os.path.exists('results.csv') else pd.DataFrame(columns=['الاسم','الحالة','الوقت'])
            new_data = pd.DataFrame({'الاسم':[selected_name], 'الحالة':['حاضر'], 'الوقت':[datetime.now().strftime("%I:%M %p")]})
            pd.concat([res[res['الاسم'] != selected_name], new_data], ignore_index=True).to_csv('results.csv', index=False, encoding='utf-8-sig')
            st.success(f"تم تسجيل حضورك يا {selected_name}")
            st.rerun()
    with col2:
        if st.button("❌ تقديم اعتذار"):
            res = pd.read_csv('results.csv') if os.path.exists('results.csv') else pd.DataFrame(columns=['الاسم','الحالة','الوقت'])
            new_data = pd.DataFrame({'الاسم':[selected_name], 'الحالة':['معتذر'], 'الوقت':[datetime.now().strftime("%I:%M %p")]})
            pd.concat([res[res['الاسم'] != selected_name], new_data], ignore_index=True).to_csv('results.csv', index=False, encoding='utf-8-sig')
            st.warning("تم تسجيل اعتذارك")
            st.rerun()

st.divider()

# --- 6. لوحة التحكم ---
with st.expander("⚙️ لوحة تحكم المشرف"):
    if st.text_input("كلمة المرور", type="password") == "1234":
        tab1, tab2, tab3 = st.tabs(["إعدادات المناسبة", "إدارة الأسماء", "تصفير السجل"])
        with tab1:
            nt = st.text_input("العنوان:", value=current_settings['title'])
            nd = st.text_input("التاريخ:", value=current_settings['date'])
            nw = st.text_input("الوقت:", value=current_settings['time'])
            nl = st.text_input("الموقع:", value=current_settings['location'])
            nm = st.text_input("رابط الخريطة:", value=current_settings['map_url'])
            if st.button("حفظ الإعدادات"):
                save_settings({"title":nt, "date":nd, "time":nw, "location":nl, "map_url":nm})
                st.rerun()
        with tab2:
            new_n = st.text_input("اسم جديد:", key=f"add_{st.session_state.input_key}")
            if st.button("إضافة"):
                if new_n and new_n not in st.session_state.names:
                    st.session_state.names.append(new_n.strip())
                    save_names(sorted(st.session_state.names))
                    st.session_state.input_key += 1
                    st.rerun()
            del_n = st.selectbox("حذف اسم:", options=["-- اختر --"] + st.session_state.names)
            if st.button("حذف"):
                if del_n != "-- اختر --":
                    st.session_state.names.remove(del_n)
                    save_names(st.session_state.names)
                    st.rerun()
        with tab3:
            if st.button("مسح السجل بالكامل"):
                if os.path.exists('results.csv'): os.remove('results.csv')
                st.rerun()

st.markdown("<p style='text-align:center; color:#888; font-size:0.7em;'>صقر العقارات 2026</p>", unsafe_allow_html=True)