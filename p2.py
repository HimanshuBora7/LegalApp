import streamlit as st
from urllib.parse import quote_plus
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.edge.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def fetch_justia_search_results(keyword, page):
    """
    Fetch Justia search results using Selenium.
    The Justia search page accepts a "start" parameter where page 1 is start=0, page 2 is start=10, etc.
    """
    edge_options = Options()
    edge_options.add_argument("--headless")
    edge_options.add_argument("--disable-gpu")
    driver = webdriver.Edge(options=edge_options)
    
    try:
        # Build the URL with the start parameter based on the page number.
        search_url = (
            f"https://www.justia.com/search?q={quote_plus(keyword)}"
            f"&cx=012624009653992735869%3Acyxxdwappru&start={(page - 1) * 10}"
        )
        driver.get(search_url)
        # Wait until at least one result is present.
        WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.CLASS_NAME, "gsc-webResult"))
        )
        html = driver.page_source
    except Exception as err:
        st.error("Error fetching Justia results: " + str(err))
        html = ""
    finally:
        driver.quit()
    
    soup = BeautifulSoup(html, "html.parser")
    results = []
    # Each result is assumed to reside in a div with class "gsc-webResult" and
    # the anchor tag with class "gs-title" holds the title and link.
    for result in soup.select("div.gsc-webResult a.gs-title"):
        title = result.get_text(strip=True)
        link = result.get("href", "")
        results.append({"title": title, "link": link})
    return results

def format_justia_results(results, current_page):
    """
    Format the Justia results with continuous numbering.
    The starting number is calculated from the number of search results on all previous pages.
    If page 1 returns 9 results, then page 2's numbering will start at 10.
    """
    if not results:
        return "No results found."
    
    # Ensure we have a session state dictionary to store result counts.
    if "justia_counts" not in st.session_state:
        st.session_state.justia_counts = {}
    
    # Store the count for the current page.
    st.session_state.justia_counts[current_page] = len(results)
    
    # Calculate the cumulative count from previous pages.
    cumulative = 0
    for page in range(1, current_page):
        # If a previous page hasn't been visited, assume 10 results.
        cumulative += st.session_state.justia_counts.get(page, 10)
    start_num = cumulative + 1

    formatted = ""
    for i, res in enumerate(results, start=start_num):
        formatted += f"**{i}. {res['title']}**\n- Link: {res['link']}\n\n"
    return formatted

################################
# Standalone Streamlit App for Justia Pagination
################################

st.header("Justia Search Pagination Demo")

# Input for search keyword.
keyword = st.text_input("Enter Justia search keyword:")

# Initialize session state for page number if not already defined.
if "justia_page" not in st.session_state:
    st.session_state.justia_page = 1

# Create pagination buttons in three columns.
col1, col2, col3 = st.columns(3)

if col1.button("← Previous") and st.session_state.justia_page > 1:
    st.session_state.justia_page -= 1

if col3.button("Next →"):
    st.session_state.justia_page += 1

# Display the current page number.
col2.write(f"Page {st.session_state.justia_page}")

# Fetch and display results if a keyword has been entered.
if keyword:
    results = fetch_justia_search_results(keyword, st.session_state.justia_page)
    st.markdown(format_justia_results(results, st.session_state.justia_page))
