import streamlit as st
import google.generativeai as genai
import urllib.parse
import re
from openai import OpenAI
import pandas as pd

# ==========================================
# 1. إعدادات الصفحة والـ CSS الاحترافي الشامل والمرن
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
    
    /* فرض خط Cairo على العناوين والفقرات والماركدوان بشكل آمن */
    h1, h2, h3, h4, h5, h6, p, span, label, button, .stMarkdown, .stMarkdown p {
        font-family: 'Cairo', sans-serif !important;
        color: #ffffff !important;
    }
    
    .stButton button, [data-testid="baseButton-secondary"] {
        font-family: 'Cairo', sans-serif !important;
    }

    /* كود الصور الذكي والكامل (Fit Width) */
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
        display: block !important;
        margin: 0 auto !important;
        border-radius: 12px;
    }

    /* 🛠️ هندسة التبويبات (Tabs) لتظهر كأزرار بارزة ومحاذاتها بشكل صحيح */
    div[data-testid="stTabs"] {
        margin-top: 65px !important;
    }

    div[data-testid="stTabs"] [data-baseweb="tab-list"] {
        display: flex !important;
        justify-content: flex-start !important;
        gap: 8px !important;
        background-color: #111116 !important;
        padding: 10px !important;
        border-radius: 16px !important;
        border: 1px solid #1f1f2e !important;
        width: 100% !important;
        overflow-x: auto !important;
        white-space: nowrap !important;
    }
    
    div[data-testid="stTabs"] [data-baseweb="tab"] {
        font-family: 'Cairo', sans-serif !important;
        font-size: 14px !important;
        font-weight: 700 !important;
        color: #a0a0ab !important;
        background-color: #161622 !important;
        border: 1px solid #222232 !important;
        border-radius: 10px !important;
        padding: 10px 16px !important;
        flex-grow: 1 !important;
        text-align: center !important;
        transition: all 0.3s ease !important;
    }
    
    div[data-testid="stTabs"] [data-baseweb="tab"]:hover {
        color: #ffffff !important;
        border-color: #f39c12 !important;
        background-color: #1c1c28 !important;
    }
    
    div[data-testid="stTabs"] [aria-selected="true"] {
        color: #0d0d11 !important;
        background-color: #f39c12 !important;
        border-color: #f39c12 !important;
        font-weight: 900 !important;
    }

    /* صناديق ومربعات التأصيل العلمي المتراصة */
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
        box-shadow: 0 10px 30px rgba(0,0,0,0.3) !important;
        display: inline-block !important;
    }
    
    .science-box p, .science-box span {
        font-family: 'Cairo', sans-serif !important;
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

    /* كروت محادثة البوت */
    div[data-testid="stChatMessage"] {
        direction: rtl !important;
        background-color: #14141c !important;
        border-radius: 12px;
        border: 1px solid #222232;
        padding: 15px;
        margin-bottom: 10px;
    }

    .badge-bar { margin: 20px 0; display: flex; justify-content: center; gap: 10px; flex-wrap: wrap; }
    .custom-badge { background: #1e1e2a; padding: 6px 16px; border-radius: 50px; font-size: 13px; border: 1px solid #f39c12; color: #f39c12; }
    .block-container { padding-top: 1.5rem !important; padding-bottom: 2rem !important; max-width: 92% !important; }
    
    /* سنترة وجدولة البيانات التغذوية */
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
    }
    .stTable td, .stTable td span {
        font-family: 'Cairo', sans-serif !important;
    }
    </style>
""", unsafe_allow_html=True)

# تهيئة الـ Session States
if "want_m" not in st.session_state: st.session_state.want_m = False
if "qty_m" not in st.session_state: st.session_state.qty_m = 1
if "want_s" not in st.session_state: st.session_state.want_s = False
if "qty_s" not in st.session_state: st.session_state.qty_s = 1
if "chat_history" not in st.session_state: st.session_state.chat_history = []
if "chosen_lat" not in st.session_state: st.session_state.chosen_lat = 30.0444
if "chosen_lon" not in st.session_state: st.session_state.chosen_lon = 31.2357

# ==========================================
# 2. إعدادات الـ APIs والـ Persona (حظر الأسعار)
# ==========================================
genai.configure(api_key=st.secrets["GEMINI_API_KEY"])

customer_service_persona = """
أنت مساعد خدمة عملاء ومستشار علمي ذكي جداً ودبلوماسي لمنتج "SheroWhey" (آيس كريم شربت وظيفي وصحي مبتكر من تطوير فريق أوكتانوفا بكلية الزراعة جامعة عين شمس لعام 2026).
المنتج مصنع باستبدال الجوامد اللادهنية الفرز (SNF) بشرش اللبن السائل الطبيعي الخام ومطابق للمواصفات القياسية المصرية 1185/2005 جـ1.

الموسوعة العلمية والتغذوية الخاصة بك:
1. شربت المانجو الطبيعي المدعم بالكركمين: يحتوي على المانجيفيرين والكركمينويدات لتعزيز المناعة ومضاد للأكسدة.
2. شربت الفراولة والرمان الطبيعي: يحتوي على الأنثوسيانين وحمض الإيلاجيك لدعم صحة القلب وضبط ضغط الدم.

⚠️ الرد الدبلوماسي الصارم بخصوص السعر:
إذا سألك المستخدم عن السعر، جاوبه كالتالي:
"يا فندم شيرو واي مش مجرد آيس كريم عادي، ده ابتكار غذائي وظيفي وصحي متكامل مصنع من مواد طبيعية 100% لتعزيز صحتك ومناعتك. بخصوص السعر وطرق الدفع، أول ما تشرفنا بتسجيل طلبك وتحديد الكمية في التبويب الرابع، الفريق المختص بالمعمل هينسق معاك فوراً ويبعتلك السعر المناسب وتفاصيل التوصيل لحد عندك!"

قواعد عامة: رد بلهجة مصرية ودودة ومحاذاة سنتر، وضع الكود للأتمتة عند الطلب: [SET_ORDER: MANGO=X, STRAWBERRY=Y]
"""
model_gemini = genai.GenerativeModel('gemini-2.5-flash', system_instruction=customer_service_persona)

client_meta = None
if "GROQ_API_KEY" in st.secrets:
    client_meta = OpenAI(base_url="https://api.groq.com/openai/v1", api_key=st.secrets["GROQ_API_KEY"])

# 3. بناء لوحة التبويبات الأربعة
tab1, tab2, tab3, tab4 = st.tabs([
    "✨ تجربة SheroWhey", 
    "🔬 التأصيل العلمي والاستدامة",
    "💬 المساعد الذكي SheroBot", 
    "🚀 تأكيد وإرسال الطلبات"
])

# ==========================================
# التبويب الأول: الكتالوج المقسم بالتساوي
# ==========================================
with tab1:
    st.write("")
    st.markdown("<h1 style='font-size: 55px; font-weight: 900;'>SheroWhey</h1>", unsafe_allow_html=True)
    st.markdown("<h3 style='color: #f39c12; font-weight: 600;'>معنى جديد للشربت | إنتاج شربت وظيفي مبتكر</h3>", unsafe_allow_html=True)
    
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
    with t1: st.markdown("<div class='science-box' style='max-width:100%;'><strong style='color:#f39c12;'>🎯 رؤيتنا وهدفنا الأساسي</strong><p style='font-size:13px; color:#ccc; margin-top:5px;'>تطوير منتجات وظيفية تدعم الصحة العامة وتعزز المناعة، لسد الفجوة بين المثلجات التقليدية والمتطلبات الصحية للمستهلك الواعي.</p></div>", unsafe_allow_html=True)
    with t2: st.markdown("<div class='science-box' style='max-width:100%;'><strong style='color:#f39c12;'>📈 ثقة المستهلك والأمان الحيوي</strong><p style='font-size:13px; color:#ccc; margin-top:5px;'>أثبتت الدراسات الميدانية للفريق أن 96% من المستهلكين رحبوا تماماً بفكرة استخدام الشرش في المنتج بمجرد معرفة فوائده البيئية والصحية.</p></div>", unsafe_allow_html=True)
    with t3: st.markdown("<div class='science-box' style='max-width:100%;'><strong style='color:#f39c12;'>📜 المواصفات القياسية المصرية</strong><p style='font-size:13px; color:#ccc; margin-top:5px;'>المنتج مصنع ومطور علمياً ومطابق تماماً للمواصفات القياسية المصرية رقم 1185 لسنة 2005 الجزء الأول الخاص بالمثلجات اللبنية وشربت الآيس كريم.</p></div>", unsafe_allow_html=True)

    st.markdown("<br><hr style='border-color:#222232;'><br>", unsafe_allow_html=True)
    st.markdown("<h2 style='font-weight:700; margin-bottom:30px;'>🍨 عبوات وحقائق SheroWhey الغذائية</h2>", unsafe_allow_html=True)
    
    col_right, col_left = st.columns(2, gap="large")
    
    with col_right:
        st.markdown("<div class='science-box' style='max-width:100%; margin:0;'>", unsafe_allow_html=True)
        st.markdown("<h3 style='color:#f39c12;'>🥭 شربت المانجو الطبيعي المدعم بالكركمين</h3>", unsafe_allow_html=True)
        st.markdown("<p style='font-size:14px; color:#ccc; line-height:1.5;'><b>المكونات الأصلية:</b> شرش سائل، سكر (سكروز)، بيوريه المانجو، عسل جلوكوز، كريمة خفق، مواد مثبتة (صمغ السليلوز CMC E466)، منظم لون ومضاد أكسدة طبيعي (كركمين E100)، منظم حموضة (حمض الستريك E330).</p>", unsafe_allow_html=True)
        st.markdown("<p style='font-size:13px; color:#e74c3c;'>⚠️ تنبيه الحساسية: يحتوي على مكونات الحليب (اللاكتوز والبروتينات) | الحجم: 120 مل</p>", unsafe_allow_html=True)
        try: st.image("mango_pack.png", use_container_width=True)
        except Exception: st.info("💡 يرجى التأكد من رفع ملف باسم mango_pack.png")
        
        st.table({
            "العنصر الغذائي": ["السعرات الحرارية", "إجمالي الدهون", "البروتين", "إجمالي الكربوهيدرات", "الرماد", "الكالسيوم", "البوتاسيوم", "فيتامين سي"],
            "الكمية في الحصة": ["117.7 kcal", "1.1 g", "0.11 g", "26.85 g", "0.64 g", "26.8 mg", "173.9 mg", "22.1 mg"]
        })
        if st.button("🛍️ إضافة عبوة المانجو", key="add_m_box", use_container_width=True):
            st.session_state.want_m = True; st.toast("🎯 تم إضافة شربت المانجو!"); st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)

    with col_left:
        st.markdown("<div class='science-box' style='max-width:100%; margin:0;'>", unsafe_allow_html=True)
        st.markdown("<h3 style='color:#f39c12;'>🍓 شربت الفراولة والرمان الطبيعي</h3>", unsafe_allow_html=True)
        st.markdown("<p style='font-size:14px; color:#ccc; line-height:1.5;'><b>المكونات الأصلية:</b> شرش سائل، سكر (سكروز)، بيوريه فراولة، عصير رمان طبيعي، عسل جلوكوز، كريمة خفق، مواد مثبتة مثخنات قوام (صمغ السليلوز CMC E466)، منظم حموضة (حمض الستريك E330).</p>", unsafe_allow_html=True)
        st.markdown("<p style='font-size:13px; color:#e74c3c;'>⚠️ تنبيه الحساسية: يحتوي على مكونات الحليب (اللاكتوز والبروتينات) | الحجم: 120 مل</p>", unsafe_allow_html=True)
        try: st.image("strawberry_pack.png", use_container_width=True)
        except Exception: st.info("💡 يرجى التأكد من رفع ملف باسم strawberry_pack.png")
        
        st.table({
            "العنصر الغذائي": ["السعرات الحرارية", "إجمالي الدهون", "البروتين", "إجمالي الكربوهيدرات", "الرماد", "الكالسيوم", "البوتاسيوم", "فيتامين سي"],
            "الكمية في الحصة": ["116.42 kcal", "1.02 g", "0.10 g", "26.71 g", "0.87 g", "19.45 mg", "165.01 mg", "20.46 mg"]
        })
        if st.button("🛍️ إضافة عبوة الفراولة", key="add_s_box", use_container_width=True):
            st.session_state.want_s = True; st.toast("🎯 تم إضافة شربت الفراولة والرمان!"); st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)

# ==========================================
# التبويب الثاني: التأصيل العلمي والاستدامة
# ==========================================
with tab2:
    st.write("")
    st.markdown("<h2 class='centered-title' style='color:#f39c12; margin-bottom:30px;'>🔬 التأصيل العلمي والهوية الأكاديمية الكاملة للمشروع</h2>", unsafe_allow_html=True)
    try: st.image("team_photo.jpg", use_container_width=True)
    except Exception: st.info("💡 يرجى رفع ملف باسم team_photo.jpg لتظهر الصورة بالمنتصف")
        
    st.markdown("""
    <div class='science-box'>
        <span class='sub-heading'>🏫 الجهة الأكاديمية والبحثية</span>
        <b>الجهة:</b> كلية الزراعة - جامعة عين شمس | قسم علوم الأغذية (شعبة الألبان وصناعات الأغذية)<br>
        <b>المرحلة الدراسية:</b> طلبة المستوى الرابع (فريق أوكتانوفا - 2026)
    </div>
    <div class='science-box'>
        <span class='sub-heading'>👥 أسماء أعضاء فريق العمل بالكامل</span>
        <b>شعبة الألبان:</b> مصطفى صبحي | بسام عادل | رجب محمد | فؤاد سيد <br>
        <b>شعبة صناعات الأغذية:</b> نورهان محمد | مريم طارق | شمس محمود | منة الله عوض
    </div>
    <div class='science-box'>
        <span class='sub-heading'>👨‍🏫 الهيئة الإشرافية العليا</span>
        <b>أ.د. عزة فرحات</b> (أستاذ تكنولوجيا الألبان)<br>
        <b>د. نعمة سعيد</b> (مدرس تكنولوجيا الألبان)<br>
        <b>م.م. حسام الرحماني</b> (مدرس مساعد تكنولوجيا الألبان)<br>
        <b>أ. آيه أحمد إسماعيل</b> (معيدة بقسم علوم الأغذية)
    </div>
    <div class='science-box'>
        <span class='sub-heading'>🥛 القيمة الغذائية لشرش اللبن السائل الطبيعي</span>
        <b>لماذا الشرش؟</b> الشرش غني بالبروتينات عالية القيمة الحيوية (Whey Proteins)، واستخدامه بداخل صياغة الهيكل التكويني للشربت يعطي قواماً كريمياً ناعماً ومميزاً، ويعزز الامتصاص الحيوي الكامل للمواد الفعالة والنشطة مثل الكركمين في الجسم.
    </div>
    <div class='science-box'>
        <span class='sub-heading'>🌍 الجانب العلمي والبيئي والاستدامة (OUR SUSTAINABLE PLANET)</span>
        يُعتبر "الشرش السائل" ناتجاً ثانوياً ضخماً متخلفاً عن صناعة الأجبان، والتخلص منه دون معالجة يمثل عبئاً بيئياً كبيراً على شبكات الصرف ومستودعات المياه العذبة. قام الفريق بتحويل هذا التحدي البيئي إلى فرصة ابتكارية واعدة عبر استبدال المكون المائي الكامل والمواد الصلبة اللادهنية (SNF) للبن الفرز في الشربت بالشرش الحلو السائل الخام، لتحقيق معادلة الاستدامة وتقليل الهدر البيئي مع رفع القيمة الحيوية للمنتج الوظيفي النهائي (Zero Waste).
    </div>
    <div class='science-box'>
        <span class='sub-heading'>🧪 المركبات النشطة حيوياً والفوائد الصحية الموثقة</span>
        <p style='font-size:15px; line-height:1.8; text-align:right;'>
            <b>🥭 توليفة شربت المانجو والكركمين (التوليفة الذهبية لتعزيز المناعة):</b><br>
            • <b>المانجيفيرين:</b> مضاد أكسدة قوي مستخلص طبيعياً من ثمار المانجو.<br>
            • <b>الكركمينويدات:</b> المركب الفعال والنشط في الكركم بخصائصه الفريدة المضادة للالتهابات.<br>
            • <b>فيتامين C والكاروتينات:</b> لتعزيز نضارة الخلايا وحمايتها من الإجهاد التأكسدي، مع تكامل حيوي بين بروتينات الشرش والكركمين لزيادة معدل الامتصاص.<br><br>
            <b>🍓 توليفة شربت الفراولة والرمان (إنتعاش وصحة القلب):</b><br>
            • <b>الأنثوسيانين:</b> الصبغات الحمراء الطبيعية التي تحمي الأوعية الدموية وتدعم الدورة الدموية.<br>
            • <b>حمض الإيلاجيك:</b> متوفر بكثرة في الرمان لمكافحة الشوارد الحرة والمساعدة في ضبط ضغط الدم طبيعياً.<br>
            • <b>البولي فينولات:</b> لدعم الوظائف الحيوية ونشاط مضاد للميكروبات، وتعويض الفيتامينات والمعادن بفضل الشرش الحلو السائل.
        </p>
    </div>
    """, unsafe_allow_html=True)

# ==========================================
# التبويب الثالث: الشات الذكي
# ==========================================
with tab3:
    st.markdown("### 💬 SheroBot - مستشارك الذكي")
    if st.button("🗑️ مسح سجل المحادثة بالكامل", key="clear_chat_tab3"):
        st.session_state.chat_history = []; st.toast("🧹 تم تصفير المحادثة بنجاح!"); st.rerun()

    bot_avatar_url = "https://cdn-icons-png.flaticon.com/512/4712/4712035.png"
    user_avatar_url = "https://cdn-icons-png.flaticon.com/512/1144/1144709.png"

    for message in st.session_state.chat_history:
        current_avatar = bot_avatar_url if message["role"] == "assistant" else user_avatar_url
        with st.chat_message(message["role"], avatar=current_avatar): st.markdown(message["text"])

    if prompt := st.chat_input("اكتب استفسارك التغذوي أو العلمي هنا..."):
        with st.chat_message("user", avatar=user_avatar_url): st.markdown(prompt)
        st.session_state.chat_history.append({"role": "user", "text": prompt})
        
        raw_text = ""
        try: response = model_gemini.generate_content(prompt); raw_text = response.text
        except Exception: raw_text = "خط الاتصال مشغول حالياً يا فندم، تفضل بالانتقال للتبويب الأخير مباشرة لإتمام طلبك."

        if raw_text:
            match = re.search(r'\[SET_ORDER:\s*MANGO=(\d+),\s*STRAWBERRY=(\d+)\]', raw_text)
            if match:
                m_qty = int(match.group(1)); s_qty = int(match.group(2))
                if m_qty > 0: st.session_state.want_m = True; st.session_state.qty_m = m_qty
                if s_qty > 0: st.session_state.want_s = True; st.session_state.qty_s = s_qty
                st.toast("🛒 تم تحديث سلة المشتريات تلقائياً!")

            clean_display_text = re.sub(r'\[SET_ORDER:.*?\]', '', raw_text)
            clean_display_text = clean_display_text.replace("smart_toy", "").replace("face", "").replace(":", "")
            
            st.session_state.chat_history.append({"role": "assistant", "text": clean_display_text})
            with st.chat_message("assistant", avatar=bot_avatar_url): st.markdown(clean_display_text)
            st.rerun()

# ==========================================
# التبويب الرابع: استمارة الشحن والطلب السريع مع الخريطة الرسمية المستقرة
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
    st.markdown("#### 🗺️ موقع التوصيل الجغرافي")
    
    # 🛠️ استخدام الخريطة الرسمية والداخلية السريعة جداً لـ Streamlit لحل مشكلة المساحة الرمادية للأبد
    st.write("اختر إحداثيات موقعك عبر المؤشرات بالأسفل لتثبيت الدبوس على الخريطة الرسمية الحية:")
    
    sl_col1, sl_col2 = st.columns(2)
    with sl_col1:
        st.session_state.chosen_lat = st.slider("خط العرض (Latitude):", min_value=22.0, max_value=32.0, value=30.0444, step=0.0001, format="%.4f")
    with sl_col2:
        st.session_state.chosen_lon = st.slider("خط الطول (Longitude):", min_value=25.0, max_value=35.0, value=31.2357, step=0.0001, format="%.4f")
        
    # رص الداتا في DataFrame وعرض الخريطة التفاعلية الرسمية
    map_data_df = pd.DataFrame({'lat': [st.session_state.chosen_lat], 'lon': [st.session_state.chosen_lon]})
    st.map(map_data_df, zoom=12)

    st.markdown("#### 👤 بيانات الشحن والتواصل")
    c_col1, c_col2 = st.columns(2)
    with c_col1:
        customer_name = st.text_input("الاسم الكامل للعميل:")
        customer_phone = st.text_input("رقم الهاتف للتواصل:")
    with c_col2:
        generated_map_url = f"https://www.google.com/maps?q={st.session_state.chosen_lat},{st.session_state.chosen_lon}"
        customer_address = st.text_area("عنوان التوصيل (رابط الخريطة الحية مدمج):", value=f"تم تحديد إحداثيات التوصيل بدقة 📍\nرابط جوجل مابس المباشر للموقع المختار:\n{generated_map_url}")
    
    product_details = ""
    if st.session_state.want_m: product_details += f"• شربت مانجو وكركمين [الكمية: {st.session_state.qty_m} كوب]\n"
    if st.session_state.want_s: product_details += f"• شربت فراولة ورمان [الكمية: {st.session_state.qty_s} كوب]\n"
    if not st.session_state.want_m and not st.session_state.want_s: product_details = "• العربة فارغة!\n"

    msg_template = f"🛒 طلب شراء جديد لمنتج SheroWhey\n\n👤 العميل: {customer_name}\n📱 الهاتف: {customer_phone}\n🏠 العنوان واللوكيشن:\n{customer_address}\n\n🍦 تفاصيل الأكواب:\n{product_details}\n✨ إنتاج فريق أوكتانوفا 2026 - كلية الزراعة جامعة عين شمس"
    
    st.markdown("#### 🚀 تنفيذ الطلب السريع:")
    btn_col1, btn_col2 = st.columns(2)
    with btn_col1: st.link_button("📱 إرسال الطلب عبر الواتساب", f"https://wa.me/201090416662?text={urllib.parse.quote(msg_template)}", use_container_width=True, disabled=(not st.session_state.want_m and not st.session_state.want_s))
    with btn_col2: st.link_button("📧 إرسال الطلب عبر الإيميل", f"mailto:sheroway78@gmail.com?subject=Order&body={urllib.parse.quote(msg_template)}", use_container_width=True, disabled=(not st.session_state.want_m and not st.session_state.want_s))

    st.markdown("<br><br><div style='text-align: center; color: #666677; font-size: 0.9rem; border-top: 1px solid #222232; padding-top: 15px;'>© Octanova 2026 | جميع الحقوق محفوظة لمشروع SheroWhey 🍦</div>", unsafe_allow_html=True)
