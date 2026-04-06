# 5. عرض الإحصائيات والنتائج (محدثة للإدارة)
st.divider()
df_final = load_results()

if not df_final.empty:
    # حساب الأعداد
    total_responses = len(df_final)
    confirmed_guests = len(df_final[df_final['الحالة'] == 'حاضر'])
    apologies = len(df_final[df_final['الحالة'] == 'معتذر'])

    st.markdown("### 📊 ملخص الحضور")
    
    # توزيع الإحصائيات في أعمدة ملونة
    c1, c2, c3 = st.columns(3)
    with c1:
        st.metric(label="إجمالي المسجلين", value=total_responses)
    with c2:
        st.success(f"✅ الحاضرون: {confirmed_guests}")
    with c3:
        st.error(f"❌ المعتذرون: {apologies}")

    with st.expander("👁️ عرض كشف الأسماء بالتفصيل"):
        # تمييز الحالات بالألوان في الجدول
        def highlight_status(val):
            color = '#2ecc71' if val == 'حاضر' else '#e74c3c'
            return f'color: {color}; font-weight: bold;'

        # تطبيق التنسيق على عمود الحالة
        styled_df = df_final.style.applymap(highlight_status, subset=['الحالة'])
        
        st.dataframe(styled_df, use_container_width=True, hide_index=True)
        
        # زر التحميل
        csv = df_final.to_csv(index=False).encode('utf-8-sig')
        st.download_button("📥 تحميل التقرير النهائي للمشرف", data=csv, file_name="attendance_report.csv")
else:
    st.info("💡 لا توجد بيانات مسجلة حتى الآن. بانتظار مشاركة الجماعة.")