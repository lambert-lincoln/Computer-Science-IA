# TRADINGALGO — README

> Short repo guide: dependencies, installation, and quick start.

---

## Requirements

* Python 3.8 — 3.12 (recommended)
* Git
* `pip` (or `pip3`)

---

## Python dependencies

This project uses the following Python packages:

* `pandas`
* `yfinance`
* `streamlit`
* `zai-sdk` (Z.AI Python SDK)
* `plotly` (use `plotly.graph_objects` in code)

---

## Quick install (Unix / macOS)

```bash
# 1. clone repo (if not already)
git clone https://github.com/lambert-lincoln/TradingAlgo.git
cd TradingAlgo

# 2. create a virtual environment
python -m venv venv

# 3. activate the venv
# macOS / Linux:
source venv/bin/activate
# Windows (PowerShell):
# .\venv\Scripts\Activate.ps1
# Windows (cmd):
# .\venv\Scripts\activate.bat

# 4. install dependencies
pip install --upgrade pip
pip install pandas yfinance streamlit zai-sdk plotly

# (optional) freeze installed packages to requirements.txt
pip freeze > requirements.txt
```

### Quick install (Windows cmd)

```cmd
python -m venv venv
venv\Scripts\activate
pip install --upgrade pip
pip install pandas yfinance streamlit zai-sdk plotly
pip freeze > requirements.txt
```

---

## Example `requirements.txt`

You can paste this into `requirements.txt` (or generate using `pip freeze`):

```
pandas
yfinance
streamlit
zai-sdk
plotly
```

---

## Environment variables / API keys

If your project uses API keys (Alpha Vantage, OpenAI, Z.ai, broker keys, etc.):

1. Create a `.env` file in the repo root (DO NOT commit this file).
2. Add keys there:

```
ZAI_API_KEY=your_zai_key_here
ALPHA_VANTAGE_KEY=your_alpha_vantage_key
OTHER_KEY=...
```

3. Load keys in Python (example with `python-dotenv`—install if needed):

```python
from dotenv import load_dotenv
import os

load_dotenv()
ZAI_KEY = os.getenv("ZAI_API_KEY")
```

> Important: Add `.env`, `APIkey.py` (or any file that contains secrets) to `.gitignore`. If secrets were already committed, rotate the keys immediately.

---

## Running the app / common commands

* Run Streamlit app (if your entrypoint is `app.py`):

```bash
streamlit run app.py
```

* Run a regular Python script:

```bash
python data_fetcher.py
```

* Run tests (if present):

```bash
# example: pytest
pytest
```

---

## Import examples

```python
import pandas as pd
import yfinance as yf
import streamlit as st
import plotly.graph_objects as go
from zai import ZaiClient  # if using zai-sdk
```

Simple `yfinance` fetch example:

```python
import yfinance as yf
df = yf.download("AAPL", period="1mo", interval="1d")
print(df.head())
```

Simple `plotly` example:

```python
import plotly.graph_objects as go

fig = go.Figure(go.Scatter(x=[1,2,3], y=[1,3,2]))
fig.show()
```

Z.AI SDK quick check:

```python
import zai
print(zai.__version__)
# or
from zai import ZaiClient
client = ZaiClient(api_key="YOUR_KEY_HERE")
```

---

## Security & best practices

* Never commit `venv/`, `.env`, `APIkey.py`, or other secret files. Add those to your `.gitignore`.
* If you accidentally pushed secrets, **rotate the keys immediately**.
* Use `requirements.txt` to lock dependencies, or use `poetry`/`pip-tools` for reproducible installs.
* Prefer environment variables or secret management for deployments (GitHub Actions secrets, CI/CD vaults).

---

## Troubleshooting

* If a package fails to install, make sure your Python version is supported and `pip` is up-to-date:

```bash
python -m pip install --upgrade pip
```

* If `zai-sdk` name changes in future, check the [official Z.AI docs] (Z.AI-Python-SDK-Docs) or project README (install command currently: `pip install zai-sdk`).

(Z.AI-Python-SDK-Docs) = https://docs.z.ai/guides/develop/python/introduction