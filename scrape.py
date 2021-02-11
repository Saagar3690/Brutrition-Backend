import requests
import requests.exceptions
from bs4 import BeautifulSoup
from datetime import date, timedelta


def scrapeNutritionInfo(url):
    src = requests.get(url).content
    soup = BeautifulSoup(src, "lxml")

    # container of all nutritional info
    recipeContainer = soup.find('div', {'class': 'recipecontainer'})
    if not recipeContainer:
        return {
            'prodWebCodes': '',
            'servingSize': '',
            'calories': '',
            'fatCalories': '',
            'totalFat': '',
            'saturatedFat': '',
            'transFat': '',
            'sodium': '',
            'totalCarbohydrate': '',
            'dietaryFiber': '',
            'sugars': '',
            'protein': '',
            'vitaminA': '',
            'vitaminC': '',
            'calcium': '',
            'iron': '',
            'ingredients': '',
            'allergens': '',
        }
    # print(recipeContainer)

    # product web codes (i.e. contains wheat, gluten, etc.)
    prodWebCodeContainer = recipeContainer.div.findAll(
        'div', {'class': 'prodwebcode'})
    prodWebCodes = [item.text.strip() for item in prodWebCodeContainer]

    # nutrition label container
    nfBoxContainer = recipeContainer.find('div', {'class': 'nfbox'})
    servingSize = nfBoxContainer.find(
        'p', {'class': 'nfserv'}).text[13:].strip()
    caloriesContainer = nfBoxContainer.find(
        'p', {'class': 'nfcal'}).text.split(' ')
    calories, fatCalories = caloriesContainer[1], caloriesContainer[-1]

    # nutrient container - contains info about total fat, cholesterol, sodium, carbs, fiber, sugar, and protein
    nfNutrientContainer = nfBoxContainer.findAll(
        'p', {'class': 'nfnutrient'})
    totalFat = {
        'val': nfNutrientContainer[0].text.strip().split(' ')[2].strip(),
        'dailyVal': nfNutrientContainer[0].text.strip().split(' ')[-1].strip()
    }
    saturatedFat = {
        'val': nfNutrientContainer[1].text.strip().split(' ')[2].strip(),
        'dailyVal': nfNutrientContainer[1].text.strip().split(' ')[-1].strip()
    }
    transFat = nfNutrientContainer[2].text.strip().split(' ')[-1].strip()
    cholesterol = {
        'val': nfNutrientContainer[3].text.strip().split(' ')[1].strip(),
        'dailyVal': nfNutrientContainer[3].text.strip().split(' ')[-1].strip()
    }
    sodium = {
        'val': nfNutrientContainer[4].text.strip().split(' ')[1].strip(),
        'dailyVal': nfNutrientContainer[4].text.strip().split(' ')[-1].strip()
    }
    totalCarbohydrate = {
        'val': nfNutrientContainer[5].text.strip().split(' ')[2].strip(),
        'dailyVal': nfNutrientContainer[5].text.strip().split(' ')[-1].strip()
    }
    dietaryFiber = {
        'val': nfNutrientContainer[6].text.strip().split(' ')[2].strip(),
        'dailyVal': nfNutrientContainer[6].text.strip().split(' ')[-1].strip()
    }
    sugars = nfNutrientContainer[7].text.strip().split(' ')[-1].strip()
    protein = nfNutrientContainer[8].text.strip().split(' ')[-1].strip()

    # vitamin container - vitamin A, vitamin C, calcium, and iron
    nfVitContainer = nfBoxContainer.findAll('div', {'class': 'nfvit'})
    vitaminA = nfVitContainer[0].find('span', {'class': 'nfvitleft'}).find(
        'span', {'class': 'nfvitpct'}).text.strip()
    vitaminC = nfVitContainer[0].find('span', {'class': 'nfvitright'}).find(
        'span', {'class': 'nfvitpct'}).text.strip()
    calcium = nfVitContainer[1].find('span', {'class': 'nfvitleft'}).find(
        'span', {'class': 'nfvitpct'}).text.strip()
    iron = nfVitContainer[1].find('span', {'class': 'nfvitright'}).find(
        'span', {'class': 'nfvitpct'}).text.strip()

    ingredientsAllergensContainer = recipeContainer.find(
        'div', {'class': 'ingred_allergen'}).findAll('p')
    ingredients = ingredientsAllergensContainer[0].text.strip(
        'INGREDIENTS:').strip()
    allergens = ingredientsAllergensContainer[1].text.strip(
        'ALLERGENS*:').strip() if 1 < len(ingredientsAllergensContainer) else ''

    return {
        'prodWebCodes': prodWebCodes,
        'servingSize': servingSize,
        'calories': calories,
        'fatCalories': fatCalories,
        'totalFat': totalFat,
        'saturatedFat': saturatedFat,
        'transFat': transFat,
        'sodium': sodium,
        'totalCarbohydrate': totalCarbohydrate,
        'dietaryFiber': dietaryFiber,
        'sugars': sugars,
        'protein': protein,
        'vitaminA': vitaminA,
        'vitaminC': vitaminC,
        'calcium': calcium,
        'iron': iron,
        'ingredients': ingredients,
        'allergens': allergens,
    }


