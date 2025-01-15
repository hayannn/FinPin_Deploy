import requests
import os
import streamlit as st

load_dotenv()

NAVER_CLIENT_ID = st.secrets["NAVER_CLIENT_ID"]
NAVER_CLIENT_SECRET = st.secrets["NAVER_CLIENT_SECRET"]

print(f"Client ID: {NAVER_CLIENT_ID}")
print(f"Client Secret: {NAVER_CLIENT_SECRET}")


def fetch_naver_news(query, display=100):
    url = "https://openapi.naver.com/v1/search/news.json"
    headers = {
        "X-Naver-Client-Id": NAVER_CLIENT_ID,
        "X-Naver-Client-Secret": NAVER_CLIENT_SECRET
    }
    params = {
        "query": query,
        "display": display,
        "sort": "sim"
    }
    response = requests.get(url, headers=headers, params=params)
    if response.status_code == 200:
        return response.json()["items"]
    else:
        raise Exception(f"Error {response.status_code}: {response.text}")
