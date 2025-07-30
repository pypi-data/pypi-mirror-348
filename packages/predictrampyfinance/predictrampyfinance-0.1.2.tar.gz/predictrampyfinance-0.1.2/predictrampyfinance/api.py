import pkgutil
import re
import json

PACKAGE_NAME = "predictrampyfinance"

def get_symbols():
    content = pkgutil.get_data(PACKAGE_NAME, "symbol.js").decode("utf-8")
    match = re.search(r'symbol_list\s*=\s*\[(.*?)\]', content, re.DOTALL)
    if match:
        return re.findall(r'"(.*?)"', match.group(1))
    return []

def load_data(symbol):
    filename = f"stock_json/{symbol}.json"
    raw = pkgutil.get_data(PACKAGE_NAME, filename)
    if raw:
        return json.loads(raw.decode("utf-8"))
    raise FileNotFoundError(f"Data for symbol '{symbol}' not found.")

def get_income_statement(symbol):
    return load_data(symbol).get("IncomeStatement", [])

def get_balance_sheet(symbol):
    return load_data(symbol).get("BalanceSheet", [])
