import streamlit as st
import streamlit.components.v1 as components
import google.generativeai as genai
import urllib.parse  # مخصصة لتنسيق وتوليد روابط الواتساب والإيميل بشكل سليم

# ==========================================
# 1. إعدادات الصفحة وجعلها متناسقة مع الـ Dark Mode
# ==========================================
st.set_page_config(page_title="SheroWhey | آيس كريم صحي", page_icon="🍦", layout="wide")

# إجبار عناصر بايثون الأصلية في Streamlit على التناسق مع الوضع الداكن لحماية النصوص
st.markdown("""
    <style>
    /* تعديل تنسيق التبويب والخلفية العامة للـ Dark Mode */
    .stTabs [data-baseweb="tab-list"] {
        gap: 10px;
    }
    .stTabs [data-baseweb="tab"] {
        background-color: #1e1e1e;
        border-radius: 10px 10px 0px 0px;
        padding: 10px 20px;
        color: #ffffff !important;
    }
    .stTabs [aria-selected="true"] {
        background-color: #e67e22 !important;
        font-weight: bold;
    }
    /* تنسيق الكروت العلوية والسفلية لتبدو مودرن وواضحة جداً في الخلفية المظلمة */
    .hero-box {
        background: linear-gradient(135deg, #1e1e1e, #2d2d2d);
        border-radius: 25px;
        padding: 30px;
        border-right: 8px solid #f9a825;
        box-shadow: 0 4px 15px rgba(0,0,0,0.3);
        color: #ffffff !important;
    }
    .product-card {
        background-color: #1e1e1e;
        border-radius: 20px;
        padding: 25px;
        text-align: center;
        box-shadow: 0 10px 25px rgba(0,0,0,0.4);
        border: 1px solid #333333;
        color: #ffffff !important;
    }
    .indicator-dots {
        font-size: 20px;
        text-align: center;
        color: #f9a825;
        margin-top: 10px;
    }
    /* ضمان وضوح نصوص الإدخال والراديو في الثيم الغامق */
    label, .stMarkdown, p, h1, h2, h3, h4 {
        color: #ffffff !important;
    }
    div[data-testid="stCheckbox"] label p {
        color: #ffffff !important;
    }
    </style>
""", unsafe_allow_html=True)

# ==========================================
# 2. إعدادات البوت وسحب المفتاح بأمان
# ==========================================
genai.configure(api_key=st.secrets["GEMINI_API_KEY"])

# شخصية خدمة العملاء لـ SheroWhey
customer_service_persona = """
أنت مساعد خدمة عملاء ذكي لمنتج "SheroWhey".
المنتج عبارة عن آيس كريم صحي طبيعي 100% مصنوع من شرش اللبن الطبيعي (Whey).
فوائد المنتج: غني بالكالسيوم، البوتاسيوم، الفيتامينات، وصديق للبيئة (Zero Waste).
الأنواع المتاحة: "مانجو وكركمين" و "فراولة ورمان".
أسلوبك: ودود، احترافي، مباشر، وتتحدث باللهجة المصرية.
ردودك يجب أن تكون قصيرة جداً ومقنعة، ووجّه العميل دائماً للذهاب لتبويب "تصفح المنتجات والطلب" أو "إدارة وتنفيذ الطلبات السريعة" لإتمام الطلب.
"""
model = genai.GenerativeModel('gemini-2.5-flash', system_instruction=customer_service_persona)

# 3. تقسيم الواجهة لثلاث تبويبات (Tabs)
tab1, tab2, tab3 = st.tabs([
    "🛒 تصفح المنتجات والطلب", 
    "💬 المساعد الذكي للاستفسارات", 
    "📋 إدارة وتنفيذ الطلبات السريعة"
])

