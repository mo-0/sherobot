import streamlit as st
import google.generativeai as genai
import urllib.parse
import re
from openai import OpenAI

# ==========================================
# 1. إعدادات الصفحة والـ CSS الاحترافي الشامل والمرن (Responsive & Centered)
# ==========================================
st.set_page_config(page_title="SheroWhey | ابتكار أوكتانوفا 2026", page_icon="🍦", layout="wide")

# هندسة الـ CSS المتقدم لحل مشكلة المحاذاة، الفونت، الألوان، والمرونة على كافة الشاشات
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@300;400;600;700;900&display=swap');
    
    /* 1. ضبط الأساس اللغوي والفونت وبنية الصفحة (بدون خلفيات سوداء زائدة) */
    html, body, [data-testid="stAppViewContainer"] {
        font-family: 'Cairo', sans-serif !important;
        background-color: #0d0d11 !important; /* خلفية الصفحة الرئيسية الداكنة */
        color: #ffffff !important;
        direction: rtl !important;
    }
    
    /* 2. سنترة إجبارية ونظيفة لجميع العناوين والنصوص المحددة بأمان (بدون تداخل خلفيات) */
    .centered-title, .centered-text, .stMarkdown p {
        font-family: 'Cairo', sans-serif !important;
        text-align: center !important;
        color: #ffffff !important;
        margin-left: auto !important;
        margin-right: auto !important;
    }

    /* 3. حاوية صور ذكية ومرنة 100% (سنترة وملاءمة تلقائية لعرض الشاشة - للموبايل والكمبيوتر) */
    [data-testid="stImage"] {
        display: flex !important;
        justify-content: center !important;
        align-items: center !important;
        width: 100% !important;
        max-width: 100% !important;
        margin: 15px auto !important; /* سنترة الحاوية */
        overflow: hidden !important;
    }
    [data-testid="stImage"] img {
        max-width: 100% !important; /* تجعل الصورة تصغر مع عرض الشاشة */
        height: auto !important; /* تحافظ على الأبعاد */
        display: block !important;
        margin: 0 auto !important; /* سنترة الصورة نفسها داخل الحاوية */
        border-radius: 12px;
    }

    /* 4. تأمين مظهر التبويبات العلوية (Tabs) لتصبح مرنة واحترافية */
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
        padding: 12px 15px !important;
        flex-grow: 1 !important;
        text-align: center !important;
    }
    div[data-testid="stTabs"] button[aria-selected="true"] {
        color: #f39c12 !important;
        background-color: #1c1c28 !important;
        border-bottom: 3px solid #f39c12 !important;
    }
    
    /* كروت المعلومات المودرن الفخمة (الخلفية الداكنة هنا فقط) */
    .info-card {
        background: linear-gradient(145deg, #14141c, #1a1a26);
        border: 1px solid #222232;
        border-radius: 16px;
        padding: 22px;
        margin-bottom: 15px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.2);
        width: 100% !important;
        max-width: 900px;
        margin-left: auto;
        margin-right: auto;
        text-align: center !important;
    }
    .badge-bar { margin: 20px 0; display: flex; justify-content: center; gap: 10px; flex-wrap: wrap; }
    .custom-badge { background: #1e1e2a; padding: 6px 16px; border-radius: 50px; font-size: 13px; border: 1px solid #f39c12; color: #f39c12; }
    
    /* كروت الشات للبوت */
    div[data-testid="stChatMessage"] {
        direction: rtl !important;
        text-align: right !important;
        background-color: #14141c !important;
        border-radius: 12px;
        border: 1px solid #222232;
        padding: 15px;
        margin-bottom: 10px;
    }

    /* ضبط الحواف الإجمالية للموقع */
    .block-container {
        padding-top: 2rem !important;
        padding-bottom: 2rem !important;
        padding-left: 2.5rem !important;
        padding-right: 2.5rem !important;
    }
    
    /* تصميم جداول البيانات التغذوية المحاذى للمنتصف */
    .stTable table {
        background-color: #14141c !important;
        border-radius: 12px !important;
        overflow: hidden !important;
        border: 1px solid #222232 !important;
        width: 100% !important;
        max-width: 500px !important;
        margin-left: auto !important;
        margin-right: auto !important;
    }
    .stTable th {
        background-color: #1c1c28 !important;
        color: #f39c12 !important;
        font-weight: 700 !important;
        text-align: center !important;
    }
    .stTable td {
        text-align: center !important;
        color: #ffffff !important;
    }
    
    /* حاوية بديلة شيك للعبوات لحين رفعها */
    .photo-placeholder {
        background: #1b1b26; 
        border: 1px dashed #f39c12; 
        border-radius: 12px; 
        padding: 30px; 
        text-align: center; 
        color: #aaa; 
        font-size: 13px; 
        margin-bottom: 15px;
        max-width: 400px;
        margin-left: auto;
        margin-right: auto;
    }
    </style>
""", unsafe_allow_html=True)

# تهيئة الـ Session States للسلة والطلبات والـ Slider
if "want_m" not in st.session_state: st.session_state.want_m = False
if "qty_m" not in st.session_state: st.session_state.qty_m = 1
if "want_s" not in st.session_state: st.session_state.want_s = False
if "qty_s" not in st.session_state: st.session_state.qty_s = 1
if "current_slide" not in st.session_state: st.session_state.current_slide = 0

# ==========================================
# 2. إعدادات الـ APIs (جوجل + ميتا لاما كاحتياطي)
# ==========================================
genai.configure(api_key=st.secrets["GEMINI_API_KEY"])

customer_service_persona = """
أنت مساعد خدمة عملاء ومستشار علمي ذكي لمنتج "SheroWhey" (آيس كريم شربت وظيفي وصحي مبتكر من تطوير فريق أوكتانوفا بكلية الزراعة جامعة عين شمس لعام 2026).
المنتج مصنع باستبدال الجوامد اللادهنية الفرز (SNF) بشرش اللبن السائل الطبيعي الخام ومطابق للمواصفات القياسية المصرية 1185/2005 جـ1.
الأنواع المتوفرة: مانجو وكركمين، وفراولة ورمان.

⚠️ الحتمية اللغوية وقواعد الرد الصارمة:
1. إذا سألك المستخدم بالإنجليزي، رد بالإنجليزي الاحترافي فقط وبمحاذاة سنتر.
2. إذا سألك بالعربي، رد بلهجة مصرية ودودة ومحاذاة سنتر.
3. وجّه العميل دائماً للتبويب الرابع لإتمام الشراء.
"""
model_gemini = genai.GenerativeModel('gemini-2.5-flash', system_instruction=customer_service_persona)

client_meta = None
if "GROQ_API_KEY" in st.secrets:
    client_meta = OpenAI(base_url="https://api.groq.com/openai/v1", api_key=st.secrets["GROQ_API_KEY"])

# 3. بناء لوحة التبويبات الـ Tabs بأسماء عصرية ومرنة
tab1, tab2, tab3, tab4 = st.tabs([
    "🎨 كتالوج المنتجات التفاعلي", 
    "🔬 البعد العلمي والاستدامة",
    "💬 المساعد الذكي SheroBot", 
    "🚀 تأكيد وإرسال الطلبات"
])

# ==========================================
# التبويب الأول: الكتالوج والتجربة المودرن (سنترة ومرونة شاملة للصور)
# ==========================================
with tab1:
    st.write("")
    st.markdown("<h1 class='centered-title' style='font-size: 50px; font-weight: 900; color: white; margin-bottom: 0;'>SheroWhey</h1>", unsafe_allow_html=True)
    st.markdown("<h3 class='centered-title' style='color: #f39c12; font-weight: 600; margin-top: 0;'>معنى جديد للشربت | إنتاج شربت وظيفي مبتكر</h3>", unsafe_allow_html=True)
    
    st.markdown("""
    <div class='centered-text' style='max-width: 850px; font-size: 16px; color: #b3b3b3; line-height: 1.8; margin-top: 15px;'>
        🚀 <b>ابتكار علمي مستدام من فكرة وتطوير فريق أوكتانوفا 2026</b><br>
        • يقوم المشروع على فكرة هندسية متطورة في تكنولوجيا الألبان والأغذية.<br>
        • تم استبدال الجوامد اللادهنية للبن الفرز (SNF) بالكامل بشرش اللبن السائل الحلو الخام.<br>
        • نهدف إلى تحقيق التوازن المثالي بين المذاق الاستوائي الفاخر والقيمة الغذائية الحيوية الفائقة للمستهلك.
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class='badge-bar'>
        <span class='custom-badge'>🌿 100% شرش لبن طبيعي</span>
        <span class='custom-badge'>✨ قوام كريمي ناعم ونكهة غنية</span>
        <span class='custom-badge'>♻️ Zero Waste صديق للبيئة</span>
    </div>
    """, unsafe_allow_html=True)

    # الـ Carousel التفاعلي (Centered & Responsive Container)
    slides = [
        {"title": "🎯 رؤيتنا وهدفنا الأساسي", "desc": "تتويج البحث العلمي بتطوير منتجات غذائية 'وظيفية' لا تكتفي بتقديم المذاق الرائع، بل تدعم الصحة العامة وتعزز المناعة، لسد الفجوة بين المثلجات التقليدية والمتطلبات الصحية العصرية للمستهلك الواعي.", "img": "team_photo.jpg"},
        {"title": "📈 ثقة المستهلك والأمان الحيوي", "desc": "أثبتت الدراسات الميدانية للفريق أن 96% من المستهلكين رحبوا تماماً بفكرة استخدام الشرش في المنتج بمجرد معرفة فوائده البيئية والصحية، مع التزامنا بأعلى معايير الجودة الحسية والأمان.", "img": "mango_pack.jpg"},
        {"title": "📜 المواصفات القياسية المصرية", "desc": "المنتج مصنع ومطور علمياً داخل معامل القسم ومطابق تماماً للمواصفات القياسية المصرية رقم 1185 لسنة 2005 الجزء الأول الخاص بالمثلجات اللبنية وشربت الآيس كريم.", "img": "strawberry_pack.jpg"}
    ]
    
    c_slide_col1, c_slide_col2, c_slide_col3 = st.columns([1, 2.2, 1])
    with c_slide_col2:
        st.markdown(f"""
        <div class='info-card' style='margin-bottom: 10px;'>
            <strong style='color:#f39c12; font-size:16px;'>{slides[st.session_state.current_slide]['title']}</strong><br>
            <p style='color:#dddddd; font-size:14px; line-height:1.6; margin-top:8px;'>{slides[st.session_state.current_slide]['desc']}</p>
        </div>
        """, unsafe_allow_html=True)
        
        # أزرار السلايدر أفقية ومسطرة (use_container_width يجعلها تأخذ العرض المتاح بمرونة)
        b_s1, b_s2 = st.columns([1, 1])
        with b_s1:
            if st.button("⬅️ السابق", key="prev_carousel", use_container_width=True):
                st.session_state.current_slide = (st.session_state.current_slide - 1) % len(slides)
                st.rerun()
        with b_s2:
            if st.button("التالي ➡️", key="next_carousel", use_container_width=True):
                st.session_state.current_slide = (st.session_state.current_slide + 1) % len(slides)
                st.rerun()

    st.markdown("<br><hr style='border-color:#222232;'><br>", unsafe_allow_html=True)
    
    # قسم عرض المنتجات بالكروت المودرن
    st.markdown("<h2 class='centered-title' style='font-weight:700; margin-bottom:30px;'>🍨 عبوات وحقائق SheroWhey الغذائية</h2>", unsafe_allow_html=True)
    prod_col1, prod_col2 = st.columns(2, gap="large")
    
    with prod_col1:
        st.markdown("""
        <div class='info-card'>
            <h3 style='color:#f39c12; margin-top:0;'>🥭 SheroWhey مانجو وكركمين</h3>
            <p style='font-size:14px; color:#ccc; line-height:1.5;'><b>المكونات:</b> شرش سائل طبيعي، بيوريه مانجو، سكر، مستخلص كركمين نشط، مثبتات قوام طبيعية.</p>
            <p style='font-size:13px; color:#e74c3c; margin-bottom:0;'>⚠️ يحتوي على مكونات حليب | الحجم: 120 مل</p>
        </div>
        """, unsafe_allow_html=True)
        
        # حاوية صورة المانجو (Centered & Responsive)
        try:
            # استخدام width=400 يضمن حجم مناسب للكمبيوتر، و max-width في الـ CSS سيجعله مناسباً للموبايل
            st.image("mango_pack.jpg", caption="عبوة شربت المانجو والكركمين 120 مل", width=400)
        except Exception:
            st.markdown("<div class='photo-placeholder'>💡 [ارفع صورة عبوة المانجو هنا باسم mango_pack.jpg]</div>", unsafe_allow_html=True)
        
        st.markdown("<b style='color:#f39c12;'>الحقائق الغذائية (حصة 100 جرام | 4oz):</b>", unsafe_allow_html=True)
        st.table({
            "العنصر الغذائي": ["السعرات الحرارية", "إجمالي الدهون", "البروتين", "إجمالي الكربوهيدرات", "الرماد", "الكالسيوم", "البوتاسيوم", "فيتامين سي"],
            "الكمية في الحصة": ["117.7 kcal", "1.1 g", "0.11 g", "26.85 g", "0.64 g", "26.8 mg", "173.9 mg", "22.1 mg"]
        })
        if st.button("🛍️ أطلب المانجو والكركمين", key="add_m_tab1", use_container_width=True):
            st.session_state.want_m = True
            st.toast("🎯 تم إضافة المانجو لعربتك تلقائياً!")
            st.rerun()

    with prod_col2:
        st.markdown("""
        <div class='info-card'>
            <h3 style='color:#f39c12; margin-top:0;'>🍓 SheroWhey فراولة ورمان</h3>
            <p style='font-size:14px; color:#ccc; line-height:1.5;'><b>المكونات:</b> شرش سائل، سكر، بيوريه فراولة، عصير رمان طبيعي، عسل جلوكوز، كريمة خفق، مواد مثبتة ( صمغ السليلوز CMC E466)، منظم حموضة (حمض الستريك E330).</p>
            <p style='font-size:13px; color:#e74c3c; margin-bottom:0;'>⚠️ يحتوي على مكونات حليب | الحجم: 120 مل</p>
        </div>
        """, unsafe_allow_html=True)
        
        # حاوية صورة الفراولة والرمان (Centered & Responsive)
        try:
            st.image("strawberry_pack.jpg", caption="عبوة شربت الفراولة والرمان 120 مل", width=400)
        except Exception:
            st.markdown("<div class='photo-placeholder'>💡 [ارفع صورة عبوة الفراولة هنا باسم strawberry_pack.jpg]</div>", unsafe_allow_html=True)
        
        st.markdown("<b style='color:#f39c12;'>الحقائق الغذائية (حصة 92.6 جرام | 4oz):</b>", unsafe_allow_html=True)
        st.table({
            "العنصر الغذائي": ["السعرات الحرارية", "إجمالي الدهون", "البروتين", "إجمالي الكربوهيدرات", "الرماد", "الكالسيوم", "البوتاسيوم", "فيتامين سي"],
            "الكمية في الحصة": ["116.42 kcal", "1.02 g", "0.10 g", "26.71 g", "0.87 g", "19.45 mg", "165.01 mg", "20.46 mg"]
        })
        if st.button("🛍️ أطلب الفراولة والرمان", key="add_s_tab1", use_container_width=True):
            st.session_state.want_s = True
            st.toast("🎯 تم إضافة الفراولة لعربتك تلقائياً!")
            st.rerun()

# ==========================================
# التبويب الثاني: البعد العلمي والاستدامة (المادة العلمية الكاملة والمحاذاة المظبوطة)
# ==========================================
with tab2:
    st.write("")
    st.markdown("<h2 class='centered-title' style='color:#f39c12;'>🔬 التأصيل العلمي والهوية الأكاديمية للمشروع</h2>", unsafe_allow_html=True)
    
    col_team, col_science = st.columns([1, 1.2], gap="large")
    
    with col_team:
        st.markdown("""
        <div class='info-card'>
            <h4 style='color:#f39c12; margin-top:0;'>🏫 الجهة الأكاديمية والبحثية</h4>
            <p style='font-size:15px; margin-bottom:5px;'><b>الجامعة:</b> جامعة عين شمس</p>
            <p style='font-size:15px; margin-bottom:5px;'><b>الكلية:</b> كلية الزراعة</p>
            <p style='font-size:15px; margin-bottom:15px;'><b>القسم:</b> علوم الأغذية (شعبة الألبان وصناعات)</p>
        </div>
        """, unsafe_allow_html=True)
        
        # قسم صورة التيم (استدعاء ذكي ومرن بالمنتصف)
        st.markdown("<b style='color:#f39c12;' class='centered-title'>📸 فريق عمل أوكتانوفا 2026 برحاب الكلية:</b>", unsafe_allow_html=True)
        try:
            # استخدام width=550 يضمن حجم مناسب للكمبيوتر، و max-width في الـ CSS سيجعله مناسباً للموبايل
            st.image("team_photo.jpg", caption="فريق عمل مشروع SheroWhey 🍦", width=550)
        except Exception:
            st.markdown("<div class='photo-placeholder' style='max-width:550px; text-align:center;'>💡 [مكان وضع صورة الفريق الرسمية - ارفع ملف باسم team_photo.jpg]</div>", unsafe_allow_html=True)
            
        st.markdown("""
        <div class='info-card' style='margin-top:10px;'>
            <h4 style='color:#f39c12; margin-top:0;'>👥 أعضاء فريق البحث (Octanova):</h4>
            <p style='font-size:14px; color:#ddd; line-height:1.6;'>
                مصطفى صبحي | بسام عادل | رجب محمد | فؤاد سيد <br>
                نورهان محمد | مريم طارق | شمس محمود | منة الله عوض
            </p>
            <h4 style='color:#f39c12; margin-top:10px; border-top:1px solid #222232; padding-top:10px;'>👨‍🏫 الهيئة الإشرافية العليا:</h4>
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
            <p style='font-size:14px; line-height:1.6; color:#ddd; text-align:justify;'>
                <b>القيمة الغذائية للشرش:</b> الشرش غني بالبروتينات عالية القيمة الحيوية، واستخدامه في صياغة الشربت يعطي قواماً غنياً وناعماً، ويعزز الامتصاص الحيوي للمواد الفعالة والنشطة في الجسم بفضل ارتباطه بالمركبات الطبيعية.<br><br>
                <b>الاستدامة والبيئة (OUR SUSTAINABLE PLANET):</b> يُعتبر "الشرش السائل" ناتجاً ثانوياً ضخماً لصناعة الأجبان، والتخلص منه بدون معالجة يمثل عبئاً بيئياً كبيراً على الصرف ومصادر المياه. قام الفريق بتحويل هذا التحدي البيئي إلى فرصة ابتكارية واعدة عبر استبدال المكون المائي الكامل والمواد الصلبة اللادهنية (SNF) للبن الفرز في "الشربت" بالشرش الحلو السائل الخام، لتحقيق معادلة الاستدامة وتقليل الهدر البيئي مع رفع القيمة الحيوية للمنتج الوظيفي النهائي.
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class='info-card'>
            <h4 style='color:#f39c12; margin-top:0;'>🧪 المركبات النشطة حيوياً والفوائد الصحية</h4>
            <p style='font-size:14px; line-height:1.6; color:#ddd; text-align:justify;'>
                <b>🥭 توليفة المانجو والكركمين (التوليفة الذهبية لتعزيز المناعة):</b> تشتمل على مركب <b>المانجيفيرين</b> (مضاد أكسدة قوي مستخلص من المانجو) والـ<b>كركمينويدات</b> وفيتامين C والكاروتينات. تعمل على دعم جهاز المناعة ومضاد للالتهابات وحماية الخلايا من الإجهاد التأكسدي بفضل التكامل الحيوي بين بروتينات الشرش والكركمين لزيادة الامتصاص في خلايا الجسد.<br><br>
                <b>🍓 توليفة الفراولة والرمان (إنتعاش وصحة القلب):</b> تشتمل على صبغات <b>الأنثوسيانين</b> لحماية الأوعية الدموية و<b>حمض الإيلاجيك</b> (متوفر بكثرة في الرمان لمكافحة الشوارد الحرة) والـ<b>بولي فينولات</b> لدعم الوظائف الحيوية ونشاط مضاد للميكروبات والالتهابات وتعويض العناصر بفضل الشرش الحلو السائل.
            </p>
        </div>
        """, unsafe_allow_html=True)

# ==========================================
# التبويب الثالث: البوت المطور والمنقح لغوياً والمحاذى بالكامل سنتر بأمان
# ==========================================
with tab3:
    st.markdown("### 💬 SheroBot - مستشارك الذكي")
    st.write("اسأل البوت عن الفوائد العلمية للمنتج، أو المركبات النشطة، أو دعه يضيف العبوات لعربتك تلقائياً:")
    
    if "chat_history" not in st.session_state: st.session_state.chat_history = []
    
    # عرض تاريخ الشات المتبادل
    for message in st.session_state.chat_history:
        with st.chat_message(message["role"]): st.markdown(message["text"])

    if prompt := st.chat_input("اكتب استفسارك التغذوي هنا..."):
        with st.chat_message("user"): st.markdown(prompt)
        st.session_state.chat_history.append({"role": "user", "text": prompt})
        
        raw_text = ""
        try:
            response = model_gemini.generate_content(prompt)
            raw_text = response.text
        except Exception as e:
            if client_meta is not None:
                st.toast("⚠️ جاري المزامنة عبر السيرفر الاحتياطي لضمان السرعة...")
                try:
                    meta_response = client_meta.chat.completions.create(
                        model="llama-3.3-70b-versatile",
                        messages=[{"role": "system", "content": customer_service_persona}, {"role": "user", "content": prompt}]
                    )
                    raw_text = meta_response.choices[0].message.content
                except Exception:
                    raw_text = f"عذراً يا فندم، ضغط السيرفرات عالي جداً. لكن تقدر تطلب وتتصفح النكهات من التبويب الرابع مباشرة وسنتواصل معك فوراً!"
            else:
                raw_text = "خط الاتصال مشغول حالياً يا فندم، تفضل بالانتقال للتبويب الأخير مباشرة لإتمام طلبك وسنتواصل معك فوراً!"

        # تحديث العربة أوتوماتيك وعرض الرد
        if raw_text:
            st.session_state.chat_history.append({"role": "assistant", "text": raw_text})
            
            match = re.search(r'\[SET_ORDER:\s*MANGO=(\d+),\s*STRAWBERRY=(\d+)\]', raw_text)
            if match:
                m_qty = int(match.group(1)); s_qty = int(match.group(2))
                if m_qty > 0: st.session_state.want_m = True; st.session_state.qty_m = m_qty
                if s_qty > 0: st.session_state.want_s = True; st.session_state.qty_s = s_qty
                st.toast("🛒 تم تحديث سلة المشتريات تلقائياً!")

            with st.chat_message("assistant"): st.markdown(raw_text)
            st.rerun()

# ==========================================
# التبويب الرابع: لوحة التحكم والطلب السريع المباشر بالإيميل والواتساب
# ==========================================
with tab4:
    st.markdown("### 📋 تأكيد الفاتورة وإتمام الطلب السريع")
    st.write("البيانات في الأسفل تتحدث تلقائياً إذا طلبت من البوت أو من الكتالوج:")

    col_order_m, col_order_s = st.columns(2, gap="large")
    
    with col_order_m:
        st.checkbox("🥭 عبوة المانجو والكركمين", key="want_m")
        if st.session_state.want_m: 
            st.number_input("الكمية المطلوبة (كوب 120 مل):", min_value=1, max_value=100, key="qty_m")
        
    with col_order_s:
        st.checkbox("🍓 عبوة الفراولة والرمان", key="want_s")
        if st.session_state.want_s: 
            st.number_input("الكمية المطلوبة (كوب 120 مل):", min_value=1, max_value=100, key="qty_s")
        
    st.markdown("<br>", unsafe_allow_html=True)
    
    customer_name = st.text_input("👤 الاسم الكامل للعميل:", placeholder="اكتب اسمك هنا")
    customer_phone = st.text_input("📱 رقم الهاتف للتواصل:", placeholder="010xxxxxxxx")
    customer_address = st.text_area("🏠 العنوان بالتفصيل لشحن المنتج:", placeholder="المحافظة، الحي، الشارع، المنزل")
    
    product_details = ""
    if st.session_state.want_m: product_details += f"• شربت مانجو وكركمين وظيفي [الكمية: {st.session_state.qty_m} كوب]\n"
    if st.session_state.want_s: product_details += f"• شربت فراولة ورمان صحي [الكمية: {st.session_state.qty_s} كوب]\n"
    if not st.session_state.want_m and not st.session_state.want_s: product_details = "• العربة فارغة، لم تضف أي نكهة بعد!\n"

    msg_template = f"🛒 طلب شراء جديد لمنتج SheroWhey\n\n👤 العميل: {customer_name}\n📱 الهاتف: {customer_phone}\n🏠 العنوان: {customer_address}\n\n🍦 تفاصيل الأكواب:\n{product_details}\n✨ إنتاج فريق أوكتانوفا 2026 - كلية الزراعة جامعة عين شمس"
    
    # تنسيق وتوليد روابط التنفيذ المباشرة بالإيميل والواتساب
    st.markdown("#### 🚀 تنفيذ الطلب وقنوات التواصل الرسمية للفريق:")
    col_w, col_g, col_info = st.columns([1, 1, 1.2])
    with col_w: 
        st.link_button("📱 إرسال الطلب عبر الواتساب", f"https://wa.me/201090416662?text={urllib.parse.quote(msg_template)}", use_container_width=True, disabled=(not st.session_state.want_m and not st.session_state.want_s))
    with col_g: 
        st.link_button("📧 إرسال الفاتورة للمعمل (Email)", f"https://mail.google.com/mail/?view=cm&fs=1&to=sheroway78@gmail.com&su=Order&body={urllib.parse.quote(msg_template)}", use_container_width=True, disabled=(not st.session_state.want_m and not st.session_state.want_s))
    with col_info:
        st.markdown("""
        <div style='background:#14141c; padding:8px 15px; border-radius:10px; border:1px solid #222232; font-size:12px; text-align:center; display:flex; justify-content:center; align-items:center;'>
            🌐 الموقع: www.sherowhey.com <br> 📱 انستجرام: @Octanova_Team
        </div>
        """, unsafe_allow_html=True)
