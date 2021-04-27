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
delay = 10

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
delay = 10

n = 1

while n < retry:
     html = driver.page_source
     soup = bs(html, 'lxml')
     value_SMILES = soup.find('section', {'id': 'Canonical-SMILES'})
     if value_SMILES is not None:
        get_value = value_SMILES.find('div', {'class': 'section-content-item'})
        value_Canonical = get_value.find('p')
#       print(value_Canonical.text)
        break
     else:
        n += 1
     time.sleep(delay)

get_NAME = soup.find('h1')

value_Name = soup.find('section', {'id': 'IUPAC-Name'})
get_value1 = value_Name.find('div', {'class': 'section-content-item'})
value_IUPAC= get_value1.find('p')

value_InCh = soup.find('section', {'id': 'InChI'})
get_value2 = value_InCh.find('div', {'class': 'section-content-item'})
value_InChI = get_value2.find('p')

value_Inchik = soup.find('section', {'id': 'InChI-Key'})
get_value3 = value_Inchik.find('div', {'class': 'section-content-item'})
value_InChIK = get_value3.find('p')

value_Molecula = soup.find('section', {'id': 'Molecular-Formula'})
get_value4 = value_Molecula.findAll('p')


print('Name= ' +get_NAME.text)
print('IUPAC Name= '+value_IUPAC.text)
print('InChl Name= '+value_InChI.text)
print('InChl Key Name= '+value_InChIK.text)
print('Canonical SMILES= '+value_Canonical.text)
print('Molecular Formula= '+get_value4[0].text + ', ' +get_value4[1].text + ', ' + get_value4[2].text + ', ' + get_value4[3].text)
