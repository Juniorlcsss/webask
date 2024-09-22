#imports
import streamlit as st
import time
from scrape import scrape_page, clear_soup, split_dom_content
from parse import parse_with_ollama

#title
st.title('webask')

#input url
url = st.text_input("Please enter the url: ")

#scrape button
if st.button("Scrape!"):
    st.write("Scraping...")

    soup_input = scrape_page(url)
    clean_soup = clear_soup(soup_input)

    #error checking
    if clean_soup != "":
        st.write("Done!\n")
        st.session_state.dom_content = clean_soup

        #DOM content
        with st.expander("View DOM Content..."):
            st.text_area("DOM Content", clean_soup, height=300)

    else:
        st.error("Failed to scrape the page.")  #error message comes up, able to reenter url :)

#parse button
if "dom_content" in st.session_state:
    parse_description = st.text_area("Describe what you want to parse")
    if st.button("Parse Content"):
        if parse_description:
            st.write("Parsing...")

            dom_chunks = split_dom_content(st.session_state.dom_content)
            result = parse_with_ollama(dom_chunks, parse_description)
            st.write(result)

            #download the string
            st.download_button("Download text: ", str(result))

            st.session_state.result = result
