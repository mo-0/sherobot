import streamlit as st
import streamlit.components.v1 as components
import google.generativeai as genai
import urllib.parse  # مخصصة لتنسيق وتوليد روابط الواتساب والإيميل بشكل سليم
import re  # لمسح واستخراج أكواد الطلبات التلقائية من البوت
from openai import OpenAI  # 1. استيراد المكتبة الخاصة بالنموذج الاحتياطي (ميتا لاما)

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

# تهيئة الـ Session States للتحكم المباشر في الـ Widgets عن طريق الـ Keys
if "want_m" not in st.session_state:
    st.session_state.want_m = False
if "qty_m" not in st.session_state:
    st.session_state.qty_m = 1
if "want_s" not in st.session_state:
    st.session_state.want_s = False
if "qty_s" not in st.session_state:
    st.session_state.qty_s = 1

# ==========================================
# 2. إعدادات الـ APIs (جوجل + ميتا لاما)
# ==========================================
# إعداد السيرفر الأساسي (جيمناي من جوجل)
genai.configure(api_key=st.secrets["GEMINI_API_KEY"])

customer_service_persona = """
You are a highly precise and smart customer service and scientific assistant for "SheroWhey" functional frozen dessert.
- Product info: Made with sweet liquid whey as a functional replacement for solids-not-fat (SNF) from skimmed milk, complying with Egyptian Standards (ES 1185/2005 Part 1).
- Flavors available: "Mango with Curcumin" (مانجو وكركمين) and "Strawberry with Pomegranate" (فراولة ورمان).

CRITICAL AUTOMATION RULE:
If the user explicitly mentions they want to order a specific flavor and quantity (e.g., "أريد 2 كوب مانجو", "I want 3 strawberry cups"), you MUST append a hidden command at the very end of your response text in this exact format:
[SET_ORDER: MANGO=X, STRAWBERRY=Y]
Replace X and Y with the integer quantities requested. If a flavor is not ordered, set it to 0.
Example: If they want 2 mango, append: [SET_ORDER: MANGO=2, STRAWBERRY=0]

Language Rules:
1. If asked in Arabic, reply in friendly Egyptian Arabic.
2. If asked in English, reply in perfect English.
Always be polite and let them know that you have prepared their cart in the third tab!
"""
model_gemini = genai.GenerativeModel('gemini-2.5-flash', system_instruction=customer_service_persona)

