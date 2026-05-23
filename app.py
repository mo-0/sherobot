import streamlit as st
import google.generativeai as genai

# 1. إعدادات الصفحة
st.set_page_config(
    page_title="مساعد مشاريع التخرج 🎓",
    page_icon="🎓",
    layout="wide"
)

# 2. أكواد CSS للواجهة
custom_css = """
<style>
    [data-testid="stChatMessage"]:nth-child(even) {
        background-color: #f0f8ff; 
        border-radius: 10px;
        padding: 10px;
    }
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
</style>
"""
st.markdown(custom_css, unsafe_allow_html=True)

# 3. الشريط الجانبي (Sidebar) - عام لمشاريع التخرج
with st.sidebar:
    st.title("Graduation Project Assistant 🎓")
    st.write("مساعد ذكي مبني لمساعدتك في تخطيط، كتابة، وإدارة مشروع تخرجك بأسلوب منهجي.")
    st.info("التركيز: تنظيم الأفكار، هيكلة البحث، حل مشاكل التيم، وإدارة الوقت.")

# 4. إعدادات المفتاح
genai.configure(api_key=st.secrets["GEMINI_API_KEY"])

# 5. شخصيتك (تم مسح SheroWay والاحتفاظ بالصفات العقلانية)
mostafa_persona = """
أنت مصطفى، خبير في إدارة وتخطيط مشاريع التخرج. شخصيتك تميل لنمط (INTJ).
تفكيرك تحليلي، استراتيجي، ومنطقي جداً.
عندما يطلب منك شخص مساعدة في مشروع تخرجه، تعتمد في شرحك على "نظرية التنقيط": تبدأ بسرد الحقائق والنقاط الأساسية المجردة، ثم تربطها لتكوين نظام منطقي وهيكل واضح.
ردودك عملية، مباشرة جداً، وتدخل في صلب الموضوع فوراً دون مجاملات أو رغي زائد.
تساعد الطلاب في هيكلة الأبحاث، تقسيم المهام على الفريق، وكتابة تقارير المشاريع (Thesis) بأسلوب علمي.
لهجتك مصرية.
"""

model = genai.GenerativeModel('gemini-2.5-flash', system_instruction=mostafa_persona)

# 6. الواجهة الأساسية
st.title("مساعد مشاريع التخرج 🎓")

# زرار مسح المحادثة
if st.button("مسح المحادثة وبدء محادثة جديدة 🔄"):
    st.session_state.chat = model.start_chat(history=[])

if "chat" not in st.session_state:
    st.session_state.chat = model.start_chat(history=[])

for message in st.session_state.chat.history:
    role = "assistant" if message.role == "model" else "user"
    with st.chat_message(role):
        st.markdown(message.parts[0].text)

# استقبال الأسئلة
if prompt := st.chat_input("اكتب سؤالك هنا (مثال: إزاي أقسم شغل العملي على تيم من 8 أشخاص؟)..."):
    with st.chat_message("user"):
        st.markdown(prompt)
    
    try:
        response = st.session_state.chat.send_message(prompt)
        with st.chat_message("assistant"):
            st.markdown(response.text)
    except Exception as e:
        st.error(f"حصلت مشكلة: {e}")
