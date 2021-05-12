
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
search_value = '67-64-1'
chrome_options = Options()
chrome_options.add_argument("--headless")
driver = webdriver.Chrome(os.environ.get('CHROME_DRIVER_PATH'), options=chrome_options)
driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")

driver.execute_cdp_cmd('Network.setUserAgentOverride', {"userAgent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.53 Safari/537.36'})
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
    value_Syns = soup.find('section', {'id': 'MeSH-Entry-Terms'})
    if value_Syns is not None:
        get_syn = value_Syns.find('div', {'class': 'section-content-item'})
        for p in get_syn:
            ret += p.text + '; '
    else :
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
                    getallGHS_HTML_td = value_GHS.findAll('td')
                    ret = getallGHS_HTML_td
                    break
                else:
                    n += 1
                time.sleep(delay)
    return ret

hazards_GHS_HTML_td = get_GHS_hazards_HTML(soup, driver, bs)

def get_hazards_GHS(soup):
    ret = ''
    retH = ''
    retHS = ''
    retGHS = ''
    retP = ''
    retPS = ''
    retL = []
    if hazards_GHS_HTML_td is not None:
        for td in hazards_GHS_HTML_td:
            GHS_HTML_allp = td.findAll('p')
            for p in GHS_HTML_allp:
                if 'H' in p.text and 'E' not in p.text and 'P' not in p.text:
                    retH += p.text[0:4] + ' '
                    retL = retH.split()
                    retL = list(dict.fromkeys(retL))
                    retGHS = (' '.join(retL))
                    retHS = 'GHS Hazard Statement: ' + retGHS
            for p in GHS_HTML_allp:
                if 'P' in p.text and '(' not in p.text:
                    retP += p.text + ' '
                    retL = retP.split()
                    retL = list(dict.fromkeys(retL))
                    retPSC = (' '.join(retL))
                    retPS = 'Precautionary Statement Codes: ' + retPSC
        ret = retHS + retPS
        return ret
    else:
       value_GHS = soup.find('section', {'id': 'GHS-Classification'})
       GHS_alltd = value_GHS.findAll('td')
       for td in GHS_alltd:
           GHS_allp = td.findAll('p')
           for p in GHS_allp:
                if 'H' in p.text and 'P' not in p.text and 'E' not in p.text:
                    retH += p.text[0:4] + ' '
                    retHS = 'GHS Hazard Statement: ' + retH
           for p in GHS_allp:
               if 'P' in p.text and '(' not in p.text:
                   retP = ' Precautionary Statement: ' + p.text
       ret = retHS + retP
    return ret

driver.quit()
driver = webdriver.Chrome(os.environ.get('CHROME_DRIVER_PATH'), options=chrome_options)

def get_Classes_hazards_HTML(soup, driver, bs):
    ret = None
    value_CLA_FP = soup.find('section', {'id': 'Hazard-Classes-and-Categories'})
    if value_CLA_FP is not None:
        research_CLA_HTML = value_CLA_FP.find('a', {'class': 'button has-icon-right with-padding-small lh-1'})
        if research_CLA_HTML is not None:
            HTML_PAGE = soup.find('meta', {'property': 'og:url'})
            HTML_ACTUAL_URL = HTML_PAGE.get('content')
            take_HTML_CLA_URL = research_CLA_HTML.get('href')
            driver.get(HTML_ACTUAL_URL + take_HTML_CLA_URL)
            retry = 20
            delay = 1
            n = 1
            while n < retry:
                html = driver.page_source
                #print(html)
                soup_CLA_HTML = bs(html, 'lxml')
                #print(soup_CLA_HTML)
                value_CLA = soup_CLA_HTML.find('section', {'id': 'Hazard-Classes-and-Categories'})
                #print(value_CLA)
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
    retL = []
    rethC = ''
    if hazards_Classes_HTML_p is not None:
        for p in hazards_Classes_HTML_p:
            rethC += p.text
            retL = rethC.split()
            retL = list(dict.fromkeys(retL))
            retPSC = (' '.join(retL))
            ret += p.text + ' '
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
    ret = get_hazards_GHS(soup) + ' Hazard Classes and Categories: ' + get_hazards_Classes(soup) + ' NFPA Hazard Classification: ' + get_hazards_NFPA(soup)
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