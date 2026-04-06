import streamlit as st
import pandas as pd
from datetime import datetime
import os
import base64
import json

# --- إعدادات الصفحة ---
st.set_page_config(page_title="مناسبات آل علي", layout="centered")

# --- وظائف البيانات ---
def load_settings():
    if os.path.exists('settings.json'):
        with open('settings.json', 'r', encoding='utf-8') as f: return json.load(f)
    return {"title": "مناسبات آل علي", "date": "", "time": "", "location": "", "map_url": ""}

def load_names():
    if os.path.exists('names.xlsx'):
        try: return sorted(pd.read_excel('names.xlsx').iloc[:, 0].dropna().unique().tolist())
        except: return []
    return []

# --- التنسيق (تم تحسينه لسرعة الاستجابة) ---
st.markdown("""
    <style>
    #MainMenu, footer, header {visibility: hidden;}
    .stApp { background-color: #F5F5DC; }
    .main .block-container {
        border: 2px solid #D4AF37; padding: 20px !important; 
        border-radius: 15px; background-color: #ffffff;
        max-width: 95% !important; margin: auto;
    }
    /* تكبير الخط في حقول الإدخال لضمان استجابة الجوال */
    input { font-size: 18px !important; }
    .stButton>button { 
        border-radius: 10px; border: 2px solid #D4AF37; 
        background-color: #1a1a1a; color: #D4AF37; 
        font-weight: bold; width: 100%; height: 3.5em;
    }
    </style>
    """, unsafe_allow_html=True)

# استرجاع البيانات
settings = load_settings()
all_names = load_names()

st.markdown(f"<h2 style='text-align:center; color:#D4AF37;'>{settings['title']}</h2>", unsafe_allow_html=True)

# بطاقة الدعوة
st.markdown(f"""
    <div style="background-color: #FFFDF5; border: 1px solid #D4AF37; border-radius: 10px; padding: 15px; text-align: center; margin-bottom: 20px;">
        <p>📅 <b>التاريخ:</b> {settings['date']}</p>
        <p>📍 <b>الموقع:</b> {settings['location']}</p>
        <a href="{settings['map_url']}" target="_blank" style="color: #D4AF37; font-weight: bold;">📍 اضغط لفتح الخريطة</a>
    </div>
""", unsafe_allow_html=True)

# --- نظام البحث الجديد (الأكثر استجابة) ---
st.write("### 🔍 ابحث عن اسمك")
search_term = st.text_input("اكتب اسمك هنا (سيظهر الاسم المختار بالأسفل):", placeholder="مثلاً: محمد..")

if search_term:
    # تصفية الأسماء بناءً على ما كتبه المستخدم
    filtered_names = [name for name in all_names if search_term in name]
    
    if filtered_names:
        final_name = st.radio("اختر اسمك الصحيح من القائمة:", options=filtered_names)
        
        if final_name:
            st.info(f"الاسم المختار: **{final_name}**")
            col1, col2 = st.columns(2)
            with col1:
                if st.button("✅ تأكيد الحضور"):
                    # حفظ النتيجة (نفس الكود السابق)
                    res = pd.read_csv('community_events_results.csv') if os.path.exists('community_events_results.csv') else pd.DataFrame(columns=['الاسم', 'الحالة', 'الوقت'])
                    new_row = pd.DataFrame({'الاسم': [final_name], 'الحالة': ['حاضر'], 'الوقت': [datetime.now().strftime("%I:%M %p")]})
                    pd.concat([res[res['الاسم'] != final_name], new_row], ignore_index=True).to_csv('community_events_results.csv', index=False, encoding='utf-8-sig')
                    st.success("تم تسجيل حضورك")
                    st.rerun()
            with col2:
                if st.button("❌ اعتذار"):
                    res = pd.read_csv('community_events_results.csv') if os.path.exists('community_events_results.csv') else pd.DataFrame(columns=['الاسم', 'الحالة', 'الوقت'])
                    new_row = pd.DataFrame({'الاسم': [final_name], 'الحالة': ['معتذر'], 'الوقت': [datetime.now().strftime("%I:%M %p")]})
                    pd.concat([res[res['الاسم'] != final_name], new_row], ignore_index=True).to_csv('community_events_results.csv', index=False, encoding='utf-8-sig')
                    st.warning("تم تسجيل الاعتذار")
                    st.rerun()
    else:
        st.error("لم يتم العثور على اسم مطابق.")
else:
    st.write("يرجى كتابة حرفين على الأقل للبحث..")

# --- لوحة التحكم (مختصرة للضرورة) ---
with st.expander("⚙️ الإدارة"):
    if st.text_input("كلمة المرور", type="password") == "1234":
        # هنا تضع تبويبات الإعدادات كما في الكود السابق
        st.write("يمكنك إضافة الأسماء أو تعديل المناسبة هنا..")

st.markdown("<p style='text-align:center; color:#888; font-size:0.8em; margin-top:20px;'>صقر العقارات 2026</p>", unsafe_allow_html=True)