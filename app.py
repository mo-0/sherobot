import streamlit as st
import streamlit.components.v1 as components
import google.generativeai as genai
import urllib.parse  # مخصصة لتنسيق وتوليد روابط الواتساب والإيميل بشكل سليم

# 1. إعدادات الصفحة
st.set_page_config(page_title="Shero Whey | آيس كريم صحي", page_icon="🍦", layout="wide")

# 2. إعدادات البوت وسحب المفتاح بأمان
genai.configure(api_key=st.secrets["GEMINI_API_KEY"])

# شخصية خدمة العملاء لـ Shero Whey
customer_service_persona = """
أنت مساعد خدمة عملاء ذكي لمنتج "Shero Whey".
المنتج عبارة عن آيس كريم صحي طبيعي 100% مصنوع من شرش اللبن الطبيعي (Whey).
فوائد المنتج: غني بالكالسيوم، البوتاسيوم، الفيتامينات، وصديق للبيئة (Zero Waste).
الأنواع المتاحة: "مانجو والكركومين" و "فراولة ورمان".
أسلوبك: ودود، احترافي، مباشر، وتتحدث باللهجة المصرية.
ردودك يجب أن تكون قصيرة جداً ومقنعة، ووجّه العميل دائماً للذهاب لتبويب "تصفح المنتجات" أو "إدارة وتنفيذ الطلبات السريعة" لإتمام الطلب.
"""
model = genai.GenerativeModel('gemini-2.5-flash', system_instruction=customer_service_persona)

# 3. تقسيم الواجهة لثلاث تبويبات (Tabs)
tab1, tab2, tab3 = st.tabs([
    "🛒 تصفح المنتجات والطلب", 
    "💬 المساعد الذكي للاستفسارات", 
    "📋 إدارة وتنفيذ الطلبات السريعة"
])

# --- الهيدر العلوي والأقسام الثابتة (إضافة اللوجو الحقيقي) ---
# قمنا بتقسيم السطر العلوي بحيث يأخذ اللوجو مساحة صغيرة على اليمين تماماً مثل الإسكتش
col_brand, col_logo = st.columns([4, 1])

with col_brand:
    # عنوان البراند والترحيب على اليسار والمنتصف
    st.markdown("""
        <div style='text-align: right; direction: rtl; padding-top: 15px;'>
            <h1 style='color: #e67e22; margin-bottom: 0;'>Shero Whey</h1>
            <h3 style='color: #2c3e50; font-weight: normal; margin-top: 5px;'>✨ آيس كريم صحي طبيعي مبتكر من شرش اللبن</h3>
        </div>
    """, unsafe_allow_html=True)

with col_logo:
    # عرض اللوجو المرفوع بدلاً من الأيقونة التقليدية
    try:
        st.image("logo.jpg", use_column_width=True)
    except Exception:
        # حل بديل في حال لم يجد ملف الصورة أثناء التشغيل التجريبي
        st.markdown("<h1 style='text-align: center;'>🍦</h1>", unsafe_allow_html=True)

