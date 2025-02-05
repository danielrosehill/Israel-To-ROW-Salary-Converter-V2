import streamlit as st
import requests
import datetime
from typing import Dict, Optional
import os

# Page config
st.set_page_config(
    page_title="Israel To World Salary Calculator",
    page_icon="🇮🇱",
    layout="wide"
)

def get_exchange_rates() -> Dict[str, float]:
    """Get current exchange rates for ILS to various currencies using ECB API"""
    # Default fallback rates (updated Feb 2024)
    default_rates = {
        'USD': 0.27,
        'EUR': 0.25,
        'GBP': 0.21,
        'CAD': 0.36,
        'AUD': 0.41,
        'JPY': 40.0
    }
    
    try:
        # European Central Bank API (XML feed)
        response = requests.get('https://www.ecb.europa.eu/stats/eurofxref/eurofxref-daily.xml')
        if response.status_code == 200:
            from xml.etree import ElementTree
            
            # Parse XML
            root = ElementTree.fromstring(response.content)
            namespaces = {'ns': 'http://www.ecb.int/vocabulary/2002-08-01/eurofxref'}
            
            # Extract rates to EUR
            eur_rates = {}
            for rate in root.findall('.//ns:Cube[@currency][@rate]', namespaces):
                currency = rate.attrib['currency']
                rate_value = float(rate.attrib['rate'])
                eur_rates[currency] = rate_value
            
            # Add EUR rate
            eur_rates['EUR'] = 1.0
            
            # Get ILS to EUR rate (inverse of EUR to ILS)
            eur_to_ils = eur_rates.get('ILS', 1/default_rates['EUR'])
            ils_to_eur = 1 / eur_to_ils
            
            # Calculate rates from ILS
            rates = {}
            for currency in default_rates.keys():
                if currency == 'EUR':
                    rates[currency] = ils_to_eur
                elif currency in eur_rates:
                    # Convert through EUR
                    rates[currency] = ils_to_eur * eur_rates[currency]
                else:
                    rates[currency] = default_rates[currency]
            
            return rates
        else:
            st.warning("⚠️ Unable to fetch current exchange rates. Using fallback rates.")
            return default_rates
    except Exception as e:
        st.warning(f"⚠️ Error connecting to exchange rate service: {str(e)}. Using fallback rates.")
        return default_rates

def format_currency(amount: float, currency: str) -> str:
    """Format currency with appropriate symbol and no decimal places"""
    symbols = {
        'USD': '$',
        'EUR': '€',
        'GBP': '£',
        'CAD': 'C$',
        'AUD': 'A$',
        'JPY': '¥'
    }
    
    # Format all currencies without decimal places
    return f"{symbols.get(currency, '')}{int(amount):,}"

# Get current exchange rates
rates = get_exchange_rates()

# Add GitHub badge
st.markdown('[![GitHub](https://img.shields.io/badge/GitHub-View%20Source-black?style=flat&logo=github)](https://github.com/danielrosehill/Israel-To-ROW-Salary-Converter-V2)', unsafe_allow_html=True)

