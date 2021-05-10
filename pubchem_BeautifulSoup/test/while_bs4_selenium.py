
from bs4 import BeautifulSoup as bs
from selenium import webdriver
import time
import lxml
import os
from selenium.webdriver.chrome.options import Options
from datetime import datetime

Time = datetime.now()

# element cherché
# multiple Hazards 67-64-1
# one hazards 57-27-2
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



def get_GHS_hazards_HTML(soup, driver, bs):
    ret = None
    value_GHS = soup.find('section', {'id': 'GHS-Classification'})
    if value_GHS is not None:
        research_GHS_HTML = value_GHS.find('a', {'class': 'button has-icon-right with-padding-small lh-1'})
        if research_GHS_HTML is not None:
            HTML_PAGE = soup.find('meta', {'property': 'og:url'})
            HTML_ACTUAL = HTML_PAGE.get('content')
            take_HTML_GHS = research_GHS_HTML.get('href')
            driver.get(HTML_ACTUAL + take_HTML_GHS)
            retry = 100
            delay = 1
            n = 1
            while n < retry:
                html = driver.page_source
                soup_GHS_HTML = bs(html, 'lxml')
                value_GHS = soup_GHS_HTML.find('section', {'id': 'GHS-Classification'})
                if value_GHS is not None:
                    getallGHS_HTML_tr = value_GHS.findAll('tr')
                    ret = getallGHS_HTML_tr
                    break
                else:
                    n += 1
                time.sleep(delay)
    return ret

hazards_GHS_HTML_tr = get_GHS_hazards_HTML(soup, driver, bs)

def get_hazards_GHS(soup):
    ret = ''
    if hazards_GHS_HTML_tr is not None:
        for tr in hazards_GHS_HTML_tr:
            if 'GHS Hazard Statements' in tr.text:
                ret += tr.text + ' '
    else:
       value_GHS = soup.find('section', {'id': 'GHS-Classification'})
       GHS_alltr = value_GHS.findAll('tr')
       for tr in GHS_alltr:
          if 'GHS Hazard Statements' in tr.text:
                ret += tr.text + ' '
    return ret

def get_Classes_hazards_HTML(soup, driver, bs):
    ret = None
    value_CLA = soup.find('section', {'id': 'Hazard-Classes-and-Categories'})
    if value_CLA is not None:
        research_CLA_HTML = value_CLA.find('a', {'class': 'button has-icon-right with-padding-small lh-1'})
        if research_CLA_HTML is not None:
            HTML_PAGE = soup.find('meta', {'property': 'og:url'})
            HTML_ACTUAL = HTML_PAGE.get('content')
            take_HTML_CLA = research_CLA_HTML.get('href')
            driver.get(HTML_ACTUAL + take_HTML_CLA)
            retry = 100
            delay = 1
            n = 1
            while n < retry:
                html = driver.page_source
                soup_CLA_HTML = bs(html, 'lxml')
                value_CLA = soup_CLA_HTML.find('section', {'id': 'Hazard-Classes-and-Categories'})
                if value_CLA is not None:
                    getallCLA_HTML_p = value_CLA.findAll('p')
                    ret = getallCLA_HTML_p
                    break
                else:
                    n += 1
                time.sleep(delay)
    return ret

hazards_Classes_HTML_p = get_Classes_hazards_HTML(soup, driver, bs)

def get_hazards_Classes(soup):
    ret = ''
    if hazards_Classes_HTML_p is not None:
            ret += hazards_Classes_HTML_p + ' '
    else:
       value_CLA = soup.find('section', {'id': 'Hazard-Classes-and-Categories'})
       CLA_allp = value_CLA.findAll('p')
       for p in CLA_allp:
            ret += p.text + ' '
    return ret


def get_hazards_NFPA(soup):
    ret = ''
    ret1 = ''
    ret2 = ''
    ret3 = ''
    value_NFPA = soup.find('section', {'id': 'NFPA-Hazard-Classification'})
    if value_NFPA is not None:
        NFPA_alltr = value_NFPA.findAll('tr')
        for th in NFPA_alltr:
            if 'NFPA Health Rating' in th.text:
                ret1 += th.text + ' '
                for th in NFPA_alltr:
                     if 'NFPA Fire Rating' in th.text:
                         ret2 += th.text + ' '
                         for th in NFPA_alltr:
                            if 'NFPA Instability Rating' in th.text:
                                 ret3 += th.text + ' '
                                 ret = ret1 + ret2 + ret3
    return ret


def get_hazards(soup):
    ret = 'GHS Hazard Statements: ' + get_hazards_GHS(soup) + 'Hazard Classes and Categories: ' + get_hazards_Classes(soup) + ' NFPA Hazard Classification: ' + get_hazards_NFPA(soup)
    return ret


print('Name= ' + get_name(soup))
print('CAS= ' + get_CAS(soup))
print('Molecular Formula= ' + get_value[0].text)
print('MolarMass= ' + get_Molecular_weight(soup))
print('Structure= ' + get_image_structure(soup))
print('Synonyms= ' + get_synonyms(soup))
print('Flash Point= ' + get_flash_point(soup))
print('Properties: ' + get_properties(soup))
print('Hazards= ' + get_hazards(soup))
print(datetime.now() - Time)