# المميزات السريعة أسفل الهيدر مباشرة
st.markdown("""
<div style='display: flex; justify-content: center; gap: 15px; flex-wrap: wrap; margin-bottom: 30px; direction: rtl;'>
    <span style='background: white; padding: 8px 20px; border-radius: 50px; font-weight: bold; color: #2e7d32; border: 2px solid #4caf50;'>🌿 شرش اللبن الطبيعي</span>
    <span style='background: white; padding: 8px 20px; border-radius: 50px; font-weight: bold; color: #2e7d32; border: 2px solid #4caf50;'>🥛 غني بالكالسيوم والبوتاسيوم</span>
    <span style='background: white; padding: 8px 20px; border-radius: 50px; font-weight: bold; color: #2e7d32; border: 2px solid #4caf50;'>🍊 فيتامينات ومضادات أكسدة</span>
    <span style='background: white; padding: 8px 20px; border-radius: 50px; font-weight: bold; color: #2e7d32; border: 2px solid #4caf50;'>♻️ Zero Waste صديق للبيئة</span>
</div>
""", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# --- كود الـ Carousel (نفس المنطق السابق بدون تغيير) ---
slides = [
    {
        "image": "https://images.unsplash.com/photo-1560512823-829485b8bf24?w=600&auto=format&fit=crop&q=80", 
        "title": "ابتكار طعم المانجو والكركومين 🥭",
        "description": "مزيج فريد ومدروس علمياً يجمع بين فوائد شرش اللبن الوظيفي ونكهة المانجو الطبيعية، معزز بمستخلص الكركومين النشط كمضاد أكسدة طبيعي يدعم صحتك وقوام الآيس كريم."
    },
    {
        "image": "https://images.unsplash.com/photo-1601004890684-d8cbf643f5f2?w=600&auto=format&fit=crop&q=80", 
        "title": "انتعاش الفراولة والرمان 🍓",
        "description": "تركيبة فاخرة ومبتكرة تمزج عصير الفراولة والرمان المركز مع بروتينات الشرش الحلو، لتمنحك قواماً كريمياً ناعماً ونكهة غنية بمضادات الأكسدة الطبيعية بدون مواد حافظة."
    },
    {
        "image": "https://images.unsplash.com/photo-1576092768241-dec231879fc3?w=600&auto=format&fit=crop&q=80", 
        "title": "رؤية مستدامة وصديقة للبيئة ♻️",
        "description": "مشروع Shero Whey يقوم على استغلال (الشرش الحلو السائل) الناتج من صناعة الألبان كبديل للمواد الصلبة اللادهنية (SNF)، لنساهم في تقليل الهلاك البيئي وتقديم منتج وظيفي أعلى في القيمة الغذائية."
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
        <h2 style='color: #bf5b1c; margin-bottom: 15px;'>{current_data['title']}</h2>
        <p style='font-size: 1.15rem; line-height: 1.7; color: #2c3e50;'>{current_data['description']}</p>
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

    # --- القسم السفلي: كروت المنتجات (The Grid) ---
    st.markdown("<h3 style='text-align: center; color: #2c3e50; margin-bottom:25px;'>🍨 منتجاتنا المتوفرة</h3>", unsafe_allow_html=True)
    
    prod_col1, prod_col2 = st.columns(2)
    
    with prod_col1:
        st.markdown("""
        <div class="product-card">
            <span style="background:#e67e22; padding:4px 15px; border-radius:40px; color:white; font-size: 0.9rem;">⭐ الأكثر طلباً</span>
            <h3 style="color:#bf5b1c; margin-top:15px;">Shero Whey مانجو والكركومين</h3>
            <p style="color: #555; margin: 15px 0;">مزيج فريد من شرش اللبن الطبيعي مع نكهة المانجو ومستخلص الكركومين النشط.</p>
        </div>
        """, unsafe_allow_html=True)
        # زر تفاعلي ينقله للـ Tab الثالثة للطلب السريع
        if st.button("طلب نكهة المانجو الآن 🥭", key="order_m", use_container_width=True):
            st.info("تم تفعيل الاختيار! فضلاً اذهب لتبويب 'إدارة وتنفيذ الطلبات السريعة' بالأسفل لإتمام بياناتك.")

    with prod_col2:
        st.markdown("""
        <div class="product-card">
            <span style="background:#e67e22; padding:4px 15px; border-radius:40px; color:white; font-size: 0.9rem;">🌟 جديد</span>
            <h3 style="color:#bf5b1c; margin-top:15px;">Shero Whey فراولة ورمان</h3>
            <p style="color: #555; margin: 15px 0;">تركيبة غنية وفاخرة ممزوجة بالفراولة والرمان الغنيين بمضادات الأكسدة الطبيعية.</p>
        </div>
        """, unsafe_allow_html=True)
        if st.button("طلب نكهة الفراولة الآن 🍓", key="order_s", use_container_width=True):
            st.info("تم تفعيل الاختيار! فضلاً اذهب لتبويب 'إدارة وتنفيذ الطلبات السريعة' بالأسفل لإتمام بياناتك.")


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
# التبويب الثالث: لوحة التحكم والطلب السريع (Streamlit Native)
# ==========================================
with tab3:
    st.markdown("### 📋 نموذج إتمام الشراء السريع المباشر")
    st.write("إذا واجهت أي مشكلة في إرسال الطلب من التبويب الأول، يمكنك ملء الاستمارة هنا والتنفيذ فوراً:")

    st.markdown("---")
    product_selection = st.radio(
        "🍦 اختر النكهة المفضلة:",
        ["Shero Whey مانجو والكركومين", "Shero Whey فراولة ورمان"],
        index=0
    )
    
    customer_name = st.text_input("👤 الاسم الكامل (ثلاثي):", placeholder="اكتب اسمك هنا")
    customer_phone = st.text_input("📱 رقم الهاتف للتواصل:", placeholder="010xxxxxxxx")
    customer_address = st.text_area("🏠 العنوان بالتفصيل:", placeholder="المدينة، الحي، الشارع، رقم المنزل")
    
    order_quantity = st.selectbox(
        "🔢 اختر الكمية المطلوبة:",
        ["كوب واحد", "كوبان", "3 أكواب", "4 أكواب", "5 أكواب فأكثر"]
    )
    
    order_notes = st.text_area("💬 ملاحظات إضافية:", placeholder="موعد التوصيل المناسب أو تعليمات خاصة")
    customer_rating = st.slider("⭐ قيم تجربة التسوق من 1 إلى 5 نجوم:", 1, 5, 5)

    msg_template = f"""🛒 *طلب جديد من Shero Whey* 🛒

👤 الاسم: {customer_name}
📱 الهاتف: {customer_phone}
🏠 العنوان: {customer_address}
🍦 المنتج: {product_selection}
🔢 الكمية: {order_quantity}
⭐ التقييم: {customer_rating} من 5 نجوم

 📝 ملاحظات إضافية:
{order_notes if order_notes.strip() else "لا توجد ملاحظات"}
──────────────────────
يرجى تأكيد الطلب، شكراً لكم! 🙏"""

    encoded_msg = urllib.parse.quote(msg_template)
    whatsapp_url = f"https://wa.me/201090416662?text={encoded_msg}"
    
    email_subject = urllib.parse.quote(f"طلب شراء جديد - Shero Whey من {customer_name}")
    email_body = urllib.parse.quote(msg_template)
    gmail_url = f"https://mail.google.com/mail/?view=cm&fs=1&to=sheroway78@gmail.com&su={email_subject}&body={email_body}"

    st.markdown("#### 🚀 أزرار التنفيذ السريع:")
    col1, col2 = st.columns(2)
    
    with col1:
        st.link_button("📱 إرسال الطلب عبر الواتساب", whatsapp_url, use_container_width=True)
        
    with col2:
        st.link_button("📧 إرسال الطلب عبر Gmail", gmail_url, use_container_width=True)

    with st.expander("👀 معاينة نص الرسالة اللي هتروح للدعم الفني"):
        st.code(msg_template, language="markdown")
