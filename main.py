#imports
import streamlit as st
import time
from scrape import scrape_page, clear_soup, split_dom_content
from parse import parse_with_ollama
import pandas as pd

#title
st.title('webask')

#input url
url = st.text_input("Please enter the url: ")

if st.button("Scrape!"):
    st.write("Scraping...")

    soup_input = scrape_page(url)
    clean_soup = clear_soup(soup_input)
    st.write("Done!\n")
    st.session_state.dom_content = clean_soup

    with st.expander("View DOM Content..."):
        st.text_area("DOM Content", clean_soup, height=300)

if "dom_content" in st.session_state:
    parse_description = st.text_area("Describe what you want to parse")

    if st.button("Parse Content"):
        if parse_description:
            st.write("Parsing...")

            dom_chunks = split_dom_content(st.session_state.dom_content)
            result = parse_with_ollama(dom_chunks, parse_description)
            st.write(result)
            print(result) #for testing purposes
            st.session_state.parse_result = result

if "parse_result" in st.session_state:
    parse_export = st.text("Would you like to export this content?")
    if st.button("CSV File"):
        if parse_export:
            st.write("Exporting...")
            df = pd.DataFrame(result)
            output_csv_data = df.to_csv('output.csv', index=True)
            st.write("Exported to csv")