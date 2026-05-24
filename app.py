import streamlit as st
import google.generativeai as genai
import urllib.parse
import re
from openai import OpenAI

# ==========================================
# 1. إعدادات الصفحة والـ CSS المودرن (Clean UI)
# ==========================================
st.set_page_config(page_title="SheroWhey | آيس كريم صحي", page_icon="🍦", layout="wide")

# ضبط الـ CSS بالكامل ليعطي المظهر العصري البسيط والمساحات الفاضية (White Space)
st.markdown("""
    <style>
    /* تغيير الخط العام للموقع ليكون نظيف ومودرن */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700&display=swap');
    
    html, body, [data-testid="stAppViewContainer"] {
        font-family: 'Inter', sans-serif;
        background-color: #0f0f11 !important; /* خلفية داكنة مطفية فاخرة */
    }
    
    /* تنسيق قائمة التبويبات العلوية (Tabs) لتصبح كأنها نيدبار موقع حقيقي */
    div[data-testid="stTabs"] button {
        font-size: 16px !important;
        font-weight: 400 !important;
        color: #888888 !important;
        background-color: transparent !important;
        border: none !important;
        padding: 10px 20px !important;
    }
    div[data-testid="stTabs"] button[aria-selected="true"] {
        color: #e67e22 !important;
        font-weight: 600 !important;
        border-bottom: 2px solid #e67e22 !important;
    }
    
    /* تنسيق البوت ومحادثة الشات (Direction auto) */
    div[data-testid="stChatMessage"] {
        direction: rtl !important;
        text-align: right !important;
        background-color: #16161a !important;
        border-radius: 15px;
        margin-bottom: 10px;
        border: 1px solid #232329;
    }
    div[data-testid="stChatMessage"] p {
        direction: auto !important;
    }
    
    /* كروت المنتجات العصرية المفتوحة (Clean Modern Cards) */
    .product-card {
        background-color: #16161a;
        border: 1px solid #232329;
        border-radius: 16px;
        padding: 24px;
        margin-bottom: 20px;
        transition: transform 0.3s ease, border-color 0.3s ease;
    }
    .product-card:hover {
        border-color: #e67e22;
        transform: translateY(-4px);
    }
    
    /* تحسين شكل جداول البيانات التغذوية لتبدو كأنها كروت بيانات */
    .stTable table {
        background-color: #1a1a22 !important;
        border-collapse: collapse !important;
        border-radius: 12px !important;
        overflow: hidden !important;
        border: none !important;
    }
    .stTable th {
        background-color: #23232f !important;
        color: #e67e22 !important;
        font-weight: 600 !important;
        padding: 12px !important;
        border: none !important;
    }
    .stTable td {
        padding: 12px !important;
        border-bottom: 1px solid #232329 !important;
        color: #ffffff !important;
    }
    
    /* تنسيق العناوين الكبيرة المودرن */
    .modern-title {
        font-size: 42px !important;
        font-weight: 700 !important;
        color: #ffffff !important;
        line-height: 1.2 !important;
        margin-bottom: 10px;
    }
    .modern-subtitle {
        font-size: 18px !important;
        color: #888888 !important;
        font-weight: 300 !important;
        margin-bottom: 30px;
    }
    </style>
""", unsafe_allow_html=True)

# تهيئة الـ Session States للتحكم المباشر في الـ Widgets عن طريق الـ Keys
if "want_m" not in st.session_state: st.session_state.want_m = False
if "qty_m" not in st.session_state: st.session_state.qty_m = 1
if "want_s" not in st.session_state: st.session_state.want_s = False
if "qty_s" not in st.session_state: st.session_state.qty_s = 1

# ==========================================
# 2. إعدادات الـ APIs (جوجل + ميتا لاما)
# ==========================================
genai.configure(api_key=st.secrets["GEMINI_API_KEY"])

