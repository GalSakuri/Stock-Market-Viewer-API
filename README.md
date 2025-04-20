# Stock-Market-Viewer

**Tkinter app that:**
- shows a chart of a stock’s daily closing price (past 6 months).
- lists the latest 5 news headlines about that company (click to open in your browser).
---
### API Rate Limits
- AlphaVantage
   - 5 requests/min , 500/day
- NewsAPI
  - 100requests/day


### Requirements
- Python 3.9+
- requests, pandas, matplotlib

---
**Setup**
### 1. Clone the repo


    git clone https://github.com/<your‑user>/stock‑news‑viewer.git
    cd stock‑news‑viewer

   
   ### 2.	Add your API keys

Open Stock Market main.py and replace:

     STOCK_API_KEY = "YOUR_STOCK_API_KEY"
     NEWS_API_KEY  = "YOUR_STOCK_NEWS_API_KEY"


### 3.	Install the few packages

      python -m pip install requests pandas matplotlib
      # On Linux you may also need: sudo apt install python3-tk
  

### Run

      python "Stock Market main.py"

Type a ticker symbol like AAPL or MSFT, hit Search, and the app fetches the data.

---

MIT License

