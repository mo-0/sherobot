import streamlit as st
import google.generativeai as genai

# 1. سحب المفتاح من إعدادات Streamlit
genai.configure(api_key=st.secrets["GEMINI_API_KEY"])

# 2. شخصيتك الأكاديمية (INTJ)
mostafa_persona = """
أنت مصطفى، طالب في السنة النهائية بكلية الزراعة قسم الألبان. شخصيتك (INTJ).
شرحك يعتمد على نظرية التنقيط: سرد الحقائق ثم ربطها لتكوين نظام منطقي.
ردودك عملية ومباشرة جداً. استخدم أمثلة من مشروعك (استبدال SNF اللبن الفرز بـ SNF الشرش الحلو السائل في المخاليط لتقليل التكلفة ورفع القيمة الحيوية مع الحفاظ على قوام المنتج).
لهجتك مصرية.
"""

# 3. تحديد الموديل بالإصدار الصحيح
model = genai.GenerativeModel('gemini-2.0-flash', system_instruction=mostafa_persona)

# 4. واجهة الموقع
st.title("SheroBot 🍦 - Academic Assistant")

# زرار مسح المحادثة
if st.button("مسح المحادثة وبدء محادثة جديدة 🔄"):
    st.session_state.chat = model.start_chat(history=[])

if "chat" not in st.session_state:
    st.session_state.chat = model.start_chat(history=[])

for message in st.session_state.chat.history:
    role = "assistant" if message.role == "model" else "user"
    with st.chat_message(role):
        st.markdown(message.parts[0].text)

# 5. استقبال الأسئلة والرد
if prompt := st.chat_input("اكتب سؤالك هنا..."):
    with st.chat_message("user"):
        st.markdown(prompt)
    
    try:
        response = st.session_state.chat.send_message(prompt)
        with st.chat_message("assistant"):
            st.markdown(response.text)
    except Exception as e:
        st.error(f"حصلت مشكلة: {e}")
