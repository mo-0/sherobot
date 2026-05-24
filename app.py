import streamlit as st
import google.generativeai as genai
import urllib.parse
import re
from openai import OpenAI

# ==========================================
# 1. إعدادات الصفحة والـ CSS الاحترافي الشامل والمرن (Responsive & Centered)
# ==========================================
st.set_page_config(page_title="SheroWhey | ابتكار أوكتانوفا 2026", page_icon="🍦", layout="wide")

# هندسة الـ CSS المتقدم لإجبار الخط وسنترة الصور بكامل عرض الصفحة بدون قص
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght=300;400;600;700;900&display=swap');
    
    /* 1. ضبط الأساس اللغوي والفونت وبنية الصفحة (بدون خلفيات سوداء زائدة) */
    html, body, [data-testid="stAppViewContainer"], [data-testid="stHeader"] {
        font-family: 'Cairo', sans-serif !important;
        background-color: #0d0d11 !important;
        color: #ffffff !important;
        direction: rtl !important;
    }
    
    /* 2. فرض خط Cairo والسنترة على جميع أنواع النصوص والعناوين والمكونات */
    h1, h2, h3, h4, h5, h6, p, span, label, .stMarkdown, .stMarkdown p {
        font-family: 'Cairo', sans-serif !important;
        text-align: center !important;
        color: #ffffff !important;
        margin-left: auto !important;
        margin-right: auto !important;
    }
    
    /* استثناء أزرار Streamlit لجعل نصوصها تتبع خط كايرو أيضاً وبخلفية متناسقة */
    .stButton button {
        font-family: 'Cairo', sans-serif !important;
    }

    /* 3. حاوية صور ذكية ومرنة تفرد بكامل العرض المتاح (Fit Width) بدون قص */
    [data-testid="stImage"] {
        display: flex !important;
        justify-content: center !important;
        align-items: center !important;
        width: 100% !important;
        max-width: 100% !important;
        margin: 20px auto !important;
    }
    [data-testid="stImage"] img {
        width: 100% !important; /* تجعل الصورة تفرد لتملأ عرض الحاوية بالكامل */
        max-width: 100% !important;
        height: auto !important; /* الحفاظ على أبعاد الصورة بدون تمطيط أو قص */
        display: block !important;
        margin: 0 auto !important;
        border-radius: 12px;
    }

    /* 4. تأمين مظهر التبويبات العلوية (Tabs) */
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
    
    /* كروت المعلومات المودرن الفخمة */
    .info-card {
        background: linear-gradient(145deg, #14141c, #1a1a26);
        border: 1px solid #222232;
        border-radius: 16px;
        padding: 25px;
        margin-bottom: 20px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.2);
        width: 100% !important;
        max-width: 900px;
        margin-left: auto;
        margin-right: auto;
        text-align: center !important;
    }
    
    /* صناديق التأصيل العلمي العريضة الممتدة */
    .science-box {
        background: linear-gradient(145deg, #14141c, #1a1a26);
        border: 1px solid #222232;
        border-radius: 20px;
        padding: 30px;
        margin-bottom: 25px;
        width: 100%;
        max-width: 950px;
        margin-left: auto !important;
        margin-right: auto !important;
        text-align: center !important;
        box-shadow: 0 10px 30px rgba(0,0,0,0.3);
    }
    
    .sub-heading {
        font-family: 'Cairo', sans-serif !important;
        color: #f39c12;
        font-size: 22px;
        font-weight: 700;
        display: block;
        margin-bottom: 15px;
        border-bottom: 1px solid #222232;
        padding-bottom: 10px;
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

    /* ضبط الحواف الإجمالية للموقع لتقليل المساحات الميتة */
    .block-container {
        padding-top: 2rem !important;
        padding-bottom: 2rem !important;
        max-width: 92% !important;
    }
    
    /* تصميم جداول البيانات التغذوية المحاذى للمنتصف */
    .stTable table {
        background-color: #14141c !important;
        border-radius: 12px !important;
        overflow: hidden !important;
        border: 1px solid #222232 !important;
        width: 100% !important;
        max-width: 600px !important;
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
        font-family: 'Cairo', sans-serif !important;
        text-align: center !important;
        color: #ffffff !important;
    }
    
    /* حاوية بديلة شيك للعبوات والصور لحين رفعها لمنع انهيار السيرفر */
    .photo-placeholder {
        background: #1b1b26; 
        border: 1px dashed #f39c12; 
        border-radius: 12px; 
        padding: 30px; 
        text-align: center; 
        color: #aaa; 
        font-size: 14px; 
        margin-bottom: 15px;
        max-width: 600px;
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
if "chat_history" not in st.session_state: st.session_state.chat_history = []

# ==========================================
# 2. إعدادات الـ APIs (جوجل جيمني + ميتا لاما كاحتياطي)
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

# 3. بناء لوحة التبويبات الأربعة بأسماء عصرية ومرنة
tab1, tab2, tab3, tab4 = st.tabs([
    "✨ تجربة SheroWhey", 
    "🔬 التأصيل العلمي والاستدامة",
    "💬 المساعد الذكي SheroBot", 
    "🚀 تأكيد وإرسال الطلبات"
])

# ==========================================
# التبويب الأول: الكتالوج والتجربة المودرن (توسيط وفرد كامل للصور)
# ==========================================
with tab1:
    st.write("")
    st.markdown("<h1 class='centered-title' style='font-size: 55px; font-weight: 900; color: white; margin-bottom: 0;'>SheroWhey</h1>", unsafe_allow_html=True)
    st.markdown("<h3 class='centered-title' style='color: #f39c12; font-weight: 600; margin-top: 0;'>معنى جديد للشربت | إنتاج شربت وظيفي مبتكر</h3>", unsafe_allow_html=True)
    
    st.markdown("""
    <div class='centered-text' style='max-width: 850px; font-size: 17px; color: #b3b3b3; line-height: 1.8; margin-top: 15px;'>
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
        {"title": "🎯 رؤيتنا وهدفنا الأساسي", "desc": "تتويج البحث العلمي بتطوير منتجات غذائية 'وظيفية' لا تكتفي بتقديم المذاق الرائع، بل تدعم الصحة العامة وتعزز المناعة، لسد الفجوة بين المثلجات التقليدية والمتطلبات الصحية العصرية للمستهلك الواعي."},
        {"title": "📈 ثقة المستهلك والأمان الحيوي", "desc": "أثبتت الدراسات الميدانية للفريق أن 96% من المستهلكين رحبوا تماماً بفكرة استخدام الشرش في المنتج بمجرد معرفة فوائده البيئية والصحية، مع التزامنا بأعلى معايير الجودة الحسية والأمان."},
        {"title": "📜 المواصفات القياسية المصرية", "desc": "المنتج مصنع ومطور علمياً داخل معامل القسم ومطابق تماماً للمواصفات القياسية المصرية رقم 1185 لسنة 2005 الجزء الأول الخاص بالمثلجات اللبنية وشربت الآيس كريم."}
    ]
    
    c_slide_col1, c_slide_col2, c_slide_col3 = st.columns([1, 2.5, 1])
    with c_slide_col2:
        st.markdown(f"""
        <div class='info-card' style='margin-bottom: 10px;'>
            <strong style='color:#f39c12; font-size:16px;'>{slides[st.session_state.current_slide]['title']}</strong><br>
            <p style='color:#dddddd; font-size:14px; line-height:1.6; margin-top:8px;'>{slides[st.session_state.current_slide]['desc']}</p>
        </div>
        """, unsafe_allow_html=True)
        
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
    
    # قسم عرض المنتجات بالحاويات الفليكس الممتدة (عرض كامل مرن للصور)
    st.markdown("<h2 class='centered-title' style='font-weight:700; margin-bottom:30px;'>🍨 عبوات وحقائق SheroWhey الغذائية</h2>", unsafe_allow_html=True)
    
    # عبوة المانجو
    st.markdown("<div class='science-box'>", unsafe_allow_html=True)
    st.markdown("""
        <h3 style='color:#f39c12; margin-top:0;'> Manny Mango 🥭 شربت المانجو الطبيعي المدعم بالكركمين</h3>
        <p style='font-size:15px; color:#ccc; line-height:1.6;'><b>المكونات الأصلية:</b> شرش سائل، سكر (سكروز)، بيوريه المانجو، عسل جلوكوز، كريمة خفق، مواد مثبتة (صمغ السليلوز CMC E466)، منظم لون ومضاد أكسدة طبيعي (كركمين E100)، منظم حموضة (حمض الستريك E330).</p>
        <p style='font-size:13px; color:#e74c3c;'>⚠️ تنبيه الحساسية: يحتوي على مكونات الحليب (اللاكتوز والبروتينات) | الحجم: 120 مل</p>
    """, unsafe_allow_html=True)
    
    # 🛠️ تأمين استدعاء صورة المانجو بـ try-except لمنع الـ Storage Error
    try:
        st.image("mango_pack.jpg", caption="عبوة شربت المانجو والكركمين 120 مل", use_container_width=True)
    except Exception:
        st.markdown("<div class='photo-placeholder'>💡 [لم يتم العثور على ملف الصورة الحقيقية، يرجى رفع ملف باسم mango_pack.jpg على جيت هاب ليظهر هنا بكامل عرض الصفحة]</div>", unsafe_allow_html=True)
    
    st.markdown("<b style='color:#f39c12;' class='centered-title'>الحقائق الغذائية الرسمية (حصة 100 جرام):</b>", unsafe_allow_html=True)
    st.table({
        "العنصر الغذائي": ["السعرات الحرارية", "إجمالي الدهون", "البروتين", "إجمالي الكربوهيدرات", "الرماد", "الكالسيوم", "البوتاسيوم", "فيتامين سي"],
        "الكمية في الحصة": ["117.7 kcal", "1.1 g", "0.11 g", "26.85 g", "0.64 g", "26.8 mg", "173.9 mg", "22.1 mg"]
    })
    if st.button("🛍️ إضافة العبوة لعربتك", key="add_m_box", use_container_width=True):
        st.session_state.want_m = True
        st.toast("🎯 تم إضافة شربت المانجو لعربتك بنجاح!")
        st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("<br><br>", unsafe_allow_html=True)

    # عبوة الفراولة
    st.markdown("<div class='science-box'>", unsafe_allow_html=True)
    st.markdown("""
        <h3 style='color:#f39c12; margin-top:0;'> Fresh Berry 🍓 شربت الفراولة والرمان الطبيعي</h3>
        <p style='font-size:15px; color:#ccc; line-height:1.6;'><b>المكونات الأصلية:</b> شرش سائل، سكر (سكروز)، بيوريه فراولة، عصير رمان طبيعي، عسل جلوكوز، كريمة خفق، مواد مثبتة مثخنات قوام (صمغ السليلوز CMC E466)، منظم حموضة (حمض الستريك E330).</p>
        <p style='font-size:13px; color:#e74c3c;'>⚠️ تنبيه الحساسية: يحتوي على مكونات الحليب (اللاكتوز والبروتينات) | الحجم: 120 مل</p>
    """, unsafe_allow_html=True)
    
    # 🛠️ تأمين استدعاء صورة الفراولة بـ try-except لمنع الـ Storage Error
    try:
        st.image("strawberry_pack.jpg", caption="عبوة شربت الفراولة والرمان 120 مل", use_container_width=True)
    except Exception:
        st.markdown("<div class='photo-placeholder'>💡 [لم يتم العثور على ملف الصورة الحقيقية، يرجى رفع ملف باسم strawberry_pack.jpg على جيت هاب ليظهر هنا بكامل عرض الصفحة]</div>", unsafe_allow_html=True)
    
    st.markdown("<b style='color:#f39c12;' class='centered-title'>الحقائق الغذائية الرسمية (حصة 92.6 جرام):</b>", unsafe_allow_html=True)
    st.table({
        "العنصر الغذائي": ["السعرات الحرارية", "إجمالي الدهون", "البروتين", "إجمالي الكربوهيدرات", "الرماد", "الكالسيوم", "البوتاسيوم", "فيتامين سي"],
        "الكمية في الحصة": ["116.42 kcal", "1.02 g", "0.10 g", "26.71 g", "0.87 g", "19.45 mg", "165.01 mg", "20.46 mg"]
    })
    if st.button("🛍️ إضافة العبوة لعربتك", key="add_s_box", use_container_width=True):
        st.session_state.want_s = True
        st.toast("🎯 تم إضافة شربت الفراولة والرمان لعربتك بنجاح!")
        st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)

# ==========================================
# التبويب الثاني: التأصيل العلمي والاستدامة (رص كتل الفلكس بوكس متتالية وعمود واحد)
# ==========================================
with tab2:
    st.write("")
    st.markdown("<h2 class='centered-title' style='color:#f39c12; margin-bottom:30px;'>🔬 التأصيل العلمي والهوية الأكاديمية للمشروع</h2>", unsafe_allow_html=True)
    
    # 1. صندوق الجهة الأكاديمية
    st.markdown("""
    <div class='science-box'>
        <span class='sub-heading'>🏫 الجهة الأكاديمية والبحثية</span>
        <p style='font-size:16px; margin:5px 0;'><b>الجامعة:</b> جامعة عين شمس &nbsp;|&nbsp; <b>الكلية:</b> كلية الزراعة</p>
        <p style='font-size:16px; margin:5px 0;'><b>القسم:</b> قسم علوم الأغذية ( شعبة الألبان وشعب صناعات الأغذية )</p>
    </div>
    """, unsafe_allow_html=True)
    
    # 2. قسم صورة التيم المخصصة بالمنتصف (تفرش العرض بالكامل ومرنة)
    st.markdown("<b style='color:#f39c12;' class='centered-title'>📸 فريق عمل أوكتانوفا 2026 برحاب الكلية</b>", unsafe_allow_html=True)
    try:
        st.image("team_photo.jpg", caption="فريق عمل مشروع شيرو واي 2026 برحاب الكلية", use_container_width=True)
    except Exception:
        st.markdown("<div class='photo-placeholder' style='max-width:800px;'>💡 [لم يتم العثور على صورة التيم، يرجى رفع ملف باسم team_photo.jpg على جيت هاب لتظهر هنا في المنتصف تماماً وبشكل مرن]</div>", unsafe_allow_html=True)
        
    # 3. صندوق أسماء أعضاء الفريق
    st.markdown("""
    <div class='science-box'>
        <span class='sub-heading'>👥 أعضاء فريق أوكتانوفا (Octanova 2026)</span>
        <p style='font-size:15px; line-height:1.8; margin:0;'>
            <b>شعبة الألبان:</b> مصطفى صبحي | بسام عادل | رجب محمد | فؤاد سيد <br>
            <b>شعبة صناعات الأغذية:</b> نورهان محمد | مريم طارق | شمس محمود | منة الله عوض
        </p>
    </div>
    """, unsafe_allow_html=True)

    # 4. صندوق الهيئة الإشرافية
    st.markdown("""
    <div class='science-box'>
        <span class='sub-heading'>👨‍🏫 الهيئة الإشرافية العليا للمشروع</span>
        <p style='font-size:15px; line-height:1.7; margin:0; color:#dddddd;'>
            <b>أ.د. عزة فرحات</b> (أستاذ تكنولوجيا الألبان)<br>
            <b>د. نعمة سعيد</b> (مدرس تكنولوجيا الألبان)<br>
            <b>م.م. حسام الرحماني</b> (مدرس مساعد تكنولوجيا الألبان)<br>
            <b>أ. آيه أحمد إسماعيل</b> (معيدة بقسم علوم الأغذية)
        </p>
    </div>
    """, unsafe_allow_html=True)

    # 5. صندوق القيمة الغذائية لشرش اللبن
    st.markdown("""
    <div class='science-box'>
        <span class='sub-heading'>🥛 القيمة الغذائية لشرش اللبن السائل الطبيعي</span>
        <p style='font-size:15px; line-height:1.8; margin:0;'>
            يتميز <b>شرش اللبن السائل الحلو الطبيعي الخام</b> باحتوائه على بروتينات الشرش (Whey Proteins) عالية القيمة الحيوية مثل بيتا-لاكتوجلوبولين وألفا-لاكتالبومين. استخدامه كبديل برامجي للجوامد اللادهنية للبن الفرز (SNF) يمنح الشربت قواماً متماسكاً وناعماً، بالإضافة إلى زيادة الذوبانية والانتشار للمركبات النشطة حيوياً بداخل جسم الإنسان، مما يعزز الاستفادة الفورية من المغذيات الحيوية المضافة.
        </p>
    </div>
    """, unsafe_allow_html=True)

    # 6. صندوق الاستدامة والبيئة
    st.markdown("""
    <div class='science-box'>
        <span class='sub-heading'>🌍 الاستدامة والبيئة (OUR SUSTAINABLE PLANET)</span>
        <p style='font-size:15px; line-height:1.8; margin:0;'>
            يُعد "الشرش السائل" أحد أضخم النواتج الثانوية المتخلفة عن صناعة الجبن، ويمثل التخلص منه دون معالجة عبئاً بيئياً ثقيلاً ومصدراً للتلوث العضوي العالي لشبكات الصرف ومجاري المياه (ارتفاع معامل BOD و COD). نجح الفريق في تدوير هذا التحدي عبر استبدال المكون المائي الكامل والمواد الصلبة اللادهنية (SNF) للبن الفرز في الشربت بالشرش السائل، محققاً صفر نفايات (Zero Waste) ومساهماً في صياغة اقتصاد دائري ومستدام للقطاع الغذائي.
        </p>
    </div>
    """, unsafe_allow_html=True)

    # 7. صندوق المركبات النشطة
    st.markdown("""
    <div class='science-box'>
        <span class='sub-heading'>🧪 المركبات النشطة حيوياً والفوائد الصحية الموثقة</span>
        <p style='font-size:15px; line-height:1.8;'>
            <b>?? توليفة المانجو والكركمين الطبيعي (التوليفة الذهبية لتعزيز المناعة):</b> تشتمل التركيبة على مركب <b>المانجيفيرين (Mangiferin)</b> قوي الفعالية المتواجد في بيوريه المانجو، بالتكامل مع الـ<b>كركمينويدات (Curcuminoids)</b> المضافة و فيتامين C والكاروتينات. تعمل هذه التوليفة كمضاد أكسدة جبار لحماية الخلايا ومكافحة الالتهابات، ورفع كفاءة الجهاز المناعي بفضل زيادة الإتاحة الحيوية للكركمين بارتباطه ببروتينات الشرش السائل الطبيعي.<br><br>
            <b>🍓 توليفة الفراولة وعصير الرمان الطبيعي (إنتعاش وصحة القلب):</b> غنية بصبغات <b>الأنثوسيانين (Anthocyanins)</b> الفعالة في دعم وصيانة سلامة الأوعية الدموية وضبط ضغط الدم، بالإضافة إلى <b>حمض الإيلاجيك (Ellagic Acid)</b> ومجموعة الـ<b>بولي فينولات</b> المضادة للميكروبات والالتهابات، مما يمنح الجسم درعاً واقياً طبيعياً يعوض العناصر والكهرباء الحيوية المفقودة بفضل الشرش الحلو.
        </p>
    </div>
    """, unsafe_allow_html=True)

# ==========================================
# التبويب الثالث: الشات الذكي مع المساعد وزرار مسح سجل المحادثة (Centered Button)
# ==========================================
with tab3:
    st.markdown("<h3 class='centered-title'>💬 SheroBot - مستشارك الذكي</h3>", unsafe_allow_html=True)
    
    # 🛠️ إضافة وإرجاع زر مسح سجل المحادثة بالكامل في المنتصف
    chat_control_col1, chat_control_col2, chat_control_col3 = st.columns([1, 1.2, 1])
    with chat_control_col2:
        if st.button("🗑️ مسح سجل المحادثة بالكامل", use_container_width=True, key="clear_chat_button"):
            st.session_state.chat_history = []
            st.toast("🧹 تم تصفير محادثة المساعد الذكي والمزامنة!")
            st.rerun()

    st.write("")
    
    for message in st.session_state.chat_history:
        with st.chat_message(message["role"]): st.markdown(message["text"])

    if prompt := st.chat_input("اكتب استفسارك التغذوي أو العلمي هنا..."):
        with st.chat_message("user"): st.markdown(prompt)
        st.session_state.chat_history.append({"role": "user", "text": prompt})
        
        raw_text = ""
        try:
            response = model_gemini.generate_content(prompt)
            raw_text = response.text
        except Exception:
            if client_meta is not None:
                st.toast("⚠️ جاري المزامنة عبر السيرفر الاحتياطي...")
                try:
                    meta_response = client_meta.chat.completions.create(
                        model="llama-3.3-70b-versatile",
                        messages=[{"role": "system", "content": customer_service_persona}, {"role": "user", "content": prompt}]
                    )
                    raw_text = meta_response.choices[0].message.content
                except Exception:
                    raw_text = "⚠️ السيرفرات مشغولة حالياً، تفضل بالانتقال للتبويب الأخير لإرسال طلبك فوراً!"
            else:
                raw_text = "خط الاتصال مشغول حالياً يا فندم، تفضل بالانتقال للتبويب الأخير مباشرة لإتمام طلبك."

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
# التبويب الرابع: استمارة الشحن والطلب السريع
# ==========================================
with tab4:
    st.markdown("### 📋 تأكيد الفاتورة وإتمام الطلب السريع")
    st.write("البيانات في الأسفل تتحدث تلقائياً إذا طلبت من البوت أو من الكتالوج:")

    col_order_m, col_order_s = st.columns(2, gap="large")
    
    with col_order_m:
        st.checkbox("🥭 عبوة شربت المانجو والكركمين", key="want_m")
        if st.session_state.want_m: 
            st.number_input("الكمية المطلوبة (كوب 120 مل):", min_value=1, max_value=100, key="qty_m")
        
    with col_order_s:
        st.checkbox("🍓 عبوة شربت الفراولة والرمان", key="want_s")
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
    
    st.markdown("#### 🚀 تنفيذ الطلب وقنوات التواصل الرسمية للفريق:")
    col_w, col_g, col_info = st.columns([1, 1, 1.2])
    with col_w: 
        st.link_button("📱 إرسال الطلب عبر الواتساب", f"https://wa.me/201090416662?text={urllib.parse.quote(msg_template)}", use_container_width=True, disabled=(not st.session_state.want_m and not st.session_state.want_s))
    with col_g: 
        st.link_button("📧 إرسال الفاتورة للمعمل (Email)", f"mailto:sheroway78@gmail.com?subject=Order&body={urllib.parse.quote(msg_template)}", use_container_width=True, disabled=(not st.session_state.want_m and not st.session_state.want_s))
    with col_info:
        st.markdown("""
        <div style='background:#14141c; padding:8px 15px; border-radius:10px; border:1px solid #222232; font-size:12px; text-align:center;'>
            🌐 الموقع: www.sherowhey.com <br> 📱 انستجرام: @Octanova_Team
        </div>
        """, unsafe_allow_html=True)

    st.markdown("""
        <br><br>
        <div style="text-align: center; color: #666677; font-size: 0.9rem; border-top: 1px solid #222232; padding-top: 15px;">
            © Octanova 2026 | جميع الحقوق محفوظة لمشروع SheroWhey 🍦
        </div>
    """, unsafe_allow_html=True)
