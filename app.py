import streamlit as st
import google.generativeai as genai
import urllib.parse
import re
from openai import OpenAI
import folium
from streamlit_folium import st_folium

# ==========================================
# 1. إعدادات الصفحة والـ CSS الاحترافي الشامل والمرن
# ==========================================
st.set_page_config(page_title="SheroWhey | ابتكار أوكتانوفا 2026", page_icon="🍦", layout="wide")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@300;400;600;700;900&display=swap');
    
    html, body, [data-testid="stAppViewContainer"], [data-testid="stHeader"] {
        font-family: 'Cairo', sans-serif !important;
        background-color: #0d0d11 !important;
        color: #ffffff !important;
        direction: rtl !important;
    }
    
    h1, h2, h3, h4, h5, h6, p, span, label, button, .stMarkdown, .stMarkdown p, .stMarkdown div, .stMarkdown span {
        font-family: 'Cairo', sans-serif !important;
        text-align: center !important;
        color: #ffffff !important;
    }
    
    .stButton button, [data-testid="baseButton-secondary"] {
        font-family: 'Cairo', sans-serif !important;
    }

    [data-testid="stImage"] {
        display: flex !important;
        justify-content: center !important;
        align-items: center !important;
        width: 100% !important;
        max-width: 100% !important;
        margin: 10px auto !important;
    }
    [data-testid="stImage"] img {
        width: 100% !important;
        max-width: 100% !important;
        height: auto !important;
        border-radius: 12px;
    }

    div[data-testid="stTabs"] {
        width: 100% !important;
        margin-top: 30px !important;
    }
    div[data-testid="stTabs"] button {
        font-family: 'Cairo', sans-serif !important;
        font-size: 15px !important;
        font-weight: 600 !important;
        color: #8c8c9a !important;
        background-color: #14141c !important;
        border: 1px solid #1f1f2e !important;
        padding: 12px 15px !important;
        flex-grow: 1 !important;
        text-align: center !important;
    }
    div[data-testid="stTabs"] button[aria-selected="true"] {
        color: #f39c12 !important;
        background-color: #1c1c28 !important;
        border-bottom: 3px solid #f39c12 !important;
    }
    
    .science-box {
        background: linear-gradient(145deg, #14141c, #1a1a26) !important;
        border: 1px solid #222232 !important;
        border-radius: 20px !important;
        padding: 25px !important;
        margin-top: 15px !important;
        margin-bottom: 20px !important;
        width: 100% !important;
        max-width: 950px !important;
        margin-left: auto !important;
        margin-right: auto !important;
        text-align: center !important;
        box-shadow: 0 10px 30px rgba(0,0,0,0.3) !important;
        display: inline-block !important;
    }
    
    .science-box * {
        font-family: 'Cairo', sans-serif !important;
        text-align: center !important;
    }
    
    .sub-heading {
        font-family: 'Cairo', sans-serif !important;
        color: #f39c12 !important;
        font-size: 22px !important;
        font-weight: 700 !important;
        display: block !important;
        margin-bottom: 15px !important;
        border-bottom: 1px solid #222232 !important;
        padding-bottom: 10px !important;
        text-align: center !important;
    }

    div[data-testid="stChatMessage"] {
        direction: rtl !important;
        text-align: right !important;
        background-color: #14141c !important;
        border-radius: 12px;
        border: 1px solid #222232;
        padding: 15px;
        margin-bottom: 10px;
    }
    div[data-testid="stChatMessage"] p, div[data-testid="stChatMessage"] span, div[data-testid="stChatMessage"] div {
        text-align: right !important;
    }

    .badge-bar { margin: 20px 0; display: flex; justify-content: center; gap: 10px; flex-wrap: wrap; }
    .custom-badge { background: #1e1e2a; padding: 6px 16px; border-radius: 50px; font-size: 13px; border: 1px solid #f39c12; color: #f39c12; }
    .block-container { padding-top: 1.5rem !important; padding-bottom: 2rem !important; max-width: 92% !important; }
    
    .stTable table {
        background-color: #14141c !important;
        border-radius: 12px !important;
        overflow: hidden !important;
        border: 1px solid #222232 !important;
        width: 100% !important;
        max-width: 100% !important;
        margin: 10px auto !important;
    }
    .stTable th {
        background-color: #1c1c28 !important;
        color: #f39c12 !important;
        font-weight: 700 !important;
        text-align: center !important;
    }
    .stTable td, .stTable td span {
        font-family: 'Cairo', sans-serif !important;
        text-align: center !important;
    }
    </style>
""", unsafe_allow_html=True)

# تهيئة الـ Session States
if "want_m" not in st.session_state: st.session_state.want_m = False
if "qty_m" not in st.session_state: st.session_state.qty_m = 1
if "want_s" not in st.session_state: st.session_state.want_s = False
if "qty_s" not in st.session_state: st.session_state.qty_s = 1
if "chat_history" not in st.session_state: st.session_state.chat_history = []
# نقطة ارتكاز الخريطة الابتدائية (القاهرة)
if "map_center" not in st.session_state: st.session_state.map_center = [30.0444, 31.2357]
if "clicked_coords" not in st.session_state: st.session_state.clicked_coords = None

# ==========================================
# 2. إعدادات الـ APIs والـ Persona (حظر الأسعار)
# ==========================================
genai.configure(api_key=st.secrets["GEMINI_API_KEY"])

customer_service_persona = """
أنت مساعد خدمة عملاء ومستشار علمي ذكي لمنتج "SheroWhey" (آيس كريم شربت وظيفي وصحي مبتكر من تطوير فريق أوكتانوفا بكلية الزراعة جامعة عين شمس لعام 2026).

⚠️ قواعد صارمة جداً بخصوص الأسعار (مهم للغاية):
- ممنوع منعاً باتاً ذكر أي سعر أو تكلفة للمنتج تحت أي ظرف من الظروف.
- إذا سألك المستخدم "بكام؟" أو "ما هو السعر؟" أو "التكلفة كام؟"، يجب عليك الإجابة بالصيغة التالية فقط:
"لما تتواصل معاهم وتحدد طلبك هيبعتولك طرق الدفع ويحددو معاك السعر المناسب."

قواعد عامة:
- رد بلهجة مصرية ودودة جداً وموزونة ومحاذاة سنتر.
- إذا طلب العميل منك كمية ونوع، ضع هذا الكود بالملي في نهاية ردك للأتمتة: [SET_ORDER: MANGO=X, STRAWBERRY=Y]
- وجه العميل دائماً للتبويب الرابع لتسجيل الفاتورة.
"""
model_gemini = genai.GenerativeModel('gemini-2.5-flash', system_instruction=customer_service_persona)

client_meta = None
if "GROQ_API_KEY" in st.secrets:
    client_meta = OpenAI(base_url="https://api.groq.com/openai/v1", api_key=st.secrets["GROQ_API_KEY"])

# 3. بناء لوحة التبويبات
tab1, tab2, tab3, tab4 = st.tabs([
    "✨ تجربة SheroWhey", 
    "🔬 التأصيل العلمي والاستدامة",
    "💬 المساعد الذكي SheroBot", 
    "🚀 تأكيد وإرسال الطلبات"
])

# ==========================================
# التبويب الأول والثاني (محتوى الكتالوج والتأصيل)
# ==========================================
with tab1:
    st.write("")
    st.markdown("<h1 style='font-size: 55px; font-weight: 900; color: white; margin-bottom: 0;'>SheroWhey</h1>", unsafe_allow_html=True)
    st.markdown("<h3 style='color: #f39c12; font-weight: 600; margin-top: 0;'>معنى جديد للشربت | إنتاج شربت وظيفي مبتكر</h3>", unsafe_allow_html=True)
    
    st.markdown("""
    <div style='max-width: 850px; font-size: 17px; color: #b3b3b3; line-height: 1.8; margin-left: auto; margin-right: auto;'>
        🚀 <b>ابتكار علمي مستدام من فكرة وتطوير فريق أوكتانوفا 2026</b><br>
        • يقوم المشروع على فكرة هندسية متطورة في تكنولوجيا الألبان والأغذية عبر استبدال الجوامد اللادهنية للبن الفرز (SNF) بالكامل بشرش اللبن السائل الحلو الخام.
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class='badge-bar'>
        <span class='custom-badge'>🌿 100% شرش لبن طبيعي</span>
        <span class='custom-badge'>✨ قوام كريمي ناعم ونكهة غنية</span>
        <span class='custom-badge'>♻️ Zero Waste صديق للبيئة</span>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    t1, t2, t3 = st.columns(3, gap="medium")
    with t1: st.markdown("<div class='science-box' style='max-width:100%;'><strong style='color:#f39c12;'>🎯 رؤيتنا وهدفنا الأساسي</strong><p style='font-size:13px; color:#ccc; margin-top:5px;'>تطوير منتجات وظيفية تدعم الصحة العامة وتعزز المناعة.</p></div>", unsafe_allow_html=True)
    with t2: st.markdown("<div class='science-box' style='max-width:100%;'><strong style='color:#f39c12;'>📈 ثقة المستهلك</strong><p style='font-size:13px; color:#ccc; margin-top:5px;'>أثبتت الدراسات الميدانية للفريق أن 96% من المستهلكين رحبوا بالفكرة.</p></div>", unsafe_allow_html=True)
    with t3: st.markdown("<div class='science-box' style='max-width:100%;'><strong style='color:#f39c12;'>📜 المواصفات القياسية</strong><p style='font-size:13px; color:#ccc; margin-top:5px;'>المنتج مطابق تماماً للمواصفات القياسية المصرية رقم 1185 لسنة 2005 جـ1.</p></div>", unsafe_allow_html=True)

    st.markdown("<br><hr style='border-color:#222232;'><br>", unsafe_allow_html=True)
    col_right, col_left = st.columns(2, gap="large")
    
    with col_right:
        st.markdown("<div class='science-box' style='max-width:100%; margin:0;'>", unsafe_allow_html=True)
        st.markdown("<h3 style='color:#f39c12; margin-top:0;'>🥭 شربت المانجو الطبيعي المدعم بالكركمين</h3>", unsafe_allow_html=True)
        try: st.image("mango_pack.png", use_container_width=True)
        except Exception: st.info("💡 يرجى التأكد من رفع ملف باسم mango_pack.png")
        st.table({"العنصر الغذائي": ["السعرات الحرارية", "إجمالي الدهون"], "الكمية في الحصة": ["117.7 kcal", "1.1 g"]})
        if st.button("🛍️ إضافة عبوة المانجو", key="add_m_box", use_container_width=True):
            st.session_state.want_m = True; st.toast("🎯 تم إضافة شربت المانجو!"); st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)

    with col_left:
        st.markdown("<div class='science-box' style='max-width:100%; margin:0;'>", unsafe_allow_html=True)
        st.markdown("<h3 style='color:#f39c12; margin-top:0;'>🍓 شربت الفراولة والرمان الطبيعي</h3>", unsafe_allow_html=True)
        try: st.image("strawberry_pack.png", use_container_width=True)
        except Exception: st.info("💡 يرجى التأكد من رفع ملف باسم strawberry_pack.png")
        st.table({"العنصر الغذائي": ["السعرات الحرارية", "إجمالي الدهون"], "الكمية في الحصة": ["116.42 kcal", "1.02 g"]})
        if st.button("🛍️ إضافة عبوة الفراولة", key="add_s_box", use_container_width=True):
            st.session_state.want_s = True; st.toast("🎯 تم إضافة شربت الفراولة!"); st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)

