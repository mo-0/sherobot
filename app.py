# ─── قنوات التواصل والفوتر المظبوط والمقفل برمجياً ───
    st.markdown("#### 🚀 تنفيذ الطلب السريع:")
    btn_col1, btn_col2 = st.columns(2)
    
    with btn_col1: 
        st.link_button("📱 إرسال الطلب عبر الواتساب", f"https://wa.me/201090416662?text={urllib.parse.quote(msg_template)}", use_container_width=True, disabled=(not st.session_state.want_m and not st.session_state.want_s))
    
    with btn_col2: 
        st.link_button("📧 إرسال الطلب عبر الإيميل", f"mailto:octanova.team@example.com?subject=SheroWhey_Order&body={urllib.parse.quote(msg_template)}", use_container_width=True, disabled=(not st.session_state.want_m and not st.session_state.want_s))

    # الفوتر السفلي الموحد والمحاذى للمنتصف بأمان
    st.markdown("""
        <br><br>
        <div style="text-align: center; color: #666677; font-size: 0.9rem; border-top: 1px solid #222232; padding-top: 15px;">
            © Octanova 2026 | جميع الحقوق محفوظة لمشروع SheroWhey 🍦
        </div>
    """, unsafe_allow_html=True)
