import streamlit as st
from apify_client import ApifyClient


def scrape_employees_from_companies(company_url):
  ApifyKey=st.secrets["apify_key"]
  appify_client = ApifyClient(ApifyKey)
  if company_url:
    run_input = {
        "proxy": {
            "useApifyProxy": True
        },
        "urls": [company_url]
    }
    actor_call = appify_client.actor("sanjeta/linkedin-company-profile-scraper").call(run_input=run_input)
    res=[]
    # Fetch and print Actor results from the run's dataset (if there are any)
    for item in appify_client.dataset(actor_call["defaultDatasetId"]).iterate_items():
      company_data.append(item)
      
  return company_data
