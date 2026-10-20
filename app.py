import os
import io
import json
from datetime import datetime

import streamlit as st
from openai import OpenAI
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet

st.set_page_config(page_title="Urdu AI Luna", page_icon="🌙", layout="wide")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Noto+Nastaliq+Urdu&family=Noto+Sans:wght@400;600;700&display=swap');
html, body, [class*="css"] { font-family: 'Noto Sans', sans-serif; }
.urdu { direction: rtl; text-align: right; font-family: 'Noto Nastaliq Urdu', serif; line-height: 2.1; }
.hero { padding: 1.2rem 1.5rem; border-radius: 18px; color: white; background: linear-gradient(120deg,#101b45,#4c2a85,#176b87); }
.hero h1 { color:white; margin:0; }
.small-note { color: #64748b; font-size: .9rem; }
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div class="hero">
<h1>🌙 اردو AI Luna</h1>
<p class="urdu">آپ کا ذاتی ذہین معاون — سوالات، تعلیم، تحریر، پروگرامنگ، تحقیق اور روزمرہ کاموں کے لیے</p>
</div>
""", unsafe_allow_html=True)

DEFAULT_MODEL = "gpt-6-luna"

def get_secrets():
    try:
        key = st.secrets.get("OPENAI_API_KEY", "")
        model = st.secrets.get("OPENAI_MODEL", DEFAULT_MODEL)
    except Exception:
        key = os.getenv("OPENAI_API_KEY", "")
        model = os.getenv("OPENAI_MODEL", DEFAULT_MODEL)
    return key, model

api_key, configured_model = get_secrets()

SYSTEM_PROMPT = """
You are Urdu AI Luna, a helpful multilingual assistant for users in Pakistan.
Reply in the language the user uses. If the user writes in Urdu script, answer in natural Urdu script.
If the user writes Roman Urdu, answer in Roman Urdu unless asked otherwise. If English is used, answer in English.
Be respectful, clear, practical, and structured. Support education, writing, translation, coding, engineering,
summarization, brainstorming, and general questions. Do not pretend to have live web access unless a web tool is
actually enabled. Explain uncertainty and recommend qualified professional review for safety-critical matters.
"""

def demo_reply(prompt, mode):
    p = prompt.lower()
    if any(x in p for x in ["translate", "ترجمہ", "tarjuma"]):
        return "ڈیمو موڈ: براہِ کرم وہ متن بھیجیں جس کا ترجمہ درکار ہے، اور مطلوبہ زبان بھی بتائیں۔"
    if any(x in p for x in ["python", "پائتھن", "code", "کوڈ"]):
        return "ڈیمو موڈ: پروگرامنگ کے مسئلے کو چھوٹے مراحل میں تقسیم کریں۔ مطلوبہ نتیجہ، موجودہ کوڈ اور error message فراہم کریں تاکہ زیادہ درست رہنمائی دی جا سکے۔"
    if any(x in p for x in ["essay", "مضمون", "application", "درخواست", "letter", "خط"]):
        return "ڈیمو موڈ: میں تحریر کا خاکہ بنانے میں مدد کر سکتا ہوں۔ موضوع، مقصد، مخاطب، زبان اور مطلوبہ طوالت بتائیں۔ حقیقی AI تحریر کے لیے OpenAI API Mode فعال کریں۔"
    return ("السلام علیکم! میں اردو AI Luna کا Demo Mode ہوں۔ اس موڈ میں نمونہ جاتی رہنمائی دستیاب ہے، "
            "لیکن حقیقی، تفصیلی AI جوابات کے لیے OpenAI API Mode اور درست API key درکار ہے۔ "
            "آپ اپنا سوال اردو، رومن اردو یا انگریزی میں لکھ سکتے ہیں۔")

def get_ai_response(messages, mode, model):
    if mode == "Demo Mode":
        return demo_reply(messages[-1]["content"], mode)
    if not api_key:
        raise RuntimeError("API key نہیں ملی۔ Streamlit Secrets میں OPENAI_API_KEY شامل کریں۔")
    client = OpenAI(api_key=api_key)
    response = client.chat.completions.create(
        model=model,
        messages=[{"role": "system", "content": SYSTEM_PROMPT}] + messages,
    )
    return response.choices[0].message.content or "معذرت، کوئی متن واپس نہیں آیا۔"

if "chat_sessions" not in st.session_state:
    st.session_state.chat_sessions = {"نئی گفتگو": []}
if "active_chat" not in st.session_state:
    st.session_state.active_chat = "نئی گفتگو"

with st.sidebar:
    st.title("🌙 Luna Menu")
    mode = st.radio("AI موڈ", ["Demo Mode", "OpenAI API Mode"], index=0)
    model = st.text_input("API model ID", value=configured_model, help="یہ model ID آپ کے API اکاؤنٹ میں دستیاب ہونا ضروری ہے۔")
    st.caption("Default model ID: gpt-6-luna")
    if mode == "OpenAI API Mode":
        if api_key:
            st.success("API key ملی ہے۔")
        else:
            st.warning("API key سیٹ نہیں ہے۔")
    st.divider()
    chat_names = list(st.session_state.chat_sessions.keys())
    active = st.selectbox("گفتگو منتخب کریں", chat_names, index=chat_names.index(st.session_state.active_chat) if st.session_state.active_chat in chat_names else 0)
    st.session_state.active_chat = active
    new_name = st.text_input("نئی گفتگو کا نام")
    if st.button("＋ نئی گفتگو"):
        name = new_name.strip() or f"گفتگو {len(st.session_state.chat_sessions)+1}"
        if name in st.session_state.chat_sessions:
            name += f" {datetime.now().strftime('%H%M%S')}"
        st.session_state.chat_sessions[name] = []
        st.session_state.active_chat = name
        st.rerun()
    st.divider()
    st.markdown("**خصوصیات**")
    st.markdown("- اردو اور رومن اردو چیٹ\n- تحریر اور ترجمہ\n- تعلیم اور پروگرامنگ\n- چیٹ ایکسپورٹ\n- PDF گفتگو رپورٹ")
    st.caption("API استعمال کرنے پر OpenAI کی API billing لاگو ہو سکتی ہے۔")

st.subheader("آپ کس کام میں مدد چاہتے ہیں؟")
quick = st.columns(4)
quick_prompts = [
    ("✍️ تحریر", "میرے لیے ایک رسمی اردو درخواست لکھیں۔"),
    ("🌐 ترجمہ", "اس متن کا اردو میں ترجمہ کریں: "),
    ("💻 پروگرامنگ", "مجھے Python پروگرامنگ میں مدد دیں: "),
    ("📚 تعلیم", "یہ موضوع آسان اردو میں سمجھائیں: "),
]
for col, (label, prompt) in zip(quick, quick_prompts):
    if col.button(label, use_container_width=True):
        st.session_state.pending_prompt = prompt

messages = st.session_state.chat_sessions[st.session_state.active_chat]
for msg in messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

pending = st.session_state.pop("pending_prompt", "")
user_input = st.chat_input("اپنا سوال اردو، رومن اردو یا انگریزی میں لکھیں…")
if pending and not user_input:
    user_input = pending

if user_input:
    messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)
    with st.chat_message("assistant"):
        with st.spinner("Luna سوچ رہی ہے…"):
            try:
                answer = get_ai_response(messages, mode, model.strip() or DEFAULT_MODEL)
            except Exception as exc:
                answer = f"**مسئلہ:** {exc}\n\nاپنی API key، model ID، انٹرنیٹ کنکشن اور API access چیک کریں۔"
            st.markdown(answer)
    messages.append({"role": "assistant", "content": answer})

st.divider()
left, right = st.columns(2)
with left:
    export_text = "\n\n".join(
        [("آپ: " if m["role"] == "user" else "Luna: ") + m["content"] for m in messages]
    )
    st.download_button("⬇️ گفتگو TXT میں ڈاؤن لوڈ کریں", data=export_text or "ابھی کوئی گفتگو نہیں۔",
                       file_name="urdu_ai_luna_chat.txt", mime="text/plain", use_container_width=True)
with right:
    if st.button("📄 PDF رپورٹ تیار کریں", use_container_width=True):
        buf = io.BytesIO()
        doc = SimpleDocTemplate(buf, pagesize=A4, rightMargin=40, leftMargin=40, topMargin=40, bottomMargin=40)
        styles = getSampleStyleSheet()
        story = [Paragraph("Urdu AI Luna — Chat Report", styles["Title"]),
                 Spacer(1, 12),
                 Paragraph(f"Conversation: {st.session_state.active_chat}", styles["Heading2"]),
                 Paragraph(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}", styles["Normal"]),
                 Spacer(1, 12)]
        for m in messages:
            label = "User" if m["role"] == "user" else "Luna"
            safe_text = (m["content"].replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
                         .replace("\n", "<br/>"))
            story.append(Paragraph(f"<b>{label}:</b> {safe_text}", styles["BodyText"]))
            story.append(Spacer(1, 8))
        doc.build(story)
        st.session_state.pdf_bytes = buf.getvalue()
    if st.session_state.get("pdf_bytes"):
        st.download_button("⬇️ PDF ڈاؤن لوڈ کریں", data=st.session_state.pdf_bytes,
                           file_name="urdu_ai_luna_report.pdf", mime="application/pdf", use_container_width=True)

st.caption("اہم: یہ ابتدائی قابلِ توسیع ورژن ہے۔ AI کے جوابات کی تصدیق کریں۔ Demo Mode حقیقی GPT ماڈل استعمال نہیں کرتا۔")
