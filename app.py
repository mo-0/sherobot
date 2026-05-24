import streamlit as st
import streamlit.components.v1 as components
import google.generativeai as genai
import urllib.parse  # مخصصة لتنسيق وتوليد روابط الواتساب والإيميل بشكل سليم

# ==========================================
# 1. إعدادات الصفحة وجعلها متناسقة مع الـ Dark Mode
# ==========================================
st.set_page_config(page_title="SheroWhey | آيس كريم صحي", page_icon="🍦", layout="wide")

# ضبط الـ CSS لحل مشكلة اتجاه النصوص وتنسيق الجداول والبوت
st.markdown("""
    <style>
    /* إجبار اتجاه النص والدعم الكامل للعربي والإنجليزي في الشات */
    div[data-testid="stChatMessage"] {
        direction: rtl !important;
        text-align: right !important;
    }
    div[data-testid="stChatMessage"] p {
        direction: auto !important;
        text-align: right !important;
    }
    /* تحسين شكل الجداول الأصلية في بايثون لتناسب الدارك مود */
    .stTable {
        background-color: #1e1e1e !important;
        border-radius: 10px;
        overflow: hidden;
    }
    table {
        color: #ffffff !important;
    }
    th {
        background-color: #e67e22 !important;
        color: white !important;
    }
    /* تنسيق البانر العلوي */
    .hero-box {
        background: linear-gradient(135deg, #1e1e1e, #2d2d2d);
        border-radius: 25px;
        padding: 30px;
        border-right: 8px solid #f9a825;
        box-shadow: 0 4px 15px rgba(0,0,0,0.3);
        color: #ffffff !important;
    }
    .indicator-dots {
        font-size: 20px;
        text-align: center;
        color: #f9a825;
        margin-top: 10px;
    }
    </style>
""", unsafe_allow_html=True)

# ==========================================
# 2. إعدادات البوت وتطوير الـ Persona بدقة علمية ولغوية
# ==========================================
genai.configure(api_key=st.secrets["GEMINI_API_KEY"])

customer_service_persona = """
You are a highly precise and smart customer service and scientific assistant for "SheroWhey" functional frozen dessert (Sherbet).
- The product is a healthy, 100% natural ice cream alternative made with sweet liquid whey as a functional replacement for solids-not-fat (SNF) from skimmed milk, complying with Egyptian Standards (ES 1185/2005 Part 1).
- Flavors available: "Mango with Curcumin" and "Strawberry with Pomegranate".
- Health benefits: High in natural Calcium (Ca), Potassium (K), Vitamin C, rich in antioxidants, eco-friendly (Zero Waste concept).
- Language Rules: 
  1. If the user greets or asks in Arabic (e.g., "صلي على النبي", "whats the product"), reply in friendly Egyptian Arabic.
  2. If the user asks in English, reply in perfect, professional English.
  3. Provide highly accurate scientific and nutritional info when asked about ingredients, calculations, or data. Keep answers brief and direct.
"""
model = genai.GenerativeModel('gemini-2.5-flash', system_instruction=customer_service_persona)

# 3. تقسيم الواجهة لثلاث تبويبات (Tabs)
tab1, tab2, tab3 = st.tabs([
    "🛒 تصفح المنتجات والطلب", 
    "💬 المساعد الذكي للاستفسارات", 
    "📋 إدارة وتنفيذ الطلبات السريعة"
])

