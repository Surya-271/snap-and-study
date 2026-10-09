# 📚 Snap & Study

> **Snap it. Understand it. Study smarter.**

Snap & Study is an AI-powered multimodal study tutor designed to help students learn complex academic material with ease. By combining Google Gemini's advanced vision and conversational reasoning with Streamlit's intuitive web interface, students can photograph problems, diagrams, notes, or textbook pages, receive step-by-step explanations in plain language, ask interactive follow-up questions, and send clean revision summaries directly to Telegram.

---

## 🌟 Features

- **Multimodal Study Assistant**: Upload images of math/physics problems, code, chemical reactions, diagrams, handwritten notes, or textbook pages (`.jpg`, `.jpeg`, `.png`).
- **Step-by-Step Breakdown**: Clear, conversational explanations that focus on core concepts, definitions, and reasoning rather than just providing bare answers.
- **Interactive Follow-up Chat**: Continuous multi-turn conversation preserving full context, allowing students to ask clarifying questions.
- **Smart Image Fallback**: Automatically provides tailored educational analysis if an image is uploaded without typed instructions.
- **One-Click Revision Summaries**: Generates a clean study guide summarizing key takeaways, formulas, and conclusions from the session.
- **Telegram Integration**: Directly dispatches generated revision summaries to the student's personal Telegram chat for quick on-the-go revision.
- **Streamlined Onboarding**: Simple two-step onboarding requiring only the student's name and Telegram Chat ID.

---

## 🛠️ Tech Stack

- **Frontend & Web Framework**: [Streamlit](https://streamlit.io/)
- **AI & Vision Model**: [Google GenAI SDK](https://github.com/googleapis/python-genai) (`gemini-3.5-flash`)
- **Messaging Integration**: [python-telegram-bot](https://python-telegram-bot.org/) (`telegram.Bot` with `asyncio`)
- **Runtime**: Python 3.10+

---

## 📁 Project Structure

```text
snap/
├── .streamlit/
│   └── secrets.toml         # Local secrets (API keys & bot token)
├── .gitignore               # Ignored files (secrets, virtualenv, caches)
├── app.py                   # Main Streamlit application and Telegram delivery logic
├── prompts.py               # System prompts, welcome templates, and summary prompts
├── requirements.txt         # Project dependencies
└── README.md                # Project documentation
```

---

## ⚙️ Prerequisites & Setup

### 1. Clone or Open the Repository
```bash
git clone <repository-url>
cd snap
```

### 2. Create and Activate a Virtual Environment
```bash
# Windows
python -m venv venv
.\venv\Scripts\activate

# macOS / Linux
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

---

## 🔑 Configuration & Secrets

Snap & Study requires two secrets: a **Google Gemini API Key** and a **Telegram Bot Token**.

### 1. Obtain a Gemini API Key
- Go to [Google AI Studio](https://aistudio.google.com/).
- Generate an API key.

### 2. Create a Telegram Bot & Get Chat ID
1. Open Telegram and search for [@BotFather](https://t.me/BotFather).
2. Send `/newbot` and follow the prompts to create your bot.
3. Copy the HTTP API token provided by BotFather.
4. Open your newly created bot in Telegram and click **Start** (or send any message). This step is mandatory so Telegram permits outgoing messages from the bot to your account.
5. Retrieve your Telegram Chat ID (you can use [@userinfobot](https://t.me/userinfobot) or [@myidbot](https://t.me/myidbot) on Telegram).

### 3. Configure Secrets Locally
Create or edit `.streamlit/secrets.toml` in the project root:

```toml
GEMINI_API_KEY = "your-gemini-api-key-here"
TELEGRAM_BOT_TOKEN = "your-telegram-bot-token-here"
```

---

## 🚀 Running the App Locally

Ensure your virtual environment is active and run:

```bash
streamlit run app.py
```

Streamlit will launch the web application in your default browser at `http://localhost:8501`.

### Using the App:
1. Enter your name and numeric Telegram Chat ID on the onboarding screen.
2. Type a study question or upload an image of a problem, diagram, or page of notes.
3. Review Gemini's step-by-step explanation and ask follow-up questions as needed.
4. Once you have finished studying, click **📤 Send to Telegram** to receive a structured revision summary on your phone.

---

## ☁️ Streamlit Community Cloud Deployment

To deploy Snap & Study on [Streamlit Community Cloud](https://share.streamlit.io/):

1. **Push your code to GitHub**:
   Ensure `.streamlit/secrets.toml` is ignored and never committed (verified by `.gitignore`).
2. **Deploy on Streamlit Cloud**:
   - Link your GitHub repository.
   - Set the main file path to `app.py`.
3. **Set Secrets in the Cloud Dashboard**:
   - In your app settings on Streamlit Cloud, navigate to **Secrets**.
   - Paste your configuration:
     ```toml
     GEMINI_API_KEY = "your-actual-gemini-key"
     TELEGRAM_BOT_TOKEN = "your-actual-telegram-bot-token"
     ```
4. **Deploy**: Click **Deploy** and test the live application.

---

## 🔒 Security Note

- **Never commit `.streamlit/secrets.toml`**: API keys and bot tokens must remain confidential.
- The repository includes a `.gitignore` specifically ignoring `.streamlit/secrets.toml`, virtual environments (`venv/`), and Python cache files (`__pycache__/`, `*.pyc`).
- If an API key or bot token is ever exposed publicly, revoke and rotate it immediately.

---

## 👨‍💻 Author

**Konda Suryaprakash Goud**
