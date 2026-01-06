# TRADING PLATFORM

A Python-based trading analysis and dashboard application built with
[pandas][pandas], [Streamlit][streamlit], [yfinance][yfinance], the
[Z.AI Python SDK][zai-sdk], and [Plotly][plotly].

---

## Requirements
- Python 3.8 — 3.12 (recommended)
- Git
- `pip` or `pip3`

---

## Python Dependencies

This project depends on the following libraries. Click each name to access its official documentation:

- [pandas][pandas] — data manipulation and analysis  
- [yfinance][yfinance] — Yahoo Finance market data  
- [Streamlit][streamlit] — interactive web dashboards  
- [Z.AI Python SDK][zai-sdk] — AI-powered features  
- [Plotly][plotly] — interactive charts (`plotly.graph_objects`)

---

## Installation

### 1. Clone the repository
```bash
git clone https://github.com/lambert-lincoln/TradingAlgo.git
cd TradingAlgo
````

### 2. Create a virtual environment

```bash
python -m venv venv
```

### 3. Activate the virtual environment

**macOS / Linux**

```bash
source venv/bin/activate
```

**Windows (PowerShell)**

```powershell
.\venv\Scripts\Activate.ps1
```

---

### 4. Install dependencies

```bash
pip install --upgrade pip
pip install pandas yfinance streamlit zai-sdk plotly
```

(Optional) Freeze dependencies:

```bash
pip freeze > requirements.txt
```

---

## Example `requirements.txt`

```txt
pandas
yfinance
streamlit
zai-sdk
plotly
```

---

## Running the App

If your main entry point is `app.py`:

```bash
streamlit run app.py
```

---

## Example Imports

```python
import pandas as pd
import yfinance as yf
import streamlit as st
import plotly.graph_objects as go
from zai import ZaiClient
```

---

## API Keys & Environment Variables

If the project uses API keys:

1. Create a `.env` file in the project root (do **not** commit it)
2. Add your keys:

```env
ZAI_API_KEY=your_key_here
```

3. Load them in Python:

```python
import os
from dotenv import load_dotenv

load_dotenv()
ZAI_KEY = os.getenv("ZAI_API_KEY")
```

Make sure `.env` and any secret files are listed in `.gitignore`.

---

## Documentation Links

* pandas docs: [https://pandas.pydata.org/docs/](https://pandas.pydata.org/docs/)
* Streamlit docs: [https://docs.streamlit.io](https://docs.streamlit.io)
* yfinance docs: [https://pypi.org/project/yfinance/](https://pypi.org/project/yfinance/)
* Plotly Python docs: [https://plotly.com/python/](https://plotly.com/python/)
* Z.AI SDK docs: [https://pypi.org/project/zai-sdk/](https://pypi.org/project/zai-sdk/)

---

## Reference Links

[pandas]: https://pandas.pydata.org/docs/
[yfinance]: https://pypi.org/project/yfinance/
[streamlit]: https://docs.streamlit.io
[plotly]: https://plotly.com/python/
[zai-sdk]: https://pypi.org/project/zai-sdk/

```
