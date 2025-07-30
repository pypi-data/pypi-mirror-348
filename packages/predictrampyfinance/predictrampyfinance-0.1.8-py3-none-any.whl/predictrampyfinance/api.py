import pkgutil
import json
import re

PACKAGE_NAME = "predictrampyfinance"

# Section frequency mapping
SECTION_FREQUENCY = {
    "IncomeStatement": "quarterly",
    "BalanceSheet": "yearly",
    "CashFlow": "yearly",
}

def get_symbols():
    """Returns a list of all stock symbols from symbol.js"""
    content = pkgutil.get_data(PACKAGE_NAME, "symbol.js").decode("utf-8")
    match = re.search(r'symbol_list\s*=\s*\[(.*?)\]', content, re.DOTALL)
    return re.findall(r'"(.*?)"', match.group(1)) if match else []

def load_data(symbol):
    """Loads all JSON data for a given stock symbol"""
    filename = f"stock_json/{symbol}.json"
    raw = pkgutil.get_data(PACKAGE_NAME, filename)
    if raw:
        return json.loads(raw.decode("utf-8"))
    raise FileNotFoundError(f"Data for symbol '{symbol}' not found.")

def get_metadata(symbol):
    """Returns metadata (symbol and label) for a stock"""
    data = load_data(symbol)
    return {"symbol": data.get("symbol"), "label": data.get("label")}

def get_available_sections():
    """Returns available sections and their frequency"""
    return SECTION_FREQUENCY

def get_section_frequency(section):
    """Returns frequency of the section (quarterly or yearly)"""
    return SECTION_FREQUENCY.get(section, "unknown")

def get_dates(symbol, section):
    """Returns all available dates in a section"""
    data = load_data(symbol)
    if section in data:
        return [entry.get("Date") for entry in data[section]]
    raise ValueError(f"Section '{section}' not found for symbol '{symbol}'.")

def get_data_by_date(symbol, section, date):
    """Fetches specific entry from a section by date"""
    data = load_data(symbol)
    if section in data:
        for entry in data[section]:
            if entry.get("Date") == date:
                return entry
        raise ValueError(f"Date '{date}' not found in section '{section}' for symbol '{symbol}'.")
    raise ValueError(f"Section '{section}' not found for symbol '{symbol}'.")

def get_data_by_frequency(symbol, frequency):
    """Returns all sections of a given frequency (e.g. yearly or quarterly)"""
    data = load_data(symbol)
    result = {}
    for section, freq in SECTION_FREQUENCY.items():
        if freq == frequency and section in data:
            result[section] = data[section]
    return result

def get_income_statement(symbol):
    """Returns income statement data for a stock"""
    return load_data(symbol).get("IncomeStatement", [])

def get_balance_sheet(symbol):
    """Returns balance sheet data for a stock"""
    return load_data(symbol).get("BalanceSheet", [])

def get_cash_flow(symbol):
    """Returns cash flow data for a stock"""
    return load_data(symbol).get("CashFlow", [])

def search_by_label(query):
    """Searches stocks by partial label match"""
    results = []
    for symbol in get_symbols():
        try:
            label = load_data(symbol).get("label", "")
            if query.lower() in label.lower():
                results.append({"symbol": symbol, "label": label})
        except:
            continue
    return results

def get_data_between_dates(symbol, section, start_date, end_date):
    """Returns entries between two dates for a given section"""
    data = load_data(symbol).get(section, [])
    return [entry for entry in data if start_date <= entry.get("Date") <= end_date]
