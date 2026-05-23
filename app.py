import streamlit as st
import google.generativeai as genai

# 1. سحب المفتاح من إعدادات Streamlit
genai.configure(api_key=st.secrets["GEMINI_API_KEY"])

# 2. الكود بيسحب اسم الموديل المتاح أوتوماتيك عشان يمنع إيرور NotFound
@st.cache_resource
def get_best_model_name():
    try:
        for m in genai.list_models():
            if 'generateContent' in m.supported_generation_methods and 'flash' in m.name:
                return m.name
    except:
        pass
    return "models/gemini-1.5-flash" # اسم احتياطي لو مقدرش يسحب القائمة

flash_model_name = get_best_model_name()

# 3. شخصيتك الأكاديمية
mostafa_persona = """
أنت طوخي، طالب في السنة النهائية بكلية الزراعة قسم الألبان. شخصيتك (INTJ).
شرحك يعتمد على نظرية التنقيط: سرد الحقائق ثم ربطها لتكوين نظام منطقي.
ردودك عملية ومباشرة جداً. استخدم أمثلة .
لهجتك مصرية.
"""

# 4. تجهيز الموديل بالاسم اللي تم سحبه
model = genai.GenerativeModel(flash_model_name, system_instruction=mostafa_persona)

# 5. واجهة الموقع
st.title("TOKHYgbt - Academic Assistant")

if "chat" not in st.session_state:
    st.session_state.chat = model.start_chat(history=[])

for message in st.session_state.chat.history:
    role = "assistant" if message.role == "model" else "user"
    with st.chat_message(role):
        st.markdown(message.parts[0].text)

# 6. استقبال الأسئلة مع نظام حماية من الكراش
if prompt := st.chat_input("اكتب سؤالك هنا..."):
    with st.chat_message("user"):
        st.markdown(prompt)
    
    try:
        response = st.session_state.chat.send_message(prompt)
        with st.chat_message("assistant"):
            st.markdown(response.text)
    except Exception as e:
        # لو حصلت مشكلة، هتظهر رسالة حمراء شيك بدل ما الموقع يكراش
        st.error(f"حصلت مشكلة في الاتصال بالسيرفر: {e}")