customer_service_persona = """
أنت مساعد خدمة عملاء ذكي، ودود، واحترافي لمنتج "SheroWhey" (آيس كريم شربت وظيفي وصحي مبتكر من شرش اللبن الطبيعي).
الأنواع المتاحة: مانجو وكركمين، وفراولة ورمان.

⚠️ الحتمية اللغوية (قواعد صارمة جداً):
1. إذا قام المستخدم بكتابة رسالته باللغة الإنجليزية (English)، يجب عليك حتماً ولزاماً الرد باللغة الإنجليزية فقط وبشكل احترافي تماماً (Reply in English only).
2. إذا قام المستخدم بكتابة رسالته باللغة العربية، رد عليه باللغة العربية (اللهجة المصرية الودودة والواضحة)، ويُمنع تماماً خلط لغات أخرى أو حروف غريبة في النص.

قواعد عامة:
- ردودك ملخصة ومقنعة وتجيب بدقة علمية وتوجه العميل للتبويب الثالث لإتمام الشراء السريع.

قاعدة الأتمتة الإلزامية:
إذا طلب العميل كمية ونوع، ضع هذا الكود بالملي في نهاية الرد:
[SET_ORDER: MANGO=X, STRAWBERRY=Y]
"""

model_gemini = genai.GenerativeModel('gemini-2.5-flash', system_instruction=customer_service_persona)

client_meta = None
if "GROQ_API_KEY" in st.secrets:
    client_meta = OpenAI(base_url="https://api.groq.com/openai/v1", api_key=st.secrets["GROQ_API_KEY"])

# 3. تقسيم الواجهة لثلاث تبويبات (Tabs)
tab1, tab2, tab3 = st.tabs([
    "🎨 تصفح المنتجات", 
    "💬 المساعد الذكي", 
    "📋 تأكيد الطلب السريع"
])

