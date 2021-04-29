from bs4 import BeautifulSoup as bs
from selenium import webdriver
import time
import lxml
import os
from selenium.webdriver.chrome.options import Options


# element cherché
search_value = 'InChI=1S/C3H6O/c1-3(2)4/h1-2H3'
chrome_options = Options()
chrome_options.add_argument("--headless")
driver = webdriver.Chrome(os.environ.get('CHROME_DRIVER_PATH'), options=chrome_options)
#driver = webdriver.Firefox()
driver.get('https://pubchem.ncbi.nlm.nih.gov/#query=' + search_value)

retry = 100
delay = 1

n = 1

while n < retry:
     html = driver.page_source
     soup = bs(html, 'lxml')
     number_of_value = soup.find('div', {'class': 'f-medium p-md-right'})
     if number_of_value is not None:
        number_of_value = number_of_value.text
#       print(number_of_value)
        break
     else:
        n += 1
     time.sleep(delay)

if number_of_value == '1 result':
    research_value = soup.find('div', {'class': 'f-medium p-sm-top p-sm-bottom f-1125'})
    url_compound = research_value.find('a')
    next_url = url_compound.get('href')
#   print(next_url)
else:
   print('not lucky today')

driver.get(next_url)

retry = 100
delay = 1

n = 1

while n < retry:
     html = driver.page_source
     soup = bs(html, 'lxml')
     value_Molecula = soup.find('section', {'id': 'Molecular-Formula'})
     if value_Molecula is not None:
        get_value = value_Molecula.findAll('p')
        break
     else:
        n += 1
     time.sleep(delay)

get_NAME = soup.find('h1')

print('Name= ' +get_NAME.text)
print('CAS= ' +get_CAS.text)
print('Molecular Formula= '+get_value[0].text + ', ' +get_value[1].text + ', ' + get_value[2].text + ', ' + get_value[3].text)
