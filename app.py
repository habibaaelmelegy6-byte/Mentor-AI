import streamlit as st
from groq import Groq

client = Groq(
    api_key=st.secrets["GROQ_API_KEY"]
)


# ==========================
# PAGE SETTINGS
# ==========================
st.set_page_config(
    page_title="Mentor AI",
    page_icon="🤖",
    layout="wide"
)

# ==========================
# SESSION
# ==========================
if "messages" not in st.session_state:
    st.session_state.messages = []

# ==========================
# SIDEBAR
# ==========================
with st.sidebar:

    st.title("🤖 Mentor AI")

    if st.button("🗑️ New Chat"):
        st.session_state.messages = []
        st.rerun()

    st.markdown("---")

    st.subheader("🚀 Quick Actions")

    if st.button("📚 Study"):
        st.session_state.messages.append(
            {"role":"user","content":"Help me study."}
        )

    if st.button("💻 Coding"):
        st.session_state.messages.append(
            {"role":"user","content":"Help me write Python code."}
        )

    if st.button("☁️ Cloud"):
        st.session_state.messages.append(
            {"role":"user","content":"Explain cloud computing simply."}
        )

    if st.button("🤖 AI"):
        st.session_state.messages.append(
            {"role":"user","content":"Teach me Artificial Intelligence."}
        )

    st.markdown("---")
    st.caption("Made with Habiba")

# ==========================
# MAIN PAGE
# ==========================

st.title("🤖 Mentor AI")

st.caption(
    "🎓 Your personal AI assistant for studying, programming, AI, cloud, productivity, daily planning, and everyday life."
)

st.info(
    "👋 Welcome! Upload a PDF or ask me anything."
)

# ==========================
# PDF
# ==========================

uploaded_file = st.file_uploader(
    "📄 Upload PDF",
    type=["pdf"]
)

pdf_text = ""

if uploaded_file is not None:

    pdf = fitz.open(
        stream=uploaded_file.read(),
        filetype="pdf"
    )

    for page in pdf:
        pdf_text += page.get_text()

    st.success("✅ PDF Uploaded Successfully!")

    with st.expander("Preview PDF"):
        st.write(pdf_text[:3000])

# ==========================
# SHOW CHAT
# ==========================

for message in st.session_state.messages:

    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# ==========================
# USER INPUT
# ==========================

prompt = st.chat_input("Ask Mentor AI...")

if prompt:

    st.session_state.messages.append(
        {
            "role":"user",
            "content":prompt
        }
    )

    with st.chat_message("user"):
        st.markdown(prompt)

    messages = [
    {
        "role": "system",
        "content": """
You are Mentor AI.

You are a warm, friendly, intelligent AI assistant who helps people with studying, programming, AI, cloud computing, career advice, productivity, daily life, and personal questions.

Your personality:
- Friendly, calm, supportive, and easy to talk to.
- Speak naturally like a real person, not like a robot.
- Be funny when appropriate, but don't overdo it.
- Be kind, patient, and respectful.
- Make people feel comfortable asking anything.

Language:
- Always reply in the same language as the user.
- If the user writes in Egyptian Arabic, reply in natural Egyptian Arabic.
- If the user writes in English, reply in English.
- If the user mixes Arabic and English, reply naturally using both.
- Match the user's tone and style.

Conversation style:
- Never repeat the user's message before answering.
- Answer directly.
- Keep the conversation flowing naturally.
- Ask follow-up questions when it helps.
- Show empathy when someone is stressed or confused.
- Celebrate the user's achievements and encourage them.
- Remember the context of the conversation.

Knowledge:
- Help with studying.
- Help with programming and debugging.
- Help with AI and Machine Learning.
- Help with Cloud Computing.
- Help with English.
- Help with writing.
- Help with productivity and planning.
- Help with career advice.
- Help with technology.
- Help with everyday life questions.

Daily life:
- You can discuss relationships, friendships, university life, work, motivation, habits, stress, and everyday decisions.
- Give balanced, practical advice without judging the user.
- If the topic is emotional, be supportive and understanding.
- For serious topics (medical, legal, financial, or safety), make it clear when professional help may be appropriate instead of pretending to know everything.

Coding:
- Explain code clearly.
- Give complete examples when appropriate.
- Explain errors simply.
- Encourage learning instead of only giving answers.

Your goal:
Help people learn, solve problems, make better decisions, and leave every conversation feeling more confident and supported.
"""
    }
]

    if pdf_text != "":

        messages.append(
            {
                "role":"system",
                "content":f"""
The user uploaded the following PDF.

Use it whenever the user asks about the document.

PDF:

{pdf_text[:12000]}
"""
            }
        )

    messages.extend(st.session_state.messages)
        # ==========================
    # PDF COMMANDS
    # ==========================

    user_prompt = prompt

    if pdf_text != "":

        lower_prompt = prompt.lower()

        if "summarize" in lower_prompt or "summary" in lower_prompt:

            user_prompt = f"""
Summarize the following PDF in simple bullet points.

PDF:

{pdf_text[:12000]}
"""

        elif "quiz" in lower_prompt:

            user_prompt = f"""
Create 10 multiple choice questions from this PDF.

PDF:

{pdf_text[:12000]}
"""

        elif "flashcard" in lower_prompt:

            user_prompt = f"""
Create flashcards from this PDF.

PDF:

{pdf_text[:12000]}
"""

    messages.append(
        {
            "role": "user",
            "content": user_prompt
        }
    )

    # ==========================
    # SEND TO GROQ
    # ==========================
api_messages = [
        {
            "role": "system",
            "content": "You are Mentor AI. A warm, friendly, intelligent AI assistant."
        }
    ]
     with st.spinner("🤖 Mentor AI is thinking..."):

        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=api_messages,
            temperature=0.5,
            max_tokens=1024,
        )

    reply = response.choices[0].message.content

    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": reply
        }
    )

    with st.chat_message("assistant"):
        st.markdown(reply)

# ==========================
# PDF SHORTCUT BUTTONS
# ==========================

if uploaded_file is not None:

    st.markdown("---")
    st.subheader("📄 PDF Tools")

    col1, col2 = st.columns(2)

    with col1:

        if st.button("📄 Summarize PDF"):

            summary = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[
                    {
                        "role": "user",
                        "content": f"""
Summarize this PDF in simple bullet points.

PDF:

{pdf_text[:12000]}
"""
                    }
                ],
                temperature=0.4,
                max_tokens=1024,
            )

            st.success(summary.choices[0].message.content)

    with col2:

        if st.button("🎓 Quiz Me"):

            quiz = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[
                    {
                        "role": "user",
                        "content": f"""
Create 10 MCQ questions from this PDF.

After every question give the correct answer.

PDF:

{pdf_text[:12000]}
"""
                    }
                ],
                temperature=0.5,
                max_tokens=1024,
            )

            st.success(quiz.choices[0].message.content)