with tab2:
    st.markdown("<h2 class='centered-title' style='color:#f39c12; text-align:center;'>🔬 التأصيل العلمي والهوية الأكاديمية للمشروع</h2>", unsafe_allow_html=True)
    try: st.image("team_photo.jpg", use_container_width=True)
    except Exception: st.info("💡 يرجى رفع ملف باسم team_photo.jpg")
    st.markdown("<div class='science-box' style='width:100%;'><b>فريق عمل أوكتانوفا 2026 برحاب كلية الزراعة جامعة عين شمس</b></div>", unsafe_allow_html=True)

# ==========================================
# التبويب الثالث: الشات الذكي (حظر الأسعار التام)
# ==========================================
with tab3:
    st.markdown("### 💬 SheroBot - مستشارك الذكي")
    if st.button("🗑️ مسح سجل المحادثة", key="clear_chat_button"):
        st.session_state.chat_history = []; st.rerun()

    bot_avatar_url = "https://cdn-icons-png.flaticon.com/512/4712/4712035.png"
    user_avatar_url = "https://cdn-icons-png.flaticon.com/512/1144/1144709.png"

    for message in st.session_state.chat_history:
        with st.chat_message(message["role"], avatar=(bot_avatar_url if message["role"] == "assistant" else user_avatar_url)):
            st.markdown(message["text"])

    if prompt := st.chat_input("اكتب استفسارك التغذوي أو العلمي هنا..."):
        st.chat_message("user", avatar=user_avatar_url).markdown(prompt)
        st.session_state.chat_history.append({"role": "user", "text": prompt})
        
        try:
            response = model_gemini.generate_content(prompt)
            raw_text = response.text
        except Exception:
            raw_text = "خط الاتصال مشغول حالياً يا فندم، تفضل بالانتقال للتبويب الأخير مباشرة لإتمام طلبك."

        if raw_text:
            match = re.search(r'\[SET_ORDER:\s*MANGO=(\d+),\s*STRAWBERRY=(\d+)\]', raw_text)
            if match:
                m_qty = int(match.group(1)); s_qty = int(match.group(2))
                if m_qty > 0: st.session_state.want_m = True; st.session_state.qty_m = m_qty
                if s_qty > 0: st.session_state.want_s = True; st.session_state.qty_s = s_qty
                st.toast("🛒 تم تحديث سلة المشتريات تلقائياً!")

            clean_display_text = re.sub(r'\[SET_ORDER:.*?\]', '', raw_text)
            st.session_state.chat_history.append({"role": "assistant", "text": clean_display_text})
            st.rerun()

