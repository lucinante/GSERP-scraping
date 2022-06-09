# Data: 17 giugno 2021
# Oggetto: uno scraper di {num_results} URL dei risultati di Google
#           SERP tramite webdriver di selenium
#
# Suggerimenti:
#     -fare import di tutte le module
#     -adattare executable_path di chromedriver (ln:26)
#     -installare la versione corretta di chromedriver


from bs4 import BeautifulSoup
from selenium import webdriver
from urlpage_has_tokens import urlpage_has_tokens


#La funzione rivece parametri:
#   -str term: parola chiave da cercare
#   -int num_results: numero di risultati
#   -str lang: lingua dei risultati
#e restituisce:
#   -una lista contentente {num_results} URL che sono i
#    risultati della ricerca
def search(term, num_results=5, lang="it"):

    #funzione che restituisce la pagina di SERP di parametri passati
    def fetch_results(search_term, number_results, language_code):
        escaped_search_term = search_term.replace(' ', '+')

        #inviare HTTP req tramite il chromedriver, con le API di selenium
        google_url = "https://www.google.com/search?q={}&num={}&hl={}".format(
                escaped_search_term, number_results,
                language_code
            )
        options = webdriver.ChromeOptions()
        options.add_argument('--incognito')
        options.add_argument('--headless')

        driver = webdriver.Chrome(executable_path="C:\\Users\\xizh0\\Documents\\chromedriver.exe", options=options)
        driver.get(google_url)  #DO A TRY CATCH AND IN CASE OF AN EXCEPTION WRITE ERROR IN ERRORLOG.TXT

        return driver.page_source

    #funzione che analizza e astrae tutte le href di <a> del blocco <div class="g">
    # della pagina html passata come attributo.
    def parse_results(raw_html):
        soup = BeautifulSoup(raw_html, 'html.parser')
        result_block = soup.find_all('div', attrs={'class': 'g'})

        for result in result_block:
            link = result.find('a', href=True)
            title = result.find('h3')
            #controllare se href è effettivamente di un risultato di ricerca
            if link and title:
                yield link['href']

    html = fetch_results(term, num_results, lang)
    return list(parse_results(html))


def search_news(term, azienda, num_results=6, lang="en"):

    def fetch_results(search_term, number_results, language_code):
        escaped_search_term = search_term.replace(' ', '+')

        google_url = "https://www.google.com/search?q={}&num={}&hl={}&tbm=nws".format(
            escaped_search_term, number_results,
            language_code
        )

        options = webdriver.ChromeOptions()
        options.add_argument('--incognito')
        options.add_argument('--headless')
        driver = webdriver.Chrome(executable_path="C:\\Users\\xizh0\\Documents\\chromedriver.exe", options=options)
        driver.get(google_url)  # DO A TRY CATCH AND IN CASE OF AN EXCEPTION WRITE ERROR IN ERRORLOG.TXT

        #per accettare cookie policy di ...news.google.com... ||...google.com/search=?tbm=nws...
        driver.find_element_by_xpath("/html/body/c-wiz/div/div/div/div[2]/div[1]/div[4]/form/div[1]/div/button").click()

        return driver.page_source

    def parse_results(raw_html):
        soup = BeautifulSoup(raw_html, 'html.parser')
        result_block = soup.find_all('div', attrs={'id': 'search'})

        for result in result_block:
            link = result.find('a', href=True)
            #verificare se i link di news siano coerenti o meno
            if link and urlpage_has_tokens(link['href'],keywords=[azienda]):
                yield link['href']

    html = fetch_results(term, num_results, lang)
    return list(parse_results(html))
