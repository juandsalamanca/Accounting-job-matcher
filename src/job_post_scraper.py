from apify_client import ApifyClient
import urllib.parse
import streamlit as st

def job_post_scraper(job_title, count):
  scraped_data = {"Job_title":[], "Company_name":[], "Company_LI_URL":[], "Job_post_url":[]}
  ApifyKey = st.secrets["apify_key"]
  apify_client = ApifyClient(ApifyKey)
  encoded_title = urllib.parse.quote(title)
  run_input = {
    "urls": [f"https://www.linkedin.com/jobs/search-results/?keywords={job_title}&origin=SWITCH_SEARCH_VERTICAL"],
    "scrapeCompany": True,
    "count": count,
  }

  # Run the Actor and wait for it to finish
  run = appify_client.actor("hKByXkMQaC5Qt9UMN").call(run_input=run_input)
  for item in appify_client.dataset(run["defaultDatasetId"]).iterate_items():
    scraped_data["Job_title"].append(item["title"])
    scraped_data["Company_name"].append(item["companyName"])
    scraped_data["Company_LI_URL"].append(item["companyLinkedinUrl"])
    scraped_data["Job_post_url"].append(item["link"])
    
  return scraped_data
    