# ==========================================
# التبويب الأول: الويب سايت التفاعلي المودرن (Clean Layout)
# ==========================================
with tab1:
    st.write("") # مساحة علوية فاضية
    
    # الهيدر المفتوح والمودرن بدون كروت مقفولة
    col_text, col_img = st.columns([1.2, 1], gap="large")
    
    with col_text:
        st.markdown("<h1 class='modern-title'>The World's First<br><span style='color:#e67e22;'>Functional Whey</span> Sherbet.</h1>", unsafe_allow_html=True)
        st.markdown("<p class='modern-subtitle'>ابتكار ألباني مصري 100٪ يستبدل الجوامد اللادهنية الفرز بشرش اللبن السائل الطبيعي لتقديم تجربة تحلية وظيفية ومستدامة.</p>", unsafe_allow_html=True)
        
        # التاجز السريعة بشكل ناعم ودائري
        st.markdown("""
        <div style='display: flex; gap: 10px; flex-wrap: wrap; margin-bottom: 25px; direction: rtl;'>
            <span style='background: #16161a; padding: 6px 16px; border-radius: 50px; font-size:14px; color: #4caf50; border: 1px solid #232329;'>🌿 شرش طبيعي</span>
            <span style='background: #16161a; padding: 6px 16px; border-radius: 50px; font-size:14px; color: #e67e22; border: 1px solid #232329;'>🥛 غني بالكالسيوم</span>
            <span style='background: #16161a; padding: 6px 16px; border-radius: 50px; font-size:14px; color: #2196f3; border: 1px solid #232329;'>♻️ Zero Waste</span>
        </div>
        """, unsafe_allow_html=True)
        
        # أزرار تحريك السلايدر
        if 'current_slide' not in st.session_state: st.session_state.current_slide = 0
        slides = [
            {"title": "ابتكار طعم المانجو والكركمين 🥭", "desc": "مزيج فريد يجمع فوائد الشرش الوظيفي ونكهة المانجو، معزز بالكركمين النشط كمضاد أكسدة يدعم القوام وصحتك."},
            {"title": "SheroWhey فراولة ورمان 🍓", "desc": "انتعاش حقيقي بقوام ناعم وخفيف متوازن تماماً، مصنع بقاعدة كاملة من الشرش السائل ومطابق للمواصفات القياسية المصرية."},
            {"title": "رؤية مستدامة صديقة للبيئة ♻️", "desc": "نعيد تدوير الشرش الناتج من صناعة الجبن لنحمي البيئة ونقدم منتجاً وظيفياً عالي القيمة الغذائية للفرد والمجتمع."}
        ]
        
        st.markdown(f"<div style='min-height:90px; direction:rtl; text-align:right;'><b style='color:#e67e22;'>{slides[st.session_state.current_slide]['title']}</b><br><span style='color:#aaa; font-size:14px;'>{slides[st.session_state.current_slide]['desc']}</span></div>", unsafe_allow_html=True)
        
        b_col1, b_col2, _ = st.columns([1, 1, 3])
        with b_col1:
            if st.button("⬅️ السابق", key="prev_btn", use_container_width=True):
                st.session_state.current_slide = (st.session_state.current_slide - 1) % len(slides)
                st.rerun()
        with b_col2:
            if st.button("التالي ➡️", key="next_btn", use_container_width=True):
                st.session_state.current_slide = (st.session_state.current_slide + 1) % len(slides)
                st.rerun()
                
    with col_img:
        carousel_images = [
            "https://images.unsplash.com/photo-1560512823-829485b8bf24?w=600&auto=format&fit=crop&q=80",
            "https://images.unsplash.com/photo-1601004890684-d8cbf643f5f2?w=600&auto=format&fit=crop&q=80",
            "https://images.unsplash.com/photo-1576092768241-dec231879fc3?w=600&auto=format&fit=crop&q=80"
        ]
        st.image(carousel_images[st.session_state.current_slide], use_container_width=True)

    st.markdown("<br><br><br>", unsafe_allow_html=True)
    
    # قسم عرض المنتجات بالكروت المودرن (Grid Layout)
    st.markdown("<h2 style='text-align: center; font-weight:700; margin-bottom:40px;'>🍨 Our Functional Catalog</h2>", unsafe_allow_html=True)
    
    prod_col1, prod_col2 = st.columns(2, gap="large")
    
    with prod_col1:
        st.markdown("""
        <div class='product-card' style='direction:rtl; text-align:right;'>
            <h3 style='color:#e67e22; margin-top:0;'>🥭 SheroWhey مانجو وكركمين</h3>
            <p style='color:#888; font-size:14px;'><b>المكونات:</b> شرش سائل طبيعي، بيوريه مانجو، سكر، مستخلص كركمين نشط، مثبتات طبيعية.</p>
        </div>
        """, unsafe_allow_html=True)
        st.image("https://images.unsplash.com/photo-1560512823-829485b8bf24?w=400&auto=format&fit=crop&q=80", use_container_width=True)
        st.table({"العنصر الغذائي": ["السعرات", "الدهون", "البروتين", "الكربوهيدرات"], "الحصة": ["112 kcal", "0.95 g", "0.12 g", "25.10 g"]})
        if st.button("🛍️ أطلب المانجو الآن", key="btn_m_native", use_container_width=True):
            st.session_state.want_m = True
            st.toast("🎯 تم إضافة المانجو لعربتك تلقائياً!")
            st.rerun()

    with prod_col2:
        st.markdown("""
        <div class='product-card' style='direction:rtl; text-align:right;'>
            <h3 style='color:#e67e22; margin-top:0;'>🍓 SheroWhey فراولة ورمان</h3>
            <p style='color:#888; font-size:14px;'><b>المكونات:</b> شرش سائل، بيوريه فراولة، عصير رمان طبيعي، عسل جلوكوز، كريمة خفق، مثبت قوام عالي الجودة.</p>
        </div>
        """, unsafe_allow_html=True)
        st.image("https://images.unsplash.com/photo-1601004890684-d8cbf643f5f2?w=400&auto=format&fit=crop&q=80", use_container_width=True)
        st.table({"العنصر الغذائي": ["السعرات", "الدهون", "البروتين", "الكالسيوم", "البوتاسيوم"], "الحصة": ["116.42 kcal", "1.02 g", "0.10 g", "19.45 mg", "165.01 mg"]})
        if st.button("🛍️ أطلب الفراولة الآن", key="btn_s_native", use_container_width=True):
            st.session_state.want_s = True
            st.toast("🎯 تم إضافة الفراولة لعربتك تلقائياً!")
            st.rerun()

