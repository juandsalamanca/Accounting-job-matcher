import streamlit as st
import json

st.header("Accounting-Job-Matcher")

st.text("Use the cookie editor chrome extension to export your sales navigator cookies as JSON")
cookie_input = st.text_area("Paste here your Sales Navigator cookie", height=300)
cookie_input = cookie_input.replace("true", "True").replace("false", "False").replace("null", "None")
cookies = json.loads(cookie_input)
list_url = st.text_area("Paste here your Sales Navigator Lead list URL", height=300)
