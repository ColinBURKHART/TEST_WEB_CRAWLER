import os
import urllib
import time
from urllib import request
from bs4 import BeautifulSoup
import lxml

search_value = 'C1=CC=C(C=C1)C=O'
page = urllib.request.urlopen('https://pubchem.ncbi.nlm.nih.gov/#query='+ search_value)
time.sleep(10)
code_page = BeautifulSoup(page, "lxml")
#print(code_page.body)
number_of_value = code_page.find('body')
print(number_of_value)
file = open("osef.html","w",newline='\n',encoding='utf8')
file.write(str(number_of_value))
file.close()

exit()

max_retries = 10
retry_delay = 60

n = 1
ready = 0
while n < max_retries:
     number_of_value = code_page.findAll("div", {"class": "main-width"})
     if number_of_value is not None:
        ready = 1
        break
     else:
        print("Website not available...")
        n += 1
time.sleep(retry_delay)

if ready != 1:
  print("nope")
else:
  print(number_of_value)

  # JAVASCRIPT.