# ==========================================
# التبويب الرابع: استمارة الشحن مع الخريطة التفاعلية الفعالة (حفظ الدبوس)
# ==========================================
with tab4:
    st.markdown("### 📋 تأكيد الفاتورة وإتمام الطلب السريع")
    
    col_order_m, col_order_s = st.columns(2, gap="large")
    with col_order_m:
        st.checkbox("🥭 عبوة شربت المانجو والكركمين", key="want_m")
        if st.session_state.want_m: st.number_input("الكمية المطلوبة:", min_value=1, max_value=100, key="qty_m")
    with col_order_s:
        st.checkbox("🍓 عبوة شربت الفراولة والرمان", key="want_s")
        if st.session_state.want_s: st.number_input("الكمية المطلوبة:", min_value=1, max_value=100, key="qty_s")
        
    st.markdown("---")
    st.markdown("#### 🗺️ حدد موقع التوصيل على الخريطة (اضغط لتثبيت الدبوس)")
    
    # بناء وتوليد الخريطة التفاعلية
    m = folium.Map(location=st.session_state.map_center, zoom_start=11)
    
    # إذا كان العميل قد ضغط وحط دبوس بالفعل، نقوم بعرض الدبوس على الخريطة
    if st.session_state.clicked_coords:
        folium.Marker(
            location=st.session_state.clicked_coords,
            popup="موقع الشحن المختار",
            icon=folium.Icon(color="orange", icon="info-sign")
        ).add_to(m)
        
    # عرض الخريطة داخل جدار الحماية بـ Streamlit والتقاط إشارة الضغط
    map_data = st_folium(m, width="100%", height=400)
    
    # التقاط الإحداثيات عند ضغط المستخدم الفعلي على الخريطة
    if map_data and map_data.get("last_clicked"):
        clicked = map_data["last_clicked"]
        new_coords = [clicked["lat"], clicked["lng"]]
        if st.session_state.clicked_coords != new_coords:
            st.session_state.clicked_coords = new_coords
            st.toast("📌 تم تثبيت دبوس الموقع بنجاح على الخريطة!")
            st.rerun()

    st.markdown("#### 👤 بيانات الشحن والتواصل")
    c_col1, c_col2 = st.columns(2)
    with c_col1:
        customer_name = st.text_input("الاسم الكامل للعميل:")
        customer_phone = st.text_input("رقم الهاتف للتواصل:")
    with c_col2:
        # توليد الرابط المباشر الذكي بناءً على الدبوس المختار
        if st.session_state.clicked_coords:
            lat_val, lng_val = st.session_state.clicked_coords
            generated_map_url = f"https://www.google.com/maps?q={lat_val},{lng_val}"
            customer_address = st.text_area("عنوان التوصيل (رابط موقعك الحالي جاهز):", value=f"تم تحديد الموقع عبر الخريطة التفاعلية 📍\nرابط جوجل مابس المباشر لقسم الشحن:\n{generated_map_url}")
        else:
            customer_address = st.text_area("عنوان التوصيل بالتفصيل لشحن المنتج:", placeholder="اضغط على الخريطة بالأعلى لتوليد اللوكيشن تلقائياً، أو اكتبه هنا")
    
    product_details = ""
    if st.session_state.want_m: product_details += f"• شربت مانجو وكركمين [الكمية: {st.session_state.qty_m} كوب]\n"
    if st.session_state.want_s: product_details += f"• شربت فراولة ورمان [الكمية: {st.session_state.qty_s} كوب]\n"
    if not st.session_state.want_m and not st.session_state.want_s: product_details = "• العربة فارغة!\n"

    msg_template = f"🛒 طلب شراء جديد لمنتج SheroWhey\n\n👤 العميل: {customer_name}\n📱 الهاتف: {customer_phone}\n🏠 العنوان واللوكيشن:\n{customer_address}\n\n🍦 تفاصيل الأكواب:\n{product_details}\n✨ إنتاج فريق أوكتانوفا 2026 - كلية الزراعة جامعة عين شمس"
    
    st.markdown("#### 🚀 تنفيذ الطلب السريع:")
    btn_col1, btn_col2 = st.columns(2)
    with btn_col1: 
        st.link_button("📱 إرسال الطلب عبر الواتساب", f"https://wa.me/201090416662?text={urllib.parse.quote(msg_template)}", use_container_width=True, disabled=(not st.session_state.want_m and not st.session_state.want_s))
    with btn_col2: 
        st.link_button("📧 إرسال الطلب عبر الإيميل", f"mailto:sheroway78@gmail.com?subject=Order&body={urllib.parse.quote(msg_template)}", use_container_width=True, disabled=(not st.session_state.want_m and not st.session_state.want_s))

    st.markdown("<br><br><div style='text-align: center; color: #666677; font-size: 0.9rem; border-top: 1px solid #222232; padding-top: 15px;'>© Octanova 2026 | جميع الحقوق محفوظة لمشروع SheroWhey 🍦</div>", unsafe_allow_html=True)
