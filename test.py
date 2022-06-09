from selenium import webdriver
from bs4 import BeautifulSoup as bs
import time
7
options = webdriver.ChromeOptions()

driver = webdriver.Chrome(executable_path="C:\\Users\\xizh0\\Documents\\chromedriver.exe", options=options)
driver.get("https://www.google.com/search?q=covid&num=3&hl=it&tbm=nws")  # DO A TRY CATCH AND IN CASE OF AN EXCEPTION WRITE ERROR IN ERRORLOG.TXT
btnAccept=driver.find_element_by_xpath("/html/body/c-wiz/div/div/div/div[2]/div[1]/div[4]/form/div[1]/div/button")
btnAccept.click()

bs_articles=bs(driver.page_source,"html.parser")
result_block=bs_articles.find_all("div",attrs={"id":"search"})
for result in result_block:
    link = result.find('a', href=True)
    print(link['href'])
