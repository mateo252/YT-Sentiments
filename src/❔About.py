import streamlit as st


st.set_page_config(
    page_title = "YT-Sentiments",
    page_icon = "❔"
)

with st.sidebar:
    st.write("")

st.title("YT-Sentiments ❔")
st.subheader("How does it work? 🤔", divider="blue")

markdown_text = """
The goal of this project was to create a site that pulls sentiment information and other statistics from the comments section of videos on YT.
The best results are available for the English language.

On the site you can see two pages:
- **About** ❔ - this is the current page, which shows instructions on how to use the various elements of the page,
- **Movie** 🎬 - this is the main page, which contains two elements:
    - YT-API Key - text field that accepts the youtube api key, which can be obtained from Google Cloud
    - Search bar - text field accepting a link to a video from youtube, but the most important thing is that the link **IS NOT** a sharing link and **DOES NOT HAVE** a timestamp, just a link of the video

**YT-API key is required to get results !!!**
"""

st.markdown(markdown_text)
