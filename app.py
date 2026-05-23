import streamlit as st
import streamlit.components.v1 as components
import google.generativeai as genai

# 1. إعدادات الصفحة
st.set_page_config(page_title="Shero Whey | آيس كريم صحي", page_icon="🍦", layout="wide")

# 2. إعدادات البوت وسحب المفتاح بأمان
genai.configure(api_key=st.secrets["GEMINI_API_KEY"])

# شخصية خدمة العملاء لـ Shero Whey
customer_service_persona = """
أنت مساعد خدمة عملاء ذكي لمنتج "Shero Whey".
المنتج عبارة عن آيس كريم صحي طبيعي 100% مصنوع من شرش اللبن الطبيعي (Whey).
فوائد المنتج: غني بالكالسيوم، البوتاسيوم، الفيتامينات، وصديق للبيئة (Zero Waste).
الأنواع المتاحة: "مانجو والكركومين" و "فراولة ورمان".
أسلوبك: ودود، احترافي، مباشر، وتتحدث باللهجة المصرية.
ردودك يجب أن تكون قصيرة جداً ومقنعة، ووجّه العميل دائماً للذهاب لتبويب "تصفح المنتجات" لإتمام الطلب.
"""
model = genai.GenerativeModel('gemini-2.5-flash', system_instruction=customer_service_persona)

# 3. تقسيم الواجهة لتبويبات (Tabs)
tab1, tab2 = st.tabs(["🛒 تصفح المنتجات والطلب", "💬 المساعد الذكي للاستفسارات"])

# التبويب الأول: الويب سايت بتاعك
with tab1:
    # حط كود الـ HTML بتاعك بالكامل هنا بين علامات التنصيص الثلاثية
    html_code = """
    """
    
    # الكود ده بيعرض الويب سايت بتاعك جوه Streamlit بكامل الشاشة
    components.html(html_code, height=850, scrolling=True)

# التبويب الثاني: البوت (البانل الخاص بالاستفسارات)
with tab2:
    st.markdown("### 🍦 SheroBot - أقدر أساعدك إزاي؟")
    st.info("اسألني عن مكونات الآيس كريم، فوايده، أو إزاي تطلب.")
    
    # زرار مسح المحادثة
    if st.button("🔄 محادثة جديدة", key="reset_btn"):
        st.session_state.chat = model.start_chat(history=[])
        st.rerun()

    # الذاكرة
    if "chat" not in st.session_state:
        st.session_state.chat = model.start_chat(history=[])

    # عرض الرسايل
    for message in st.session_state.chat.history:
        role = "assistant" if message.role == "model" else "user"
        with st.chat_message(role):
            st.markdown(message.parts[0].text)

    # استقبال الأسئلة
    if prompt := st.chat_input("اكتب استفسارك هنا..."):
        with st.chat_message("user"):
            st.markdown(prompt)
        
        try:
            response = st.session_state.chat.send_message(prompt)
            with st.chat_message("assistant"):
                st.markdown(response.text)
        except Exception as e:
            st.error(f"حصلت مشكلة في الاتصال: {e}")
