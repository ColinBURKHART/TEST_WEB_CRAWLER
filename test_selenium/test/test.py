import os

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.expected_conditions import presence_of_element_located, title_contains, title_is, \
    visibility_of_element_located, visibility_of, presence_of_all_elements_located, text_to_be_present_in_element_value, \
    text_to_be_present_in_element, frame_to_be_available_and_switch_to_it, invisibility_of_element_located, \
    staleness_of, element_to_be_clickable, element_to_be_selected, element_located_to_be_selected, \
    element_selection_state_to_be, element_located_selection_state_to_be, alert_is_present

## option
options = Options()
options.headless = True
options.add_argument("--window-size=1920,1200")
## selection du driver web
driver = webdriver.Chrome(os.environ.get('CHROME_DRIVER_PATH'))
## aller sur une page web
driver.get("https://www.nintendo.com/")
## localiser les informations avec un id
#els = driver.find_element_by_id('feature-slider-9a30010c-13d4-31a6-b104-21383cfd2c21')

# get first body
# in body get third span
# if span doesn't exist load other url
# if span exist, get 5th <p>
# return result


## localiser les informations avec un nom
lis = driver.find_element_by_name('description')
## changer de page web
driver.get("https://www.nintendo.com/switch/")
## changer de page web en fonction de l'historique des pages parcourue
driver.back()
driver.forward()
## COMMANDE DE recherche
## title_is
## title_contains
## presence_of_element_located
## visibility_of_element_located
## visibility_of
## presence_of_all_elements_located
## text_to_be_present_in_element
## text_to_be_present_in_element_value
## frame_to_be_available_and_switch_to_it
## invisibility_of_element_located
## element_to_be_clickable
## staleness_of
## element_to_be_selected
## element_located_to_be_selected
## element_selection_state_to_be
## element_located_selection_state_to_be
## alert_is_present

print(els)
print(lis)
driver.quit()