# ==========================================
# التبويب الأول: الويب سايت التفاعلي المطور (Carousel + Products)
# ==========================================
with tab1:
    # --- الهيدر العلوي والأقسام الثابتة ---
    col_brand, col_logo = st.columns([4, 1])

    with col_brand:
        st.markdown("""
            <div style='text-align: right; direction: rtl; padding-top: 15px;'>
                <h1 style='color: #e67e22 !important; margin-bottom: 0;'>SheroWhey</h1>
                <h3 style='color: #cccccc !important; font-weight: normal; margin-top: 5px;'>✨ آيس كريم صحي طبيعي مبتكر من شرش اللبن</h3>
            </div>
        """, unsafe_allow_html=True)

    with col_logo:
        try:
            st.image("logo.jpg", use_column_width=True)
        except Exception:
            st.markdown("<h1 style='text-align: center;'>🍦</h1>", unsafe_allow_html=True)

    # المميزات السريعة
    st.markdown("""
    <div style='display: flex; justify-content: center; gap: 15px; flex-wrap: wrap; margin-bottom: 30px; direction: rtl;'>
        <span style='background: #1e1e1e; padding: 8px 20px; border-radius: 50px; font-weight: bold; color: #4caf50; border: 2px solid #4caf50;'>🌿 شرش اللبن الطبيعي</span>
        <span style='background: #1e1e1e; padding: 8px 20px; border-radius: 50px; font-weight: bold; color: #4caf50; border: 2px solid #4caf50;'>🥛 غني بالكالسيوم والبوتاسيوم</span>
        <span style='background: #1e1e1e; padding: 8px 20px; border-radius: 50px; font-weight: bold; color: #4caf50; border: 2px solid #4caf50;'>🍊 فيتامينات ومضادات أكسدة</span>
        <span style='background: #1e1e1e; padding: 8px 20px; border-radius: 50px; font-weight: bold; color: #4caf50; border: 2px solid #4caf50;'>♻️ Zero Waste صديق للبيئة</span>
    </div>
    """, unsafe_allow_html=True)

    # --- إعداد بيانات الـ Carousel ---
    slides = [
        {
            "image": "https://images.unsplash.com/photo-1560512823-829485b8bf24?w=600&auto=format&fit=crop&q=80", 
            "title": "ابتكار طعم المانجو والكركمين 🥭",
            "description": "مزيج فريد ومدروس علمياً يجمع بين فوائد شرش اللبن الوظيفي ونكهة المانجو الطبيعية، معزز بمستخلص الكركمين النشط كمضاد أكسدة طبيعي يدعم صحتك وقوام الآيس كريم."
        },
        {
            "image": "https://images.unsplash.com/photo-1601004890684-d8cbf643f5f2?w=600&auto=format&fit=crop&q=80", 
            "title": "شيروواي - شربت الفراولة والرمان الطبيعي 🍓",
            "description": "الابتكار في كل ملعقة! استمتع بالانتعاش الحقيقي والمذاق المتوازن مع توليفة مبتكرة تجمع بين حلاوة الفراولة الطبيعية ونكهة الرمان الغنية. تم تصنيعه بقاعدة مميزة من الشرش السائل الطبيعي لتقديم قوام ناعم وخفيف ومثالي يمنحك الحيوية الاستثنائية."
        },
        {
            "image": "https://images.unsplash.com/photo-1576092768241-dec231879fc3?w=600&auto=format&fit=crop&q=80", 
            "title": "رؤية مستدامة وصديقة للبيئة ♻️",
            "description": "مشروع SheroWhey يقوم على استغلال (الشرش الحلو السائل) الناتج من صناعة الألبان كبديل للمواد الصلبة اللادهنية (SNF)، لنساهم في تقليل الهلاك البيئي وتقديم منتج وظيفي أعلى في القيمة الغذائية."
        }
    ]

    if 'current_slide' not in st.session_state:
        st.session_state.current_slide = 0

    def next_slide():
        st.session_state.current_slide = (st.session_state.current_slide + 1) % len(slides)

    def prev_slide():
        st.session_state.current_slide = (st.session_state.current_slide - 1) % len(slides)

    # عرض الـ Carousel (القسم العلوي)
    hero_col1, hero_col2 = st.columns([1.2, 1])
    current_data = slides[st.session_state.current_slide]

    with hero_col1:
        st.markdown(f"""
        <div class="hero-box" style="direction: rtl; text-align: right;">
            <h2 style='color: #f39c12 !important; margin-bottom: 15px;'>{current_data['title']}</h2>
            <p style='font-size: 1.15rem; line-height: 1.7; color: #ffffff !important;'>{current_data['description']}</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.write("")
        btn_col1, btn_col2, btn_col3 = st.columns([1, 2, 1])
        with btn_col1:
            st.button("⬅️ السابق", on_click=prev_slide, key="prev_btn", use_container_width=True)
        with btn_col3:
            st.button("التالي ➡️", on_click=next_slide, key="next_btn", use_container_width=True)

    with hero_col2:
        st.image(current_data['image'], use_column_width=True)
        dots = "".join(["● " if i == st.session_state.current_slide else "○ " for i in range(len(slides))])
        st.markdown(f"<div class='indicator-dots'>{dots}</div>", unsafe_allow_html=True)

    st.markdown("<br><hr><br>", unsafe_allow_html=True)

    # --- القسم السفلي: كروت المنتجات والحقائق الغذائية (The Grid) ---
    st.markdown("<h3 style='text-align: center; color: #ffffff; margin-bottom:25px;'>🍨 منتجاتنا المتوفرة والحقائق الغذائية</h3>", unsafe_allow_html=True)
    
    prod_col1, prod_col2 = st.columns(2)
    
    with prod_col1:
        st.markdown("""
        <div class="product-card">
            <span style="background:#e67e22; padding:4px 15px; border-radius:40px; color:white; font-size: 0.9rem; font-weight: bold;">⭐ الأكثر طلباً</span>
            <h3 style="color:#f39c12 !important; margin-top:15px; margin-bottom:15px;">SheroWhey مانجو وكركمين</h3>
            
            <img src="https://images.unsplash.com/photo-1560512823-829485b8bf24?w=400&auto=format&fit=crop&q=80" style="width:100%; border-radius:15px; margin-bottom:15px;" />
            
            <div style="direction: rtl; text-align: right; background: #252525; padding: 15px; border-radius: 12px; border: 1px dashed #f9a825; color: #ffffff !important;">
                <p><b>📋 المكونات:</b> شرش سائل، بيوريه مانجو طبيعي، سكر، مستخلص كركمين نشط، مثبتات قوام طبيعية.</p>
                <hr style="margin: 10px 0; border: 0; border-top: 1px solid #444;">
                <p style="font-weight: bold; color: #f39c12 !important; margin-bottom: 5px;">📊 الحقائق الغذائية (لكل حصة):</p>
                <ul style="margin-right: 20px; font-size: 0.95rem; color: #ffffff !important;">
                    <li>السعرات الحرارية: 112 kcal</li>
                    <li>إجمالي الدهون: 0.95 g</li>
                    <li>البروتين: 0.12 g</li>
                    <li>الكربوهيدرات: 25.10 g</li>
                </ul>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        st.write("")
        if st.button("🛍️ أطلب نكهة المانجو", key="btn_order_mango", use_container_width=True):
            st.success("🎯 تم تحديد المانجو! تقدر دلوقتي تنقل لتبويب 'إدارة وتنفيذ الطلبات السريعة' لتأكيد بياناتك.")

    with prod_col2:
        st.markdown("""
        <div class="product-card">
            <span style="background:#e67e22; padding:4px 15px; border-radius:40px; color:white; font-size: 0.9rem; font-weight: bold;">🌟 جديد</span>
            <h3 style="color:#f39c12 !important; margin-top:15px; margin-bottom:15px;">SheroWhey فراولة ورمان</h3>
            
            <img src="https://images.unsplash.com/photo-1601004890684-d8cbf643f5f2?w=400&auto=format&fit=crop&q=80" style="width:100%; border-radius:15px; margin-bottom:15px;" />
            
            <div style="direction: rtl; text-align: right; background: #252525; padding: 15px; border-radius: 12px; border: 1px dashed #f9a825; color: #ffffff !important;">
                <p><b>📋 المكونات:</b> شرش سائل، سكر (سكروز)، بيوريه فراولة طبيعي، عصير رمان طبيعي، عسل جلوكوز، كريمة خفق، مواد مثبتة ومثخنات قوام (صمغ السليلوز E466 CMC)، منظم حموضة (حمض الستريك E330).</p>
                <p><b>طريقة الحفظ:</b> يحفظ مجمداً عند (-18°C) | <b>الحجم:</b> 120 مل | <b>م ق م 1185/2005 جـ1</b></p>
                <hr style="margin: 10px 0; border: 0; border-top: 1px solid #444;">
                <p style="font-weight: bold; color: #f39c12 !important; margin-bottom: 5px;">📊 الحقائق الغذائية (الحصة 92.6 جرام):</p>
                <ul style="margin-right: 20px; font-size: 0.95rem; color: #ffffff !important;">
                    <li>السعرات الحرارية: 116.42 kcal</li>
                    <li>إجمالي الدهون: 1.02 g | البروتين: 0.10 g</li>
                    <li>الكربوهيدرات: 26.71 g | الرماد: 0.87 g</li>
                    <li>الكالسيوم: 19.45 mg | البوتاسيوم: 165.01 mg | فيتامين سي: 20.46 mg</li>
                </ul>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        st.write("")
        if st.button("🛍️ أطلب نكهة الفراولة", key="btn_order_strawberry", use_container_width=True):
            st.success("🎯 تم تحديد الفراولة! تقدر دلوقتي تنقل لتبويب 'إدارة وتنفيذ الطلبات السريعة' لتأكيد بياناتك.")

    # الفوتر السفلي (Footer) المكتوب في الإسكتش
    st.markdown("""
        <br><br>
        <div style="text-align: center; color: #888888; font-size: 0.9rem; border-top: 1px solid #333; padding-top: 15px;">
            © octanova 2026 | جميع الحقوق محفوظة لمشروع SheroWhey
        </div>
    """, unsafe_allow_html=True)


# ==========================================
# التبويب الثاني: البوت (البانل الخاص بالاستفسارات)
# ==========================================
with tab2:
    st.markdown("### 🍦 SheroBot - أقدر أساعدك إزاي؟")
    st.info("اسألني عن مكونات الآيس كريم، فوايده، أو إزاي تطلب.")
    
    if st.button("🔄 محادثة جديدة", key="reset_btn"):
        st.session_state.chat = model.start_chat(history=[])
        st.rerun()

    if "chat" not in st.session_state:
        st.session_state.chat = model.start_chat(history=[])

    for message in st.session_state.chat.history:
        role = "assistant" if message.role == "model" else "user"
        with st.chat_message(role):
            st.markdown(message.parts[0].text)

    if prompt := st.chat_input("اكتب استفسارك هنا..."):
        with st.chat_message("user"):
            st.markdown(prompt)
        
        try:
            response = st.session_state.chat.send_message(prompt)
            with st.chat_message("assistant"):
                st.markdown(response.text)
        except Exception as e:
            st.error(f"حصلت مشكلة في الاتصال: {e}")


# ==========================================
# التبويب الثالث: لوحة التحكم والطلب السريع المطور (متعدد المنتجات)
# ==========================================
with tab3:
    st.markdown("### 📋 نموذج إتمام الشراء السريع المباشر")
    st.write("يمكنك تحديد الكميات المطلوبة من كل نكهة وتحديث الطلب فوراً:")

    st.markdown("---")
    st.markdown("#### 🍦 اختر النكهات والكميات المطلوبة:")
    
    # تقسيم المساحة لعرض النكهتين جنب بعض لتحديد الكمية
    col_mango, col_strawberry = st.columns(2)
    
    mango_ordered = False
    mango_qty = 0
    strawberry_ordered = False
    strawberry_qty = 0
    
    with col_mango:
        st.markdown("<div style='background: #1e1e1e; padding: 15px; border-radius: 10px; border: 1px solid #333333;'>", unsafe_allow_html=True)
        want_mango = st.checkbox("🥭 نكهة المانجو والكركمين", key="want_m")
        if want_mango:
            mango_ordered = True
            mango_qty = st.number_input("الكمية (عدد الأكواب):", min_value=1, max_value=50, value=1, key="qty_m")
        st.markdown("</div>", unsafe_allow_html=True)
        
    with col_strawberry:
        st.markdown("<div style='background: #1e1e1e; padding: 15px; border-radius: 10px; border: 1px solid #333333;'>", unsafe_allow_html=True)
        want_strawberry = st.checkbox("🍓 نكهة الفراولة والرمان", key="want_s")
        if want_strawberry:
            strawberry_ordered = True
            strawberry_qty = st.number_input("الكمية (عدد الأكواب):", min_value=1, max_value=50, value=1, key="qty_s")
        st.markdown("</div>", unsafe_allow_html=True)
        
    st.markdown("<br>", unsafe_allow_html=True)
    
    # بيانات العميل الأساسية
    customer_name = st.text_input("👤 الاسم الكامل (ثلاثي):", placeholder="اكتب اسمك هنا")
    customer_phone = st.text_input("📱 رقم الهاتف للتواصل:", placeholder="010xxxxxxxx")
    customer_address = st.text_area("🏠 العنوان بالتفصيل:", placeholder="المدينة، الحي، الشارع، رقم المنزل")
    
    order_notes = st.text_area("💬 ملاحظات إضافية:", placeholder="موعد التوصيل المناسب أو تعليمات خاصة")
    customer_rating = st.slider("⭐ قيم تجربة التسوق من 1 إلى 5 نجوم:", 1, 5, 5)

    # تجميع تفاصيل المنتجات بناءً على الاختيارات
    product_details = ""
    if mango_ordered:
        product_details += f"• SheroWhey مانجو وكركمين [الكمية: {mango_qty}]\n"
    if strawberry_ordered:
        product_details += f"• SheroWhey فراولة ورمان [الكمية: {strawberry_qty}]\n"
        
    if not mango_ordered and not strawberry_ordered:
        product_details = "• لم يتم اختيار أي نكهة بعد!\n"

    # بناء نص الرسالة المحدثة بالفاتورة الجديدة والاسم الموحد
    msg_template = f"""🛒 *طلب جديد ومتنوع من SheroWhey* 🛒

👤 الاسم: {customer_name}
📱 الهاتف: {customer_phone}
🏠 العنوان: {customer_address}

🍦 تفاصيل الطلبية:
{product_details}
⭐ التقييم: {customer_rating} من 5 نجوم

 📝 ملاحظات إضافية:
{order_notes if order_notes.strip() else "لا توجد ملاحظات"}
──────────────────────
يرجى تأكيد الطلب وحساب الإجمالي، شكراً لكم! 🙏"""

    # تحويل النص لـ URL encoded للروابط الخارجية بشكل سليم
    encoded_msg = urllib.parse.quote(msg_template)
    whatsapp_url = f"https://wa.me/201090416662?text={encoded_msg}"
    
    email_subject = urllib.parse.quote(f"طلب شراء متعدد جديد - SheroWhey من {customer_name}")
    email_body = urllib.parse.quote(msg_template)
    gmail_url = f"https://mail.google.com/mail/?view=cm&fs=1&to=sheroway78@gmail.com&su={email_subject}&body={email_body}"

    # أزرار الإجراءات الفورية
    st.markdown("#### 🚀 أزرار التنفيذ السريع:")
    col1, col2 = st.columns(2)
    
    with col1:
        st.link_button("📱 إرسال الطلب عبر الواتساب", whatsapp_url, use_container_width=True, disabled=(not mango_ordered and not strawberry_ordered))
        
    with col2:
        st.link_button("📧 إرسال الطلب عبر Gmail", gmail_url, use_container_width=True, disabled=(not mango_ordered and not strawberry_ordered))

    # معاينة الفاتورة قبل الإرسال
    with st.expander("👀 معاينة نص الفاتورة المتنوعة قبل الإرسال"):
        st.code(msg_template, language="markdown")
