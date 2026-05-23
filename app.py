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

# ==========================================
# التبويب الأول: الويب سايت الأساسي (HTML)
# ==========================================
with tab1:
    html_code = """
    <!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0, user-scalable=yes" />
    <title>Shero Whey - آيس كريم صحي طبيعي</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background: #fefaf5; scroll-behavior: smooth; }
        section { padding: 20px; max-width: 1280px; margin: 0 auto; }
        .logo-header { display: flex; justify-content: space-between; align-items: center; max-width: 1300px; margin: 20px auto 0; padding: 0 20px; flex-wrap: wrap; gap: 15px; }
        .logo-circle { width: 85px; height: 85px; background-color: #f9e0b0; border-radius: 50%; display: flex; align-items: center; justify-content: center; box-shadow: 0 8px 18px rgba(0,0,0,0.1); border: 3px solid #f9a825; transition: transform 0.2s; overflow: hidden; cursor: pointer; }
        .logo-circle img { width: 100%; height: 100%; object-fit: cover; }
        .logo-placeholder { font-size: 2.2rem; font-weight: bold; color: #e67e22; text-align: center; line-height: 1.2; }
        .header-center { text-align: center; flex: 1; }
        .brand-name { font-size: 2rem; font-weight: bold; color: #e67e22; letter-spacing: 1px; }
        .product-features { display: flex; justify-content: center; gap: 20px; flex-wrap: wrap; margin: 30px 0 15px; }
        .feature { background: white; padding: 12px 28px; border-radius: 50px; font-size: 1.05rem; font-weight: bold; color: #2e7d32; border: 2px solid #4caf50; transition: transform 0.2s; cursor: default; }
        .product-description-box { background: linear-gradient(125deg, #fff8e7, #fef4e0); border-radius: 36px; padding: 35px 30px; margin: 35px auto; max-width: 1150px; border-right: 8px solid #f9a825; }
        .benefits-list { display: flex; justify-content: center; flex-wrap: wrap; gap: 20px; margin-top: 30px; }
        .benefit { background: white; padding: 12px 28px; border-radius: 40px; font-weight: bold; border: 2px solid #f9a825; cursor: default; }
        .section-title { color: #2c3e50; border-bottom: 4px solid #f9a825; padding-bottom: 12px; margin: 40px 0 30px; font-size: 2rem; text-align: center; display: inline-block; }
        .products { display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 40px; }
        .card { background: #fff; border-radius: 32px; padding: 25px 20px; box-shadow: 0 12px 28px rgba(0,0,0,0.08); text-align: center; transition: 0.3s; }
        .card:hover { transform: translateY(-8px); }
        .image-container { width: 220px; height: 220px; margin: 0 auto 20px; border-radius: 24px; overflow: hidden; background: #fff0df; border: 3px solid #f9a825; }
        .image-container img { width: 100%; height: 100%; object-fit: cover; }
        button.primary { background: linear-gradient(95deg, #f39c12, #e67e22); border: none; padding: 14px 28px; border-radius: 50px; font-weight: bold; color: white; cursor: pointer; transition: 0.25s; }
        button.primary:hover { transform: scale(1.02); box-shadow: 0 6px 12px rgba(230,126,34,0.3); }
        form { background: white; border-radius: 40px; padding: 35px; box-shadow: 0 20px 35px rgba(0,0,0,0.08); margin-top: 30px; }
        input, textarea, select { width: 100%; padding: 14px 18px; margin: 12px 0; border-radius: 34px; border: 2px solid #ffe0b5; background: #fffef7; font-family: inherit; font-size: 1rem; }
        input:focus, textarea:focus, select:focus { border-color: #f39c12; outline: none; box-shadow: 0 0 0 3px rgba(243,156,18,0.2); }
        label.radio-label { display: flex; align-items: center; padding: 14px 20px; margin: 12px 0; background: #fef9f0; border-radius: 60px; border: 1px solid #ffddb0; transition: 0.2s; cursor: pointer; }
        label.radio-label input { width: auto; margin-left: 15px; transform: scale(1.2); cursor: pointer; }
        .rating { direction: ltr; text-align: center; margin: 15px 0; }
        .rating span { font-size: 2.4rem; cursor: pointer; color: #ddd; margin: 0 4px; transition: 0.1s; }
        .rating span.active { color: #ffb400; }
        .message { background: #2e7d32; color: white; padding: 20px; border-radius: 60px; text-align: center; margin-bottom: 30px; font-weight: bold; }
        .hidden { display: none; }
        .action-buttons { display: flex; flex-wrap: wrap; gap: 15px; justify-content: center; margin-top: 25px; }
        .secondary-btn { background: #2c3e50; color: white; border: none; padding: 14px 28px; border-radius: 50px; font-weight: bold; cursor: pointer; font-size: 1rem; transition: 0.2s; }
        .secondary-btn:hover { transform: scale(1.02); filter: brightness(1.05); }
        .whatsapp-send { background: #25D366; }
        .gmail-send { background: #D14836; }
        .reset-btn { background: #7f8c8d; }
        footer { background: #1e2a36; color: #eceff1; text-align: center; padding: 45px 20px; margin-top: 70px; border-radius: 40px 40px 0 0; }
        .contact-info h3 { color: #f9a825; margin-bottom: 20px; }
        .social-btn { display: inline-block; padding: 12px 28px; border-radius: 60px; margin: 12px 8px; font-weight: bold; text-decoration: none; color: white; transition: 0.2s; }
        .social-btn:hover { transform: translateY(-2px); }
        .whatsapp-footer { background: #25D366; }
        .email-footer { background: #3498db; }
        .designer-credit { background: #f0f3f5; border-radius: 50px; padding: 12px 18px; display: inline-block; margin-top: 20px; color: #2c3e50; }
        .designer-credit span { color: #e67e22; font-weight: bold; }
        @media (max-width: 680px) { .image-container { width: 160px; height: 160px; } .brand-name { font-size: 1.5rem; } }
    </style>
</head>
<body>

<div class="logo-header">
    <div class="logo-circle" id="logoLeft"><div class="logo-placeholder" id="leftPlaceholder">🍦</div></div>
    <div class="header-center"><h2><span class="brand-name">Shero Whey</span> ✨ آيس كريم صحي طبيعي</h2></div>
    <div class="logo-circle" id="logoRight"><div class="logo-placeholder" id="rightPlaceholder">🥛</div></div>
</div>

<div class="product-features">
    <div class="feature">🌿 يحتوي على شرش اللبن الطبيعي</div>
    <div class="feature">🥛 غني بالكالسيوم (Ca) والبوتاسيوم (K)</div>
    <div class="feature">🍊 فيتامينات ومضادات أكسدة</div>
    <div class="feature">♻️ Zero Waste صديق للبيئة</div>
</div>

<section>
    <div style="text-align:center;"><h2 class="section-title">🍨 منتجات Shero Whey</h2></div>
    <div class="products">
        <div class="card">
            <div class="product-label" style="background:#e67e22; display:inline-block; padding:6px 20px; border-radius:40px; color:white;">⭐ الأكثر طلباً</div>
            <div class="image-container"><svg xmlns="http://www.w3.org/2000/svg" width="100%" height="100%"><rect width="100%" height="100%" fill="%23ffd966"/><text x="50%" y="55%" font-size="60" text-anchor="middle">🥭</text></svg></div>
            <h3 style="color:#bf5b1c;">Shero Whey مانجو والكركومين</h3>
            <p>مزيج فريد من شرش اللبن الطبيعي مع نكهة المانجو ومستخلص الكركومين النشط.</p>
        </div>
        <div class="card">
            <div class="product-label" style="background:#e67e22; display:inline-block; padding:6px 20px; border-radius:40px; color:white;">🌟 جديد</div>
            <div class="image-container"><svg xmlns="http://www.w3.org/2000/svg" width="100%" height="100%"><rect width="100%" height="100%" fill="%23f9b7b7"/><text x="50%" y="55%" font-size="60" text-anchor="middle">🍓</text></svg></div>
            <h3 style="color:#bf5b1c;">Shero Whey فراولة ورمان</h3>
            <p>تركيبة غنية وفاخرة ممزوجة بالفراولة والرمان الغنيين بمضادات الأكسدة الطبيعية.</p>
        </div>
    </div>
</section>

</body>
</html>
    """
    components.html(html_code, height=650, scrolling=True)

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

    # بناء الاستمارة عناصر بايثون أصلية
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

    # تجهيز وتنسيق نص الرسالة الجاهزة للإرسال
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

    # تحويل النص لـ URL encoded للروابط الخارجية
    encoded_msg = urllib.parse.quote(msg_template)
    
    # روابط التنفيذ
    whatsapp_url = f"https://wa.me/201090416662?text={encoded_msg}"
    
    email_subject = urllib.parse.quote(f"طلب شراء جديد - Shero Whey من {customer_name}")
    email_body = urllib.parse.quote(msg_template)
    gmail_url = f"https://mail.google.com/mail/?view=cm&fs=1&to=sheroway78@gmail.com&su={email_subject}&body={email_body}"

    # أزرار الإجراءات الفورية
    st.markdown("#### 🚀 أزرار التنفيذ السريع:")
    col1, col2 = st.columns(2)
    
    with col1:
        # زرار يفتح الواتساب مباشرة بالرسالة المكتوبة فوق
        st.link_button("📱 إرسال الطلب عبر الواتساب", whatsapp_url, use_container_width=True)
        
    with col2:
        # زرار يفتح الجيميل مباشرة ببيانات الإيميل المكتوبة
        st.link_button("📧 إرسال الطلب عبر Gmail", gmail_url, use_container_width=True)

    # ميزة إضافية: عرض شكل الفاتورة أو الرسالة قبل الإرسال
    with st.expander("👀 معاينة نص الرسالة اللي هتروح للدعم الفني"):
        st.code(msg_template, language="markdown")
