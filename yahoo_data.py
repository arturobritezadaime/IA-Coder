import yfinance as yf
import pandas as pd

# Función auxiliar para buscar columnas con nombres distintos
def find_col(df, candidates):
    for col in candidates:
        if col in df.columns:
            return df[col]
    return pd.Series(dtype="float64")

def get_financials_yahoo(ticker: str, years: int = 5):
    """
    Devuelve un DataFrame con Revenues, NetIncome, Assets, Liabilities, Equity,
    más los ratios ROE y CurrentRatio, para los últimos N años disponibles.
    """
    stock = yf.Ticker(ticker)

    # Income statement (Revenues, Net Income)
    financials = stock.financials.T  
    # Balance sheet (Assets, Liabilities, Equity)
    balance = stock.balance_sheet.T  

    # Buscar columnas (a veces cambian los nombres)
    revenues = financials.get("Total Revenue")
    net_income = financials.get("Net Income")
    assets = balance.get("Total Assets")

    liabilities = find_col(balance, [
        "Total Liab",
        "Total Liabilities Net Minority Interest",
        "Total Non Current Liabilities Net Minority Interest"
    ])

    equity = find_col(balance, [
        "Total Stockholder Equity",
        "Common Stock Equity"
    ])

    # Armar DataFrame
    df = pd.DataFrame({
        "Revenues": revenues,
        "NetIncome": net_income,
        "Assets": assets,
        "Liabilities": liabilities,
        "Equity": equity
    })

    # Limitar a últimos N años
    df = df.head(years)

    # Convertir a numérico
    for col in df.columns:
        df[col] = pd.to_numeric(df[col], errors="coerce")

    # Ratios
    df["ROE"] = (df["NetIncome"] / df["Equity"]).round(4)
    df["CurrentRatio"] = (df["Assets"] / df["Liabilities"]).round(4)

    # Ordenar cronológicamente
    df = df.sort_index()

    # Eliminar años completamente vacíos (NaN)
    df = df.dropna(how="all")

    return df

def get_yfinance_revenue_growth(ticker: str):
    """
    Devuelve {'RevenueGrowth': float | None} calculado a partir de financials (anual),
    con fallback a quarterly_financials si falta.
    """
    stock = yf.Ticker(ticker)
    revenue_growth = None

    # Intento con anual
    if stock.financials is not None and not stock.financials.empty and "Total Revenue" in stock.financials.index:
        fin = stock.financials.loc["Total Revenue"].sort_index()
        if len(fin) >= 2:
            revenue_growth = float((fin.iloc[-1] - fin.iloc[-2]) / fin.iloc[-2])

    # Fallback con trimestral
    if revenue_growth is None and stock.quarterly_financials is not None and not stock.quarterly_financials.empty and "Total Revenue" in stock.quarterly_financials.index:
        qfin = stock.quarterly_financials.loc["Total Revenue"].sort_index()
        if len(qfin) >= 2:
            revenue_growth = float((qfin.iloc[-1] - qfin.iloc[-2]) / qfin.iloc[-2])

    return {"RevenueGrowth": None if revenue_growth is None else round(revenue_growth, 4)}
