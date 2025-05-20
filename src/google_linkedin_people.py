import requests
import streamlit as st

# Replace with your actual API Key and Search Engine ID
API_KEY = st.secrets["google_key"]
CX = st.secrets["cx"]

def get_linkedin_url(person_info):
    """
    Uses Google Custom Search API to find the LinkedIn company URL.
    """
    query = f"{person_info} site:linkedin.com/in"
    url = f"https://www.googleapis.com/customsearch/v1?q={query}&key={API_KEY}&cx={CX}"

    try:
        response = requests.get(url)
        data = response.json()

        # Extract the first result URL
        if "items" in data:
            return data["items"][0]["link"]
        else:
            #print("[-] No results found")
            return None

    except Exception as e:
        print(f"[-] Error fetching LinkedIn URL: {e}")
        return None
