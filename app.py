import streamlit as st
import google.generativeai as genai
import urllib.parse
import re
from openai import OpenAI

# ==========================================
# 1. إعدادات الصفحة والـ CSS الاحترافي (Modern Grid Layout)
# ==========================================
st.set_page_config(page_title="SheroWhey | ابتكار أوكتانوفا 2026", page_icon="🍦", layout="wide")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@300;400;600;700;900&display=swap');
    
    /* ضبط أساس الصفحة والفونت الموحد الشامل */
    html, body, [data-testid="stAppViewContainer"], [data-testid="stHeader"] {
        font-family: 'Cairo', sans-serif !important;
        background-color: #0d0d11 !important;
        color: #ffffff !important;
        direction: rtl !important;
    }
    
    /* إجبار خط Cairo والسنترة على جميع المكونات بدون استثناء */
    h1, h2, h3, h4, h5, h6, p, span, label, button, .stMarkdown, .stMarkdown p, .stMarkdown div, .stMarkdown span {
        font-family: 'Cairo', sans-serif !important;
        text-align: center !important;
        color: #ffffff !important;
    }

    /* كود الصور الذكي والكامل (Fit Width) */
    [data-testid="stImage"] {
        display: flex !important;
        justify-content: center !important;
        align-items: center !important;
        width: 100% !important;
        margin: 10px auto !important;
    }
    [data-testid="stImage"] img {
        width: 100% !important;
        max-width: 100% !important;
        height: auto !important;
        border-radius: 12px;
    }

    /* التبويبات العلوية المريحة */
    div[data-testid="stTabs"] {
        width: 100% !important;
        margin-top: 20px !important;
    }
    div[data-testid="stTabs"] button {
        font-family: 'Cairo', sans-serif !important;
        font-size: 15px !important;
        font-weight: 600 !important;
        color: #8c8c9a !important;
        background-color: #14141c !important;
        border: 1px solid #1f1f2e !important;
        padding: 10px 15px !important;
        flex-grow: 1 !important;
    }
    div[data-testid="stTabs"] button[aria-selected="true"] {
        color: #f39c12 !important;
        background-color: #1c1c28 !important;
        border-bottom: 3px solid #f39c12 !important;
    }
    
    /* صناديق التأصيل العلمي والمنتجات (Glassmorphism Effect) */
    .custom-box {
        background: linear-gradient(145deg, #14141c, #1a1a26) !important;
        border: 1px solid #222232 !important;
        border-radius: 20px !important;
        padding: 20px !important;
        margin-bottom: 15px !important;
        text-align: center !important;
        box-shadow: 0 10px 30px rgba(0,0,0,0.3) !important;
        height: 100%; /* لضمان تساوي الطول في حالة الأعمدة */
    }

    /* إجبار الفونت داخل الصناديق */
    .custom-box * {
        font-family: 'Cairo', sans-serif !important;
    }

    .badge-bar { margin: 15px 0; display: flex; justify-content: center; gap: 10px; flex-wrap: wrap; }
    .custom-badge { background: #1e1e2a; padding: 5px 15px; border-radius: 50px; font-size: 12px; border: 1px solid #f39c12; color: #f39c12; }
    
    /* كروت محادثة البوت */
    div[data-testid="stChatMessage"] {
        direction: rtl !important;
        text-align: right !important;
        background-color: #14141c !important;
        border-radius: 12px;
        border: 1px solid #222232;
    }
    
    /* الجداول التغذوية */
    .stTable table {
        background-color: #14141c !important;
        border-radius: 12px !important;
        width: 100% !important;
        margin: 10px auto !important;
    }
    .stTable th { color: #f39c12 !important; font-weight: 700 !important; }
    </style>
""", unsafe_allow_html=True)

# تهيئة الـ Session States
if "want_m" not in st.session_state: st.session_state.want_m = False
if "qty_m" not in st.session_state: st.session_state.qty_m = 1
if "want_s" not in st.session_state: st.session_state.want_s = False
if "qty_s" not in st.session_state: st.session_state.qty_s = 1
if "chat_history" not in st.session_state: st.session_state.chat_history = []

# ==========================================
# 2. إعدادات الـ APIs
# ==========================================
genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
customer_service_persona = "أنت مساعد ذكي لمنتج SheroWhey، رد بلهجة مصرية ودودة جداً وموزونة ومحاذاة سنتر وبخط كايرو."
model_gemini = genai.GenerativeModel('gemini-2.5-flash', system_instruction=customer_service_persona)

# 3. بناء الواجهة
tab1, tab2, tab3, tab4 = st.tabs([
    "✨ تجربة SheroWhey", 
    "🔬 التأصيل العلمي والاستدامة",
    "💬 المساعد الذكي SheroBot", 
    "🚀 تأكيد وإرسال الطلبات"
])

# ==========================================
# التبويب الأول: الكتالوج الجديد (Tiled Layout & Side-by-Side Products)
# ==========================================
with tab1:
    st.markdown("<h1 style='font-size: 55px; font-weight: 900; color: white;'>SheroWhey</h1>", unsafe_allow_html=True)
    st.markdown("<h3 style='color: #f39c12; font-weight: 600; margin-top: -15px;'>معنى جديد للشربت | إنتاج شربت وظيفي مبتكر</h3>", unsafe_allow_html=True)
    
    st.markdown("""
    <div style='max-width: 850px; font-size: 17px; color: #b3b3b3; line-height: 1.8; margin: 0 auto;'>
        🚀 <b>ابتكار علمي مستدام من فكرة وتطوير فريق أوكتانوفا 2026</b><br>
        استبدال الجوامد اللادهنية للبن الفرز (SNF) بالكامل بشرش اللبن السائل الحلو الخام لتحقيق التوازن بين المذاق الاستوائي الفاخر والقيمة التغذوية الوظيفية.
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class='badge-bar'>
        <span class='custom-badge'>🌿 100% شرش لبن طبيعي</span>
        <span class='custom-badge'>✨ قوام كريمي ناعم</span>
        <span class='custom-badge'>♻️ Zero Waste صديق للبيئة</span>
    </div>
    """, unsafe_allow_html=True)

    # 🛠️ التعديل الأول: استبدال الكاروسيل بـ 3 مربعات ثابتة جنب بعض
    st.markdown("<br>", unsafe_allow_html=True)
    t1, t2, t3 = st.columns(3, gap="medium")
    with t1:
        st.markdown("<div class='custom-box'><strong style='color:#f39c12;'>🎯 رؤيتنا وهدفنا</strong><p style='font-size:13px; color:#ccc;'>تطوير منتجات وظيفية تدعم الصحة العامة وتعزز المناعة لسد الفجوة في السوق.</p></div>", unsafe_allow_html=True)
    with t2:
        st.markdown("<div class='custom-box'><strong style='color:#f39c12;'>📈 ثقة المستهلك</strong><p style='font-size:13px; color:#ccc;'>96% من المستهلكين رحبوا باستخدام الشرش بمجرد معرفة فوائده البيئية.</p></div>", unsafe_allow_html=True)
    with t3:
        st.markdown("<div class='custom-box'><strong style='color:#f39c12;'>📜 المعايير القياسية</strong><p style='font-size:13px; color:#ccc;'>مطابق للمواصفات المصرية 1185/2005 الجزء الأول للمثلجات اللبنية.</p></div>", unsafe_allow_html=True)

    st.markdown("<br><hr style='border-color:#222232;'><br>", unsafe_allow_html=True)
    
    # 🛠️ التعديل الثاني: المنتجين جنب بعض (Split Layout)
    st.markdown("<h2 style='font-weight:700; margin-bottom:30px;'>🍨 عبوات وحقائق SheroWhey الغذائية</h2>", unsafe_allow_html=True)
    
    col_left, col_right = st.columns(2, gap="large")
    
    with col_right: # المانجو على اليمين
        st.markdown("<div class='custom-box'>", unsafe_allow_html=True)
        st.markdown("<h3 style='color:#f39c12;'>🥭 شربت المانجو بالكركمين</h3>", unsafe_allow_html=True)
        try:
            st.image("mango_pack.png", use_container_width=True)
        except:
            st.info("ارفع صورة mango_pack.png")
        
        st.table({
            "العنصر الغذائي": ["سعرات", "بروتين", "كالسيوم"],
            "الحصة (100ج)": ["117.7 kcal", "0.11 g", "26.8 mg"]
        })
        if st.button("🛍️ إضافة المانجو", key="add_m_split", use_container_width=True):
            st.session_state.want_m = True
            st.toast("🎯 تم إضافة المانجو!")
        st.markdown("</div>", unsafe_allow_html=True)

    with col_left: # الفراولة على الشمال
        st.markdown("<div class='custom-box'>", unsafe_allow_html=True)
        st.markdown("<h3 style='color:#f39c12;'>🍓 شربت الفراولة والرمان</h3>", unsafe_allow_html=True)
        try:
            st.image("strawberry_pack.png", use_container_width=True)
        except:
            st.info("ارفع صورة strawberry_pack.png")
        
        st.table({
            "العنصر الغذائي": ["سعرات", "بروتين", "كالسيوم"],
            "الحصة (92ج)": ["116.42 kcal", "0.10 g", "19.45 mg"]
        })
        if st.button("🛍️ إضافة الفراولة", key="add_s_split", use_container_width=True):
            st.session_state.want_s = True
            st.toast("🎯 تم إضافة الفراولة!")
        st.markdown("</div>", unsafe_allow_html=True)

# ==========================================
# التبويب الثاني: التأصيل العلمي (رص المربعات عمودياً)
# ==========================================
with tab2:
    st.markdown("<h2 style='color:#f39c12; margin-bottom:30px;'>🔬 التأصيل العلمي والهوية الأكاديمية</h2>", unsafe_allow_html=True)
    
    blocks = [
        {"h": "🏫 الجهة الأكاديمية", "t": "جامعة عين شمس | كلية الزراعة | قسم علوم الأغذية (شعبة الألبان وصناعات)"},
        {"h": "👥 فريق أوكتانوفا 2026", "t": "مصطفى صبحي | بسام عادل | رجب محمد | فؤاد سيد | نورهان محمد | مريم طارق | شمس محمود | منة الله عوض"},
        {"h": "👨‍🏫 الهيئة الإشرافية", "t": "أ.د. عزة فرحات | د. نعمة سعيد | م.م. حسام الرحماني | أ. آيه أحمد إسماعيل"},
        {"h": "🥛 قيمة الشرش السائل", "t": "غني ببروتينات الشرش عالية القيمة، يعزز القوام وامتصاص المركبات النشطة حيوياً في الجسم."},
        {"h": "🌍 الابتكار المستدام", "t": "تحويل ناتج ثانوي ملوث للبيئة إلى مكون أساسي وظيفي، محققاً صفر نفايات (Zero Waste)."},
        {"h": "🧪 المركبات النشطة", "t": "مانجيفيرين، كركمينويدات، أنثوسيانين، وحمض الإيلاجيك لدعم المناعة وصحة القلب."}
    ]
    
    # عرض صورة الفريق في السنتر قبل الكتل
    st.markdown("<b style='color:#f39c12;'>📸 فريق البحث العلمي</b>", unsafe_allow_html=True)
    try:
        st.image("team_photo.jpg", use_container_width=True)
    except:
        st.info("ارفع team_photo.jpg")

    for block in blocks:
        st.markdown(f"""
        <div class='custom-box'>
            <span class='sub-heading'>{block['h']}</span>
            <p style='font-size:15px; line-height:1.7;'>{block['t']}</p>
        </div>
        """, unsafe_allow_html=True)

# ==========================================
# 🛠️ التبويب الثالث: الشات بأيقونات فلات أيكون (FlatIcon Style)
# ==========================================
with tab3:
    st.markdown("<h3 class='centered-title'>💬 SheroBot - مستشارك الذكي</h3>", unsafe_allow_html=True)
    
    if st.button("🗑️ مسح سجل المحادثة", use_container_width=True):
        st.session_state.chat_history = []
        st.rerun()

    # استخدام روابط أيقونات Modern ونظيفة جداً للبوت والمستخدم
    bot_icon = "https://cdn-icons-png.flaticon.com/512/4712/4712035.png"
    user_icon = "https://cdn-icons-png.flaticon.com/512/1144/1144709.png"

    for message in st.session_state.chat_history:
        icon = bot_icon if message["role"] == "assistant" else user_icon
        with st.chat_message(message["role"], avatar=icon): 
            st.markdown(message["text"])

    if prompt := st.chat_input("اسأل عن الفوائد الصحية أو اطلب عبوة..."):
        with st.chat_message("user", avatar=user_icon): st.markdown(prompt)
        st.session_state.chat_history.append({"role": "user", "text": prompt})
        
        try:
            response = model_gemini.generate_content(prompt)
            res_text = response.text.replace("smart_toy", "").replace("face", "")
            st.session_state.chat_history.append({"role": "assistant", "text": res_text})
            with st.chat_message("assistant", avatar=bot_icon): st.markdown(res_text)
        except:
            st.error("السيرفر مشغول حالياً")
        st.rerun()

# ==========================================
# التبويب الرابع: الطلب السريع
# ==========================================
with tab4:
    st.markdown("### 📋 تأكيد الفاتورة وإتمام الطلب")
    c1, c2 = st.columns(2)
    with c1: 
        st.checkbox("🥭 عبوة المانجو والكركمين", key="want_m")
        if st.session_state.want_m: st.number_input("الكمية:", 1, 100, key="qty_m")
    with c2: 
        st.checkbox("🍓 عبوة الفراولة والرمان", key="want_s")
        if st.session_state.want_s: st.number_input("الكمية:", 1, 100, key="qty_s")
    
    st.markdown("---")
    name = st.text_input("👤 الاسم الكامل:")
    phone = st.text_input("📱 رقم الهاتف:")
    addr = st.text_area("🏠 عنوان التوصيل:")
    
    msg = f"طلب شراء SheroWhey للعميل {name}"
    
    col_btn1, col_btn2 = st.columns(2)
    with col_btn1: st.link_button("📱 واتساب", f"https://wa.me/201090416662?text={urllib.parse.quote(msg)}", use_container_width=True)
    with col_btn2: st.link_button("📧 إيميل", f"mailto:octanova.team@example.com?subject=Order&body={urllib.parse.quote(msg)}", use_container_width=True)
    
    st.markdown("<br><p style='color:#666; font-size:12px;'>© Octanova 2026 | SheroWhey Project</p>", unsafe_allow_html=True)