# 2. إعداد السيرفر الاحتياطي (ميتا لاما عبر منصة Groq) باستخدام المفتاح اللي ضفناه في السيكرتس
client_meta = None
if "GROQ_API_KEY" in st.secrets:
    client_meta = OpenAI(
        base_url="https://api.groq.com/openai/v1",
        api_key=st.secrets["GROQ_API_KEY"]
    )

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

    st.markdown("""
    <div style='display: flex; justify-content: center; gap: 15px; flex-wrap: wrap; margin-bottom: 30px; direction: rtl;'>
        <span style='background: #1e1e1e; padding: 8px 20px; border-radius: 50px; font-weight: bold; color: #4caf50; border: 2px solid #4caf50;'>🌿 شرش اللبن الطبيعي</span>
        <span style='background: #1e1e1e; padding: 8px 20px; border-radius: 50px; font-weight: bold; color: #4caf50; border: 2px solid #4caf50;'>🥛 غني بالكالسيوم والبوتاسيوم</span>
        <span style='background: #1e1e1e; padding: 8px 20px; border-radius: 50px; font-weight: bold; color: #4caf50; border: 2px solid #4caf50;'>🍊 فيتامينات ومضادات أكسدة</span>
        <span style='background: #1e1e1e; padding: 8px 20px; border-radius: 50px; font-weight: bold; color: #4caf50; border: 2px solid #4caf50;'>♻️ Zero Waste صديق للبيئة</span>
    </div>
    """, unsafe_allow_html=True)

    slides = [
        {"image": "https://images.unsplash.com/photo-1560512823-829485b8bf24?w=600&auto=format&fit=crop&q=80", "title": "ابتكار طعم المانجو والكركمين 🥭", "description": "مزيج فريد ومدروس علمياً يجمع بين فوائد شرش اللبن الوظيفي ونكهة المانجو الطبيعية، معزز بمستخلص الكركمين النشط كمضاد أكسدة طبيعي يدعم صحتك وقوام الآيس كريم."},
        {"image": "https://images.unsplash.com/photo-1601004890684-d8cbf643f5f2?w=600&auto=format&fit=crop&q=80", "title": "SheroWhey فراولة ورمان 🍓", "description": "الابتكار في كل ملعقة! استمتع بالانتعاش الحقيقي والمذاق المتوازن مع توليفة مبتكرة تجمع بين حلاوة الفراولة الطبيعية ونكهة الرمان الغنية. تم تصنيعه بقاعدة مميزة من الشرش السائل الطبيعي لتقديم قوام ناعم وخفيف ومثالي."},
        {"image": "https://images.unsplash.com/photo-1576092768241-dec231879fc3?w=600&auto=format&fit=crop&q=80", "title": "رؤية مستدامة وصديقة للبيئة ♻️", "description": "مشروع SheroWhey يقوم على استغلال (الشرش الحلو السائل) الناتج من صناعة الألبان كبديل للمواد الصلبة اللادهنية (SNF)، لنساهم في تقليل الهلاك البيئي وتقديم منتج وظيفي أعلى في القيمة الغذائية."}
    ]

    if 'current_slide' not in st.session_state:
        st.session_state.current_slide = 0

    def next_slide(): st.session_state.current_slide = (st.session_state.current_slide + 1) % len(slides)
    def prev_slide(): st.session_state.current_slide = (st.session_state.current_slide - 1) % len(slides)

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
        with btn_col1: st.button("⬅️ السابق", on_click=prev_slide, key="prev_btn", use_container_width=True)
        with btn_col3: st.button("التالي ➡️", on_click=next_slide, key="next_btn", use_container_width=True)

    with hero_col2:
        st.image(current_data['image'], use_column_width=True)
        dots = "".join(["● " if i == st.session_state.current_slide else "○ " for i in range(len(slides))])
        st.markdown(f"<div class='indicator-dots'>{dots}</div>", unsafe_allow_html=True)

    st.markdown("<br><hr><br>", unsafe_allow_html=True)

    st.markdown("<h2 style='text-align: center; color: #ffffff;'>🍨 منتجاتنا المتوفرة والتحليلات التغذوية</h2>", unsafe_allow_html=True)
    prod_col1, prod_col2 = st.columns(2)
    
    with prod_col1:
        st.markdown("<h3 style='color: #f39c12; text-align: center;'>🥭 SheroWhey مانجو وكركمين</h3>", unsafe_allow_html=True)
        st.image("https://images.unsplash.com/photo-1560512823-829485b8bf24?w=400&auto=format&fit=crop&q=80", use_column_width=True)
        st.markdown("<div style='direction: rtl; text-align: right; padding: 10px;'><p><b>📋 المكونات:</b> شرش سائل طبيعي، بيوريه مانجو طبيعي، سكر، مستخلص كركمين نشط، مثبتات قوام طبيعية.</p></div>", unsafe_allow_html=True)
        st.table({"العنصر الغذائي": ["السعرات الحرارية", "إجمالي الدهون", "البروتين", "الكربوهيدرات"], "الكمية لكل حصة": ["112 kcal", "0.95 g", "0.12 g", "25.10 g"]})
        if st.button("🛍️ أطلب نكهة المانجو الآن", key="btn_m_native", use_container_width=True):
            st.session_state.want_m = True
            st.toast("🎯 تم إضافة المانجو لعربتك!")
            st.rerun()

    with prod_col2:
        st.markdown("<h3 style='color: #f39c12; text-align: center;'>🍓 SheroWhey فراولة ورمان</h3>", unsafe_allow_html=True)
        st.image("https://images.unsplash.com/photo-1601004890684-d8cbf643f5f2?w=400&auto=format&fit=crop&q=80", use_column_width=True)
        st.markdown("<div style='direction: rtl; text-align: right; padding: 10px;'><p><b>📋 المكونات:</b> شرش سائل، سكر (سكروز)، بيوريه فراولة طبيعي، عصير رمان طبيعي، عسل جلوكوز، كريمة خفق، مواد مثبتة (E466 CMC)، حمض الستريك.</p></div>", unsafe_allow_html=True)
        st.table({"العنصر الغذائي": ["السعرات الحرارية", "إجمالي الدهون", "البروتين", "إجمالي الكربوهيدرات", "الكالسيوم", "البوتاسيوم"], "الكمية (حصّة 92.6 جرام)": ["116.42 kcal", "1.02 g", "0.10 g", "26.71 g", "19.45 mg", "165.01 mg"]})
        if st.button("🛍️ أطلب نكهة الفراولة الآن", key="btn_s_native", use_container_width=True):
            st.session_state.want_s = True
            st.toast("🎯 تم إضافة الفراولة لعربتك!")
            st.rerun()

