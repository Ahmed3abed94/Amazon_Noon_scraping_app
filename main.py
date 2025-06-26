import streamlit as st
import pandas as pd
import io
from selenium.webdriver.chrome.options import Options
from Amazon_Noon_scraping_app.utilis import init_driver
from Amazon_Noon_scraping_app.noon import scrap_noon
from Amazon_Noon_scraping_app.amazon import amazone_scrap

st.set_page_config(layout="wide")
# Load external CSS
with open("style.css", encoding="utf-8") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)


st.title("🛒 Product Comparison: Amazon vs Noon")


# Function to export to Excel bytes
def to_excel_bytes(df):
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        df.to_excel(writer, index=False)
    return output.getvalue()

# Initialize session state
if "df_noon" not in st.session_state:
    st.session_state.df_noon = pd.DataFrame()

if "df_amazon" not in st.session_state:
    st.session_state.df_amazon = pd.DataFrame()

search = st.text_input("What are you looking for?")

if st.button("Search") and search:
    with st.spinner("Scraping..."):
        noon_driver = init_driver()
        amazon_driver = init_driver()

        # Scraping
        st.session_state.df_noon = pd.DataFrame(scrap_noon(noon_driver, search))
        st.session_state.df_amazon = pd.DataFrame(amazone_scrap(amazon_driver, search))

# Show results if available
if not st.session_state.df_noon.empty:
    cols = st.columns(2)
    with cols[0]:
        st.subheader("🔶 Noon Results")
    with cols[1]:
        st.download_button(
            label="Download Noon Excel",
            data=to_excel_bytes(st.session_state.df_noon),
            file_name="noon_results.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )

    grid = st.columns(3)
    for idx, row in st.session_state.df_noon.iterrows():
        with grid[idx % 3]: # type: ignore
            st.image(row["img"], width=150)
            st.markdown(f"**{row['title']}**")
            st.write(f"💵 Price: {row['price']}")

st.markdown("---")

if not st.session_state.df_amazon.empty:
    cols = st.columns(2)
    with cols[0]:
        st.subheader("🟦 Amazon Results")
    with cols[1]:
        st.download_button(
            label="Download Amazon Excel",
            data=to_excel_bytes(st.session_state.df_amazon),
            file_name="amazon_results.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )

    grid = st.columns(3)
    for idx, row in st.session_state.df_amazon.iterrows():
        with grid[idx % 3]: # type: ignore
            st.image(row["img"], width=150)
            st.markdown(f"**{row['title']}**")
            st.write(f"💵 Price: {row['price']}")
