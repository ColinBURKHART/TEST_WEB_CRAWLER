
from bs4 import BeautifulSoup as bs
from selenium import webdriver
import time
import lxml
import os
from selenium.webdriver.chrome.options import Options


# element cherché
search_value = '57-27-2'
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
   print('ERROR')
   exit()

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

def get_name(soup):
    ret = ''
    get_NAME = soup.find('h1')
    if get_NAME is not None:
        ret = get_NAME.text
    return ret

def get_CAS(soup):
    ret = ''
    value_CAS = soup.find('section', {'id': 'CAS'})
    if value_CAS is not None:
        get_CAS = value_CAS.find('div', {'class': 'section-content-item'})
        value_cas = get_CAS.find('p')
        ret = value_cas.text
    return ret

def get_Molecular_weight(soup):
    ret= ''
    value_mol = soup.findAll('div', {'class': 'overflow-x-auto border'})
    if value_mol is not None:
        get_molecularw = value_mol[1].find('tbody')
        get_molecular = get_molecularw.findAll('td')
        ret = get_molecular[1].text
    return ret

def get_image_structure(soup):
    ret = ''
    value_struc = soup.find('section', {'id': '2D-Structure'})
    if value_struc is not None:
        get_struc = value_struc.find('div', {'class': 'relative structure-img-container'})
        get_struct = get_struc.find('img')
        get_structure = get_struct.get('src')
        ret = get_structure
    return ret

def get_synonyms(soup):
    ret = ''
    value_Syn = soup.find('section', {'id': 'DEA-Controlled-Substances'})
    if value_Syn is not None:
        get_syn = value_Syn.find('div', {'class': 'section-content-item'})
        get_synonyms = get_syn.findAll('td')
        ret = get_synonyms[1].text
    return ret

def get_flash_point(soup):
    ret = ''
    value_FP = soup.find('section', {'id': 'Flash-Point'})
    if value_FP is not None:
        FP_allp = value_FP.findAll('p')
        for p in FP_allp:
            if '°C' in p.text:
                ret = p.text.split(' ')[0]
    return ret

def get_density(soup):
    ret = ''
    value_D = soup.find('section', {'id': 'Density'})
    if value_D is not None:
        D_allp = value_D.findAll('p')
        for p in D_allp:
            if '°C' in p.text:
                ret = p.text.split(' ')[0]
    return ret

def get_boiling_point(soup):
    ret = ''
    value_BP = soup.find('section', {'id': 'Boiling-Point'})
    if value_BP is not None:
        BP_allp = value_BP.findAll('p')
        for p in BP_allp:
            if '°C' in p.text:
                ret = p.text.split(' ')[0]
    return ret

def get_melting_point(soup):
    ret = ''
    value_MP = soup.find('section', {'id': 'Melting-Point'})
    if value_MP is not None:
        MP_allp = value_MP.findAll('p')
        for p in MP_allp:
            if '°C' in p.text:
                ret = p.text.split(' ')[0]
    return ret

def get_fusion_point(soup):
    ret = ''
    value_FP = soup.find('section', {'id': 'Other-Experiment-Properties'})
    if value_FP is not None:
        FP_allp = value_FP.findAll('p')
        for p in FP_allp:
            if 'Heat of fusion' in p.text:
                ret = p.text.split(' ')[0]
    return ret

def get_properties(soup):
    ret = 'Density= ' + get_density(soup)  + ', Boiling Point= ' + get_boiling_point(soup) + ', Melting Point= ' + get_melting_point(soup) + ', Fusion Point= ' + get_fusion_point(soup)
    return ret

print('Name= ' + get_name(soup))
print('CAS= ' + get_CAS(soup))
print('Molecular Formula= ' + get_value[0].text)
print('MolarMass= ' + get_Molecular_weight(soup))
print('Structure= ' + get_image_structure(soup))
print('Synonyms= ' + get_synonyms(soup))
print('Flash Point= ' + get_flash_point(soup))
print('Properties: ' + get_properties(soup))