# ==========================================
# التبويب الثاني: البوت المطور والمنقح لغوياً
# ==========================================
with tab2:
    st.markdown("### 💬 SheroBot")
    if "chat_history" not in st.session_state: st.session_state.chat_history = []
    
    for message in st.session_state.chat_history:
        with st.chat_message(message["role"]): st.markdown(message["text"])

    if prompt := st.chat_input("اكتب استفسارك أو طلبك هنا..."):
        with st.chat_message("user"): st.markdown(prompt)
        st.session_state.chat_history.append({"role": "user", "text": prompt})
        
        raw_text = ""
        try:
            response = model_gemini.generate_content(prompt)
            raw_text = response.text
        except Exception as e:
            if client_meta is not None:
                st.toast("⚠️ جاري المزامنة عبر السيرفر الاحتياطي...")
                try:
                    meta_response = client_meta.chat.completions.create(
                        model="llama-3.3-70b-versatile",
                        messages=[{"role": "system", "content": customer_service_persona}, {"role": "user", "content": prompt}]
                    )
                    raw_text = meta_response.choices[0].message.content
                except Exception:
                    raw_text = "⚠️ الضغط عالي حالياً، يرجى ملء بيانات الطلب في التبويب الأخير مباشرة!"
            else:
                raw_text = "⚠️ السيرفر مشغول، فضلاً استخدم تبويب تأكيد الطلب مباشرة."

        if raw_text:
            final_display_text = re.sub(r'\[SET_ORDER:.*?\]', '', raw_text)
            st.session_state.chat_history.append({"role": "assistant", "text": final_display_text})
            
            match = re.search(r'\[SET_ORDER:\s*MANGO=(\d+),\s*STRAWBERRY=(\d+)\]', raw_text)
            if match:
                m_qty = int(match.group(1)); s_qty = int(match.group(2))
                if m_qty > 0: st.session_state.want_m = True; st.session_state.qty_m = m_qty
                if s_qty > 0: st.session_state.want_s = True; st.session_state.qty_s = s_qty
                st.toast("🛒 تم تحديث عربتك تلقائياً!")

            with st.chat_message("assistant"): st.markdown(final_display_text)
            st.rerun()

# ==========================================
# التبويب الثالث: لوحة التحكم والطلب السريع
# ==========================================
with tab3:
    st.markdown("### 📋 Checkout")
    col_mango, col_strawberry = st.columns(2)
    
    with col_mango:
        want_mango = st.checkbox("🥭 نكهة المانجو والكركمين", key="want_m")
        if st.session_state.want_m: st.number_input("الكمية:", min_value=1, max_value=50, key="qty_m")
        
    with col_strawberry:
        want_strawberry = st.checkbox("🍓 نكهة الفراولة والرمان", key="want_s")
        if st.session_state.want_s: st.number_input("الكمية:", min_value=1, max_value=50, key="qty_s")
        
    st.markdown("<br>", unsafe_allow_html=True)
    customer_name = st.text_input("👤 الاسم الكامل:", placeholder="اكتب اسمك هنا")
    customer_phone = st.text_input("📱 رقم الهاتف:", placeholder="010xxxxxxxx")
    customer_address = st.text_area("🏠 العنوان بالتفصيل:", placeholder="المدينة، الحي، الشارع")
    
    product_details = ""
    if st.session_state.want_m: product_details += f"• SheroWhey مانجو [الكمية: {st.session_state.qty_m}]\n"
    if st.session_state.want_s: product_details += f"• SheroWhey فراولة [الكمية: {st.session_state.qty_s}]\n"
    if not st.session_state.want_m and not st.session_state.want_s: product_details = "• العربة فارغة\n"

    msg_template = f"🛒 *طلب جديد من SheroWhey*\n\n👤 الاسم: {customer_name}\n📱 الهاتف: {customer_phone}\n🏠 العنوان: {customer_address}\n\n🍦 الطلبية:\n{product_details}"
    
    col1, col2 = st.columns(2)
    with col1: st.link_button("📱 إرسال عبر الواتساب", f"https://wa.me/201090416662?text={urllib.parse.quote(msg_template)}", use_container_width=True, disabled=(not st.session_state.want_m and not st.session_state.want_s))
    with col2: st.link_button("📧 إرسال عبر Gmail", f"https://mail.google.com/mail/?view=cm&fs=1&to=sheroway78@gmail.com&su=Order&body={urllib.parse.quote(msg_template)}", use_container_width=True, disabled=(not st.session_state.want_m and not st.session_state.want_s))
