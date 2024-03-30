import streamlit as st

from pages import portfolio

# Create a sidebar menu
# pages = {"Portfolio": portfolio.portfolio_page, "Holdings": holdings.holdings_page}
pages = {"Portfolio": portfolio.portfolio_page}


# Display the selected page
selected_page = st.sidebar.selectbox("Select a page", list(pages.keys()))
pages[selected_page]()
