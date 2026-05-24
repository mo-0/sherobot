import streamlit as st
import google.generativeai as genai
import urllib.parse
import re
from openai import OpenAI

# ==========================================
# 1. إعدادات الصفحة والـ CSS المودرن والتفاعلي (Responsive Grid)
# ==========================================
st.set_page_config(page_title="SheroWhey | ابتكار أوكتانوفا 2026", page_icon="🍦", layout="wide")

# استدعاء خط Cairo وتطبيق التصميم المرن الذي يتجاوب مع أبعاد الشاشة
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@300;400;600;700;900&display=swap');
    
    html, body, [data-testid="stAppViewContainer"], [data-testid="stHeader"] {
        font-family: 'Cairo', sans-serif !important;
        background-color: #0d0d11 !important;
        color: #ffffff !important;
        direction: rtl !important;
        text-align: right !important;
    }
    
    h1, h2, h3, h4, h5, h6, p, span, label {
        font-family: 'Cairo', sans-serif !important;
        text-align: right !important;
        direction: rtl !important;
    }

    /* جعل التبويبات العلوية (Tabs) مرنة وموزعة بكامل عرض الشاشة لتقليل المساحات الميتة */
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
        flex-grow: 1 !important; /* تجعل التبويبات تمتد بكامل العرض لتغطية الشاشة */
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
        text-align: right !important;
        background-color: #14141c !important;
        border-radius: 12px;
        border: 1px solid #222232;
        padding: 15px;
    }
    
    /* كروت المعلومات العصرية مع استغلال أمثل للمساحات الفراغية */
    .info-card {
        background: linear-gradient(145deg, #14141c, #1a1a26);
        border: 1px solid #222232;
        border-radius: 16px;
        padding: 22px;
        margin-bottom: 15px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.2);
        width: 100% !important;
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
    
    /* تحسين وتكبير الجداول التغذوية لتملأ المساحة العرضية بجمالية */
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
        text-align: right !important;
    }
    
    /* إلغاء الهوامش الإضافية لـ Streamlit التي تسبب مساحات فارغة غير مستغلة */
    .block-container {
        padding-top: 2rem !important;
        padding-bottom: 2rem !important;
        padding-left: 3rem !important;
        padding-right: 3rem !important;
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
أنت مساعد خدمة عملاء ومستشار علمي ذكي لمنتج "SheroWhey" (آيس كريم شربت وظيفي وصحي مبتكر من تطوير فريق أوكتانوفا بكلية الزراعة جامعة عين شمس لعام 2026).
المنتج مصنع باستبدال الجوامد اللادهنية الفرز (SNF) بشرش اللبن السائل الطبيعي الخام ومطابق للمواصفات القياسية المصرية 1185/2005 جـ1.

الأنواع المتوفرة:
1. SheroWhey مانجو طبيعي مدعم بالكركمين (يحتوي على المانجيفيرين والكركمينويدات لتعزيز المناعة ومضاد للأكسدة).
2. SheroWhey فراولة ورمان طبيعي (يحتوي على الأنثوسيانين وحمض الإيلاجيك لدعم صحة القلب والدورة الدموية).

⚠️ الحتمية اللغوية وقواعد الرد الصارمة:
1. إذا سألك المستخدم بالإنجليزي، رد بالإنجليزي الاحترافي فقط.
2. إذا سألك بالعربي، رد بلهجة مصرية ودودة جداً وموزونة وبخط سليم تماماً بدون خلط حروف.
3. وجّه العميل دائماً للتبويب الرابع لإتمام الشراء السريع لتسجيل الفاتورة.

قاعدة الأتمتة الإلزامية:
إذا طلب العميل كمية ونوع، ضع هذا الكود بالملي في نهاية الرد:
[SET_ORDER: MANGO=X, STRAWBERRY=Y]
"""

model_gemini = genai.GenerativeModel('gemini-2.5-flash', system_instruction=customer_service_persona)

client_meta = None
if "GROQ_API_KEY" in st.secrets:
    client_meta = OpenAI(base_url="https://api.groq.com/openai/v1", api_key=st.secrets["GROQ_API_KEY"])

# 3. بناء لوحة التبويبات الاحترافية والبديلة تماماً
tab1, tab2, tab3, tab4 = st.tabs([
    "🎨 كتالوج المنتجات التفاعلي", 
    "🔬 البعد العلمي والاستدامة",
    "💬 مساعد SheroBot الذكي", 
    "📋 تأكيد وإرسال الطلبات السريعة"
])

# ==========================================
# التبويب الأول: الكتالوج والويب سايت واستغلال المساحات الكاملة والتفاعل
# ==========================================
with tab1:
    # تقسيم الصفحة لنسب مرنة تتجاوب مع الشاشات العريضة والموبايل
    hero_col1, hero_col2 = st.columns([1.2, 1], gap="medium")
    
    with hero_col1:
        st.markdown("<h1 style='font-size: 46px; font-weight: 900; color: #ffffff; line-height: 1.1;'>SheroWhey</h1>", unsafe_allow_html=True)
        st.markdown("<h3 style='color: #f39c12; font-weight: 600; margin-top: 5px; margin-bottom:15px;'>معنى جديد للشربت | إنتاج شربت وظيفي مبتكر</h3>", unsafe_allow_html=True)
        st.markdown("<p style='font-size: 15px; color: #b3b3b3; line-height: 1.6;'>ابتكار علمي مستدام من فكرة وتقسيم <b>فريق أوكتانوفا 2026</b>، يقوم على استبدال المكونات التقليدية (جوامد لبن فرز لادهنية) بشرش اللبن السائل الحلو لتحقيق التوازن بين الطعم الاستوائي الفاخر والقيمة التغذوية الوظيفية العليا.</p>", unsafe_allow_html=True)
        
        st.markdown("""
        <div style='margin-bottom: 15px;'>
            <span class='badge-green'>🌿 100% شرش لبن سائل طبيعي</span>
            <span class='badge-orange'>✨ قوام كريمي ناعم ونكهة غنية</span>
            <span class='badge-green'>♻️ ابتكار بيئي مستدام (Zero Waste)</span>
        </div>
        """, unsafe_allow_html=True)
        
        # سلايدر معلومات البروشور التفاعلي
        if 'current_slide' not in st.session_state: st.session_state.current_slide = 0
        slides = [
            {"title": "🎯 رؤيتنا وهدفنا الأساسي", "desc": "تطوير منتجات غذائية 'وظيفية' لا تكتفي بتقديم المذاق الرائع، بل تدعم الصحة العامة وتعزز المناعة، لسد الفجوة بين المثلجات التقليدية والمتطلبات الصحية العصرية للمستهلك الواعي."},
            {"title": "📈 ثقة المستهلك والأمان الحيوي", "desc": "أثبتت الدراسات الميدانية للفريق أن 96% من المستهلكين رحبوا تماماً بفكرة استخدام الشرش في المنتج بمجرد معرفة فوائده البيئية والصحية، مع التزامنا بأعلى معايير الجودة الحسية."},
            {"title": "📜 المواصفات القياسية المصرية", "desc": "المنتج مصنع ومطور علمياً داخل معامل القسم ومطابق تماماً للمواصفات القياسية المصرية رقم 1185 لسنة 2005 الجزء الأول الخاص بالمثلجات اللبنية وشربت الآيس كريم."}
        ]
        
        st.markdown(f"""
        <div class='info-card'>
            <strong style='color:#f39c12; font-size:16px;'>{slides[st.session_state.current_slide]['title']}</strong><br>
            <p style='color:#dddddd; font-size:14px; line-height:1.5; margin-top:5px; margin-bottom:0;'>{slides[st.session_state.current_slide]['desc']}</p>
        </div>
        """, unsafe_allow_html=True)
        
        # 🛠️ حل مشكلة أزرار التالي والسابق لتصبح بجوار بعضها أفقياً بشكل سليم وموزع
        b1, b2 = st.columns([1, 1])
        with b1:
            if st.button("⬅️ السابق", key="p_slide", use_container_width=True):
                st.session_state.current_slide = (st.session_state.current_slide - 1) % len(slides)
                st.rerun()
        with b2:
            if st.button("التالي ➡️", key="n_slide", use_container_width=True):
                st.session_state.current_slide = (st.session_state.current_slide + 1) % len(slides)
                st.rerun()

    with hero_col2:
        carousel_images = [
            "https://images.unsplash.com/photo-1560512823-829485b8bf24?w=600&auto=format&fit=crop&q=80",
            "https://images.unsplash.com/photo-1601004890684-d8cbf643f5f2?w=600&auto=format&fit=crop&q=80",
            "https://images.unsplash.com/photo-1576092768241-dec231879fc3?w=600&auto=format&fit=crop&q=80"
        ]
        st.image(carousel_images[st.session_state.current_slide], use_container_width=True)

    st.markdown("<br><hr style='border-color:#222232;'><br>", unsafe_allow_html=True)
    
    # قسم الكتالوج وجداول الحقائق الغذائية والمكونات الرسمية
    st.markdown("<h2 style='text-align: center; font-weight:700; margin-bottom:30px;'>🍦 كتالوج عبوات وحقائق SheroWhey الغذائية</h2>", unsafe_allow_html=True)
    
    prod_col1, prod_col2 = st.columns(2, gap="large")
    
    with prod_col1:
        st.markdown("""
        <div class='info-card'>
            <h3 style='color:#f39c12; margin-top:0;'>🥭 SheroWhey مانجو طبيعي مدعم بالكركمين</h3>
            <p style='font-size:14px; color:#ccc; line-height:1.5;'><b>المكونات الأصلية:</b> شرش سائل، سكر (سكروز)، بيوريه المانجو، عسل جلوكوز، كريمة خفق، مواد مثبتة (صمغ السليلوز CMC E466)، منظم لون ومضاد أكسدة طبيعي (كركمين E100)، منظم حموضة (حمض الستريك E330).</p>
            <p style='font-size:13px; color:#e74c3c; margin-bottom:0;'>⚠️ <b>تنبيه الحساسية:</b> يحتوي على مكونات الحليب (اللاكتوز، بروتينات الحليب). | <b>الحجم:</b> 120 مل</p>
        </div>
        """, unsafe_allow_html=True)
        st.image("https://images.unsplash.com/photo-1560512823-829485b8bf24?w=500&auto=format&fit=crop&q=80", use_container_width=True)
        
        st.markdown("<b style='color:#f39c12;'>الحقائق الغذائية (حصة 100 جرام | 4oz):</b>", unsafe_allow_html=True)
        st.table({
            "العنصر الغذائي": ["السعرات الحرارية", "إجمالي الدهون", "البروتين", "إجمالي الكربوهيدرات", "الرماد", "الكالسيوم", "البوتاسيوم", "فيتامين سي"],
            "الكمية في الحصة": ["117.7 kcal", "1.1 g", "0.11 g", "26.85 g", "0.64 g", "26.8 mg", "173.9 mg", "22.1 mg"]
        })
        if st.button("🛍 Tangy Mango - إضافة العبوة", key="add_mango_btn", use_container_width=True):
            st.session_state.want_m = True
            st.toast("🥭 تم إضافة شربت المانجو والكركمين لعربتك!")
            st.rerun()

    with prod_col2:
        st.markdown("""
        <div class='info-card'>
            <h3 style='color:#f39c12; margin-top:0;'>🍓 SheroWhey فراولة ورمان طبيعي</h3>
            <p style='font-size:14px; color:#ccc; line-height:1.5;'><b>المكونات الأصلية:</b> شرش سائل، سكر (سكروز)، بيوريه فراولة، عصير رمان طبيعي, عسل جلوكوز، كريمة خفق، مواد مثبتة مثخنات قوام (صمغ السليلوز CMC E466)، منظم حموضة (حمض الستريك E330).</p>
            <p style='font-size:13px; color:#e74c3c; margin-bottom:0;'>⚠️ <b>تنبيه الحساسية:</b> يحتوي على مكونات الحليب (اللاكتوز، بروتينات الحليب). | <b>الحجم:</b> 120 مل</p>
        </div>
        """, unsafe_allow_html=True)
        st.image("https://images.unsplash.com/photo-1601004890684-d8cbf643f5f2?w=500&auto=format&fit=crop&q=80", use_container_width=True)
        
        st.markdown("<b style='color:#f39c12;'>الحقائق الغذائية (حصة 92.6 جرام | 4oz):</b>", unsafe_allow_html=True)
        st.table({
            "العنصر الغذائي": ["السعرات الحرارية", "إجمالي الدهون", "البروتين", "إجمالي الكربوهيدرات", "الرماد", "الكالسيوم", "البوتاسيوم", "فيتامين سي"],
            "الكمية في الحصة": ["116.42 kcal", "1.02 g", "0.10 g", "26.71 g", "0.87 g", "19.45 mg", "165.01 mg", "20.46 mg"]
        })
        if st.button("🛍 Fresh Berry - إضافة العبوة", key="add_straw_btn", use_container_width=True):
            st.session_state.want_s = True
            st.toast("🍓 تم إضافة شربت الفراولة والرمان لعربتك!")
            st.rerun()

# ==========================================
# التبويب الثاني: البعد العلمي والبيئي الاستراتيجي (إصلاح الكود الظاهر + صورة التيم)
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
            <p style='font-size:15px; margin-bottom:15px;'><b>القسم:</b> قسم علوم الأغذية (شعبة الألبان وصناعات)</p>
        </div>
        """, unsafe_allow_html=True)
        
        # 🛠️ وضع حاوية صورة التيم هنا وتحتها الأسماء واللجنة الإشرافية بشكل نظيف وصحيح 100%
        st.markdown("<b style='color:#f39c12; font-size:16px;'>📸 فريق عمل أوكتانوفا والهيئة الإشرافية:</b>", unsafe_allow_html=True)
        try:
            # يمكنك تسمية ملف صورة الفريق بـ team_photo.jpg ووضعه في المجلد الرئيسي
            st.image("team_photo.jpg", caption="فريق عمل مشروع SheroWhey 2026", use_container_width=True)
        except Exception:
            # حاوية بديلة شيك في حالة عدم رفع الصورة بعد
            st.markdown("""
            <div style='background:#1b1b26; border:1px dashed #f39c12; border-radius:12px; padding:30px; text-align:center; color:#aaa; font-size:14px; margin-bottom:15px;'>
                💡 [مكان وضع صورة الفريق الرسمية - سمّ الملف team_photo.jpg وضعه في السيرفر]
            </div>
            """, unsafe_allow_html=True)
            
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
            <p style='font-size:14px; line-height:1.6; color:#ddd; text-align:justify;'>
                <b>القيمة الغذائية للشرش:</b> الشرش غني بالبروتينات عالية القيمة الحيوية (بروتينات الشرش)، واستخدامه في صياغة الشربت يعطي قواماً غنياً وناعماً، ويعزز الامتصاص الحيوي للمواد الفعالة والنشطة في الجسم.<br><br>
                <b>الاستدامة والبيئة (OUR SUSTAINABLE PLANET):</b> يُعتبر "الشرش السائل" ناتجاً ثانوياً ضخماً لصناعة الأجبان، والتخلص منه بدون معالجة يمثل عبئاً بيئياً كبيراً على الصرف ومصادر المياه. قام الفريق بتحويل هذا التحدي البيئي إلى فرصة ابتكارية واعدة عبر استبدال المكون المائي الكامل والمواد الصلبة اللادهنية (SNF) للبن الفرز في "الشربت" بالشرش الحلو السائل الخام، لتحقيق معادلة الاستدامة وتقليل الهدر البيئي مع رفع القيمة الحيوية للمنتج الوظيفي النهائي.
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class='info-card'>
            <h4 style='color:#f39c12; margin-top:0;'>🧪 المركبات النشطة حيوياً والفوائد الصحية</h4>
            <p style='font-size:14px; line-height:1.6; color:#ddd; text-align:justify;'>
                <b>🥭 توليفة المانجو والكركمين:</b> تشتمل على مركب <b>المانجيفيرين</b> (مضاد أكسدة قوي مستخلص من المانجو) والـ<b>كركمينويدات</b> والـ فبتامين C والكاروتينات. تعمل على دعم بقوة جهاز المناعة ومضاد للالتهابات وحماية الخلايا من الإجهاد التأكسدي بفضل التكامل الحيوي بين بروتينات الشرش والكركمين لزيادة الامتصاص في خلايا الجسد.<br><br>
                <b>🍓 توليفة الفراولة والرمان:</b> تشتمل على صبغات <b>الأنثوسيانين</b> لحماية الأوعية الدموية و<b>حمض الإيلاجيك</b> (المتوفر بكثرة في الرمان لمكافحة الشوارد الحرة) والـ<b>بولي فينولات</b> لدعم الوظائف الحيوية ونشاط مضاد للميكروبات والالتهابات وتعويض العناصر بفضل الشرش الحلو.
            </p>
        </div>
        """, unsafe_allow_html=True)

# ==========================================
# التبويب الثالث: البوت المطور والمنقح لغوياً
# ==========================================
with tab3:
    st.markdown("### 💬 SheroBot - مستشارك الذكي")
    if "chat_history" not in st.session_state: st.session_state.chat_history = []
    
    for message in st.session_state.chat_history:
        with st.chat_message(message["role"]): st.markdown(message["text"])

    if prompt := st.chat_input("اكتب استفسارك هنا أو اطلب الكمية مباشرة..."):
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
                    raw_text = "⚠️ عذراً يا فندم، السيرفرات مشغولة حالياً، تفضل بملء بيانات الشراء من التبويب الأخير مباشرة!"
            else:
                raw_text = "⚠️ السيرفر مشغول حالياً، فضلاً استخدم استمارة التبويب الأخير مباشرة لإتمام طلبك."

        if raw_text:
            final_display_text = re.sub(r'\[SET_ORDER:.*?\]', '', raw_text)
            st.session_state.chat_history.append({"role": "assistant", "text": final_display_text})
            
            match = re.search(r'\[SET_ORDER:\s*MANGO=(\d+),\s*STRAWBERRY=(\d+)\]', raw_text)
            if match:
                m_qty = int(match.group(1)); s_qty = int(match.group(2))
                if m_qty > 0: st.session_state.want_m = True; st.session_state.qty_m = m_qty
                if s_qty > 0: st.session_state.want_s = True; st.session_state.qty_s = s_qty
                st.toast("🛒 تم تحديث سلة المشتريات تلقائياً!")

            with st.chat_message("assistant"): st.markdown(final_display_text)
            st.rerun()

# ==========================================
# التبويب الرابع: استمارة تأكيد الطلبات وقنوات التواصل الرسمية للبروشور
# ==========================================
with tab4:
    st.markdown("### 📋 تأكيد الفاتورة وإتمام الطلب السريع")
    
    col_order_m, col_order_s = st.columns(2, gap="large")
    
    with col_order_m:
        st.checkbox("🥭 عبوة شربت المانجو والكركمين الوظيفي", key="want_m")
        if st.session_state.want_m: 
            st.number_input("الكمية المطلوبة (كوب 120 مل):", min_value=1, max_value=100, key="qty_m")
        
    with col_order_s:
        st.checkbox("🍓 عبوة شربت الفراولة والرمان الصحي", key="want_s")
        if st.session_state.want_s: 
            st.number_input("الكمية المطلوبة (كوب 120 مل):", min_value=1, max_value=100, key="qty_s")
        
    st.markdown("---")
    st.markdown("#### 👤 بيانات الشحن والتواصل")
    c_col1, c_col2 = st.columns(2)
    with c_col1:
        customer_name = st.text_input("الاسم الثلاثي للعميل:", placeholder="مثال: مصطفى صبحي")
        customer_phone = st.text_input("رقم الهاتف الذكي الخاص بك:", placeholder="010xxxxxxxx")
    with c_col2:
        customer_address = st.text_area("عنوان التوصيل بالتفصيل لشحن المنتج:", placeholder="المحافظة، الحي، الشارع، المنزل")
    
    product_details = ""
    if st.session_state.want_m: product_details += f"• شربت مانجو وكركمين وظيفي [الكمية: {st.session_state.qty_m} كوب]\n"
    if st.session_state.want_s: product_details += f"• شربت فراولة ورمان صحي [الكمية: {st.session_state.qty_s} كوب]\n"
    if not st.session_state.want_m and not st.session_state.want_s: product_details = "• العربة فارغة، لم تضف أي نكهة بعد!\n"

    msg_template = f"🛒 *طلب شراء جديد لمنتج SheroWhey*\n\n👤 العميل: {customer_name}\n📱 الهاتف: {customer_phone}\n🏠 العنوان: {customer_address}\n\n🍦 تفاصيل الأكواب:\n{product_details}\n✨ إنتاج فريق أوكتانوفا 2026 - كلية الزراعة جامعة عين شمس"
    # ─── قنوات التواصل والفوتر المظبوط والمقفل برمجياً ───
    st.markdown("#### 🚀 تنفيذ الطلب السريع:")
    btn_col1, btn_col2 = st.columns(2)
    
    with btn_col1: 
        st.link_button("📱 إرسال الطلب عبر الواتساب", f"https://wa.me/201090416662?text={urllib.parse.quote(msg_template)}", use_container_width=True, disabled=(not st.session_state.want_m and not st.session_state.want_s))
    
    with btn_col2: 
        st.link_button("📧 إرسال الطلب عبر الإيميل", f"mailto:octanova.team@example.com?subject=SheroWhey_Order&body={urllib.parse.quote(msg_template)}", use_container_width=True, disabled=(not st.session_state.want_m and not st.session_state.want_s))

    # الفوتر السفلي الموحد والمحاذى للمنتصف بأمان
    st.markdown("""
        <br><br>
        <div style="text-align: center; color: #666677; font-size: 0.9rem; border-top: 1px solid #222232; padding-top: 15px;">
            © Octanova 2026 | جميع الحقوق محفوظة لمشروع SheroWhey 🍦
        </div>
    """, unsafe_allow_html=True)
