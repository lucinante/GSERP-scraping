# Data: 11 giugno 2021
# Oggetto: creazione di una funzione che è ingrado di determinare
#       se una pagina html contenga alcune parole chiavi o meno,
#       tramite una ricerca delle parole chiavi

try:
    from selenium import webdriver
    from bs4 import BeautifulSoup as bs
    import requests
    import cloudscraper
except ImportError:
    print("Requested modules not installed")

# str url, list[str] keywords
def urlpage_has_tokens(url, keywords=[]):
    qty_keywords=len(keywords)


    # Usare metodo di webdriver per scraping
    # setup di opzioni
    options = webdriver.ChromeOptions()
    options.add_argument('--incognito')
    options.add_argument('--headless')
    # accesso alla url con chromedriver
    driver = webdriver.Chrome(executable_path="C:\\Users\\xizh0\\Documents\\chromedriver.exe", options=options)
    driver.get(url)
    soup = bs(driver.page_source, "html.parser")

    paragraphs = soup.find_all(
        ['p', 'p1', 'p2', 'p3', 'p4', 'p5', 'p6', 'h', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'span'])

    found=0
    #iterare i paragrafi e cercare se contiene parole chiavi
    for paragraph in paragraphs:
        for keyword in keywords:
            if keyword.lower() in paragraph.text.lower():
                found+=1
                keywords.remove(keyword)

    print("kywrd: "+str(qty_keywords))
    print("found: "+str(found))

    if found == qty_keywords:
        return True
    else:
        return False

#Test
#print(urlpage_has_tokens(
#                "https://www.abakode.com/it/",
#                keywords=["accompagniamo"]
#                )
#     )

