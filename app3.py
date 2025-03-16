import streamlit as st
from urllib.parse import quote_plus
from bs4 import BeautifulSoup
import requests
from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

#####################################
# Search Functions for Various Sources
#####################################

def format_indian_kanoon_results(results, current_page):
    """
    Format Indian Kanoon results with continuous numbering.
    If page 1 returns less than 10 results, page 2 starts counting immediately after.
    """
    if not results:
        return "No results found."
    if "ik_counts" not in st.session_state:
        st.session_state.ik_counts = {}
    st.session_state.ik_counts[current_page] = len(results)
    cumulative = sum(st.session_state.ik_counts.get(page, 0) for page in range(1, current_page))
    start_num = cumulative + 1
    formatted = f"### Indian Kanoon Results (Page {current_page})\n\n"
    for i, res in enumerate(results, start=start_num):
        formatted += f"**{i}. {res['title']}**\n- Link: {res['link']}\n"
        if res.get("details"):
            formatted += f"- Details: {res['details']}\n"
        formatted += "\n"
    return formatted

def fetch_austlii_search_results(keyword):
    encoded_keyword = quote_plus(keyword)
    search_url = f"https://www.austlii.edu.au/cgi-bin/sinosrch.cgi?method=auto&query={encoded_keyword}"
    headers = {"User-Agent": "Mozilla/5.0"}
    try:
        response = requests.get(search_url, headers=headers, timeout=20)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        st.error("Error fetching AustLII results: " + str(e))
        return [{
            "title": "AustLII",
            "link": "",
            "details": "AustLII results are currently unavailable due to a connection error."
        }]
    soup = BeautifulSoup(response.content, "html.parser")
    results = []
    for a in soup.find_all("a", href=True):
        href = a["href"]
        if "/cgi-bin/viewdoc/" not in href:
            continue
        link = href if href.startswith("http") else "https://www.austlii.edu.au" + href
        title = a.get_text(strip=True)
        if not title:
            next_text = a.next_sibling
            while next_text:
                if hasattr(next_text, "strip") and next_text.strip():
                    title = next_text.strip()
                    break
                next_text = next_text.next_sibling
        details = ""
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

def fetch_canlii_search_results(keyword):
    base_url = "https://www.canlii.org/en/"
    chrome_options = ChromeOptions()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=chrome_options)
    try:
        driver.get(base_url)
        # Remove cookie consent blocker if present.
        driver.execute_script(
            "if(document.getElementById('cookieConsentBlocker'))"
            "{document.getElementById('cookieConsentBlocker').style.display = 'none';}"
        )
        search_bar = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "#textInput"))
        )
        driver.execute_script("arguments[0].value = arguments[1];", search_bar, keyword)
        search_button = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "button[aria-label='Start a search']"))
        )
        search_button.click()
        WebDriverWait(driver, 40).until(
           EC.presence_of_element_located((By.CSS_SELECTOR, "a[data-result-uuid]"))
        )
        html = driver.page_source
    except Exception as err:
        st.error("Error fetching CanLII results: " + str(err))
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

def fetch_justia_search_results(keyword, page):
    chrome_options = ChromeOptions()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=chrome_options)
    try:
        search_url = (
            f"https://www.justia.com/search?q={quote_plus(keyword)}"
            f"&cx=012624009653992735869%3Acyxxdwappru&start={(page - 1) * 10}"
        )
        driver.get(search_url)
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
    for result in soup.select("div.gsc-webResult a.gs-title"):
        title = result.get_text(strip=True)
        link = result.get("href", "")
        results.append({"title": title, "link": link})
    return results

#####################################
# Formatting Functions
#####################################

def format_results(results, source_name):
    """
    Generic formatting for sources that restart numbering for each search.
    """
    formatted = f"### {source_name} Results:\n\n"
    if not results:
        formatted += "No results found.\n"
        return formatted
    for i, res in enumerate(results, 1):
        formatted += f"**{i}. {res['title']}**\n- Link: {res['link']}\n"
        if res.get("details"):
            formatted += f"- Details: {res['details']}\n"
        formatted += "\n"
    return formatted

def format_justia_results(results, current_page):
    """
    Format Justia results with continuous numbering.
    """
    if not results:
        return "No results found."
    if "justia_counts" not in st.session_state:
        st.session_state.justia_counts = {}
    st.session_state.justia_counts[current_page] = len(results)
    cumulative = sum(st.session_state.justia_counts.get(page, 0) for page in range(1, current_page))
    start_num = cumulative + 1
    formatted = f"### Justia Results (Page {current_page})\n\n"
    for i, res in enumerate(results, start=start_num):
        formatted += f"**{i}. {res['title']}**\n- Link: {res['link']}\n\n"
    return formatted