# ==========================================
# التبويب الثاني: البوت المطور (جيمناي أساسي 🔄 ميتا لاما احتياطي)
# ==========================================
with tab2:
    st.markdown("### 🍦 SheroBot - المساعد الذكي التفاعلي")
    
    if st.button("🔄 محادثة جديدة / New Chat", key="reset_chat_btn"):
        st.session_state.chat = model_gemini.start_chat(history=[])
        st.rerun()

    if "chat" not in st.session_state:
        st.session_state.chat = model_gemini.start_chat(history=[])

    # عرض تاريخ الشات القديم ونظافته من الأكواد المخفية
    for message in st.session_state.chat.history:
        role = "assistant" if message.role == "model" else "user"
        clean_text = re.sub(r'\[SET_ORDER:.*?\]', '', message.parts[0].text)
        with st.chat_message(role):
            st.markdown(clean_text)

    if prompt := st.chat_input("اكتب استفسارك أو طلبك هنا..."):
        with st.chat_message("user"):
            st.markdown(prompt)
        
        raw_text = ""
        
        # ─── 1. محاولة إرسال الرسالة لـ جـيـمـنـاي (الأساسي) ───
        try:
            response = st.session_state.chat.send_message(prompt)
            raw_text = response.text
            
        # ─── 2. في حالة حدوث أي مشكلة في جوجل، التحويل التلقائي لـ مـيـتـا لاما (الاحتياطي) ───
        except Exception as e:
            if client_meta is not None:
                st.toast("⚠️ سيرفر جوجل مشغول، تم التحويل للمساعد الاحتياطي (Meta Llama) تلقائياً!")
                try:
                    # استدعاء نموذج لاما 3 من ميتا عبر Groq
                    meta_response = client_meta.chat.completions.create(
                        model="llama-3.1-8b-instant",
                        messages=[
                            {"role": "system", "content": customer_service_persona},
                            {"role": "user", "content": prompt}
                        ]
                    )
                    raw_text = meta_response.choices[0].message.content
                    
                    # مزامنة الرد اليدوي في تاريخ شات جيمناي عشان السياق ميفصلش لما يرجع يشتغل
                    st.session_state.chat.history.append(genai.types.Content(role="user", parts=[genai.types.Part.from_text(prompt)]))
                    st.session_state.chat.history.append(genai.types.Content(role="model", parts=[genai.types.Part.from_text(raw_text)]))
                except Exception as meta_err:
                    st.error(f"عذراً، هناك مشكلة عامة في الاتصال بالسيرفرات: {meta_err}")
            else:
                st.error("سيرفر جوجل غير متاح، ومفتاح السيرفر الاحتياطي غير مهيأ بعد في الـ Secrets.")

        # ─── 3. معالجة الرد النهائي وتحديث السلة (سواء خرج من جوجل أو ميتا) ───
        if raw_text:
            match = re.search(r'\[SET_ORDER:\s*MANGO=(\d+),\s*STRAWBERRY=(\d+)\]', raw_text)
            if match:
                m_qty = int(match.group(1))
                s_qty = int(match.group(2))
                if m_qty > 0:
                    st.session_state.want_m = True
                    st.session_state.qty_m = m_qty
                if s_qty > 0:
                    st.session_state.want_s = True
                    st.session_state.qty_s = s_qty
                st.toast("🛒 تم تحديث سلة مشترياتك تلقائياً!")

            final_display_text = re.sub(r'\[SET_ORDER:.*?\]', '', raw_text)
            with st.chat_message("assistant"):
                st.markdown(final_display_text)
            
            st.rerun()