def scrapeByItem(item, mealType):
    linkToNutritionInfo = item.span.a['href']

    return {
        'name': item.span.a.text.strip(),
        'nutritionInfo': scrapeNutritionInfo(linkToNutritionInfo),
        'mealType': mealType
    }


def scrapeBySubMenu(subMenu, mealType):
    items = subMenu.findAll('li', {'class': 'menu-item'})

    listOfItems = []

    for item in items:
        listOfItems.append(scrapeByItem(item, mealType))

    return {
        'name': subMenu.contents[0].strip(),
        'items': listOfItems
    }


def scrapeByDiningHall(diningHall, mealType):
    subMenus = diningHall.findAll('li', {'class': 'sect-item'})

    listOfSubMenus = []

    for subMenu in subMenus:
        listOfSubMenus.append(scrapeBySubMenu(subMenu, mealType))

    return {
        'name': diningHall.h3.text.strip(),
        'subMenus': listOfSubMenus
    }


def scrapeByMealTime(url, mealType, MENUS):
    src = requests.get(url).content
    soup = BeautifulSoup(src, "lxml")

    diningHalls = soup.findAll('div', {'class': 'menu-block'})
    for diningHall in diningHalls:
        combine(MENUS, scrapeByDiningHall(diningHall, mealType))


def scrape(date):
    baseUrl = 'http://menu.dining.ucla.edu/Menus/' + date
    urls = [baseUrl + '/Breakfast', baseUrl + '/Lunch', baseUrl + '/Dinner']
    meals = ['Breakfast', 'Lunch', 'Dinner']

    MENUS = {
        'diningHalls': []
    }

    for idx, url in enumerate(urls):
        scrapeByMealTime(url, meals[idx], MENUS)

    return MENUS

#
# ---------------------------- Helper functions ----------------------------
#


def combine(MENUS, curDiningHall):
    existingDiningHall = False
    for i, diningHall in enumerate(MENUS['diningHalls']):
        if diningHall['name'] == curDiningHall['name']:
            existingDiningHall = True
            for curSubMenu in curDiningHall['subMenus']:
                existingSubMenu = False
                for j, subMenu in enumerate(MENUS['diningHalls'][i]['subMenus']):
                    if curSubMenu['name'] == subMenu['name']:
                        existingSubMenu = True
                        for curItem in curSubMenu['items']:
                            existingItem = False
                            for item in MENUS['diningHalls'][i]['subMenus'][j]['items']:
                                if item['name'] == curItem['name']:
                                    existingItem = True
                                    break

                            if not existingItem:
                                MENUS['diningHalls'][i]['subMenus'][j]['items'].append(
                                    curItem)
                        break
                if not existingSubMenu:
                    MENUS['diningHalls'][i]['subMenus'].append(curSubMenu)
            break

    if not existingDiningHall:
        MENUS['diningHalls'].append(curDiningHall)
