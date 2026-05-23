import streamlit as st
import google.generativeai as genai

# 1. إعدادات الصفحة (لازم تكون في البداية)
st.set_page_config(
    page_title="SheroBot | Dairy Assistant",
    page_icon="🍦",
    layout="wide"
)

# 2. حقن أكواد CSS لتعديل الواجهة
custom_css = """
<style>
    /* تغيير لون خلفية رسايل البوت (لون أزرق فاتح كمثال) */
    [data-testid="stChatMessage"]:nth-child(even) {
        background-color: #f0f8ff; 
        border-radius: 10px;
        padding: 10px;
    }
    /* إخفاء القائمة العلوية والعلامة المائية لـ Streamlit */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
</style>
"""
st.markdown(custom_css, unsafe_allow_html=True)

# 3. الشريط الجانبي (Sidebar)
with st.sidebar:
    st.title("SheroWay Project 🧬")
    st.write("مساعد أكاديمي مخصص لمهندسي قسم الألبان.")
    st.info("التركيز الحالي: استبدال SNF اللبن الفرز بـ SNF الشرش الحلو السائل في المخاليط لتقليل التكلفة.")
    # لو معاك اللوجو اللي صممته، نقدر نضيفه هنا بعدين
    
# إعدادات الـ API والشخصية
genai.configure(api_key=st.secrets["GEMINI_API_KEY"])

mostafa_persona = """
أنت مصطفى، طالب في السنة النهائية بكلية الزراعة قسم الألبان. شخصيتك (INTJ).
شرحك يعتمد على نظرية التنقيط: سرد الحقائق ثم ربطها لتكوين نظام منطقي.
ردودك عملية ومباشرة جداً. استخدم أمثلة من مشروعك (استبدال SNF اللبن الفرز بـ SNF الشرش الحلو السائل).
لهجتك مصرية.
"""

model = genai.GenerativeModel('gemini-2.5-flash', system_instruction=mostafa_persona)

# الواجهة الأساسية للشات
st.title("SheroBot 🍦 - Ask the Expert")

# زرار مسح المحادثة
if st.button("مسح المحادثة وبدء محادثة جديدة 🔄"):
    st.session_state.chat = model.start_chat(history=[])

if "chat" not in st.session_state:
    st.session_state.chat = model.start_chat(history=[])

for message in st.session_state.chat.history:
    role = "assistant" if message.role == "model" else "user"
    with st.chat_message(role):
        st.markdown(message.parts[0].text)

if prompt := st.chat_input("اكتب سؤالك هنا..."):
    with st.chat_message("user"):
        st.markdown(prompt)
    
    try:
        response = st.session_state.chat.send_message(prompt)
        with st.chat_message("assistant"):
            st.markdown(response.text)
    except Exception as e:
        st.error(f"حصلت مشكلة: {e}")
