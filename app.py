import streamlit as st
import requests
import pandas as pd
from datetime import datetime

# -------------------------
# PAGE CONFIG
# -------------------------
st.set_page_config(
    page_title="Advanced News Dashboard",
    page_icon="📰",
    layout="wide"
)

# -------------------------
# API CONFIG
# -------------------------
API_KEY = st.secrets.get("NEWS_API_KEY", "YOUR_API_KEY")
BASE_URL = "https://newsapi.org/v2/top-headlines"

# -------------------------
# SIDEBAR
# -------------------------
st.sidebar.title("News Filters")

country_options = {
    "United States": "us",
    "India": "in",
    "United Kingdom": "gb",
    "Australia": "au",
    "Canada": "ca",
    "Germany": "de",
    "France": "fr",
    "Japan": "jp"
}

category_options = [
    "general",
    "business",
    "entertainment",
    "health",
    "science",
    "sports",
    "technology"
]

selected_country = st.sidebar.selectbox(
    "Select Country",
    list(country_options.keys())
)

selected_category = st.sidebar.selectbox(
    "Select Category",
    category_options
)

keyword = st.sidebar.text_input(
    "Search Keyword",
    placeholder="AI, Tesla, Cricket..."
)

article_count = st.sidebar.slider(
    "Number of Articles",
    min_value=5,
    max_value=100,
    value=20
)

# -------------------------
# HEADER
# -------------------------
st.title("📰 Advanced News Dashboard")
st.markdown("Browse and search the latest headlines from around the world.")

# -------------------------
# FETCH DATA
# -------------------------
@st.cache_data(ttl=300)
def fetch_news(country, category, page_size):
    params = {
        "apiKey": API_KEY,
        "country": country,
        "category": category,
        "pageSize": page_size
    }

    response = requests.get(BASE_URL, params=params)

    if response.status_code == 200:
        return response.json()

    return None


# -------------------------
# GET NEWS
# -------------------------
with st.spinner("Fetching latest news..."):
    data = fetch_news(
        country_options[selected_country],
        selected_category,
        article_count
    )

# -------------------------
# PROCESS ARTICLES
# -------------------------
if data and data.get("articles"):

    articles = data["articles"]

    if keyword:
        articles = [
            article for article in articles
            if keyword.lower() in (
                (article.get("title") or "") +
                (article.get("description") or "")
            ).lower()
        ]

    st.success(f"Found {len(articles)} articles")

    # Create DataFrame
    table_data = []

    for article in articles:
        table_data.append({
            "Title": article.get("title"),
            "Source": article.get("source", {}).get("name"),
            "Published": article.get("publishedAt")
        })

    if table_data:
        df = pd.DataFrame(table_data)
        st.dataframe(df, use_container_width=True)

    st.divider()

    # Display Articles
    for article in articles:

        title = article.get("title", "No Title")
        source = article.get("source", {}).get("name", "Unknown")
        description = article.get("description", "")
        image_url = article.get("urlToImage")
        article_url = article.get("url")
        published = article.get("publishedAt")

        with st.container():

            col1, col2 = st.columns([1, 3])

            with col1:
                if image_url:
                    st.image(image_url, use_container_width=True)

            with col2:
                st.subheader(title)

                st.caption(
                    f"Source: {source} | Published: {published}"
                )

                if description:
                    st.write(description)

                if article_url:
                    st.link_button(
                        "Read Full Article",
                        article_url
                    )

            st.divider()

else:
    st.warning("No news articles found.")