#####################################
# Main Streamlit Dashboard App
#####################################

def main():
    st.title("Legal Search Dashboard")
    st.write("This dashboard searches multiple legal databases for your query.")

    # --- Checkbox Options to Choose Which Sites to Search ---
    search_ik = st.checkbox("Indian Kanoon", value=True)
    search_al = st.checkbox("AustLII", value=True)
    search_cl = st.checkbox("CanLII", value=True)
    search_justia = st.checkbox("Justia", value=True)

    # --- Initialize session state variables ---
    if "keyword" not in st.session_state:
        st.session_state.keyword = ""
    if "ik_page" not in st.session_state:
        st.session_state.ik_page = 1
    if "justia_page" not in st.session_state:
        st.session_state.justia_page = 1
    if "results_fetched" not in st.session_state:
        st.session_state.results_fetched = False

    # --- Search Input ---
    keyword_input = st.text_input("Enter keyword to search:", value=st.session_state.keyword)

    # When "Search" is clicked, update session state and fetch results for selected sites.
    if st.button("Search", key="search_button"):
        st.session_state.keyword = keyword_input
        if search_ik:
            st.session_state.ik_page = 1  # reset Indian Kanoon pagination
            st.session_state.ik_results = format_indian_kanoon_results(st.session_state.keyword, st.session_state.ik_page)
        else:
            st.session_state.ik_results = []
        if search_al:
            st.session_state.austlii_results = fetch_austlii_search_results(st.session_state.keyword)
        else:
            st.session_state.austlii_results = []
        if search_cl:
            st.session_state.canlii_results = fetch_canlii_search_results(st.session_state.keyword)
        else:
            st.session_state.canlii_results = []
        if search_justia:
            st.session_state.justia_page = 1  # reset Justia pagination
            st.session_state.justia_results = fetch_justia_search_results(st.session_state.keyword, st.session_state.justia_page)
        else:
            st.session_state.justia_results = []
        st.session_state.results_fetched = True
        st.session_state.ik_counts = {}
        st.session_state.justia_counts = {}

    # --- Display results if a search has been performed ---
    if st.session_state.results_fetched:
        if search_ik:
            st.markdown(format_indian_kanoon_results(st.session_state.ik_results, st.session_state.ik_page))
            ik_container = st.empty()
            col1, col2, col3 = st.columns([1, 2, 1])
            if col1.button("← Previous", key="prev_ik") and st.session_state.ik_page > 1:
                st.session_state.ik_page -= 1
                st.session_state.ik_results = fetch_indian_kanoon_results(st.session_state.keyword, st.session_state.ik_page)
                ik_container.markdown(format_indian_kanoon_results(st.session_state.ik_results, st.session_state.ik_page))
            col2.write(f"Page {st.session_state.ik_page}")
            if col3.button("Next →", key="next_ik"):
                st.session_state.ik_page += 1
                st.session_state.ik_results = fetch_indian_kanoon_results(st.session_state.keyword, st.session_state.ik_page)
                ik_container.markdown(format_indian_kanoon_results(st.session_state.ik_results, st.session_state.ik_page))
            st.markdown("---")
        if search_al:
            st.markdown(format_results(st.session_state.austlii_results, "AustLII"))
            st.markdown("---")
        if search_cl:
            st.markdown(format_results(st.session_state.canlii_results, "CanLII"))
            st.markdown("---")
        if search_justia:
            st.markdown("### Justia Results")
            justia_container = st.empty()
            justia_container.markdown(format_justia_results(st.session_state.justia_results, st.session_state.justia_page))
            col4, col5, col6 = st.columns([1, 2, 1])
            if col4.button("← Previous", key="prev_justia") and st.session_state.justia_page > 1:
                st.session_state.justia_page -= 1
                st.session_state.justia_results = fetch_justia_search_results(st.session_state.keyword, st.session_state.justia_page)
                justia_container.markdown(format_justia_results(st.session_state.justia_results, st.session_state.justia_page))
            col5.write(f"Page {st.session_state.justia_page}")
            if col6.button("Next →", key="next_justia"):
                st.session_state.justia_page += 1
                st.session_state.justia_results = fetch_justia_search_results(st.session_state.keyword, st.session_state.justia_page)
                justia_container.markdown(format_justia_results(st.session_state.justia_results, st.session_state.justia_page))

if __name__ == '__main__':
    main()
