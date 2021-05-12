import re

import requests
from bs4 import BeautifulSoup


def get_ipa(soup):
    ipas = []
    for ipa in soup.find_all("span", class_="pron"):
        ipas.append(ipa.string)
    return ipas


def get_definitions(soup):
    soup = soup.find("section", attrs={"data-src": "pons"}).extract()
    for div_cprh in soup.find_all("div", class_="cprh"):
        div_cprh.decompose()
    for item in soup.find_all(["b", "br"]):
        item.unwrap()
    for item in soup.find_all("span", class_="illustration"):
        item.decompose()
    soup = soup.find_all("div")
    return soup


def check_word(word):
    URL = "https://de.thefreedictionary.com/" + word
    page = requests.get(URL)
    soup = BeautifulSoup(page.content, "html.parser")

    for ipa in get_ipa(soup):
        print("IPA:", ipa)
    for defintion in get_definitions(soup):
        print(defintion)
        print("***")
    definitions = get_definitions(soup)
    for definition in definitions:
        print(re.sub(r", , .*", "", definition.get_text(), flags=re.DOTALL).strip())


check_word("hund")
