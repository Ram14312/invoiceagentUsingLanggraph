# Invoice Agent (LangGraph + Streamlit)

Invoice image -> EasyOCR -> LangGraph agent (clean -> extract -> validate -> format) -> SQLite -> Streamlit UI.
Details: `ARCHITECTURE.md` (read only when needed), `README.md`.

## Layout
- `app.py` — Streamlit UI (tabs: upload, history, stats); `run.py` — launcher
- `agents/invoice_agent.py` — `InvoiceProcessingAgent`, LangGraph nodes
- `utils/ocr.py` — `OCRReader` (easyocr); `utils/database.py` — `InvoiceDB` (sqlite, `invoice.db`)
- `invoices/` — sample PNGs; `*.ipynb` — experiments (don't edit by hand, outputs are large)

## Commands
- Install: `pip install -r requirements.txt`
- Run: `streamlit run app.py` (or `python run.py`)
- Syntax check: `/check`
- No tests, linter, formatter, CI or Docker exist. Don't add any unless asked.

## Conventions
- Python, type hints + docstrings on public methods; match existing style.
- Config via env / `.env` (gitignored). Never read, print or commit `.env` or `*.db`.
- Agent state is the `InvoiceState` TypedDict; add new steps as nodes in `_build_graph`.

## Config
- Env: `OPENAI_API_KEY` (required), `OPENAI_BASE_URL` (optional, for OpenAI-compatible gateways), set in `.env`.
