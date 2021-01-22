from bs4 import BeautifulSoup
import csv
import re
import requests

OUT_CSV = "datasets/urban_menu_data.csv"
COLUMNS = [
    "item_name",
    "station",
    "day_served",
    "meal_time",
    "calories",
    "contains_eggs",
    "contains_fish",
    "contains_milk",
    "contains_peanuts",
    "contains_shellfish",
    "contains_soy",
    "contains_treenuts",
    "contains_wheat",
    "is_gluten_free",
    "is_halal",
    "is_kosher",
    "is_locally_grown",
    "is_organic",
    "is_vegan",
    "is_vegetarian"
]
# the query URL used on drexel dining's website uses a 4 digit code
# to denote whether it queries for breakfast, lunch, dinner, or all day menus
# the codes are as followed:
CODE_TO_MEALTIME = {
    '2477' : 'breakfast',
    '2479' : 'lunch',
    '2480' : 'dinner',
    '3137' : 'allday'
}
MENUS_TO_SCRAPE = [ # arrays of menus to query, formated by [menu-code, MM, DD, YYYY]
    # here we are scraping all menus from 01/11/2021-02/15/2021
    ['2477', '01', '11', '2021'], 
    ['2479', '01', '11', '2021'],
    ['2480', '01', '11', '2021'],
    ['3137', '01', '11', '2021'],
    ['2477', '01', '18', '2021'], 
    ['2479', '01', '18', '2021'],
    ['2480', '01', '18', '2021'],
    ['3137', '01', '18', '2021'],
    ['2477', '01', '25', '2021'],
    ['2479', '01', '25', '2021'],
    ['2480', '01', '25', '2021'],
    ['3137', '01', '25', '2021'],
    ['2477', '02', '01', '2021'],
    ['2479', '02', '01', '2021'],
    ['2480', '02', '01', '2021'],
    ['3137', '02', '01', '2021'],
    ['2477', '02', '08', '2021'],
    ['2479', '02', '08', '2021'],
    ['2480', '02', '08', '2021'],
    ['3137', '02', '08', '2021'],
    ['2477', '02', '15', '2021'],
    ['2479', '02', '15', '2021'],
    ['2480', '02', '15', '2021'],
    ['3137', '02', '15', '2021'],
    ['2477', '02', '22', '2021'],
    ['2479', '02', '22', '2021'],
    ['2480', '02', '22', '2021'],
    ['3137', '02', '22', '2021'],
    ['2477', '03', '01', '2021'],
    ['2479', '03', '01', '2021'],
    ['2480', '03', '01', '2021'],
    ['3137', '03', '01', '2021'],
    ['2477', '03', '08', '2021'],
    ['2479', '03', '08', '2021'],
    ['2480', '03', '08', '2021'],
    ['3137', '03', '08', '2021'],
    ['2477', '03', '15', '2021'],
    ['2479', '03', '15', '2021'],
    ['2480', '03', '15', '2021'],
    ['3137', '03', '15', '2021'],
]

def normalize_text(string):
    # regex to match non-alphanumeric chars
    pattern = re.compile(r'^\W+', re.UNICODE)
    string = string.lower()
    return re.sub(pattern, '', string) # sub all non-alphanumeric char w ''

def get_parsed_content(url):
    page = requests.get(url)
    parsed_page = BeautifulSoup(page.content, 'html.parser')
    return parsed_page

def append_row_to_csv(array_of_data):
    with open(OUT_CSV, mode='a', newline='') as f:
        csv_writer = csv.writer(f, delimiter=',')
        csv_writer.writerow(array_of_data)

# mealtime is optional paramter we pass if we know what mealtime
# the menu is for (e.g. breakfast, lunch, dinner)
def parse_day_menu_and_append_to_csv(day_menu, mealtime=''):
    day = normalize_text(day_menu.find('h2', {'class':'dayName'}).contents[0])
    
    station_menus = day_menu.find_all('div', {'class':'menu__station'})
    for station_menu in station_menus:
        station = normalize_text(station_menu.find('h3', {'class':'stationName'}).contents[0])
        
        station_items = station_menu.find_all('li', {'class':'menu__item'})
        for item in station_items:
            item_name = normalize_text(item.find('span', {'class':'item__name'}).find('a').contents[0])
            item_calories = re.findall(r'\b\d+\b', (item.find('span', {'class':'item__calories'}).contents[0]))[0] \
                if item.find('span', {'class':'item__calories'}) is not None \
                else None
            contains_eggs = item.get('containseggs')
            contains_fish = item.get('containsfish')
            contains_milk = item.get('containsmilk')
            contains_peanuts = item.get('containspeanuts')
            contains_shellfish = item.get('containsshellfish')
            contains_soy = item.get('containssoy')
            contains_treenuts = item.get('containstreenuts')
            contains_wheat = item.get('containswheat')
            is_gluten_free = item.get('isglutenfree')
            is_halal = item.get('ishalal')
            is_kosher = item.get('iskosher')
            is_locally_grown = item.get('islocallygrown')
            is_organic = item.get('isorganic')
            is_vegan = item.get('isvegan')
            is_vegetarian = item.get('isvegetarian')
            if(item_calories != None):
                # on drexel dining menu site, items with no calories are 
                # usually salad/sandwich bar items that are available 
                # everyday, so we skip them
                append_row_to_csv([item_name, station, day, mealtime, \
                                item_calories, contains_eggs, \
                                contains_fish, contains_milk, contains_peanuts, \
                                contains_shellfish, contains_soy, contains_treenuts, \
                                contains_wheat, is_gluten_free, is_halal, is_kosher, \
                                is_locally_grown, is_organic, is_vegan, is_vegetarian])
            
if __name__ == "__main__":
    append_row_to_csv(COLUMNS) # add headers to dataset

    for menu in MENUS_TO_SCRAPE:
        # generate query url
        print('scraping drexel dining menu for:', CODE_TO_MEALTIME[menu[0]], menu[1], menu[2], menu[3])
        url = f"https://drexel.campusdish.com/LocationsAndMenus/UrbanEatery?locationId=9853&storeIds=&mode=Weekly&periodId={menu[0]}&date={menu[1]}%2F{menu[2]}%2F{menu[3]}"
        parsed_page = get_parsed_content(url)
        day_menus = parsed_page.find_all('div', {'class':'menu__day'})
        for day_menu in day_menus:
            parse_day_menu_and_append_to_csv(day_menu, mealtime=CODE_TO_MEALTIME[menu[0]])
    
    print('done scraping! yee haw')