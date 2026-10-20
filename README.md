# Urdu AI Luna 🌙

A Streamlit-based Urdu-first AI assistant starter app. Supports Urdu script, Roman Urdu, and English prompts; chat sessions; quick prompt starters; TXT export; and PDF conversation reports.

## Features
- Urdu-first responsive Streamlit UI
- Demo Mode (no API key needed; sample responses only)
- OpenAI API Mode
- Configurable API model ID (default `gpt-6-luna`)
- Multiple conversation sessions during the current app session
- Quick prompts for writing, translation, programming, and education
- TXT and PDF exports

## Important model note
The app defaults to `gpt-6-luna` because that is the requested model ID. Availability depends on your OpenAI API project. If your project does not have access, set `OPENAI_MODEL` to a model ID available to your account. ChatGPT subscription access and API billing are separate.

## Run on Windows
```powershell
cd urdu_ai_luna
py -m venv .venv
.venv\Scripts\activate
python -m pip install --upgrade pip
pip install -r requirements.txt
streamlit run app.py
```

## Run on macOS/Linux
```bash
cd urdu_ai_luna
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
pip install -r requirements.txt
streamlit run app.py
```

Open the local URL shown in the terminal, usually `http://localhost:8501`.

## Configure the API key
Create `.streamlit/secrets.toml`:
```toml
OPENAI_API_KEY = "your-api-key-here"
OPENAI_MODEL = "gpt-6-luna"
```
Do not upload `secrets.toml` to GitHub. Never place API keys directly in source code.

Alternatively set environment variables. On Windows PowerShell:
```powershell
$env:OPENAI_API_KEY="your-api-key-here"
$env:OPENAI_MODEL="gpt-6-luna"
streamlit run app.py
```

## Deploy to Streamlit Community Cloud
1. Create a GitHub repository.
2. Upload `app.py`, `requirements.txt`, `README.md`, and `.gitignore`.
3. Create a new app in Streamlit Community Cloud and select `app.py`.
4. In app settings, open Secrets and add:
   ```toml
   OPENAI_API_KEY = "your-api-key-here"
   OPENAI_MODEL = "gpt-6-luna"
   ```
5. Deploy and test in `OpenAI API Mode`.
6. If the model is unavailable to your API project, use a model ID listed as available in your OpenAI API account.

## Limitations in this starter version
- Demo Mode returns predefined sample guidance and is not a local language model.
- No built-in web search, document upload analysis, image generation, or speech conversation yet.
- Chat sessions are stored in Streamlit session state and may not persist after a restart or a new session.
- PDF report uses ReportLab's default fonts; complex Urdu shaping may not render perfectly in the PDF. TXT export is better for preserving Urdu text.
- Do not use generated output as a substitute for professional medical, legal, financial, or safety-critical advice.

## Project files
- `app.py` — Streamlit application
- `requirements.txt` — Python dependencies
- `README.md` — setup and deployment guide
- `.gitignore` — excludes secrets and local environment
