import streamlit as st
from forex_python.converter import CurrencyRates
import datetime

# Page config
st.set_page_config(
    page_title="Israeli Salary Calculator",
    page_icon="🇮🇱",
    layout="wide"
)

# Initialize currency converter
c = CurrencyRates()

def get_exchange_rates():
    """Get current exchange rates for ILS to USD, EUR, and GBP"""
    try:
        usd_rate = c.get_rate('ILS', 'USD')
        eur_rate = c.get_rate('ILS', 'EUR')
        gbp_rate = c.get_rate('ILS', 'GBP')
        return usd_rate, eur_rate, gbp_rate
    except:
        # Fallback rates in case of API issues
        return 0.28, 0.26, 0.22

def format_currency(amount, currency):
    """Format currency with appropriate symbol and no decimal places"""
    symbols = {
        'USD': '$',
        'EUR': '€',
        'GBP': '£'
    }
    return f"{symbols.get(currency, '')}{int(amount):,}"

# Get current exchange rates
usd_rate, eur_rate, gbp_rate = get_exchange_rates()

# Main app title
st.title("Israeli Salary Calculator")

# Create tabs
tab1, tab2 = st.tabs(["Israel To ROW 🇮🇱", "ROW to Israel 🌍"])

with tab1:
    st.header("Convert Israeli Salary to World Currencies")
    
    # Create two columns for input methods
    col1, col2 = st.columns(2)
    
    with col1:
        # Dial input using number_input with step
        ils_salary = st.number_input(
            "Select salary (ILS)",
            min_value=7000,
            max_value=60000,
            value=15000,
            step=1000,
            help="Use the up/down arrows or type directly"
        )
    
    with col2:
        # Alternative slider input
        ils_salary = st.slider(
            "Or use slider",
            min_value=7000,
            max_value=60000,
            value=ils_salary,
            step=1000
        )
    
    # Display conversions
    st.subheader("Annual Salary in World Currencies")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("### 🇺🇸 USD")
        usd_salary = ils_salary * 12 * usd_rate
        st.markdown(f"### {format_currency(usd_salary, 'USD')}")
    
    with col2:
        st.markdown("### 🇪🇺 EUR")
        eur_salary = ils_salary * 12 * eur_rate
        st.markdown(f"### {format_currency(eur_salary, 'EUR')}")
    
    with col3:
        st.markdown("### 🇬🇧 GBP")
        gbp_salary = ils_salary * 12 * gbp_rate
        st.markdown(f"### {format_currency(gbp_salary, 'GBP')}")

with tab2:
    st.header("Convert World Currencies to Israeli Salary")
    
    # Currency selection
    currency = st.selectbox(
        "Select Currency",
        ["USD 🇺🇸", "EUR 🇪🇺", "GBP 🇬🇧"]
    )
    
    # Get the appropriate exchange rate
    if currency.startswith("USD"):
        rate = usd_rate
        curr = "USD"
    elif currency.startswith("EUR"):
        rate = eur_rate
        curr = "EUR"
    else:
        rate = gbp_rate
        curr = "GBP"
    
    # Salary input
    world_salary = st.number_input(
        f"Enter annual salary in {curr}",
        min_value=0,
        max_value=1000000,
        value=50000,
        step=1000
    )
    
    # Calculate Israeli monthly salary
    ils_monthly = int((world_salary / 12) / rate)
    
    st.subheader("Monthly Salary in Israel")
    st.markdown(f"### 🇮🇱 {format_currency(ils_monthly, 'ILS')} ILS")

# Footer
st.markdown("---")
st.markdown(
    "This calculation app for converting between salaries in Israel and the rest of the world "
    "was developed by Daniel Rosehill (danielrosehill.com) prompting Sonnet 3.5."
)