# ==========================================
# التبويب الثالث: لوحة التحكم والطلب السريع
# ==========================================
with tab3:
    st.markdown("### 📋 نموذج إتمام الشراء السريع المباشر")
    st.write("البيانات في الأسفل تتحدث تلقائياً إذا طلبت من البوت أو من التبويب الأول:")

    st.markdown("---")
    st.markdown("#### 🍦 المنتجات الحالية في عربتك:")
    
    col_mango, col_strawberry = st.columns(2)
    
    with col_mango:
        want_mango = st.checkbox("🥭 نكهة المانجو والكركمين", key="want_m")
        if st.session_state.want_m:
            st.number_input("الكمية (عدد الأكواب):", min_value=1, max_value=50, key="qty_m")
        
    with col_strawberry:
        want_strawberry = st.checkbox("🍓 نكهة الفراولة والرمان", key="want_s")
        if st.session_state.want_s:
            st.number_input("الكمية (عدد الأكواب):", min_value=1, max_value=50, key="qty_s")
        
    st.markdown("<br>", unsafe_allow_html=True)
    
    customer_name = st.text_input("👤 الاسم الكامل (ثلاثي):", placeholder="اكتب اسمك هنا")
    customer_phone = st.text_input("📱 رقم الهاتف للتواصل:", placeholder="010xxxxxxxx")
    customer_address = st.text_area("🏠 العنوان بالتفصيل:", placeholder="المدينة، الحي، الشارع، رقم المنزل")
    order_notes = st.text_area("💬 ملاحظات إضافية:", placeholder="موعد التوصيل المناسب أو تعليمات خاصة")
    customer_rating = st.slider("⭐ قيم تجربة التسوق من 1 إلى 5 نجوم:", 1, 5, 5)

    product_details = ""
    if st.session_state.want_m: product_details += f"• SheroWhey مانجو وكركمين [الكمية: {st.session_state.qty_m}]\n"
    if st.session_state.want_s: product_details += f"• SheroWhey فراولة ورمان [الكمية: {st.session_state.qty_s}]\n"
    if not st.session_state.want_m and not st.session_state.want_s: product_details = "• لم يتم اختيار أي نكهة بعد!\n"

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
    gmail_url = f"https://mail.google.com/mail/?view=cm&fs=1&to=sheroway78@gmail.com&su={urllib.parse.quote(f'طلب جديد - SheroWhey من {customer_name}')}&body={urllib.parse.quote(msg_template)}"

    st.markdown("#### 🚀 أزرار التنفيذ السريع:")
    col1, col2 = st.columns(2)
    with col1: st.link_button("📱 إرسال الطلب عبر الواتساب", whatsapp_url, use_container_width=True, disabled=(not st.session_state.want_m and not st.session_state.want_s))
    with col2: st.link_button("📧 إرسال الطلب عبر Gmail", gmail_url, use_container_width=True, disabled=(not st.session_state.want_m and not st.session_state.want_s))
