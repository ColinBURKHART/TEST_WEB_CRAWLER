from bs4 import BeautifulSoup as bs
from selenium import webdriver
import time
import lxml
import os

search_value = 'C1=CC=C(C=C1)C=O'
driver = webdriver.Chrome(os.environ.get('CHROME_DRIVER_PATH'))
driver.get('https://pubchem.ncbi.nlm.nih.gov/#query=' + search_value)
time.sleep(10)
html = driver.page_source
soup = bs(html, 'lxml')
number_of_value = soup.find('div', {'class': 'f-medium p-md-right'})
number_of_value = number_of_value.text
print(number_of_value)
if number_of_value == '1 result':
    research_value = soup.find('div', {'class': 'f-medium p-sm-top p-sm-bottom f-1125'})
    print(research_value)
    url_compound = research_value.find('a')
    print(url_compound)
    next_url = url_compound.get('href')
    print(next_url)
else:
    print('STOP')
driver.get(next_url)
time.sleep(10)
html = driver.page_source
soup = bs(html, 'lxml')
value_SMILES = soup.find('section', {'id': 'Canonical-SMILES'})
get_value = value_SMILES.find('div', {'class': 'section-content-item'})
value = get_value.find('p')
print(value.text)