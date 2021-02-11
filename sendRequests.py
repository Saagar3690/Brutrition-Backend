import requests
import os
from datetime import date, timedelta
from scrape import scrape

URL = 'https://brutrition.herokuapp.com/menus'


def populateDatabase():
    created = str(date.today())
    menu = scrape(created)

    print(URL)

    r = requests.post(URL, json={
        'created': created,
        'menu': menu,
    })

    if r.status_code == 200:
        print('Successfully populated database')
        return True
    else:
        print('An error occurred trying to populate database')
        return False


def removePreviousMenu():
    yesterday = str(date.today() - timedelta(days=1))

    r = requests.delete(URL, json={
        'date': yesterday
    })

    if r.status_code == 200:
        print('Successfully delete yesterday\'s menu')
        return True
    else:
        print('An error occurred trying to delete yesterday\'s menu')
        return False


def main():
    #removed = False
    # while not removed:
    #    removed = removePreviousMenu()
    populated = False
    while not populated:
        populated = populateDatabase()


main()
