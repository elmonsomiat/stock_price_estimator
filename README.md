# Stock Price Estimator

Python tools for generating quick valuation ranges and narrative PDF reports for one or more publicly traded companies. The project combines Yahoo Finance market data, Financial Modeling Prep fundamentals, and a local LLM (via `langchain_ollama`) to draft income statement, balance sheet, and cash flow summaries before exporting them to PDF.

## Project Layout
- `src/run_stock_estimator.py` – batch entry point that fetches market data, calls the LLM, and writes a PDF.
- `src/finance_utils.py` – helpers for resolving tickers and downloading Financial Modeling Prep statements.
- `src/agent_utils.py` – loads the Ollama-hosted `gemma3:12b` chat model.
- `src/utils.py` – utilities for rendering markdown-like content into a PDF.
- `frontend/app.py` – optional Streamlit UI for interactive PDF generation.

## Prerequisites
- Python 3.10+ (tested locally with 3.11).
- [Ollama](https://ollama.com) with the `gemma3:12b` model pulled and running.
- Financial Modeling Prep API key with access to `/api/v3` endpoints (`income-statement`, `balance-sheet-statement`, `cash-flow-statement`).
- Optional: Streamlit for the UI (already listed in `requirements.txt`).

## Setup
1. Create and activate a virtual environment:
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   ```
2. Install Python dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Export your Financial Modeling Prep key so both the CLI and UI can read it:
   ```bash
   export FINANCIALS_API_KEY=your_key_here
   ```

## Usage
### Command Line Batch Script
1. Edit `stock_list` and the output path in `src/run_stock_estimator.py` if needed (defaults to `['Novo Nordisk', 'Tesla', 'Cloudflare']` and `/home/ana/Desktop/stock_output.pdf`).
2. Run the script:
   ```bash
   python -m src.run_stock_estimator
   ```
3. The script prints intermediate progress (ticker symbol resolution and table summaries) and saves a multi-page PDF with one generated analysis per company.

### Streamlit Frontend
1. Start the UI:
   ```bash
   streamlit run frontend/app.py
   ```
2. Enter one or more company names separated by commas, click **Generate PDF Report**, and download the generated file once it appears.

## Notes & Tips
- Yahoo Finance sometimes throttles unauthenticated calls; rerun the script if responses are incomplete.
- Each LLM call summarizes only the most recent four filings for brevity. Adjust the `.head(4)` slices in `finance_utils.get_long_financials` to change the lookback window.
- The PDF renderer currently expects markdown-friendly text from the LLM; avoid asking the model for tables/charts unless you extend `create_pdf_from_dict` accordingly.
