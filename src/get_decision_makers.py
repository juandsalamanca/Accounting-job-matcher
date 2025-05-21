from openai import AzureOpenAI
from sklearn.metrics import mean_squared_error
from src.get_emails_from_linkedin import get_emails_from_linkedin
import streamlit as st

def get_embedding(text):
  openai_client = AzureOpenAI(api_key=st.secrets["openai_key"],  api_version="2024-02-01", azure_endpoint = st.secrets["openai_endpoint"])
  response = openai_client.embeddings.create(
      input = text,
      model= "text-embedding-3-large"
  )
  return response.dict()['data'][0]['embedding']
  
def get_decision_makers(company_data, embedded_positions):
  positions = ["CEO", "CFO", "COO", "Chief Officer", "President", "VP", "Director", "Board Member", "Chairman", "Principal", "Executive"]
  decision_makers = []
  if "employees" in company_data:
    for employee in company_data["employees"]:
      empl_name = employee["employee_name"]
      empl_position = employee["employee_position"]
      empl_url = employee["employee_profile_url"]
      position_embedding = get_embedding(empl_position)
      switch = 0
      st.write(empl_position)
      for i, embedding in enumerate(embedded_positions):
        mse = mean_squared_error(embedding, position_embedding)
        if mse < 3.8e-4:
          switch = 1
          st.write(f"Match with {positions[i]}")
      if switch == 1:
        email = get_emails_from_linkedin(empl_url)
        decision_makers.append({"Name":empl_name, "Position":empl_position, "LinkedIn_URL":empl_url, "Email":email})
        
  return decision_makers


