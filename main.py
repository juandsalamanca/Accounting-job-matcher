import streamlit as st
import json
import pandas as pd
from src.extract_leads import extract_leads
from src.get_emails_from_linkedin import get_emails_from_linkedin
from src.google_linkedin_people import google_linkedin_people
from src.jop_post_scraper import jop_post_scraper

st.header("Accounting-Job-Matcher")

st.subheader("Get extract lead list end get emails")
st.text("Use the cookie editor chrome extension to export your sales navigator cookies as JSON")
cookie_input = st.text_area("Paste here your Sales Navigator cookie", height=300)
cookie_input = cookie_input.replace("true", "True").replace("false", "False").replace("null", "None")
cookies = json.loads(cookie_input)
list_url = st.text_area("Paste here your Sales Navigator Lead list URL", height=300)

st.text("It is recommended to not scrape more than a few hundred leads a day and preferably spaced out during the day")
max_results = st.number_input("Maximum results extracted from the list")

extract = st.button("Extract leads")
if extract:
  leads = extract_leads(cookies, list_url, max_results)
  leads["LinkedIN_URL"] = []
  leads["Email"] = []
  for i in range(len(leads["Name"])):
    name = leads["Name"][i]
    title = leads["Title"][i]
    company = leads["Company"][i]
    peronal_info_string = name + title + company
    linkedin_url = google_linkedin_people(personal_info_string)
    leads["LinkedIN_URL"].append(linkedin_url)
    email = get_email_from_linkedin(linkedin_url)
    leads["Email"].append(email)
  df = pd.DataFrame(leads)

st.subheader("Scrape job posts")
job_title = st.text_area("Write down here the job title you want to use for scraping job posts")
number_posts = st.number_input("How many job posts do you want scraped?")
scrape = st.button("Scrape job posts")
if scrape:
  posts_scraped = job_post_scraper(job_title, number_posts)
    
                     


