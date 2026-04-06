import streamlit as st
import pandas as pd
from datetime import datetime
import os

# --- 1. إعدادات الصفحة ---
st.set_page_config(page_title="مناسبات آل علي", page_icon="⚔️", layout="centered")

# --- 2. إدارة البيانات ---
def load_results():
    if os.path.exists('results.csv'):
        try:
            return pd.read_csv('results.csv', encoding='utf-8-sig')
        except:
            return pd.DataFrame(columns=['الاسم', 'الحالة', 'الوقت'])
    return pd.DataFrame(columns=['الاسم', 'الحالة', 'الوقت'])

df_results = load_results()

# --- 3. التنسيق (CSS) ---
st.markdown("""
    <style>
    .stApp { background-color: #FDFCF0; direction: rtl; }
    .main .block-container { border: 2px solid #D4AF37; border-radius: 20px; background-color: white; padding: 30px !important; }
    .stButton>button { border-radius: 10px; font-weight: bold; width: 100%; height: 3.5em; }
    h1, h2, h3, p { text-align: center; font-family: 'Cairo', sans-serif; }
    </style>
    """, unsafe_allow_html=True)

# --- 4. الواجهة الرئيسية ---
st.markdown("<h2 style='color:#1a1a1a;'>مناسبات جماعة آل علي</h2>", unsafe_allow_html=True)
st.markdown("<p style='color:#D4AF37; font-weight:bold;'>الرياض</p>", unsafe_allow_html=True)

# عدادات سريعة
h_count = len(df_results[df_results['الحالة'] == 'حاضر'])
m_count = len(df_results[df_results['الحالة'] == 'معتذر'])

st.markdown(f"""
    <div style="display: flex; justify-content: space-around; margin: 20px 0; gap: 10px;">
        <div style="background:#28a745; color:white; padding:10px; border-radius:10px; flex:1;"><b>حاضر</b><br>{h_count}</div>
        <div style="background:#dc3545; color:white; padding:10px; border-radius:10px; flex:1;"><b>معتذر</b><br>{m_count}</div>
    </div>
""", unsafe_allow_html=True)

# --- 5. منطقة تسجيل الاسم (فكرتك يا أبا فيصل) ---
st.divider()
st.markdown("### ✍️ سجل حضورك الآن")
name_input = st.text_input("أدخل اسمك الكريم (الثلاثي أو الرباعي):", placeholder="اكتب اسمك هنا...")

if name_input:
    name_clean = name_input.strip()
    
    # فحص هل الاسم سجل من قبل؟
    check_exist = df_results[df_results['الاسم'] == name_clean]
    
    if not check_exist.empty:
        st.warning(f"⚠️ الاسم '{name_clean}' مسجل مسبقاً كـ ({check_exist.iloc[0]['الحالة']})")
    else:
        st.info(f"مرحباً بك يا {name_clean}، هل ستشرفنا بالحضور؟")
        col1, col2 = st.columns(2)
        with col1:
            if st.button("✅ نعم، سأحضر"):
                new_data = pd.DataFrame({'الاسم': [name_clean], 'الحالة': ['حاضر'], 'الوقت': [datetime.now().strftime("%I:%M %p")]})
                df_updated = pd.concat([df_results, new_data], ignore_index=True)
                df_updated.to_csv('results.csv', index=False, encoding='utf-8-sig')
                st.success("تم تسجيل حضورك.. حياك الله!")
                st.rerun()
        with col2:
            if st.button("❌ أعتذر"):
                new_data = pd.DataFrame({'الاسم': [name_clean], 'الحالة': ['معتذر'], 'الوقت': [datetime.now().strftime("%I:%M %p")]})
                df_updated = pd.concat([df_results, new_data], ignore_index=True)
                df_updated.to_csv('results.csv', index=False, encoding='utf-8-sig')
                st.warning("تم تسجيل اعتذارك.. نراكم في مناسبات قادمة")
                st.rerun()

# --- 6. عرض القائمة للجميع ---
if not df_results.empty:
    st.divider()
    st.markdown("### 📋 قائمة المسجلين")
    
    # تنسيق الجدول بالألوان
    def color_status(val):
        color = '#ccffcc' if val == 'حاضر' else '#ffcccc'
        return f'background-color: {color}'

    st.dataframe(
        df_results.style.applymap(color_status, subset=['الحالة']),
        use_container_width=True,
        hide_index=True
    )

st.markdown("<br><p style='color:#aaa; font-size:0.8em;'>تصميم محمد العلالي - صقر العقارات 2026</p>", unsafe_allow_html=True)