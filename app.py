import asyncio

import streamlit as st
from google import genai
from google.genai import types
from telegram import Bot

from prompts import SUMMARY_REQUEST_PROMPT, SYSTEM_PROMPT, WELCOME_MESSAGE_TEMPLATE

MODEL_NAME = "gemini-3.5-flash"
st.set_page_config(page_title="Snap & Study", page_icon="📚")

GEMINI_API_KEY = st.secrets["GEMINI_API_KEY"]
TELEGRAM_BOT_TOKEN = st.secrets["TELEGRAM_BOT_TOKEN"]


@st.cache_resource
def get_gemini_client():
    return genai.Client(api_key=GEMINI_API_KEY)


gemini_client = get_gemini_client()


def render_message(message):
    with st.chat_message(message["role"]):
        if message["kind"] == "text":
            st.write(message["content"])
        elif message["kind"] == "image":
            st.image(message["content"])


def add_message(role, kind, content):
    st.session_state.messages.append(
        {
            "role": role,
            "kind": kind,
            "content": content,
        }
    )
    render_message(st.session_state.messages[-1])


def ask_gemini(parts):
    try:
        return st.session_state.chat.send_message(parts).text
    except Exception as error:
        return f"Sorry, something went wrong: {error}"


def send_telegram(chat_id, text):
    if not text:
        return False, "No study summary available to send."

    try:
        bot = Bot(token=TELEGRAM_BOT_TOKEN)

        async def _send():
            # Telegram supports messages up to 4096 characters; split into chunks if needed
            chunk_size = 4000
            if len(text) <= chunk_size:
                await bot.send_message(chat_id=chat_id, text=text)
            else:
                for i in range(0, len(text), chunk_size):
                    await bot.send_message(
                        chat_id=chat_id, text=text[i : i + chunk_size]
                    )

        try:
            asyncio.run(_send())
        except RuntimeError:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            loop.run_until_complete(_send())
            loop.close()

        return True, "Summary sent successfully!"
    except Exception as error:
        return False, str(error)


# Step 1: onboarding
if "onboarded" not in st.session_state:
    st.title("📚 Snap & Study")
    st.caption("Snap it. Understand it. Study smarter.")

    with st.form("onboarding_form"):
        name = st.text_input("Your name")
        telegram_chat_id = st.text_input(
            "Telegram Chat ID",
            placeholder="e.g. 123456789",
            help="Your numeric Telegram chat ID. Open our Telegram bot and send /start first so it can message you.",
        )

        st.info(
            "👉 **Important:** Open the Snap & Study Telegram bot and send it a message (or tap Start) first. "
            "Telegram bots cannot message you until you start the conversation!"
        )

        submitted = st.form_submit_button("Let's go 🚀")

    if submitted:
        if not name.strip() or not telegram_chat_id.strip():
            st.warning("Please fill in both your name and Telegram chat ID.")
        else:
            st.session_state.name = name.strip()
            st.session_state.telegram_chat_id = telegram_chat_id.strip()

            st.session_state.chat = gemini_client.chats.create(
                model=MODEL_NAME,
                config=types.GenerateContentConfig(
                    system_instruction=SYSTEM_PROMPT
                ),
            )

            st.session_state.messages = []
            st.session_state.onboarded = True
            st.rerun()

    st.stop()


# Step 2: chat interface
header_col, button_col = st.columns([5, 2], vertical_alignment="center")

with header_col:
    st.title("📚 Snap & Study")

with button_col:
    send_disabled = len(st.session_state.messages) <= 2

    if st.button(
        "📤 Send to Telegram",
        disabled=send_disabled,
        use_container_width=True,
    ):
        with st.spinner("Creating study summary..."):
            summary = ask_gemini([SUMMARY_REQUEST_PROMPT])

        success, info = send_telegram(
            st.session_state.telegram_chat_id,
            summary,
        )

        if success:
            st.success("Sent! Check your Telegram 📲")
        else:
            st.error(f"Couldn't send that: {info}")


st.caption(
    f"Logged in as {st.session_state.name} - "
    f"study summaries go to Telegram chat {st.session_state.telegram_chat_id}"
)


if not st.session_state.messages:
    add_message(
        "assistant",
        "text",
        WELCOME_MESSAGE_TEMPLATE.format(name=st.session_state.name),
    )
else:
    for message in st.session_state.messages:
        render_message(message)


user_input = st.chat_input(
    "Ask a question, or upload a problem, diagram, or page of notes...",
    accept_file=True,
    file_type=["jpg", "jpeg", "png"],
)

if user_input:
    photo = user_input.files[0] if user_input.files else None
    text = user_input.text
    parts = []

    if photo is not None:
        photo_bytes = photo.getvalue()

        add_message("user", "image", photo_bytes)

        parts.append(
            types.Part.from_bytes(
                data=photo_bytes,
                mime_type=photo.type,
            )
        )

    if text:
        add_message("user", "text", text)
        parts.append(text)

    elif photo is not None:
        parts.append(
            "Analyze this study material and explain what it contains in simple "
            "language. If it is a problem, solve it step-by-step. If it is a "
            "diagram, explain its components and relationships. If it is notes, "
            "explain and summarize the important concepts."
        )

    with st.spinner("Analyzing study material..."):
        answer = ask_gemini(parts)

    add_message("assistant", "text", answer)
