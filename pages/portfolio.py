import json

import requests
import streamlit as st

from config import API_KEY, BASE_URL

GLOBAL_QUOTE_URL = f"{BASE_URL}?function=GLOBAL_QUOTE&apikey={API_KEY}"
OVERVIEW_URL = f"{BASE_URL}?function=OVERVIEW&apikey={API_KEY}"

STOCK = "Stock"
ETF = "ETF"


def get_full_name(symbol):
    """Fetch the full name of a company or ETF based on its symbol."""
    url = f"{OVERVIEW_URL}&symbol={symbol}"
    response = requests.get(url)
    if response.status_code == 200:
        data = json.loads(response.text)

        if data and "Name" in data:
            return data["Name"]
        else:
            return None


def get_data(symbol):
    """Fetch stock or ETF data from Alpha Vantage."""
    url = f"{GLOBAL_QUOTE_URL}&symbol={symbol}"
    response = requests.get(url)
    if response.status_code == 200:
        data = json.loads(response.text)
        if "Global Quote" in data:
            return data["Global Quote"]
    return None


def add_investment(portfolio, symbol, quantity, investment_type="stock"):
    """Add a stock or ETF to the portfolio."""
    data = get_data(symbol)
    if data is not None and "05. price" in data:
        price = float(data["05. price"])
        investment = {
            "symbol": symbol.upper(),
            "quantity": quantity,
            "price": price,
            "value": quantity * price,
        }
        portfolio.append(investment)
    else:
        st.warning(f"Failed to retrieve {investment_type} data or price not available.")


def display_portfolio(portfolio, title):
    """Display the portfolio section with enhancements."""
    st.subheader(title)

    for investment in portfolio:
        symbol = investment["symbol"].upper()

        if STOCK in title:
            full_name = get_full_name(symbol)
            st.markdown(
                f"""
                **Symbol**: {symbol}
                **Name**: {full_name}
                **Quantity**: {investment['quantity']}
                **Price**: ${investment['price']:.2f}
                **Value**: ${investment['value']:.2f}
                """,
                unsafe_allow_html=True,
            )
        elif ETF in title:
            st.markdown(
                f"""
                **Symbol**: {symbol}
                **Quantity**: {investment['quantity']}
                **Price**: ${investment['price']:.2f}
                **Value**: ${investment['value']:.2f}
                """,
                unsafe_allow_html=True,
            )


def portfolio_page():
    """Main function to render the Streamlit page."""
    st.title("Portfolio Tracker")

    # Initialize portfolios using Streamlit's session_state
    if "stock_portfolio" not in st.session_state:
        st.session_state.stock_portfolio = []
    if "etf_portfolio" not in st.session_state:
        st.session_state.etf_portfolio = []

    # Stock portfolio section
    st.subheader("Stock Portfolio")
    stock_symbol = st.text_input("Enter stock symbol", key="stock_symbol_input")
    stock_quantity = st.number_input(
        "Enter stock quantity", min_value=0, step=1, key="stock_quantity_input"
    )
    if st.button("Add Stock", key="add_stock_button"):
        add_investment(st.session_state.stock_portfolio, stock_symbol, stock_quantity)

    # ETF portfolio section
    st.subheader("ETF Portfolio")
    etf_symbol = st.text_input("Enter ETF symbol", key="etf_symbol_input")
    etf_quantity = st.number_input(
        "Enter ETF quantity", min_value=0, step=1, key="etf_quantity_input"
    )
    if st.button("Add ETF", key="add_etf_button"):
        add_investment(st.session_state.etf_portfolio, etf_symbol, etf_quantity, "ETF")

    # Portfolio summary
    total_stock_value = sum(
        stock["value"] for stock in st.session_state.stock_portfolio
    )
    total_etf_value = sum(etf["value"] for etf in st.session_state.etf_portfolio)
    total_market_value = total_stock_value + total_etf_value

    st.subheader("Portfolio Summary")
    st.write(f"Total Stock Value: ${total_stock_value:.2f}")
    st.write(f"Total ETF Value: ${total_etf_value:.2f}")
    st.write(f"Total Market Value: ${total_market_value:.2f}")

    # Display current portfolios
    display_portfolio(st.session_state.stock_portfolio, "Current Stock Portfolio")
    display_portfolio(st.session_state.etf_portfolio, "Current ETF Portfolio")


portfolio_page()
