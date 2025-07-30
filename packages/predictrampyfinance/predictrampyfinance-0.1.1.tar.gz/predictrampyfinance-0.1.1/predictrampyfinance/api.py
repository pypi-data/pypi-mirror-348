import json
import os
import re
import pkgutil

def get_symbols():
    """Returns a list of all stock symbols from symbol.js"""
    content = pkgutil.get_data(__package__, "symbol.js").decode("utf-8")
    match = re.search(r'symbol_list\s*=\s*\[(.*?)\]', content, re.DOTALL)
    if match:
        return re.findall(r'"(.*?)"', match.group(1))
    return []

def load_data(symbol):
    """Loads full JSON data for the stock"""
    filename = f"stock_json/{symbol}.json"
    try:
        raw = pkgutil.get_data(__package__, filename)
        return json.loads(raw.decode("utf-8"))
    except Exception as e:
        raise FileNotFoundError(f"Data for symbol '{symbol}' not found.")

def get_income_statement(symbol):
    return load_data(symbol).get("IncomeStatement", [])

def get_balance_sheet(symbol):
    return load_data(symbol).get("BalanceSheet", [])