# Custom CSS for styling
st.markdown("""
    <style>
    /* Page background and general styles */
    .stApp {
        background: linear-gradient(135deg, #f5f7fa 0%, #e8edf5 100%);
    }
    
    .stApp > header {
        background-color: transparent;
    }
    
    .big-number {
        font-size: 4em;
        text-align: center;
        padding: 25px;
        margin: 25px 0;
        font-weight: bold;
        color: #1E88E5;
        background: linear-gradient(145deg, #f0f8ff 0%, #e3f2fd 100%);
        border-radius: 15px;
        box-shadow: 0 4px 8px rgba(0,0,0,0.1);
        transition: all 0.3s ease;
    }
    
    .big-number:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 12px rgba(0,0,0,0.15);
    }
    
    div[role="radiogroup"] > div {
        font-size: 1.3em;
        margin: 1em 0;
    }
    
    .currency-display {
        font-size: 2em;
        text-align: center;
        padding: 20px;
        margin: 15px 0;
        background: linear-gradient(145deg, #ffffff 0%, #f8f9fa 100%);
        border-radius: 12px;
        color: #2E7D32;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        border: 2px solid #e0e0e0;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
    }
    
    .currency-display:hover {
        transform: scale(1.03) translateY(-2px);
        box-shadow: 0 12px 24px rgba(0,0,0,0.1);
        border-color: #2E7D32;
        background: linear-gradient(145deg, #ffffff 0%, #f1f8f1 100%);
    }
    
    /* Much bigger and more prominent plus/minus buttons */
    button[aria-label="Decrease value"],
    button[aria-label="Increase value"] {
        width: 70px !important;
        height: 70px !important;
        font-size: 2.2em !important;
        background-color: #1E88E5 !important;
        color: white !important;
        border-radius: 35px !important;
        margin: 0 15px !important;
        cursor: pointer !important;
        transition: all 0.2s ease !important;
        box-shadow: 0 4px 8px rgba(0,0,0,0.15) !important;
        animation: pulse 2s infinite !important;
    }
    
    @keyframes pulse {
        0% {
            transform: scale(1);
            box-shadow: 0 4px 8px rgba(0,0,0,0.15);
        }
        50% {
            transform: scale(1.05);
            box-shadow: 0 8px 16px rgba(0,0,0,0.2);
        }
        100% {
            transform: scale(1);
            box-shadow: 0 4px 8px rgba(0,0,0,0.15);
        }
    }
    
    button[aria-label="Decrease value"]:hover,
    button[aria-label="Increase value"]:hover {
        transform: scale(1.15) !important;
        box-shadow: 0 8px 16px rgba(0,0,0,0.25) !important;
        background-color: #1976D2 !important;
        animation: none !important;
    }
    
    /* Improve number input styling to accommodate larger buttons */
    input[type="number"] {
        font-size: 1.6em !important;
        padding: 15px 80px !important;
        border-radius: 12px !important;
        border: 2px solid #1E88E5 !important;
        background-color: #fff !important;
        transition: all 0.3s ease !important;
        margin: 10px 0 !important;
    }
    
    input[type="number"]:focus {
        box-shadow: 0 0 0 2px rgba(30,136,229,0.2) !important;
        border-color: #1976D2 !important;
    }
    
    .stButton>button {
        width: 100%;
        font-size: 1.5em;
        padding: 12px;
        border-radius: 12px;
        background-color: #1E88E5;
        color: white;
        transition: all 0.3s ease;
    }
    
    .tooltip {
        font-size: 1em;
        color: #555;
        font-style: italic;
        margin-bottom: 10px;
    }
    
    /* Enhanced tab styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        background: transparent;
        border-bottom: 2px solid rgba(30,136,229,0.2);
        padding-bottom: 2px;
    }
    
    .stTabs [data-baseweb="tab"] {
        padding: 12px 24px;
        background-color: rgba(255, 255, 255, 0.8);
        border-radius: 12px 12px 0 0;
        border: 1px solid #e0e0e0;
        border-bottom: none;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        margin-right: 4px;
    }
    
    .stTabs [data-baseweb="tab"]:hover {
        background-color: rgba(255, 255, 255, 0.95);
        transform: translateY(-2px);
    }
    
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #1E88E5 0%, #1976D2 100%) !important;
        color: white !important;
        border: none !important;
        box-shadow: 0 4px 12px rgba(30,136,229,0.3);
    }
    </style>
""", unsafe_allow_html=True)

# Main app title
st.title("Israel To World Salary Calculator")
st.markdown("Convert salaries between Israeli Shekels and major world currencies, including Bitcoin! 🚀")

# Create tabs
tab1, tab2, tab3 = st.tabs(["Israel to World 🇮🇱", "World to Israel 🌍", "How To Use i️"])

with tab1:
    st.header("Convert Israeli Salary to World Currencies")
    
    # Salary input with tooltip
    st.markdown("<p class='tooltip'>Use the plus/minus buttons or type directly to set your monthly salary in ILS</p>", unsafe_allow_html=True)
    ils_salary = st.number_input(
        "Monthly Salary in ILS",
        min_value=7000,
        max_value=100000,
        value=15000,
        step=1000,
        help="Enter your monthly salary in Israeli Shekels (ILS)",
        label_visibility="collapsed"
    )
    
    st.markdown(f"<div class='big-number'>{int(ils_salary/1000)}K ₪</div>", unsafe_allow_html=True)
    
    # Display conversions
    st.subheader("Annual Salary in World Currencies")
    
    # Create two rows of columns for currencies
    row1_col1, row1_col2, row1_col3 = st.columns(3)
    row2_col1, row2_col2, row2_col3 = st.columns(3)
    
    # First row of currencies
    with row1_col1:
        st.markdown("#### 🇺🇸 USD")
        usd_salary = ils_salary * 12 * rates['USD']
        st.markdown(f"<div class='currency-display'>{format_currency(usd_salary, 'USD')}<br><small style='font-size: 0.6em;'>Rate: {rates['USD']:.4f}</small></div>", unsafe_allow_html=True)
    
    with row1_col2:
        st.markdown("#### 🇪🇺 EUR")
        eur_salary = ils_salary * 12 * rates['EUR']
        st.markdown(f"<div class='currency-display'>{format_currency(eur_salary, 'EUR')}<br><small style='font-size: 0.6em;'>Rate: {rates['EUR']:.4f}</small></div>", unsafe_allow_html=True)
    
    with row1_col3:
        st.markdown("#### 🇬🇧 GBP")
        gbp_salary = ils_salary * 12 * rates['GBP']
        st.markdown(f"<div class='currency-display'>{format_currency(gbp_salary, 'GBP')}<br><small style='font-size: 0.6em;'>Rate: {rates['GBP']:.4f}</small></div>", unsafe_allow_html=True)
    
    # Second row of currencies
    with row2_col1:
        st.markdown("#### 🇨🇦 CAD")
        cad_salary = ils_salary * 12 * rates['CAD']
        st.markdown(f"<div class='currency-display'>{format_currency(cad_salary, 'CAD')}<br><small style='font-size: 0.6em;'>Rate: {rates['CAD']:.4f}</small></div>", unsafe_allow_html=True)
    
    with row2_col2:
        st.markdown("#### 🇦🇺 AUD")
        aud_salary = ils_salary * 12 * rates['AUD']
        st.markdown(f"<div class='currency-display'>{format_currency(aud_salary, 'AUD')}<br><small style='font-size: 0.6em;'>Rate: {rates['AUD']:.4f}</small></div>", unsafe_allow_html=True)
    
    with row2_col3:
        st.markdown("#### 🇯🇵 JPY")
        jpy_salary = ils_salary * 12 * rates['JPY']
        st.markdown(f"<div class='currency-display'>{format_currency(jpy_salary, 'JPY')}<br><small style='font-size: 0.6em;'>Rate: {rates['JPY']:.4f}</small></div>", unsafe_allow_html=True)
    

