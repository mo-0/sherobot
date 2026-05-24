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
    
    .stButton button {
        font-family: 'Cairo', sans-serif !important;
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
    
    /* صناديق التأصيل العلمي والمنتجات */
    .custom-box {
        background: linear-gradient(145deg, #14141c, #1a1a26) !important;
        border: 1px solid #222232 !important;
        border-radius: 20px !important;
        padding: 25px !important;
        margin-bottom: 15px !important;
        text-align: center !important;
        box-shadow: 0 10px 30px rgba(0,0,0,0.3) !important;
    }

    /* إجبار الفونت داخل الصناديق */
    .custom-box * {
        font-family: 'Cairo', sans-serif !important;
        text-align: center !important;
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
    div[data-testid="stChatMessage"] p, div[data-testid="stChatMessage"] span, div[data-testid="stChatMessage"] div {
        text-align: right !important;
    }
    
    /* الجداول التغذوية */
    .stTable table {
        background-color: #14141c !important;
        border-radius: 12px !important;
        width: 100% !important;
        margin: 10px auto !important;
    }
    .stTable th { color: #f39c12 !important; font-weight: 700 !important; text-align: center !important; }
    .stTable td { text-align: center !important; }
    </style>
""", unsafe_allow_html=True)

# تهيئة الـ Session States
if "want_m" not in st.session_state: st.session_state.want_m = False
if "qty_m" not in st.session_state: st.session_state.qty_m = 1
if "want_s" not in st.session_state: st.session_state.want_s = False
if "qty_s" not in st.session_state: st.session_state.qty_s = 1
if "chat_history" not in st.session_state: st.session_state.chat_history = []

# ==========================================
# 2. إعدادات الـ APIs والمزامنة المستقرة لبوت الشات
# ==========================================
# تهيئة مفتاح جوجل جيمني بشكل نظامي ومستقر لمنع أخطاء السيرفر
genai.configure(api_key=st.secrets["GEMINI_API_KEY"])

customer_service_persona = """
أنت مساعد خدمة عملاء ومستشار علمي ذكي لمنتج "SheroWhey" (آيس كريم شربت وظيفي وصحي مبتكر من تطوير فريق أوكتانوفا بكلية الزراعة جامعة عين شمس لعام 2026).
المنتج مصنع باستبدال الجوامد اللادهنية الفرز (SNF) بشرش اللبن السائل الطبيعي الخام ومطابق للمواصفات القياسية المصرية 1185/2005 جـ1.

الأنواع المتوفرة:
1. شربت المانجو الطبيعي المدعم بالكركمين (يحتوي على المانجيفيرين لتعزيز المناعة ومضاد للأكسدة).
2. شربت الفراولة والرمان الطبيعي (يحتوي على الأنثوسيانين وحمض الإيلاجيك لدعم صحة القلب).

قواعد الرد الإلزامية: رد بلهجة مصرية ودودة ومحاذاة سنتر، ولا تستخدم مصطلحات تسبب طلاسم لغوية. وجه العميل دائماً للتبويب الرابع لإتمام الشراء.
"""
model_gemini = genai.GenerativeModel('gemini-2.5-flash', system_instruction=customer_service_persona)

client_meta = None
if "GROQ_API_KEY" in st.secrets:
    client_meta = OpenAI(base_url="https://api.groq.com/openai/v1", api_key=st.secrets["GROQ_API_KEY"])

# 3. بناء الواجهة
tab1, tab2, tab3, tab4 = st.tabs([
    "✨ تجربة SheroWhey", 
    "🔬 التأصيل العلمي والاستدامة",
    "💬 المساعد الذكي SheroBot", 
    "🚀 تأكيد وإرسال الطلبات"
])

# ==========================================
# التبويب الأول: كتالوج المنتجات التفاعلي (Side-by-Side Products)
# ==========================================
with tab1:
    st.markdown("<h1 style='font-size: 55px; font-weight: 900; color: white;'>SheroWhey</h1>", unsafe_allow_html=True)
    st.markdown("<h3 style='color: #f39c12; font-weight: 600; margin-top: -15px;'>معنى جديد للشربت | إنتاج شربت وظيفي مبتكر</h3>", unsafe_allow_html=True)
    
    st.markdown("""
    <div style='max-width: 850px; font-size: 17px; color: #b3b3b3; line-height: 1.8; margin: 0 auto;'>
        🚀 <b>ابتكار علمي مستدام من فكرة وتطوير فريق أوكتانوفا 2026</b><br>
        يقوم المشروع على فكرة هندسية متطورة عبر استبدال الجوامد اللادهنية للبن الفرز (SNF) بالكامل بشرش اللبن السائل الحلو الخام لتحقيق التوازن بين المذاق الاستوائي الفاخر والقيمة التغذوية الوظيفية العليا.
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class='badge-bar'>
        <span class='custom-badge'>🌿 100% شرش لبن طبيعي</span>
        <span class='custom-badge'>✨ قوام كريمي ناعم ونكهة غنية</span>
        <span class='custom-badge'>♻️ Zero Waste صديق للبيئة</span>
    </div>
    """, unsafe_allow_html=True)

    # المربعات الـ 3 الثابتة جنب بعض (Tiled Layout) بدل الكاروسيل
    st.markdown("<br>", unsafe_allow_html=True)
    t1, t2, t3 = st.columns(3, gap="medium")
    with t1:
        st.markdown("<div class='custom-box'><strong style='color:#f39c12;'>🎯 رؤيتنا وهدفنا الأساسي</strong><p style='font-size:13px; color:#ccc; margin-top:5px;'>تطوير منتجات وظيفية تدعم الصحة العامة وتعزز المناعة، لسد الفجوة بين المثلجات التقليدية والمتطلبات الصحية للمستهلك الواعي.</p></div>", unsafe_allow_html=True)
    with t2:
        st.markdown("<div class='custom-box'><strong style='color:#f39c12;'>📈 ثقة المستهلك والأمان الحيوي</strong><p style='font-size:13px; color:#ccc; margin-top:5px;'>أثبتت الدراسات الميدانية للفريق أن 96% من المستهلكين رحبوا بفكرة استخدام الشرش بمجرد معرفة فوائده البيئية والصحية.</p></div>", unsafe_allow_html=True)
    with t3:
        st.markdown("<div class='custom-box'><strong style='color:#f39c12;'>📜 المواصفات القياسية المصرية</strong><p style='font-size:13px; color:#ccc; margin-top:5px;'>المنتج مصنع ومطور علمياً ومطابق تماماً للمواصفات القياسية المصرية رقم 1185 لسنة 2005 جـ1 الخاصة بالمثلجات وشربت الآيس كريم.</p></div>", unsafe_allow_html=True)

    st.markdown("<br><hr style='border-color:#222232;'><br>", unsafe_allow_html=True)
    
    # عرض المنتجين جنب بعض (Split Screen Layout) مع الحقائق الغذائية الكاملة
    st.markdown("<h2 style='font-weight:700; margin-bottom:30px;'>🍨 عبوات وحقائق SheroWhey الغذائية</h2>", unsafe_allow_html=True)
    
    col_left, col_right = st.columns(2, gap="large")
    
    with col_right: # منتج المانجو على اليمين
        st.markdown("<div class='custom-box'>", unsafe_allow_html=True)
        st.markdown("<h3 style='color:#f39c12; margin-top:0;'>🥭 شربت المانجو الطبيعي المدعم بالكركمين</h3>", unsafe_allow_html=True)
        st.markdown("<p style='font-size:14px; color:#ccc; line-height:1.5;'><b>المكونات الأصلية:</b> شرش سائل، سكر (سكروز)، بيوريه المانجو، عسل جلوكوز، كريمة خفق، مواد مثبتة (صمغ السليلوز CMC E466)، منظم لون ومضاد أكسدة طبيعي (كركمين E100)، منظم حموضة (حمض الستريك E330).</p>", unsafe_allow_html=True)
        st.markdown("<p style='font-size:13px; color:#e74c3c;'>⚠️ تنبيه الحساسية: يحتوي على مكونات الحليب (اللاكتوز والبروتينات) | الحجم: 120 مل</p>", unsafe_allow_html=True)
        
        try:
            st.image("mango_pack.png", use_container_width=True)
        except:
            st.info("💡 يرجى رفع ملف العبوة باسم mango_pack.png")
        
        st.markdown("<b style='color:#f39c12;'>📊 الحقائق الغذائية الكاملة (حصة 100 جرام | 4 أوز):</b>", unsafe_allow_html=True)
        st.table({
            "العنصر الغذائي": ["السعرات الحرارية", "إجمالي الدهون", "البروتين", "إجمالي الكربوهيدرات", "الرماد", "الكالسيوم", "البوتاسيوم", "فيتامين سي"],
            "الكمية في الحصة": ["117.7 kcal", "1.1 g", "0.11 g", "26.85 g", "0.64 g", "26.8 mg", "173.9 mg", "22.1 mg"]
        })
        if st.button("🛍️ إضافة عبوة المانجو", key="add_m_split_btn", use_container_width=True):
            st.session_state.want_m = True
            st.toast("🎯 تم إضافة شربت المانجو والكركمين لعربتك!")
            st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)

    with col_left: # منتج الفراولة على الشمال
        st.markdown("<div class='custom-box'>", unsafe_allow_html=True)
        st.markdown("<h3 style='color:#f39c12; margin-top:0;'>🍓 شربت الفراولة والرمان الطبيعي</h3>", unsafe_allow_html=True)
        st.markdown("<p style='font-size:14px; color:#ccc; line-height:1.5;'><b>المكونات الأصلية:</b> شرش سائل، سكر (سكروز)، بيوريه فراولة، عصير رمان طبيعي، عسل جلوكوز، كريمة خفق، مواد مثبتة مثخنات قوام (صمغ السليلوز CMC E466)، منظم حموضة (حمض الستريك E330).</p>", unsafe_allow_html=True)
        st.markdown("<p style='font-size:13px; color:#e74c3c;'>⚠️ تنبيه الحساسية: يحتوي على مكونات الحليب (اللاكتوز والبروتينات) | الحجم: 120 مل</p>", unsafe_allow_html=True)
        
        try:
            st.image("strawberry_pack.png", use_container_width=True)
        except:
            st.info("💡 يرجى رفع ملف العبوة باسم strawberry_pack.png")
        
        st.markdown("<b style='color:#f39c12;'>📊 الحقائق الغذائية الكاملة (حصة 92.6 جرام | 4 أوز):</b>", unsafe_allow_html=True)
        st.table({
            "العنصر الغذائي": ["السعرات الحرارية", "إجمالي الدهون", "البروتين", "إجمالي الكربوهيدرات", "الرماد", "الكالسيوم", "البوتاسيوم", "فيتامين سي"],
            "الكمية في الحصة": ["116.42 kcal", "1.02 g", "0.10 g", "26.71 g", "0.87 g", "19.45 mg", "165.01 mg", "20.46 mg"]
        })
        if st.button("🛍️ إضافة عبوة الفراولة", key="add_s_split_btn", use_container_width=True):
            st.session_state.want_s = True
            st.toast("🎯 تم إضافة شربت الفراولة والرمان لعربتك!")
            st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)

# ==========================================
# التبويب الثاني: التأصيل العلمي والاستدامة (إرجاع كافة التفاصيل الدقيقة)
# ==========================================
with tab2:
    st.markdown("<h2 style='color:#f39c12; margin-bottom:30px;'>🔬 التأصيل العلمي والهوية الأكاديمية الكاملة للمشروع</h2>", unsafe_allow_html=True)
    
    # عرض صورة التيم المخصصة بالمنتصف
    st.markdown("<b style='color:#f39c12;'>📸 فريق البحث العلمي (أوكتانوفا 2026)</b>", unsafe_allow_html=True)
    try:
        st.image("team_photo.jpg", use_container_width=True)
    except:
        st.info("💡 يرجى رفع صورة التيم باسم team_photo.jpg لتظهر هنا في السنتر")

    # 1. صندوق الجهة الأكاديمية
    st.markdown("""
    <div class='custom-box'>
        <h3 style='color:#f39c12; margin-bottom:10px;'>🏫 الجهة الأكاديمية والبحثية</h3>
        <p style='font-size:16px;'><b>الجهة:</b> كلية الزراعة - جامعة عين شمس | قسم علوم الأغذية (شعبة الألبان وصناعات الأغذية)</p>
        <p style='font-size:16px;'><b>المرحلة الدراسية:</b> طلبة المستوى الرابع (فريق أوكتانوفا - 2026)</p>
    </div>
    """, unsafe_allow_html=True)
    
    # 2. صندوق أسماء أعضاء الفريق بالكامل
    st.markdown("""
    <div class='custom-box'>
        <h3 style='color:#f39c12; margin-bottom:10px;'>👥 أسماء أعضاء فريق العمل</h3>
        <p style='font-size:16px; line-height:1.8;'>
            <b>شعبة الألبان:</b> مصطفى صبحي | بسام عادل | رجب محمد | فؤاد سيد <br>
            <b>شعبة صناعات الأغذية:</b> نورهان محمد | مريم طارق | شمس محمود | منة الله عوض
        </p>
    </div>
    """, unsafe_allow_html=True)

    # 3. صندوق اللجنة الإشرافية بالكامل
    st.markdown("""
    <div class='custom-box'>
        <h3 style='color:#f39c12; margin-bottom:10px;'>👨‍🏫 الهيئة الإشرافية العليا</h3>
        <p style='font-size:16px; line-height:1.7; color:#ddd;'>
            <b>أ.د. عزة فرحات</b> (أستاذ تكنولوجيا الألبان)<br>
            <b>د. نعمة سعيد</b> (مدرس تكنولوجيا الألبان)<br>
            <b>م.م. حسام الرحماني</b> (مدرس مساعد تكنولوجيا الألبان)<br>
            <b>أ. آيه أحمد إسماعيل</b> (معيدة بقسم علوم الأغذية)
        </p>
    </div>
    """, unsafe_allow_html=True)

    # 4. القيمة الغذائية للشرش (سطر مستقل ومميز)
    st.markdown("""
    <div class='custom-box'>
        <h3 style='color:#2ecc71; margin-bottom:10px;'>🥛 القيمة الغذائية لشرش اللبن السائل الطبيعي</h3>
        <p style='font-size:15px; line-height:1.7;'>
            <b>لماذا الشرش؟</b> الشرش غني بالبرطينات عالية القيمة الحيوية (Whey Proteins)، واستخدامه بداخل صياغة الهيكل التكويني للشربت يعطي قواماً كريمياً ناعماً ومميزاً، ويعزز الامتصاص الحيوي الكامل للمواد الفعالة والنشطة مثل الكركمين في الجسم.
        </p>
    </div>
    """, unsafe_allow_html=True)

    # 5. الاستدامة والبيئة (سطر مستقل ومميز)
    st.markdown("""
    <div class='custom-box'>
        <h3 style='color:#2ecc71; margin-bottom:10px;'>🌍 الاستدامة والبيئة (OUR SUSTAINABLE PLANET)</h3>
        <p style='font-size:15px; line-height:1.7; text-align:justify;'>
            يُعتبر "الشرش السائل" ناتجاً ثانوياً ضخماً متخلفاً عن صناعة الأجبان، والتخلص منه دون معالجة يمثل عبئاً بيئياً كبيراً على شبكات الصرف ومصادر المياه العذبة. قام الفريق بتحويل هذا التحدي البيئي إلى فرصة ابتكارية واعدة عبر استبدال المكون المائي الكامل والمواد الصلبة اللادهنية (SNF) للبن الفرز في الشربت بالشرش الحلو السائل الخام، لتحقيق معادلة الاستدامة وتقليل الهدر البيئي مع رفع القيمة الحيوية للمنتج الوظيفي النهائي (Zero Waste).
        </p>
    </div>
    """, unsafe_allow_html=True)

    # 6. المركبات النشطة والفوائد الصحية بالكامل
    st.markdown("""
    <div class='custom-box'>
        <h3 style='color:#f39c12; margin-bottom:10px;'>🧪 المركبات النشطة حيوياً والفوائد الصحية الموثقة</h3>
        <p style='font-size:15px; line-height:1.8; text-align:right;'>
            <b>🥭 توليفة شربت المانجو والكركمين (التوليفة الذهبية لتعزيز المناعة):</b><br>
            • <b>المانجيفيرين:</b> مضاد أكسدة قوي مستخلص طبيعياً من ثمار المانجو.<br>
            • <b>الكركمينويدات:</b> المركب الفعال والنشط في الكركم بخصائصه الفريدة المضادة للأمراض.<br>
            • <b>فيتامين C والكاروتينات:</b> لتعزيز نضارة الخلايا وحمايتها من الإجهاد التأكسدي والالتهابات، مع تكامل حيوي بين بروتينات الشرش والكركمين لزيادة معدل الامتصاص.<br><br>
            <b>🍓 توليفة شربت الفراولة والرمان (إنتعاش وصحة القلب):</b><br>
            • <b>الأنثوسيانين:</b> الصبغات الحمراء الطبيعية التي تحمي الأوعية الدموية وتدعم الدورة الدموية.<br>
            • <b>حمض الإيلاجيك:</b> متوفر بكثرة في الرمان لمكافحة الشوارد الحرة والمساعدة في ضبط ضغط الدم طبيعياً.<br>
            • <b>البولي فينولات:</b> لدعم الوظائف الحيوية ونشاط مضاد للميكروبات، وتعويض الفيتامينات والمعادن بفضل الشرش الحلو السائل.
        </p>
    </div>
    """, unsafe_allow_html=True)

# ==========================================
# التبويب الثالث: الشات الذكي (روابط أيقونات فلات أيكون مستقرة ومفلترة)
# ==========================================
with tab3:
    st.markdown("### 💬 SheroBot - مستشارك الذكي والأكاديمي")
    
    if st.button("🗑️ مسح سجل المحادثة بالكامل", use_container_width=True, key="clear_chat_tab3"):
        st.session_state.chat_history = []
        st.toast("🧹 تم تصفير سجل المحادثة بنجاح!")
        st.rerun()

    st.write("")
    
    # استخدام روابط فلات أيكون مستقرة وعالمية تفتح على الموبايل بدون أي كود مكسور
    bot_avatar_url = "https://cdn-icons-png.flaticon.com/512/4712/4712035.png"
    user_avatar_url = "https://cdn-icons-png.flaticon.com/512/1144/1144709.png"

    # عرض تاريخ الشات
    for message in st.session_state.chat_history:
        current_avatar = bot_avatar_url if message["role"] == "assistant" else user_avatar_url
        with st.chat_message(message["role"], avatar=current_avatar): 
            st.markdown(message["text"])

    if prompt := st.chat_input("اكتب استفسارك التغذوي أو العلمي هنا للـ SheroBot..."):
        with st.chat_message("user", avatar=user_avatar_url): 
            st.markdown(prompt)
        st.session_state.chat_history.append({"role": "user", "text": prompt})
        
        # هندسة الاتصال المباشر والمستقر مع الـ API لمنع أخطاء الـ Timeout أو السيرفر مشغول
        try:
            response = model_gemini.generate_content(prompt)
            raw_text = response.text
        except Exception:
            if client_meta is not None:
                try:
                    meta_response = client_meta.chat.completions.create(
                        model="llama-3.3-70b-versatile",
                        messages=[{"role": "system", "content": customer_service_persona}, {"role": "user", "content": prompt}]
                    )
                    raw_text = meta_response.choices[0].message.content
                except Exception:
                    raw_text = "⚠️ خط الاتصال مزدحم حالياً يا فندم، تفضل بالانتقال للتبويب الأخير لإرسال طلبك فوراً!"
            else:
                raw_text = "⚠️ خط الاتصال مزدحم حالياً يا فندم، تفضل بالانتقال للتبويب الأخير لإرسال طلبك فوراً!"

        if raw_text:
            # فلترة وتنظيف النصوص من أي رموز أو كلمات مكسورة تلقائياً
            clean_display_text = re.sub(r'\[SET_ORDER:.*?\]', '', raw_text)
            clean_display_text = clean_display_text.replace("smart_toy", "").replace("face", "").replace(":", "")
            
            st.session_state.chat_history.append({"role": "assistant", "text": clean_display_text})
            
            # معالجة الأتمتة وضبط أرقام سلة المشتريات
            match = re.search(r'\[SET_ORDER:\s*MANGO=(\d+),\s*STRAWBERRY=(\d+)\]', raw_text)
            if match:
                m_qty = int(match.group(1)); s_qty = int(match.group(2))
                if m_qty > 0: st.session_state.want_m = True; st.session_state.qty_m = m_qty
                if s_qty > 0: st.session_state.want_s = True; st.session_state.qty_s = s_qty
                st.toast("🛒 تم تحديث سلة المشتريات تلقائياً!")

            with st.chat_message("assistant", avatar=bot_avatar_url): 
                st.markdown(clean_display_text)
            st.rerun()

# ==========================================
# التبويب الرابع: استمارة الشحن والطلب السريع
# ==========================================
with tab4:
    st.markdown("### 📋 تأكيد الفاتورة وإتمام الطلب السريع")
    
    col_order_m, col_order_s = st.columns(2, gap="large")
    with col_order_m:
        st.checkbox("🥭 عبوة شربت المانجو والكركمين", key="want_m")
        if st.session_state.want_m: 
            st.number_input("الكمية المطلوبة (كوب 120 مل):", min_value=1, max_value=100, key="qty_m")
        
    with col_order_s:
        st.checkbox("🍓 عبوة شربت الفراولة والرمان", key="want_s")
        if st.session_state.want_s: 
            st.number_input("الكمية المطلوبة (كوب 120 مل):", min_value=1, max_value=100, key="qty_s")
        
    st.markdown("---")
    st.markdown("#### 👤 بيانات الشحن والتواصل للطلب")
    c_col1, c_col2 = st.columns(2)
    with c_col1:
        customer_name = st.text_input("الاسم الكامل للعميل:")
        customer_phone = st.text_input("رقم الهاتف الذكي للتواصل:")
    with c_col2:
        customer_address = st.text_area("عنوان التوصيل بالتفصيل لشحن المنتج:")
    
    product_details = ""
    if st.session_state.want_m: product_details += f"• شربت مانجو وكركمين وظيفي [الكمية: {st.session_state.qty_m} كوب]\n"
    if st.session_state.want_s: product_details += f"• شربت فراولة ورمان صحي [الكمية: {st.session_state.qty_s} كوب]\n"
    if not st.session_state.want_m and not st.session_state.want_s: product_details = "• العربة فارغة، لم تضف أي نكهة بعد!\n"

    msg_template = f"🛒 طلب شراء جديد لمنتج SheroWhey\n\n👤 العميل: {customer_name}\n📱 الهاتف: {customer_phone}\n🏠 العنوان: {customer_address}\n\n🍦 تفاصيل الأكواب:\n{product_details}\n✨ إنتاج فريق أوكتانوفا 2026 - كلية الزراعة جامعة عين شمس"
    
    st.markdown("#### 🚀 تنفيذ الطلب السريع والربط الخارجي:")
    btn_col1, btn_col2 = st.columns(2)
    with btn_col1: 
        st.link_button("📱 إرسال الطلب عبر الواتساب", f"https://wa.me/201090416662?text={urllib.parse.quote(msg_template)}", use_container_width=True, disabled=(not st.session_state.want_m and not st.session_state.want_s))
    with btn_col2: 
        st.link_button("📧 إرسال الطلب عبر الإيميل للمعمل", f"mailto:sheroway78@gmail.com?subject=Order_SheroWhey&body={urllib.parse.quote(msg_template)}", use_container_width=True, disabled=(not st.session_state.want_m and not st.session_state.want_s))

    st.markdown("""
        <br><br>
        <div style="text-align: center; color: #666677; font-size: 0.9rem; border-top: 1px solid #222232; padding-top: 15px;">
            © Octanova 2026 | جميع الحقوق محفوظة لمشروع SheroWhey 🍦
        </div>
    """, unsafe_allow_html=True)