# ==========================================
# التبويب الأول: الويب سايت التفاعلي (Native Streamlit Elements)
# ==========================================
with tab1:
    # --- الهيدر العلوي والأقسام الثابتة ---
    col_brand, col_logo = st.columns([4, 1])

    with col_brand:
        st.markdown("""
            <div style='text-align: right; direction: rtl; padding-top: 15px;'>
                <h1 style='color: #e67e22 !important; margin-bottom: 0;'>SheroWhey</h1>
                <h3 style='color: #cccccc !important; font-weight: normal; margin-top: 5px;'>✨ شربت آيس كريم صحي طبيعي مبتكر من شرش اللبن</h3>
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
            "title": "SheroWhey فراولة ورمان 🍓",
            "description": "الابتكار في كل ملعقة! استمتع بالانتعاش الحقيقي والمذاق المتوازن مع توليفة مبتكرة تجمع بين حلاوة الفراولة الطبيعية ونكهة الرمان الغنية. تم تصنيعه بقاعدة مميزة من الشرش السائل الطبيعي لتقديم قوام ناعم وخفيف ومثالي."
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

    # --- القسم السفلي الجديد: تفكيك الكروت بالكامل بناءً على مقترحك ---
    st.markdown("<h2 style='text-align: center; color: #ffffff;'>🍨 منتجاتنا المتوفرة والتحليلات التغذوية</h2>", unsafe_allow_html=True)
    st.write("")

    prod_col1, prod_col2 = st.columns(2)
    
    # --- العمود الأول: المانجو والكركمين ---
    with prod_col1:
        st.markdown("<h3 style='color: #f39c12; text-align: center;'>🥭 SheroWhey مانجو وكركمين</h3>", unsafe_allow_html=True)
        st.image("https://images.unsplash.com/photo-1560512823-829485b8bf24?w=400&auto=format&fit=crop&q=80", use_column_width=True)
        
        st.markdown("""
        <div style="direction: rtl; text-align: right; padding: 10px;">
            <p><b>📋 المكونات:</b> شرش سائل طبيعي، بيوريه مانجو طبيعي، سكر، مستخلص كركمين نشط، مثبتات قوام طبيعية.</p>
        </div>
        """, unsafe_allow_html=True)
        
        # جدول البيانات التغذوية المانجو (بايثون الأصلي)
        mango_data = {
            "العنصر الغذائي": ["السعرات الحرارية", "إجمالي الدهون", "البروتين", "الكربوهيدرات"],
            "الكمية لكل حصة": ["112 kcal", "0.95 g", "0.12 g", "25.10 g"]
        }
        st.table(mango_data)
        
        if st.button("🛍️ أطلب نكهة المانجو الآن", key="btn_m_native", use_container_width=True):
            st.success("🎯 تم تحديد المانجو! فضلاً اذهب لتبويب 'إدارة وتنفيذ الطلبات السريعة' بالأسفل.")

    # --- العمود الثاني: الفراولة والرمان ---
    with prod_col2:
        st.markdown("<h3 style='color: #f39c12; text-align: center;'>🍓 SheroWhey فراولة ورمان</h3>", unsafe_allow_html=True)
        st.image("https://images.unsplash.com/photo-1601004890684-d8cbf643f5f2?w=400&auto=format&fit=crop&q=80", use_column_width=True)
        
        st.markdown("""
        <div style="direction: rtl; text-align: right; padding: 10px;">
            <p><b>📋 المكونات:</b> شرش سائل، سكر (سكروز)، بيوريه فراولة طبيعي، عصير رمان طبيعي، عسل جلوكوز، كريمة خفق، مواد مثبتة ومثخنات قوام (E466 CMC)، منظم حموضة (حمض الستريك E330).</p>
            <p><b>الحفظ والجودة:</b> يحفظ عند (-18°C) | الحجم: 120 مل | طبقاً للمواصفات القياسية المصرية (م ق م 1185/2005 جـ1).</p>
        </div>
        """, unsafe_allow_html=True)
        
        # جدول البيانات التغذوية الفراولة (بايثون الأصلي)
        strawberry_data = {
            "العنصر الغذائي": ["السعرات الحرارية", "إجمالي الدهون", "البروتين", "إجمالي الكربوهيدرات", "الرماد", "الكالسيوم", "البوتاسيوم", "فيتامين سي"],
            "الكمية (حصّة 92.6 جرام)": ["116.42 kcal", "1.02 g", "0.10 g", "26.71 g", "0.87 g", "19.45 mg", "165.01 mg", "20.46 mg"]
        }
        st.table(strawberry_data)
        
        if st.button("🛍️ أطلب نكهة الفراولة الآن", key="btn_s_native", use_container_width=True):
            st.success("🎯 تم تحديد الفراولة! فضلاً اذهب لتبويب 'إدارة وتنفيذ الطلبات السريعة' بالأسفل.")

    # الفوتر السفلي (Footer)
    st.markdown("""
        <br><br>
        <div style="text-align: center; color: #888888; font-size: 0.9rem; border-top: 1px solid #333; padding-top: 15px;">
            © octanova 2026 | جميع الحقوق محفوظة لمشروع SheroWhey
        </div>
    """, unsafe_allow_html=True)


# ==========================================
# التبويب الثاني: البوت المطور (دعم اللغات والاتجاهات الكاملة)
# ==========================================
with tab2:
    st.markdown("### 🍦 SheroBot - الذكاء الاصطناعي في خدمتك")
    st.info("Ask me about the product ingredients, nutrition facts, or how to order! / اسألني عن المكونات، الفوائد أو طريقة الطلب.")
    
    if st.button("🔄 محادثة جديدة / New Chat", key="reset_btn"):
        st.session_state.chat = model.start_chat(history=[])
        st.rerun()

    if "chat" not in st.session_state:
        st.session_state.chat = model.start_chat(history=[])

    for message in st.session_state.chat.history:
        role = "assistant" if message.role == "model" else "user"
        with st.chat_message(role):
            st.markdown(message.parts[0].text)

    if prompt := st.chat_input("Type your message here... / اكتب استفسارك هنا..."):
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
    
    customer_name = st.text_input("👤 الاسم الكامل (ثلاثي):", placeholder="اكتب اسمك هنا")
    customer_phone = st.text_input("📱 رقم الهاتف للتواصل:", placeholder="010xxxxxxxx")
    customer_address = st.text_area("🏠 العنوان بالتفصيل:", placeholder="المدينة، الحي، الشارع، رقم المنزل")
    
    order_notes = st.text_area("💬 ملاحظات إضافية:", placeholder="موعد التوصيل المناسب أو تعليمات خاصة")
    customer_rating = st.slider("⭐ قيم تجربة التسوق من 1 إلى 5 نجوم:", 1, 5, 5)

    product_details = ""
    if mango_ordered:
        product_details += f"• SheroWhey مانجو وكركمين [الكمية: {mango_qty}]\n"
    if strawberry_ordered:
        product_details += f"• SheroWhey فراولة ورمان [الكمية: {strawberry_qty}]\n"
        
    if not mango_ordered and not strawberry_ordered:
        product_details = "• لم يتم اختيار أي نكهة بعد!\n"

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

    encoded_msg = urllib.parse.quote(msg_template)
    whatsapp_url = f"https://wa.me/201090416662?text={encoded_msg}"
    
    email_subject = urllib.parse.quote(f"طلب شراء متعدد جديد - SheroWhey من {customer_name}")
    email_body = urllib.parse.quote(msg_template)
    gmail_url = f"https://mail.google.com/mail/?view=cm&fs=1&to=sheroway78@gmail.com&su={email_subject}&body={email_body}"

    st.markdown("#### 🚀 أزرار التنفيذ السريع:")
    col1, col2 = st.columns(2)
    
    with col1:
        st.link_button("📱 إرسال الطلب عبر الواتساب", whatsapp_url, use_container_width=True, disabled=(not mango_ordered and not strawberry_ordered))
        
    with col2:
        st.link_button("📧 إرسال الطلب عبر Gmail", gmail_url, use_container_width=True, disabled=(not mango_ordered and not strawberry_ordered))

    with st.expander("👀 معاينة نص الفاتورة المتنوعة قبل الإرسال"):
        st.code(msg_template, language="markdown")
