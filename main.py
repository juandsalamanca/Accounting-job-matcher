import streamlit as st
import json
import pandas as pd
import numpy as np
import time
from src.extract_leads import extract_leads
from src.get_emails_from_linkedin import get_emails_from_linkedin
from src.google_linkedin_people import get_linkedin_url
from src.job_post_scraper import job_post_scraper
from src.scrape_employees_from_companies import scrape_employees_from_companies
from src.get_decision_makers import *

st.header("Accounting-Job-Matcher")

st.subheader("Extract lead list and get emails")

restart = st.button("Restart")
if restart:
  st.session_state.leads_processed = False
  st.session_state.leads_checkpoint = False
  st.session_state.posts_processed = False
  st.session_state.posts_checkpoint = False
  st.session_state.posts_scraped = False

if "leads_processed" not in st.session_state:
  st.session_state.leads_processed = False

if "leads_checkpoint" not in st.session_state:
  st.session_state.leads_checkpoint = False

st.text("Use the cookie editor chrome extension to export your Sales Navigator cookies as JSON")
cookie_input = st.text_area("Paste here your Sales Navigator cookie", height=100)

if cookie_input:
  #cookie_string = cookie_input.replace("true", "True").replace("false", "False").replace("null", "None")
  #st.code(cookie_input)
  cookies = json.loads(cookie_input)
  
list_url = st.text_area("Paste here your Sales Navigator Lead list URL", height=70)

st.text("It is recommended to not scrape more than a few hundred leads a day and preferably spaced out during the day")
max_results = st.number_input("Maximum results extracted from the list", min_value=1, max_value=100)

if cookie_input and list_url and max_results:
  extract = st.button("Extract leads")

  if extract:
    if st.session_state.leads_checkpoint == False:
      st.session_state.leads = extract_leads(cookies, list_url, int(max_results))
      st.session_state.leads_checkpoint = True
    leads = st.session_state.leads
    leads["LinkedIN_URL"] = []
    leads["Email"] = []
    for i in range(len(leads["Name"])):
      name = leads["Name"][i]
      title = leads["Title"][i]
      company = leads["Company"][i]
      personal_info_string = f"{name} {title} {company}"
      linkedin_url = get_linkedin_url(personal_info_string)
      st.write(personal_info_string)
      st.write(linkedin_url)
      leads["LinkedIN_URL"].append(linkedin_url)
      email = get_emails_from_linkedin(linkedin_url)
      leads["Email"].append(email)
      time.sleep(3)
    st.session_state.leads_df = pd.DataFrame(leads)
    st.session_state.leads_processed = True

if st.session_state.leads_processed:
  
  st.session_state.leads_data = st.session_state.leads_df.to_csv(index = False).encode("utf-8")
  st.download_button(
        label="Download the output file",
        data=st.session_state.leads_data,
        file_name="Leads_data.csv",
        mime="text/csv",
    )
  
if "posts_processed" not in st.session_state:
  st.session_state.posts_processed = False

if "posts_checkpoint" not in st.session_state:
  st.session_state.posts_checkpoint = False

if "posts_df" not in st.session_state:
  st.session_state.posts_df = False
  
  
st.subheader("Scrape job posts")
job_title = st.text_area("Write down here the job title you want to use for scraping job posts", height=70)
number_posts = st.number_input("How many job posts do you want scraped?", min_value=100, max_value=500)

if job_title and number_posts:
  scrape = st.button("Scrape job posts")
  if scrape:
    if st.session_state.posts_checkpoint == False:
      with st.spinner("Scraping job post", show_time=True):
        try:
          st.session_state.posts_scraped = job_post_scraper(job_title, number_posts)
          st.session_state.posts_checkpoint = True
          st.success("Done getting job posts!")
        except Exception as e:
          st.error(f"Scraper failed. Error: {e}")
    posts_scraped = st.session_state.posts_scraped
    # Cut the data for testing:
    #for key in posts_scraped:
    #  posts_scraped[key] = posts_scraped[key][:5]
    #if st.session_state.posts_processed == False:
    if True:
      embedded_positions = np.load("position_embeddings.npy")
      posts_scraped["Decision_makers"] = []
      progress_text = "Scraping employees and filtering decision makers."
      my_bar = st.progress(0.0, text=progress_text)
      l = len(posts_scraped["Company_LI_URL"])
      delta = (1/l)
      percent_complete = 0.0
      try:
        for i, company_url in enumerate(posts_scraped["Company_LI_URL"]):
          company_data = scrape_employees_from_companies(company_url)
          decision_makers = get_decision_makers(company_data[0], embedded_positions)
          dm_string = ""
          time.sleep(2)
          percent_complete += delta
          if percent_complete >1.0:
            percent_complete = 1.0
          progress_text = f"Scraped {i+1} decision makers"
          my_bar.progress(percent_complete, text=progress_text)
          for decision_maker in decision_makers:
            dm_string += f"({decision_maker["Name"]}, {decision_maker["Position"]}, {decision_maker["LinkedIn_URL"]}, {decision_maker["Email"]})"
          posts_scraped["Decision_makers"].append(dm_string)
          time.sleep(2)
      except Exception as e:
        st.error(f"Problem getting decision makers: {e}")
      st.success("Done getting decision makers!")
  
      st.session_state.posts_df = pd.DataFrame(posts_scraped)
      st.session_state.posts_processed = True


if st.session_state.posts_processed:
  st.session_state.posts_data = st.session_state.posts_df.to_csv(index = False).encode("utf-8")
  st.download_button(
        label="Download the output file",
        data=st.session_state.posts_data,
        file_name="Posts_data.csv",
        mime="text/csv",
    )
                     


