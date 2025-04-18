import requests
import datetime as dt
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import tkinter as tk
from tkinter import ttk, scrolledtext
from tkinter import messagebox
import webbrowser
import os

STOCK_ENDPOINT = "https://www.alphavantage.co/query"
STOCK_API_KEY = "YOUR_STOCK_API_KEY"

NEWS_ENDPOINT = "https://newsapi.org/v2/everything"
NEWS_API_KEY = "YOUR_STOCK_NEWS_API_KEY"


def get_stock_price(symbol: str):
    params = {
        "function": "TIME_SERIES_DAILY",
        "symbol": symbol,
        "apikey": STOCK_API_KEY,
    }
    r = requests.get(STOCK_ENDPOINT, params=params)
    print("Debug stock JSON:", r.json())
    data = r.json().get("Time Series (Daily)", {})
    return data


def get_stock_news(
        symbol: str, from_dt: dt.datetime = None, to_dt: dt.datetime = None, max_results=5
):
    params_search = {
        "function": "SYMBOL_SEARCH",
        "keywords": symbol,
        "apikey": STOCK_API_KEY
    }
    try:
        search_data = requests.get(STOCK_ENDPOINT, params=params_search).json()
        matches = search_data.get("bestMatches", [])
        company_name = matches[0].get("2. name", symbol) if matches else symbol
    except Exception:
        company_name = symbol

    now = dt.datetime.now()
    params = {
        "q": company_name,
        "apiKey": NEWS_API_KEY,
        "from": (now - dt.timedelta(days=7)).isoformat(),
        "to":   now.isoformat(),
        "sortBy":  "popularity",
        "language": "en",
    }
    news_data = requests.get(NEWS_ENDPOINT, params=params)
    news_json = news_data.json()
    articles = news_json.get("articles", [])
    return articles[:max_results]


def build_gui():
    window = tk.Tk()
    symbol_var = tk.StringVar()
    window.title("Stock & News Viewer")
    window.config(padx=50, pady=50)
    window.columnconfigure(0, weight=1)
    window.columnconfigure(1, weight=1)
    window.columnconfigure(2, weight=1)
    instr_label = ttk.Label(window, text="Enter ticker symbol (e.g. AAPL):")
    instr_label.grid(row=1, column=0, columnspan=2, sticky="w", padx=5, pady=5)

    entry = ttk.Entry(window, textvariable=symbol_var, width=10)
    entry.grid(row=2, column=0, columnspan=2, sticky="ew", padx=5, pady=5)
    search_btn = ttk.Button(
        window,
        text="Search",
        command=lambda: on_search(symbol_var.get().strip().upper()),
    )
    search_btn.grid(row=2, column=2, sticky="ew", padx=5, pady=5)

    def on_search(symbol: str):
        symbol = symbol.upper()
        data = get_stock_price(symbol)
        articles = get_stock_news(symbol)

        res_win = tk.Toplevel(window)
        res_win.title(f"{symbol} Results")

        df = pd.DataFrame.from_dict(data, orient="index")
        if df.empty or "4. close" not in df.columns:
            messagebox.showerror(
                "Data Error", f"No closing price data available for {symbol}.")
            return
        df.index = pd.to_datetime(df.index)
        df = df.sort_index()
        df["4. close"] = df["4. close"].astype(float)
        fig, ax = plt.subplots(figsize=(6, 4))
        ax.plot(df.index, df["4. close"])
        ax.set_title(f"{symbol} Closing Prices")
        canvas2 = FigureCanvasTkAgg(fig, master=res_win)
        canvas2.draw()
        canvas2.get_tk_widget().pack(padx=10, pady=10)

        news_box = scrolledtext.ScrolledText(
            res_win, width=100, height=30, font=("Arial", 12))
        news_box.pack(padx=10, pady=10)
        if not articles:
            news_box.insert(
                tk.END, "No news found. Please check your News API key or network.\n")
        else:
            for idx, art in enumerate(articles[:5]):
                title = art.get("title", "")
                url = art.get("url", "")
                news_box.insert(tk.END, "• ")
                start = news_box.index(tk.INSERT)
                news_box.insert(tk.END, title)
                end = news_box.index(tk.INSERT)
                news_box.insert(tk.END, "\n\n")
                news_box.tag_add(f"url{idx}", start, end)
                news_box.tag_bind(
                    f"url{idx}", "<Button-1>", lambda event, url=url: webbrowser.open(url))
                news_box.tag_config(
                    f"url{idx}", foreground="cyan", underline=True, font=("Arial", 16, "underline"))
            news_box.config(state=tk.DISABLED)

    canvas = tk.Canvas(window, height=500, width=500)
    image_path = os.path.join(os.path.dirname(__file__), "image-min2.png")
    logo_img = tk.PhotoImage(file=image_path)
    canvas.create_image(0, 0, anchor=tk.NW, image=logo_img)
    canvas.image = logo_img
    canvas.grid(row=0, column=0, columnspan=3, sticky="ew")

    window.mainloop()


if __name__ == "__main__":
    build_gui()
