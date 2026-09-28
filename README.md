# EduGenie — Google Gemini Powered Learning Assistant

A modular educational assistant based on the supplied project document. Built with FastAPI, Jinja2, HTML/CSS/JavaScript, and Google's Gemini API.

## Features

- **Q&A** — concise educational answers
- **Explain** — beginner-friendly concept explanations with examples
- **Quiz** — exactly three MCQs, each with four options, correct answer, and explanation
- **Summarize** — key ideas and takeaways from a passage
- **Learning path** — staged learning roadmap with time estimates and projects

The default explainer uses Gemini to keep setup light. An optional local LaMini-Flan-T5-783M explainer is available, but it requires downloading model weights and additional dependencies.

## Requirements

- Python 3.10 or newer
- VS Code and its Python extension
- A Google Gemini API key from Google AI Studio
- Internet connection for Gemini API calls

## VS Code setup (Windows PowerShell)

1. Extract the project ZIP and open the `EduGenie` folder in VS Code (`File > Open Folder`).
2. Open **Terminal > New Terminal**.
3. Create a virtual environment:

   ```powershell
   py -m venv .venv
   .\.venv\Scripts\Activate.ps1
   ```

   If PowerShell blocks activation, run this for the current terminal only, then activate again:

   ```powershell
   Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
   .\.venv\Scripts\Activate.ps1
   ```

4. Install dependencies:

   ```powershell
   python -m pip install --upgrade pip
   pip install -r requirements.txt
   ```

5. Create your environment file:

   ```powershell
   Copy-Item .env.example .env
   ```

   Open `.env`, replace `your_gemini_api_key_here` with your API key. Keep `.env private; do not upload it to GitHub.

6. Start the app from the project root:

   ```powershell
   uvicorn main:app --reload
   ```

7. Open **http://127.0.0.1:8000** in your browser.

## macOS / Linux setup

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
pip install -r requirements.txt
cp .env.example .env
# Edit .env and set GEMINI_API_KEY
uvicorn main:app --reload
```

## API endpoints

All POST endpoints accept JSON with `task`, `text`, and optional `level` fields. The dedicated endpoint paths are:

| Method | Path | Purpose |
|---|---|---|
| GET | `/` | Web UI |
| GET | `/health` | Health check |
| POST | `/qa` | Answer a question |
| POST | `/explain` | Explain a concept |
| POST | `/quiz` | Generate MCQs |
| POST | `/summarize` | Summarize a passage |
| POST | `/learn/recommendations` | Generate learning path |
| POST | `/api/task` | Frontend task dispatcher |

Interactive API documentation: http://127.0.0.1:8000/docs

Example request:

```json
{
  "task": "explain",
  "text": "Photosynthesis",
  "level": "Beginner"
}
```

## Testing

With the virtual environment active, from the project root:

```powershell
pytest -q
```

The tests verify the homepage, health endpoint, and request validation. They do not call Gemini, so they can run without a configured API key.

For an end-to-end AI check, start the server and submit each of the five tasks in the web UI. Also verify `/docs` and `/health`.

## Optional local LaMini explainer

This model may use several GB of disk space and RAM, and its first run downloads model files. To enable it:

```bash
pip install transformers torch
```

Then set `USE_LOCAL_EXPLAINER=true` in `.env` and restart the server. On CPU-only systems, generation may be slow. If loading the local model fails, the explanation module falls back to Gemini.

## Troubleshooting

- **API key missing:** Ensure `.env` is in the project root beside `main.py`, and the key is assigned to `GEMINI_API_KEY`.
- **Model unavailable / API error:** Check the model name in `GEMINI_MODEL`, API access, quota, and network connection. Model availability can vary by account and region.
- **`uvicorn` not found:** Activate `.venv` and run `python -m pip install -r requirements.txt`.
- **Port already in use:** Run `uvicorn main:app --reload --port 8001`, then open `http://127.0.0.1:8001`.
- **Quiz parsing error:** Retry with a shorter, clearly structured passage.

## Security and responsible use

Never expose your API key in frontend JavaScript, source control, screenshots, or public repositories. All AI requests are made server-side. AI output may be incorrect; verify important facts with trusted educational sources.
