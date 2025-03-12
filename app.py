import streamlit as st
import time
from urllib.parse import quote_plus
from bs4 import BeautifulSoup
import requests

# --- Existing integrated search functions ---
# You can include the functions from your integrated code here
# (fetch_indian_kanoon_results, fetch_austlii_search_results, fetch_canlii_search_results,
#  and any helper formatting functions)

# For brevity, here are simplified versions. Replace these with your full functions.
def fetch_indian_kanoon_results(keyword):
    encoded_keyword = quote_plus(keyword)
    search_url = f"https://indiankanoon.org/search/?formInput={encoded_keyword}"
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(search_url, headers=headers)
    if response.status_code != 200:
        return []
    soup = BeautifulSoup(response.content, "html.parser")
    results = []
    for result in soup.find_all("div", class_="result_title"):
        anchor = result.find("a", href=True)
        if anchor:
            title = anchor.get_text(strip=True)
            link = anchor["href"]
            if not link.startswith("http"):
                link = "https://indiankanoon.org" + link
            detail_elem = result.find_next_sibling("div")
            details = detail_elem.get_text(strip=True) if detail_elem else ""
            results.append({"title": title, "link": link, "details": details})
    return results

def fetch_austlii_search_results(keyword):
    encoded_keyword = quote_plus(keyword)
    search_url = f"https://www.austlii.edu.au/cgi-bin/sinosrch.cgi?method=auto&query={encoded_keyword}"
    
    headers = {"User-Agent": "Mozilla/5.0"}
    
    try:
        response = requests.get(search_url, headers=headers, timeout=20)
        response.raise_for_status()  # Raise an exception for HTTP error responses
    except requests.exceptions.RequestException as e:
        print("Error fetching AustLII data:", e)
        # Return a fallback result indicating the problem.
        return [{
            "title": "AustLII",
            "link": "",
            "details": "AustLII results are currently unavailable due to a connection error."
        }]
    
    soup = BeautifulSoup(response.content, "html.parser")
    results = []
    
    # Iterate over all anchors; only process those that match the expected pattern.
    for a in soup.find_all("a", href=True):
        href = a["href"]
        if "/cgi-bin/viewdoc/" not in href:
            continue
        
        # Build full URL if necessary.
        link = href if href.startswith("http") else "https://www.austlii.edu.au" + href
        title = a.get_text(strip=True)
        if not title:
            # Try to get non-empty text from the siblings.
            next_text = a.next_sibling
            while next_text:
                if hasattr(next_text, "strip") and next_text.strip():
                    title = next_text.strip()
                    break
                next_text = next_text.next_sibling
        details = ""
        # Get additional details if available.
        p_meta = a.find_next("p", class_="meta")
        if p_meta:
            details = p_meta.get_text(strip=True)
        
        results.append({
            "title": title,
            "link": link,
            "details": details
        })
        
    if not results:
        results.append({
            "title": "AustLII",
            "link": "",
            "details": "No results found on AustLII."
        })
    
    return results


from selenium import webdriver
from selenium.webdriver.edge.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def fetch_canlii_search_results(keyword):
    base_url = "https://www.canlii.org/en/"
    edge_options = Options()
    edge_options.add_argument("--headless")
    edge_options.add_argument("--disable-gpu")
    driver = webdriver.Edge(options=edge_options)
    try:
        driver.get(base_url)
        # Remove cookie consent blocker if present:
        driver.execute_script(
            "if(document.getElementById('cookieConsentBlocker')){document.getElementById('cookieConsentBlocker').style.display = 'none';}"
        )
        # Find the search bar (a textarea with id="textInput")
        search_bar = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "#textInput"))
        )
        driver.execute_script("arguments[0].value = arguments[1];", search_bar, keyword)
        # Click the search button (button with aria-label "Start a search")
        search_button = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "button[aria-label='Start a search']"))
        )
        search_button.click()
        WebDriverWait(driver, 40).until(
           EC.presence_of_element_located((By.CSS_SELECTOR, "a[data-result-uuid]"))
        )
        html = driver.page_source
    except Exception as err:
        html = ""
    finally:
        driver.quit()
    soup = BeautifulSoup(html, "html.parser")
    results = []
    for a in soup.select("a[data-result-uuid]"):
        title = a.get_text(strip=True)
        link = a["href"]
        if not link.startswith("http"):
            link = "https://www.canlii.org" + link
        results.append({"title": title, "link": link})
    return results

# --- Formatting function ---
def format_results(results, source_name):
    formatted = f"### {source_name} Results:\n"
    if not results:
        formatted += "No results found.\n"
        return formatted
    for i, res in enumerate(results, 1):
        formatted += f"**{i}. {res['title']}**\n- Link: {res['link']}\n"
        if res.get("details"):
            formatted += f"- Details: {res['details']}\n"
        formatted += "\n"
    return formatted

# --- Streamlit Dashboard ---
def main():
    st.title("Legal Search Dashboard")
    st.write("This dashboard searches legal databases for your query.")
    
    keyword = st.text_input("Enter keyword to search:")
    if st.button("Search"):
        with st.spinner("Searching..."):
            ik_results = fetch_indian_kanoon_results(keyword)
            austlii_results = fetch_austlii_search_results(keyword)
            canlii_results = fetch_canlii_search_results(keyword)
            
            # Display results for each source:
            st.markdown(format_results(ik_results, "Indian Kanoon"))
            st.markdown("---")
            st.markdown(format_results(austlii_results, "AustLII"))
            st.markdown("---")
            st.markdown(format_results(canlii_results, "CanLII"))
            
if __name__ == '__main__':
    main()
