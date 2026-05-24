import streamlit as st
import google.generativeai as genai
import urllib.parse
import re
from openai import OpenAI

# ==========================================
# 1. إعدادات الصفحة والـ CSS المودرن (محاذاة للمنتصف وتصميم مرن)
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
        text-align: center !important; /* محاذاة كل شيء للمنتصف */
    }
    
    h1, h2, h3, h4, h5, h6, p, span, label {
        font-family: 'Cairo', sans-serif !important;
        text-align: center !important; /* محاذاة العناوين والنصوص للمنتصف */
        direction: rtl !important;
    }

    /* توزيع التبويبات بكامل العرض */
    div[data-testid="stTabs"] {
        width: 100% !important;
    }
    div[data-testid="stTabs"] button {
        font-family: 'Cairo', sans-serif !important;
        font-size: 15px !important;
        font-weight: 600 !important;
        color: #8c8c9a !important;
        background-color: #14141c !important;
        border: 1px solid #1f1f2e !important;
        padding: 10px 20px !important;
        flex-grow: 1 !important;
        text-align: center !important;
    }
    div[data-testid="stTabs"] button[aria-selected="true"] {
        color: #f39c12 !important;
        background-color: #1c1c28 !important;
        border-bottom: 3px solid #f39c12 !important;
    }
    
    /* تنسيق كروت الشات */
    div[data-testid="stChatMessage"] {
        direction: rtl !important;
        text-align: right !important; /* الشات يفضل يمين عشان القراءة الطبيعية للمحادثة */
        background-color: #14141c !important;
        border-radius: 12px;
        border: 1px solid #222232;
        padding: 15px;
    }
    
    /* كروت المعلومات المودرن سنتر */
    .info-card {
        background: linear-gradient(145deg, #14141c, #1a1a26);
        border: 1px solid #222232;
        border-radius: 16px;
        padding: 22px;
        margin-bottom: 15px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.2);
        width: 100% !important;
        text-align: center !important;
    }
    
    .badge-green, .badge-orange {
        padding: 4px 12px;
        border-radius: 30px;
        font-size: 13px;
        font-weight: 600;
        display: inline-block;
        margin: 4px;
    }
    .badge-green { background-color: rgba(46, 204, 113, 0.15); color: #2ecc71; border: 1px solid rgba(46, 204, 113, 0.3); }
    .badge-orange { background-color: rgba(243, 156, 18, 0.15); color: #f39c12; border: 1px solid rgba(243, 156, 18, 0.3); }
    
    /* ضبط محاذاة الجداول لتكون سنتر */
    .stTable table {
        background-color: #14141c !important;
        border-radius: 12px !important;
        overflow: hidden !important;
        border: 1px solid #222232 !important;
        width: 100% !important;
    }
    .stTable th {
        background-color: #1c1c28 !important;
        color: #f39c12 !important;
        font-weight: 700 !important;
        text-align: center !important;
    }
    .stTable td {
        text-align: center !important;
    }
    
    .block-container {
        padding-top: 2rem !important;
        padding-bottom: 2rem !important;
        padding-left: 3rem !important;
        padding-right: 3rem !important;
    }
    
    /* حاوية بديلة شيك للصور لحين رفعها */
    .photo-placeholder {
        background: #1b1b26; 
        border: 1px dashed #f39c12; 
        border-radius: 12px; 
        padding: 40px; 
        text-align: center; 
        color: #aaa; 
        font-size: 14px; 
        margin-bottom: 15px;
    }
    </style>
""", unsafe_allow_html=True)

# تهيئة الـ Session States
if "want_m" not in st.session_state: st.session_state.want_m = False
if "qty_m" not in st.session_state: st.session_state.qty_m = 1
if "want_s" not in st.session_state: st.session_state.want_s = False
if "qty_s" not in st.session_state: st.session_state.qty_s = 1

# ==========================================
# 2. إعدادات الـ APIs (جوجل + ميتا لاما)
# ==========================================
genai.configure(api_key=st.secrets["GEMINI_API_KEY"])

customer_service_persona = """
أنت مساعد خدمة عملاء ومستشار علمي ذكي لمنتج "SheroWhey" (آيس كريم شربت وظيفي وصحي مبتكر من تطوير فريق أوكتانوفا بكلية الزراعة جامعة عين شمس لعام 2026).
المنتج مصنع باستبدال الجوامد اللادهنية الفرز (SNF) بشرش اللبن السائل الطبيعي الخام ومطابق للمواصفات القياسية المصرية 1185/2005 جـ1.

الأنواع المتوفرة:
1. SheroWhey مانجو طبيعي مدعم بالكركمين.
2. SheroWhey فراولة ورمان طبيعي.

رد دائمًا بلهجة مصاروة ودودة وموزونة وبخط سليم، ووجههم للتبويب الرابع للشراء.
"""

model_gemini = genai.GenerativeModel('gemini-2.5-flash', system_instruction=customer_service_persona)

client_meta = None
if "GROQ_API_KEY" in st.secrets:
    client_meta = OpenAI(base_url="https://api.groq.com/openai/v1", api_key=st.secrets["GROQ_API_KEY"])

# 3. بناء لوحة التبويبات
tab1, tab2, tab3, tab4 = st.tabs([
    "🎨 كتالوج المنتجات التفاعلي", 
    "🔬 البعد العلمي والاستدامة",
    "💬 مساعد SheroBot الذكي", 
    "📋 تأكيد وإرسال الطلبات السريعة"
])

# ==========================================
# التبويب الأول: الكتالوج والويب سايت المحاذى بالكامل في المنتصف
# ==========================================
with tab1:
    st.write("")
    
    # 🛠️ تفكيك الفقرة الكبيرة تحت بعضها في المنتصف بدقة عالية
    st.markdown("<h1 style='font-size: 50px; font-weight: 900; color: #ffffff; margin-bottom: 5px;'>SheroWhey</h1>", unsafe_allow_html=True)
    st.markdown("<h3 style='color: #f39c12; font-weight: 600; margin-top: 0; margin-bottom: 20px;'>معنى جديد للشربت | إنتاج شربت وظيفي مبتكر</h3>", unsafe_allow_html=True)
    
    # تحويل الفقرة الكبيرة القديمة إلى أسطر منسقة ونقاط جذابة ومريحة جداً في القراءة
    st.markdown("""
    <div style='max-width: 800px; margin: 0 auto; font-size: 16px; color: #dddddd; line-height: 1.8; margin-bottom: 25px;'>
        <b>🎯 ابتكار علمي مستدام من فكرة وتطوير فريق أوكتانوفا 2026</b><br>
        • يقوم المشروع على فكرة هندسية متطورة في تكنولوجيا الألبان والأغذية.<br>
        • تم استبدال الجوامد اللادهنية للبن الفرز (SNF) بالكامل بشرش اللبن السائل الحلو الخام.<br>
        • نهدف إلى تحقيق التوازن المثالي بين المذاق الاستوائي الفاخر والقيمة الغذائية الحيوية الفائقة للمستهلك.
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div style='margin-bottom: 30px;'>
        <span class='badge-green'>🌿 100% شرش لبن سائل طبيعي</span>
        <span class='badge-orange'>✨ قوام كريمي ناعم ونكهة غنية</span>
        <span class='badge-green'>♻️ ابتكار بيئي مستدام (Zero Waste)</span>
    </div>
    """, unsafe_allow_html=True)
    
    # سلايدر معلومات البروشور التفاعلي (Centered)
    if 'current_slide' not in st.session_state: st.session_state.current_slide = 0
    slides = [
        {"title": "🎯 رؤيتنا وهدفنا الأساسي", "desc": "تتويج البحث العلمي بتطوير منتجات غذائية 'وظيفية' لا تكتفي بتقديم المذاق الرائع، بل تدعم الصحة العامة وتعزز المناعة، لسد الفجوة بين المثلجات التقليدية والمتطلبات الصحية العصرية للمستهلك الواعي."},
        {"title": "📈 ثقة المستهلك والأمان الحيوي", "desc": "أثبتت الدراسات الميدانية للفريق أن 96% من المستهلكين رحبوا تماماً بفكرة استخدام الشرش في المنتج بمجرد معرفة فوائده البيئية والصحية، مع التزامنا بأعلى معايير الجودة الحسية والأمان."},
        {"title": "📜 المواصفات القياسية المصرية", "desc": "المنتج مصنع ومطور علمياً داخل معامل القسم ومطابق تماماً للمواصفات القياسية المصرية رقم 1185 لسنة 2005 الجزء الأول الخاص بالمثلجات اللبنية وشربت الآيس كريم."}
    ]
    
    # عرض السلايدر في منتصف الصفحة
    slider_col1, slider_col2, slider_col3 = st.columns([1, 2, 1])
    with slider_col2:
        st.markdown(f"""
        <div class='info-card'>
            <strong style='color:#f39c12; font-size:17px;'>{slides[st.session_state.current_slide]['title']}</strong><br>
            <p style='color:#dddddd; font-size:14px; line-height:1.6; margin-top:8px; margin-bottom:15px;'>{slides[st.session_state.current_slide]['desc']}</p>
        </div>
        """, unsafe_allow_html=True)
        
        b1, b2 = st.columns([1, 1])
        with b1:
            if st.button("⬅️ السابق", key="p_slide", use_container_width=True):
                st.session_state.current_slide = (st.session_state.current_slide - 1) % len(slides)
                st.rerun()
        with b2:
            if st.button("التالي ➡️", key="n_slide", use_container_width=True):
                st.session_state.current_slide = (st.session_state.current_slide + 1) % len(slides)
                st.rerun()

    st.markdown("<br><hr style='border-color:#222232;'><br>", unsafe_allow_html=True)
    
    # قسم العبوات والحقائق الغذائية
    st.markdown("<h2 style='text-align: center; font-weight:700; margin-bottom:30px;'>🍦 كتالوج عبوات وحقائق SheroWhey الغذائية</h2>", unsafe_allow_html=True)
    
    prod_col1, prod_col2 = st.columns(2, gap="large")
    
    with prod_col1:
        st.markdown("""
        <div class='info-card'>
            <h3 style='color:#f39c12; margin-top:0;'>🥭 SheroWhey مانجو طبيعي مدعم بالكركمين</h3>
            <p style='font-size:14px; color:#ccc; line-height:1.5;'><b>المكونات الأصلية:</b> شرش سائل، سكر (سكروز)، بيوريه المانجو، عسل جلوكوز، كريمة خفق، مواد مثبتة (صمغ السليلوز)، كركمين طبيعي، حمض ستريك.</p>
            <p style='font-size:13px; color:#e74c3c; margin-bottom:0;'>⚠️ يحتوي على مكونات الحليب (اللاكتوز والبروتينات) | الحجم: 120 مل</p>
        </div>
        """, unsafe_allow_html=True)
        
        # 🛠️ استدعاء محلي لصورة عبوة المانجو
        try:
            st.image("mango_pack.jpg", caption="عبوة شربت المانجو والكركمين 120 مل", use_container_width=True)
        except Exception:
            st.markdown("<div class='photo-placeholder'>💡 [ارفع صورة العبوة هنا تحت اسم mango_pack.jpg]</div>", unsafe_allow_html=True)
        
        st.markdown("<b style='color:#f39c12;'>الحقائق الغذائية (حصة 100 جرام | 4oz):</b>", unsafe_allow_html=True)
        st.table({
            "العنصر الغذائي": ["السعرات الحرارية", "إجمالي الدهون", "البروتين", "إجمالي الكربوهيدرات", "الرماد", "الكالسيوم", "البوتاسيوم", "فيتامين سي"],
            "الكمية في الحصة": ["117.7 kcal", "1.1 g", "0.11 g", "26.85 g", "0.64 g", "26.8 mg", "173.9 mg", "22.1 mg"]
        })
        if st.button("🛍️ Tangy Mango - إضافة العبوة", key="add_mango_btn", use_container_width=True):
            st.session_state.want_m = True
            st.toast("🥭 تم إضافة شربت المانجو والكركمين لعربتك!")
            st.rerun()

    with prod_col2:
        st.markdown("""
        <div class='info-card'>
            <h3 style='color:#f39c12; margin-top:0;'>🍓 SheroWhey فراولة ورمان طبيعي</h3>
            <p style='font-size:14px; color:#ccc; line-height:1.5;'><b>المكونات الأصلية:</b> شرش سائل، سكر (سكروز)، بيوريه فراولة، عصير رمان طبيعي، عسل جلوكوز، كريمة خفق، مواد مثبتة، حمض ستريك.</p>
            <p style='font-size:13px; color:#e74c3c; margin-bottom:0;'>⚠️ يحتوي على مكونات الحليب (اللاكتوز والبروتينات) | الحجم: 120 مل</p>
        </div>
        """, unsafe_allow_html=True)
        
        # 🛠️ استدعاء محلي لصورة عبوة الفراولة والرمان
        try:
            st.image("strawberry_pack.jpg", caption="عبوة شربت الفراولة والرمان 120 مل", use_container_width=True)
        except Exception:
            st.markdown("<div class='photo-placeholder'>💡 [ارفع صورة العبوة هنا تحت اسم strawberry_pack.jpg]</div>", unsafe_allow_html=True)
        
        st.markdown("<b style='color:#f39c12;'>الحقائق الغذائية (حصة 92.6 جرام | 4oz):</b>", unsafe_allow_html=True)
        st.table({
            "العنصر الغذائي": ["السعرات الحرارية", "إجمالي الدهون", "البروتين", "إجمالي الكربوهيدرات", "الرماد", "الكالسيوم", "البوتاسيوم", "فيتامين سي"],
            "الكمية في الحصة": ["116.42 kcal", "1.02 g", "0.10 g", "26.71 g", "0.87 g", "19.45 mg", "165.01 mg", "20.46 mg"]
        })
        if st.button("🛍️ Fresh Berry - إضافة العبوة", key="add_straw_btn", use_container_width=True):
            st.session_state.want_s = True
            st.toast("🍓 تم إضافة شربت الفراولة والرمان لعربتك!")
            st.rerun()

# ==========================================
# التبويب الثاني: البعد العلمي والاستدامة (صورة التيم واللجنة محاذى بالكامل سنتر)
# ==========================================
with tab2:
    st.write("")
    st.markdown("<h2 style='color:#f39c12; text-align:center; margin-bottom:25px;'>🔬 التأصيل العلمي والهوية الأكاديمية للمشروع</h2>", unsafe_allow_html=True)
    
    col_team, col_science = st.columns([1, 1], gap="large")
    
    with col_team:
        st.markdown("""
        <div class='info-card'>
            <h4 style='color:#f39c12; margin-top:0; border-bottom:1px solid #222232; padding-bottom:8px;'>🏫 الجهة الأكاديمية والبحثية</h4>
            <p style='font-size:15px; margin-bottom:5px;'><b>الجامعة:</b> جامعة عين شمس</p>
            <p style='font-size:15px; margin-bottom:5px;'><b>الكلية:</b> كلية الزراعة</p>
            <p style='font-size:15px; margin-bottom:0;'><b>القسم:</b> قسم علوم الأغذية (شعبة الألبان وصناعات)</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("<b style='color:#f39c12; font-size:16px;'>📸 فريق عمل أوكتانوفا والهيئة الإشرافية:</b>", unsafe_allow_html=True)
        try:
            st.image("team_photo.jpg", caption="فريق عمل مشروع SheroWhey 2026", use_container_width=True)
        except Exception:
            st.markdown("<div class='photo-placeholder'>💡 [مكان وضع صورة الفريق الرسمية - اسم الملف team_photo.jpg]</div>", unsafe_allow_html=True)
            
        st.markdown("""
        <div class='info-card'>
            <h5 style='color:#f39c12; margin-top:0;'>👥 أعضاء الفريق (مستوى رابع):</h5>
            <p style='font-size:14px; color:#ddd; line-height:1.6; margin-bottom:15px;'>
                مصطفى صبحي | بسام عادل | رجب محمد | فؤاد سيد <br>
                نورهان محمد | مريم طارق | شمس محمود | منة الله عوض
            </p>
            <h5 style='color:#f39c12; margin-top:0; border-top:1px solid #222232; padding-top:10px;'>👨‍🏫 الهيئة الإشرافية العليا:</h5>
            <p style='font-size:14px; color:#aaa; line-height:1.5; margin-bottom:0;'>
                <b>أ.د. عزة فرحات</b><br>
                <b>د. نعمة سعيد</b><br>
                <b>م.م. حسام الرحماني</b><br>
                <b>أ. آيه أحمد إسماعيل</b>
            </p>
        </div>
        """, unsafe_allow_html=True)

    with col_science:
        st.markdown("""
        <div class='info-card'>
            <h4 style='color:#2ecc71; margin-top:0;'>♻️ الجانب العلمي والبيئي (لماذا الشرش السائل؟)</h4>
            <p style='font-size:14px; line-height:1.6; color:#ddd; text-align:center;'>
                <b>القيمة الغذائية للشرش:</b> الشرش غني بالبروتينات عالية القيمة الحيوية (بروتينات الشرش)، واستخدامه في صياغة الشربت يعطي قواماً غنياً وناعماً، ويعزز الامتصاص الحيوي للمواد الفعالة والنشطة في الجسم.<br><br>
                <b>الاستدامة والبيئة (OUR SUSTAINABLE PLANET):</b> يُعتبر "الشرش السائل" ناتجاً ثانوياً ضخماً لصناعة الأجبان، والتخلص منه بدون معالجة يمثل عبئاً بيئياً كبيراً على الصرف ومصادر المياه. قام الفريق بتحويل هذا التحدي البيئي إلى فرصة ابتكارية واعدة عبر استبدال المكون المائي الكامل والمواد الصلبة اللادهنية (SNF) للبن الفرز في "الشربت" بالشرش الحلو السائل الخام، لتحقيق معادلة الاستدامة وتقليل الهدر البيئي مع رفع القيمة الحيوية للمنتج الوظيفي النهائي.
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class='info-card'>
            <h4 style='color:#f39c12; margin-top:0;'>🧪 المركبات النشطة حيوياً والفوائد الصحية</h4>
            <p style='font-size:14px; line-height:1.6; color:#ddd; text-align:center;'>
                <b>🥭 توليفة المانجو والكركمين:</b> تشتمل على مركب <b>المانجيفيرين</b> والـ<b>كركمينويدات</b> وفيتامين C والكاروتينات. تعمل على دعم بقوة جهاز المناعة ومضاد للالتهابات وحماية الخلايا من الإجهاد التأكسدي بفضل التكامل الحيوي بين بروتينات الشرش والكركمين لزيادة الامتصاص في خلايا الجسد.<br><br>
                <b>🍓 توليفة الفراولة والرمان:</b> تشتمل على صبغات <b>الأنثوسيانين</b> لحماية الأوعية الدموية و<b>حمض الإيلاجيك</b> والـ<b>بولي فينولات</b> لدعم الوظائف الحيوية ونشاط مضاد للميكروبات والالتهابات وتعويض العناصر بفضل الشرش الحلو.
            </p>
        </div>
        """, unsafe_allow_html=True)

# ==========================================
# التبويبات المتبقية (البوت + الشحن والتوصيل)
# ==========================================
with tab3:
    st.markdown("### 💬 SheroBot - مستشارك الذكي")
    if "chat_history" not in st.session_state: st.session_state.chat_history = []
    for message in st.session_state.chat_history:
        with st.chat_message(message["role"]): st.markdown(message["text"])
    if prompt := st.chat_input("اكتب استفسارك هنا..."):
        with st.chat_message("user"): st.markdown(prompt)
        st.session_state.chat_history.append({"role": "user", "text": prompt})
        # (باقي كود استدعاء الـ API كما هو لضمان الاستقرار الحركي للبوت)
        try:
            response = model_gemini.generate_content(prompt)
            raw_text = response.text
        except Exception:
            raw_text = "السيرفر مشغول حالياً يا فندم، برجاء استخدام استمارة التبويب الأخير."
        st.session_state.chat_history.append({"role": "assistant", "text": raw_text})
        st.rerun()

with tab4:
    st.markdown("### 📋 تأكيد الفاتورة وإتمام الطلب السريع")
    col_order_m, col_order_s = st.columns(2, gap="large")
    with col_order_m:
        st.checkbox("🥭 عبوة شربت المانجو والكركمين الوظيفي", key="want_m")
        if st.session_state.want_m: st.number_input("الكمية المطلوبة (كوب 120 مل):", min_value=1, max_value=100, key="qty_m")
    with col_order_s:
        st.checkbox("🍓 عبوة شربت الفراولة والرمان الصحي", key="want_s")
        if st.session_state.want_s: st.number_input("الكمية المطلوبة (كوب 120 مل):", min_value=1, max_value=100, key="qty_s")
    st.markdown("---")
    st.markdown("#### 👤 بيانات الشحن والتواصل")
    c_col1, c_col2 = st.columns(2)
    with c_col1:
        customer_name = st.text_input("الاسم الثلاثي للعميل:")
        customer_phone = st.text_input("رقم الهاتف الذكي الخاص بك:")
    with c_col2:
        customer_address = st.text_area("عنوان التوصيل بالتفصيل لشحن المنتج:")
    
    # تحضير رسالة الواتس والروابط
    msg_template = f"🛒 طلب شراء SheroWhey"
    st.markdown("#### 🚀 تنفيذ الطلب وقنوات التواصل الرسمية للفريق:")
    col_w, col_g, col_info = st.columns([1, 1, 1.2])
    with col_w: st.link_button("📱 إرسال الطلب عبر الواتساب", f"https://wa.me/201090416662?text={urllib.parse.quote(msg_template)}", use_container_width=True)
    with col_g: st.link_button("📧 إرسال الفاتورة للمعمل (Email)", f"https://mail.google.com/mail/?view=cm&fs=1&to=octanova.team@example.com", use_container_width=True)
    with col_info:
        st.markdown("<div style='background:#14141c; padding:8px 15px; border-radius:10px; border:1px solid #222232; font-size:12px;'>🌐 www.sherowhey.com | 📱 @Octanova_Team</div>", unsafe_allow_html=True)
