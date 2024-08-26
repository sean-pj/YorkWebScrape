from urllib.request import urlopen
from bs4 import BeautifulSoup
import json

#https://realpython.com/python-web-scraping-practical-introduction/
#https://stackoverflow.com/questions/19773669/python-dictionary-replace-values
#https://www.geeksforgeeks.org/python-convert-a-list-to-dictionary/
def convert(lst):
   res_dict = {}
   for i in range(0, len(lst), 2):
       res_dict[lst[i].get_text().strip()] = lst[i + 1].get_text().strip()
   return res_dict

url = "https://www.yorku.ca/foodservices/dining-directory/"
page = urlopen(url)
html = page.read().decode("utf-8")
soup = BeautifulSoup(html, "html.parser")
# card_htmls = soup.find_all(attrs={'class':'card-deck'}).find_all(attrs={'class':'card border-0 mb-5'})
card_htmls = soup.find_all(attrs={'class':'card border-0 mb-5'})
# print(card_htmls)
# print(card_htmls.find_all("i"))
data = {}
for card_html in card_htmls:
    if card_html.find("h2") is not None:
        location_name = card_html.find("h2").text
    else:
        location_name = "No name"
    if card_html.find("a") is not None:
        location_link = card_html.find("a").get("href")
    if card_html.find("i", attrs={"alt": "location:"}) is not None:
        location = card_html.find("i", attrs={"alt": "location:"}).find_next().text.strip()
    if card_html.find("i", attrs={"alt": "menu offering:"}) is not None:
        menu_offering = card_html.find("i", attrs={"alt": "menu offering:"}).find_next().text.strip()
    if card_html.find("i", attrs={"alt": "payment options:"}) is not None:
        payment_options = card_html.find("i", attrs={"alt": "payment options:"}).find_next().text.strip()
    if card_html.find("i", attrs={"alt": "menu"}) is not None:
        menu = card_html.find("i", attrs={"alt": "menu"}).find_next().text.strip()
        menu_href = card_html.find("i", attrs={"alt": "menu"}).find_next("a").get("href")
    if card_html.find("i", attrs={"alt": "dietary options:"}) is not None:
        dietary_options = card_html.find("i", attrs={"alt": "dietary options:"}).find_next().text.strip()
    if card_html.find("i", attrs={"alt": "opening days and hours:"}) is not None:
        opening_days = convert(card_html.find("i", attrs={"alt": "opening days and hours:"}).find_next().find_all(attrs={"class": "col"}))

    new_data = {location_name: {
        'location': location,
        'location_link' : location_link,
        'menu_offering': menu_offering,
        'payment_options': payment_options,
        'menu': {
            'menu_name': menu,
            'menu_href': menu_href
        },
        'dietary_options': dietary_options,
        'opening_days': opening_days
    }}
    data.update(new_data)

#https://www.javatpoint.com/save-json-file-in-python
dining_dir = open("dining_dir.json", "w")
json.dump(data, dining_dir, indent=4)
dining_dir.close()