import streamlit as st
import google.generativeai as genai

# هنا الكود بيسحب المفتاح اللي هتحطه في إعدادات السيرفر في المحطة الرابعة
genai.configure(api_key=st.secrets["GEMINI_API_KEY"])

# شخصيتك الأكاديمية
mostafa_persona = """
أنت مصطفى، طالب في السنة النهائية بكلية الزراعة قسم الألبان. شخصيتك (INTJ).
شرحك يعتمد على نظرية التنقيط: سرد الحقائق ثم ربطها.
ردودك عملية ومباشرة. استخدم أمثلة من مشروعك (استبدال SNF اللبن الفرز بـ SNF الشرش الحلو السائل في المخاليط).
"""

model = genai.GenerativeModel('gemini-1.5-flash', system_instruction=mostafa_persona)

# واجهة الموقع
st.title("SheroBot 🍦 - Academic Assistant")

# حفظ المحادثة
if "chat" not in st.session_state:
    st.session_state.chat = model.start_chat(history=[])

for message in st.session_state.chat.history:
    role = "assistant" if message.role == "model" else "user"
    with st.chat_message(role):
        st.markdown(message.parts[0].text)

# استقبال الأسئلة والرد عليها
if prompt := st.chat_input("اكتب سؤالك هنا..."):
    with st.chat_message("user"):
        st.markdown(prompt)
    response = st.session_state.chat.send_message(prompt)
    with st.chat_message("assistant"):
        st.markdown(response.text)