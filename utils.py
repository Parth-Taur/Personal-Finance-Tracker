def format_currency(amount):
    try:
        amount = float(amount)
        return f"₹{amount:,.2f}"
    except:
        return "₹0.00"

def get_month_year(date_str):
    from datetime import datetime
    try:
        dt = datetime.strptime(date_str, "%Y-%m-%d")
        return dt.strftime("%B %Y")
    except:
        return date_str