with tab2:
    st.header("Convert World Currencies to Israeli Salary")
    
    # Currency selection with more prominent UI
    st.markdown("### Select World Currency")
    
    currency = st.radio(
        "Select Currency",
        ["USD 🇺🇸", "EUR 🇪🇺", "GBP 🇬🇧", "CAD 🇨🇦", "AUD 🇦🇺", "JPY 🇯🇵"],
        label_visibility="collapsed",
        horizontal=True,
    )
    
    # Get the appropriate exchange rate and currency code
    curr_map = {
        "USD 🇺🇸": ("USD", rates['USD']),
        "EUR 🇪🇺": ("EUR", rates['EUR']),
        "GBP 🇬🇧": ("GBP", rates['GBP']),
        "CAD 🇨🇦": ("CAD", rates['CAD']),
        "AUD 🇦🇺": ("AUD", rates['AUD']),
        "JPY 🇯🇵": ("JPY", rates['JPY'])
    }
    
    curr, rate = curr_map[currency]
    
    # Salary input
    if curr == "JPY":
        world_salary = st.number_input(
            f"Annual Salary in {curr}",
            min_value=0,
            max_value=100000000,
            value=5000000,
            step=100000,
            label_visibility="collapsed"
        )
    else:
        world_salary = st.number_input(
            f"Annual Salary in {curr}",
            min_value=0,
            max_value=1000000,
            value=50000,
            step=1000,
            label_visibility="collapsed"
        )
    
    symbol = {'USD': '$', 'EUR': '€', 'GBP': '£', 'CAD': 'C$', 'AUD': 'A$', 'JPY': '¥'}[curr]
    
    st.markdown(f"<div class='big-number'>{symbol}{int(world_salary/1000)}K</div>", unsafe_allow_html=True)
    
    # Calculate Israeli monthly salary
    ils_monthly = int((world_salary / 12) / rate)
    
    st.subheader("Monthly Salary in Israel")
    st.markdown(f"<div class='currency-display'>🇮🇱 {format_currency(ils_monthly, 'ILS')} ₪<br><small style='font-size: 0.6em;'>Rate: {1/rate:.4f}</small></div>", unsafe_allow_html=True)

with tab3:
    st.header("How To Use This Calculator")
    
    st.markdown("""
    ### Israel to World 🇮🇱
    1. Enter your monthly salary in Israeli Shekels (ILS)
    2. Use either the number input or plus/minus buttons (7,000 ILS - 100,000 ILS range)
    3. View your annual salary converted to major currencies (USD, EUR, GBP, CAD, AUD, JPY)
    
    ### World to Israel 🌍
    1. Select your currency (USD, EUR, GBP, CAD, AUD, JPY)
    2. Enter your annual salary
    3. View the equivalent monthly salary in Israeli Shekels (ILS)
    
    ### Exchange Rates Information
    - Currency rates are fetched daily from the European Central Bank (ECB)
    - If API is unavailable, fallback rates are used
    - The timestamp below shows when rates were last updated
    - Rates are updated each time you refresh the page
    
    ### Notes
    - All currency amounts are shown without decimal places
    """)

# Footer with enhanced styling
st.markdown("""
<div style="background: linear-gradient(145deg, #ffffff 0%, #f8f9fa 100%); 
            padding: 25px; 
            border-radius: 15px; 
            border: 1px solid #e0e0e0; 
            margin-top: 40px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.05);">
    <p style="text-align: center; 
              margin-bottom: 15px; 
              font-size: 1.1em;
              color: #1E88E5;">
        This calculation app for converting between salaries in Israel and the rest of the world 
        was developed by <a href="https://danielrosehill.com" 
                          style="color: #1976D2; 
                                 text-decoration: none; 
                                 font-weight: bold;
                                 border-bottom: 2px solid #1976D2;">Daniel Rosehill</a> 
        prompting Sonnet 3.5.
    </p>
</div>
""", unsafe_allow_html=True)

# Add FX rate information with matching style
current_time = datetime.datetime.now()
st.markdown(f"""
<div style="text-align: center; 
            margin-top: 20px; 
            padding: 15px; 
            color: #666;
            font-style: italic;">
    Exchange rates are provided by the European Central Bank (ECB).<br>
    Last updated: {current_time.strftime('%Y-%m-%d %H:%M')} Israel time.
</div>
""", unsafe_allow_html=True)
