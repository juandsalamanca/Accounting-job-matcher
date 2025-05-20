from apify_client import ApifyClient
import streamlit as st
import json

def extract_leads(cookies, list_url, max_results):

  scraped_info = {"Name":[], "Title":[], "Company":[]}
  # Initialize the ApifyClient with your API token
  ApifyKey = st.secrets["apify_key"]
  client = ApifyClient(ApifyKey)
  run_input = {
    "cookies": cookies,
    "search": list_url,
    "start_page": 1,
    "max_page": 0,
    "max_results": max_results
}
  # Run the Actor and wait for it to finish
  run = client.actor("oxVIg0fuZ0uMcLoyT").call(run_input=run_input)
  
  # Fetch and print Actor results from the run's dataset (if there are any)
  for item in client.dataset(run["defaultDatasetId"]).iterate_items():
    scraped_info["Name"].append(item["full_name"])
    scraped_info["Title"].append(item["jobtitle"])
    scraped_info["Company"].append(item["company_name"])
    
  return scraped_info
