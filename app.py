import streamlit as st
import google.generativeai as genai
import urllib.parse
import re
from openai import OpenAI

# ==========================================
# 1. إعدادات الصفحة والـ CSS المتقدم (Slide-Deck Look)
# ==========================================
st.set_page_config(page_title="SheroWhey | Octanova 2026", page_icon="🍦", layout="wide")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@300;400;600;700;900&display=swap');
    
    html, body, [data-testid="stAppViewContainer"] {
        font-family: 'Cairo', sans-serif !important;
        background-color: #0d0d11 !important;
        color: #ffffff !important;
        direction: rtl !important;
        text-align: center !important;
    }
    
    /* جعل كل النصوص والعناوين في المنتصف */
    h1, h2, h3, h4, h5, h6, p, span, label, .stMarkdown {
        font-family: 'Cairo', sans-serif !important;
        text-align: center !important;
        direction: rtl !important;
        margin-left: auto !important;
        margin-right: auto !important;
    }

    /* تنسيق التبويبات العلوية بأسماء جديدة ومودرن */
    div[data-testid="stTabs"] button {
        font-family: 'Cairo', sans-serif !important;
        font-size: 16px !important;
        font-weight: 600 !important;
        color: #8c8c9a !important;
        background-color: #14141c !important;
        border: 1px solid #1f1f2e !important;
        padding: 12px 25px !important;
        flex-grow: 1 !important;
    }
    div[data-testid="stTabs"] button[aria-selected="true"] {
        color: #f39c12 !important;
        background-color: #1c1c28 !important;
        border-bottom: 4px solid #f39c12 !important;
    }

    /* صناديق التأصيل العلمي (عمود واحد متراص) */
    .science-box {
        background: linear-gradient(145deg, #14141c, #1a1a26);
        border: 1px solid #222232;
        border-radius: 20px;
        padding: 30px;
        margin-bottom: 25px;
        width: 100%;
        max-width: 1000px;
        margin-left: auto;
        margin-right: auto;
        box-shadow: 0 10px 30px rgba(0,0,0,0.3);
    }
    
    .sub-heading {
        color: #f39c12;
        font-size: 22px;
        font-weight: 700;
        display: block;
        margin-bottom: 15px;
        border-bottom: 1px solid #333;
        padding-bottom: 10px;
    }

    .badge-bar {
        margin: 20px 0;
        display: flex;
        justify-content: center;
        gap: 15px;
        flex-wrap: wrap;
    }
    
    .custom-badge {
        background: #1e1e2a;
        padding: 6px 18px;
        border-radius: 50px;
        font-size: 14px;
        border: 1px solid #f39c12;
        color: #f39c12;
    }

    /* إلغاء الفراغات الزائدة */
    .block-container {
        padding-top: 1.5rem !important;
        max-width: 95% !important;
    }
    
    /* تصميم الجداول التغذوية */
    .stTable {
        margin-top: 15px;
        border-radius: 12px;
        overflow: hidden;
    }
    </style>
""", unsafe_allow_html=True)

# تهيئة الـ Session States
if "want_m" not in st.session_state: st.session_state.want_m = False
if "qty_m" not in st.session_state: st.session_state.qty_m = 1
if "want_s" not in st.session_state: st.session_state.want_s = False
if "qty_s" not in st.session_state: st.session_state.qty_s = 1

# ==========================================
# 2. إعدادات الـ APIs
# ==========================================
genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
customer_service_persona = "أنت مساعد ذكي لمنتج SheroWhey، رد بلهجة مصرية ودودة ومحاذاة سنتر."
model_gemini = genai.GenerativeModel('gemini-2.5-flash', system_instruction=customer_service_persona)

# 3. التبويبات بأسماء عصرية
tab1, tab2, tab3, tab4 = st.tabs([
    "✨ تجربة SheroWhey", 
    "🔬 التأصيل العلمي والاستدامة",
    "💬 المساعد الذكي SheroBot", 
    "🚀 تأكيد وإرسال الطلبات"
])

# ==========================================
# التبويب الأول: الواجهة الرئيسية المودرن (Centered Slide)
# ==========================================
with tab1:
    st.markdown("<h1 style='font-size: 65px; font-weight: 900; color: white; margin-bottom: 0;'>SheroWhey</h1>", unsafe_allow_html=True)
    st.markdown("<h3 style='color: #f39c12; font-weight: 600; margin-top: 0;'>معنى جديد للشربت | إنتاج شربت وظيفي مبتكر</h3>", unsafe_allow_html=True)
    
    # تفكيك الفقرة الكبيرة لنقاط جذابة
    st.markdown("""
    <div style='max-width: 900px; margin: 25px auto; font-size: 18px; color: #ccc; line-height: 1.8;'>
        🚀 <b>ابتكار علمي مستدام من فكرة وتطوير فريق أوكتانوفا 2026</b><br>
        ✅ استبدال الجوامد اللادهنية (SNF) بالكامل بشرش اللبن السائل الطبيعي.<br>
        ✅ توازن مثالي بين المذاق الاستوائي الفاخر والقيمة التغذوية الوظيفية.<br>
        ✅ حلول غذائية تدعم الصحة العامة وتعزز المناعة بشكل طبيعي.
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class='badge-bar'>
        <span class='custom-badge'>🌿 100% شرش لبن طبيعي</span>
        <span class='custom-badge'>✨ قوام كريمي ناعم</span>
        <span class='custom-badge'>♻️ ابتكار Zero Waste</span>
    </div>
    """, unsafe_allow_html=True)

    # قسم المنتجات (بدون صور عشوائية)
    st.markdown("<br><h2 style='font-weight:700;'>🍨 اختياراتنا الوظيفية</h2>", unsafe_allow_html=True)
    col_m, col_s = st.columns(2, gap="large")
    
    with col_m:
        st.markdown("<div class='science-box'><h3>🥭 مانجو طبيعي بالكركمين</h3>", unsafe_allow_html=True)
        try:
            st.image("mango_pack.jpg", use_container_width=True)
        except:
            st.warning("⚠️ ارفع صورة عبوة المانجو باسم mango_pack.jpg")
        st.table({"العنصر": ["سعرات", "بروتين", "كالسيوم"], "الكمية": ["117.7", "0.11g", "26.8mg"]})
        if st.button("🛍️ إضافة العبوة", key="add_m"):
            st.session_state.want_m = True
            st.toast("تمت الإضافة!")
        st.markdown("</div>", unsafe_allow_html=True)

    with col_s:
        st.markdown("<div class='science-box'><h3>🍓 فراولة ورمان طبيعي</h3>", unsafe_allow_html=True)
        try:
            st.image("strawberry_pack.jpg", use_container_width=True)
        except:
            st.warning("⚠️ ارفع صورة عبوة الفراولة باسم strawberry_pack.jpg")
        st.table({"العنصر": ["سعرات", "بروتين", "كالسيوم"], "الكمية": ["116.4", "0.10g", "19.4mg"]})
        if st.button("🛍️ إضافة العبوة", key="add_s"):
            st.session_state.want_s = True
            st.toast("تمت الإضافة!")
        st.markdown("</div>", unsafe_allow_html=True)

# ==========================================
# التبويب الثاني: التأصيل العلمي (عمود واحد متراص)
# ==========================================
with tab2:
    st.markdown("<h2 style='color:#f39c12; margin-bottom:30px;'>🔬 الهوية الأكاديمية والبحثية</h2>", unsafe_allow_html=True)
    
    # 1. صندوق الجهة والفريق
    st.markdown("""
    <div class='science-box'>
        <span class='sub-heading'>🏫 الجهة الأكاديمية</span>
        كلية الزراعة - جامعة عين شمس | قسم علوم الأغذية<br>
        طلبة المستوى الرابع - <b>فريق أوكتانوفا 2026</b>
    </div>
    """, unsafe_allow_html=True)
    
    # 2. صورة الفريق
    st.markdown("<b style='color:#f39c12;'>📸 صورة فريق البحث</b>", unsafe_allow_html=True)
    try:
        st.image("team_photo.jpg", use_container_width=True)
    except:
        st.info("💡 ارفع صورة التيم باسم team_photo.jpg")
        
    st.markdown("""
    <div class='science-box'>
        <span class='sub-heading'>👥 أعضاء فريق أوكتانوفا</span>
        مصطفى صبحي | بسام عادل | رجب محمد | فؤاد سيد <br>
        نورهان محمد | مريم طارق | شمس محمود | منة الله عوض
    </div>
    """, unsafe_allow_html=True)

    # 3. الهيئة الإشرافية
    st.markdown("""
    <div class='science-box'>
        <span class='sub-heading'>👨‍🏫 الهيئة الإشرافية العليا</span>
        أ.د. عزة فرحات | د. نعمة سعيد | م.م. حسام الرحماني | أ. آيه أحمد إسماعيل
    </div>
    """, unsafe_allow_html=True)

    # 4. لماذا الشرش؟
    st.markdown("""
    <div class='science-box'>
        <span class='sub-heading'>🥛 القيمة الغذائية لشرش اللبن السائل</span>
        الشرش غني بالبروتينات عالية القيمة الحيوية، واستخدامه يعطي قواماً غنياً ويعزز امتصاص المواد الفعالة مثل الكركمين في الجسم.
    </div>
    """, unsafe_allow_html=True)

    # 5. الاستدامة
    st.markdown("""
    <div class='science-box'>
        <span class='sub-heading'>🌍 الاستدامة والبيئة (OUR SUSTAINABLE PLANET)</span>
        تحويل "الشرش السائل" من عبء بيئي إلى فرصة ابتكارية عبر استبدال المكون المائي بالكامل لتحقيق معادلة الاستدامة وتقليل الهدر البيئي.
    </div>
    """, unsafe_allow_html=True)

    # 6. المركبات النشطة
    st.markdown("""
    <div class='science-box'>
        <span class='sub-heading'>🧪 المركبات النشطة حيوياً</span>
        <b>المانجيفيرين والكركمينويدات:</b> لتعزيز المناعة ومكافحة الالتهابات.<br>
        <b>الأنثوسيانين وحمض الإيلاجيك:</b> لدعم صحة القلب والدورة الدموية.
    </div>
    """, unsafe_allow_html=True)

# ==========================================
# التبويب الرابع: صفحة الطلب (تعديلات الإيميل والروابط)
# ==========================================
with tab4:
    st.markdown("### 📋 إتمام وتأكيد طلبك")
    
    c1, c2 = st.columns(2)
    with c1: st.checkbox("🥭 عبوة المانجو والكركمين", key="want_m")
    with c2: st.checkbox("🍓 عبوة الفراولة والرمان", key="want_s")
    
    st.markdown("---")
    customer_name = st.text_input("👤 الاسم الكامل للعميل:")
    customer_phone = st.text_input("📱 رقم الهاتف:")
    customer_address = st.text_area("🏠 عنوان التوصيل:")
    
    st.markdown("#### 🚀 أرسل طلبك الآن")
    btn_col1, btn_col2 = st.columns(2)
    
    # تجهيز الرسالة
    msg = f"طلب جديد SheroWhey للعميل {customer_name}"
    
    with btn_col1:
        st.link_button("📱 إرسال عبر الواتساب", f"https://wa.me/201090416662?text={urllib.parse.quote(msg)}", use_container_width=True)
    with btn_col2:
        # تعديل نص زر الإيميل
        st.link_button("📧 إرسال الطلب عبر الإيميل", f"mailto:octanova.team@example.com?subject=SheroWhey_Order&body={urllib.parse.quote(msg)}", use_container_width=True)

# (ملاحظة: تبويب الشات SheroBot تم تركه كما هو مع ضمان محاذاته للسنتر عبر الـ CSS العام)
