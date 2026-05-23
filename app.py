import streamlit as st
import google.generativeai as genai

# 1. إعدادات الصفحة (توسيع الشاشة وتغيير الأيقونة)
st.set_page_config(
    page_title="AI Research Assistant | المساعد البحثي",
    page_icon="💡",
    layout="wide"
)

# 2. حقن أكواد CSS لواجهة Modern (خطوط، ظلال، وتصميم احترافي)
custom_css = """
<style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;600;800&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Cairo', sans-serif !important;
    }
    
    /* تصميم رسايل الشات (كروت بظلال) */
    [data-testid="stChatMessage"] {
        background-color: #ffffff;
        border: 1px solid #e2e8f0;
        border-radius: 12px;
        padding: 15px;
        margin-bottom: 15px;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05);
    }
    
    /* إخفاء القوائم الافتراضية لستريملت */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* تعديل شكل زرار المسح */
    .stButton>button {
        border-radius: 8px;
        border: 1px solid #cbd5e1;
        font-family: 'Cairo', sans-serif !important;
        font-weight: 600;
        transition: all 0.3s;
    }
    .stButton>button:hover {
        background-color: #f1f5f9;
        border-color: #94a3b8;
    }
</style>
"""
st.markdown(custom_css, unsafe_allow_html=True)

# 3. تصميم الشريط الجانبي (Modern Sidebar)
with st.sidebar:
    st.markdown("## 🔬 AI Research Assistant")
    st.markdown("---")
    st.markdown("**مرحباً بك في منصة البحث الذكية.**")
    st.markdown("أنا هنا لمساعدتك في:")
    st.markdown("- 🧠 عصف ذهني وهيكلة الأبحاث\n- 📊 تحليل البيانات وتقسيم المهام\n- 📝 صياغة التقارير الأكاديمية (Thesis)")
    st.markdown("---")
    st.info("💡 **نصيحة:** ابدأ بكلمة 'أهلاً' وسأقوم بتوجيهك خطوة بخطوة لبناء مشروعك.")

# 4. إعدادات الـ API
genai.configure(api_key=st.secrets["GEMINI_API_KEY"])

# 5. الشخصية (تفعيل وضع الـ LLM الكامل مع الاستكشاف التفاعلي)
mostafa_persona = """
أنت نموذج لغوي ضخم (LLM) بقدرات كاملة، تعمل كمساعد بحثي أكاديمي موسوعي. اسمك "مصطفى".
شخصيتك: (INTJ) - عقلاني، تحليلي، ومخطط استراتيجي.
أسلوب شرحك: تعتمد على "نظرية التنقيط" (Pointillism)؛ تبدأ بسرد الحقائق المجردة ثم تربطها لتكوين نظام منطقي وهيكل واضح.
تعليماتك الأساسية:
1. عندما يبدأ المستخدم المحادثة، لا تعطِ إجابات جاهزة أو عشوائية. بدلاً من ذلك، اطرح سؤالاً أو سؤالين بالكتير لتستكشف تفاصيل مشروعه (مجال البحث، الفكرة، المرحلة الحالية، التحديات).
2. بناءً على إجاباته، قم بتحليل الموقف واعرض عليه نوع المساعدة المناسب (تخطيط المشروع، كتابة علمية، مراجعة منهجية، توزيع مهام).
3. استخدم معرفتك الواسعة في كل المجالات لدعمه بأدق التفاصيل العلمية والعملية.
4. ردودك عملية، مباشرة، خالية من الحشو.
5. لهجتك: مصرية احترافية.
"""

model = genai.GenerativeModel('gemini-2.5-flash', system_instruction=mostafa_persona)

# 6. الواجهة الرئيسية
st.title("💡 المساعد البحثي الذكي لمشاريع التخرج")
st.markdown("ابدأ المحادثة، وسأطرح عليك الأسئلة المناسبة لفهم مشروعك ومساعدتك بأفضل شكل.")

col1, col2 = st.columns([1, 5])
with col1:
    if st.button("🔄 محادثة جديدة"):
        st.session_state.chat = model.start_chat(history=[])
        st.rerun()

# 7. إدارة ذاكرة المحادثة
if "chat" not in st.session_state:
    st.session_state.chat = model.start_chat(history=[])

for message in st.session_state.chat.history:
    role = "assistant" if message.role == "model" else "user"
    with st.chat_message(role):
        st.markdown(message.parts[0].text)

# 8. استقبال الردود
if prompt := st.chat_input("اكتب 'أهلاً' لتبدأ، أو اكتب تفاصيل مشروعك مباشرة..."):
    with st.chat_message("user"):
        st.markdown(prompt)
    
    try:
        response = st.session_state.chat.send_message(prompt)
        with st.chat_message("assistant"):
            st.markdown(response.text)
    except Exception as e:
        st.error(f"حصلت مشكلة في الاتصال: {e}")
