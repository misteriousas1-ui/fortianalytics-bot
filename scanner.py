import yfinance as yf

def analyze_symbol(symbol):
    try:
        symbol = symbol.upper().replace("-", "").replace(" ", "")
        mapping = {"XAUUSD": "GC=F", "GOLD": "GC=F", "BTC": "BTC-USD", "ETH": "ETH-USD"}
        yf_symbol = mapping.get(symbol, f"{symbol}-USD")
        
        ticker = yf.Ticker(yf_symbol)
        df = ticker.history(period="1d", interval="1m")
        
        if len(df) < 50:
            return {"symbol": symbol, "price": 0, "rsi": 0, "ma50": 0, "signal": "HOLD", "entry": 0, "tp1": 0, "tp2": 0, "sl": 0}
            
        closed_candle = df.iloc[-2]
        current_price = float(df['Close'].iloc[-1])
        price = float(closed_candle['Close'])
        
        delta = df['Close'].diff()
        gain = (delta.where(delta > 0, 0)).rolling(14).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(14).mean()
        rs = gain / loss
        rsi = round(100 - (100 / (1 + rs.iloc[-2])), 1)
        
        ma50 = round(df['Close'].rolling(window=50).mean().iloc[-2], 2)
        
        signal, entry, tp1, tp2, sl = "HOLD", 0, 0, 0, 0
        
        if rsi < 40:
            signal = "BUY"
            entry = round(price, 2)
            tp1, tp2, sl = round(price * 1.005, 2), round(price * 1.01, 2), round(price * 0.995, 2)
        elif rsi > 60:
            signal = "SELL"
            entry = round(price, 2)
            tp1, tp2, sl = round(price * 0.995, 2), round(price * 0.99, 2), round(price * 1.005, 2)
            
        return {"symbol": symbol, "price": round(current_price, 2), "rsi": rsi, "ma50": ma50, "signal": signal, "entry": entry, "tp1": tp1, "tp2": tp2, "sl": sl}
    except:
        return {"symbol": symbol, "price": 0, "rsi": 0, "ma50": 0, "signal": "ERROR", "entry": 0, "tp1": 0, "tp2": 0, "sl": 0}