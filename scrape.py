#imports
import selenium.webdriver as webdriver
from selenium.webdriver.chrome.service import Service
from bs4 import BeautifulSoup

#max length of characters to feed to llm
max_chars = 8000

#scrape website
def scrape_page(website):
    print("Launching Browser...") #using chrome for this

    chrome_path = "./chromedriver.exe"  #using the driver i copied into the local directory
    options = webdriver.ChromeOptions()
    driver = webdriver.Chrome(service=Service(chrome_path), options = options)

    try:
        driver.get(website)
        print("Webpage loaded successfully!")
        html = driver.page_source
        return html

    finally:
        driver.quit()

#clean the soup
def clear_soup(html_content):
    init_soup = BeautifulSoup(html_content, 'html.parser')
    get_body = init_soup.body
    if get_body is None:
        return "" #Empty message
    else:
        messy_soup = BeautifulSoup(str(get_body), 'html.parser')
        #remove styles & scripts
        for script_or_style in messy_soup(["script", "style"]):
            script_or_style.extract()
        
        cleaned_soup = messy_soup.get_text(separator="\n")
        cleaned_soup = "\n".join(line.strip() for line in cleaned_soup.splitlines() if line.strip())
        return cleaned_soup
    

def split_dom_content(dom_content, max_length = max_chars):
    # plit content into chunks of max_length
    chunks = [
            dom_content[i:i+max_length]
            for i in range(0, len(dom_content), max_length)]
    return chunks