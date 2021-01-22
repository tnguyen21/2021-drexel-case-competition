from bs4 import BeautifulSoup
import requests

url = "https://drexel.campusdish.com/LocationsAndMenus/UrbanEatery?locationId=9853&storeIds=&mode=Weekly&date=01%2F22%2F2021&periodId=2480"
page = requests.get(url)

# print(page.content)
soup = BeautifulSoup(page.content, 'html.parser')

results = soup.find_all('div', {'class':'menu__station'})

for result in results:
    print(result)