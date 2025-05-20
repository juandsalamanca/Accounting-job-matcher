import requests
import streamlit as st

def get_emails_from_linkedin(linkedinUrl):
  url = "https://api.apollo.io/v1/people/match"

  data = {
      "first_name": firstName,
      "last_name": lastName,
      "organization_name": companyName,
      "linkedin_url": linkedinUrl,
      "reveal_personal_emails": True,
      # "webhook_url": "https://your_webhook_site"
  }

  headers = {
      'Cache-Control': 'no-cache',
      'Content-Type': 'application/json',
      'X-Api-Key': st.secrets["apollo_key"]
  }

  response = requests.request("POST", url, headers=headers, json=data)


  re=response.json()


  return re["person"]["email"],re["person"]["email_status"]
