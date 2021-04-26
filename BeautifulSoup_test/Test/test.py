import json

import bs4
from bs4 import BeautifulSoup
import urllib.request
import html5lib
import html.parser

sauce = urllib.request.urlopen('https://www.nintendo.com')
# analyseur du site
# utilise un parser auto :
#soup = bs4.BeautifulSoup(sauce)

# parser définis
soup = BeautifulSoup(sauce, "html5lib")
#soup = BeautifulSoup(sauce, "html.parser")
#soup = BeautifulSoup(sauce, "lxml")

# différent print pour tester

# récupération toute la page
print(soup)

# récupération titre
#print(soup.title.string)

# récupération nom classe a
#print(soup.a['class'])

# récupération de toute les infos de a
print(soup.a.attrs)
print(soup.a.String)

# récupère tout les a (.text permet de récupérer juste le text)
for sub_a in soup.find_all('a'):
    print(sub_a)

# récupère le premier a
# print(soup.p.a)
