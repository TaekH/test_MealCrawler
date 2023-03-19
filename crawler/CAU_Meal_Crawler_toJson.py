#!/usr/bin/env python
# coding: utf-8

# In[1]:

import os
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.chrome.options import Options
import time
import json

def jsonParser(data):
    with open('CAU_Cafeteria_Menu.json', 'w', encoding='utf-8') as file :
        json.dump(data, file, ensure_ascii=False, indent='\t')

chrome_driver = os.path.join('chromedriver')
chrome_options = Options()
chrome_options.add_argument('--headless')
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')
dr = webdriver.Chrome(chrome_driver, options=chrome_options)
dr.get('https://mportal.cau.ac.kr/main.do')

# 식당 메뉴 정보 가져오는 함수
def getMenuInfo() :
    menuInfoDict = {}
    for cafeteriaIndex in range(1, 10) :
        try :
            cafeteriaName = dr.find_element_by_css_selector('#carteP005 > li > dl:nth-child('+ str(cafeteriaIndex) +') > dt').text
            menuInfoDict[cafeteriaName] = {}
            if cafeteriaIndex != 1 : #첫번째 식당의 경우 이미 선택되어있으므로 클릭하지 않고 넘어감
                getcafeteria = dr.find_element_by_css_selector('#carteP005 > li > dl:nth-child('+ str(cafeteriaIndex) +') > dt > a')
                getcafeteria.click()
                time.sleep(0.5)
            for cafeteriaInfoIndex in range(2, 30) :
                try :
                    getcafeteriaInfo = dr.find_element_by_css_selector('#carteP005 > li > dl:nth-child('+ str(cafeteriaIndex) +') > dd:nth-child('+ str(cafeteriaInfoIndex) +')')
                    MenuType = dr.find_element_by_css_selector('#carteP005 > li > dl:nth-child('+ str(cafeteriaIndex) +') > dd:nth-child('+ str(cafeteriaInfoIndex) +') > label > ul > li:nth-child(2) > span').text
                    menuInfoDict[cafeteriaName][MenuType] = {}
                    menuInfoDict[cafeteriaName][MenuType]['price'] = dr.find_element_by_css_selector('#carteP005 > li > dl:nth-child('+ str(cafeteriaIndex) +') > dd:nth-child('+ str(cafeteriaInfoIndex) +') > label > ul > li:nth-child(3) > span').text
                    getcafeteriaInfo.click()
                    time.sleep(0.5)
                    getMealTime = dr.find_element_by_css_selector('#carteP005 > li > dl:nth-child('+ str(cafeteriaIndex) +') > dd:nth-child('+ str(cafeteriaInfoIndex) +') > label > div > div.nb-p-04-02 > div.nb-p-04-02-01.nb-font-12 > p.nb-p-04-02-01-b')
                    getMealInfo = dr.find_element_by_css_selector('#carteP005 > li > dl:nth-child('+ str(cafeteriaIndex) +') > dd:nth-child('+ str(cafeteriaInfoIndex) +') > label > div > div.nb-p-04-03.nb-font-13.nb-p-flex.nb-wrap.ng-binding')
                    menuInfoDict[cafeteriaName][MenuType]['time'] = getMealTime.text
                    menuInfoDict[cafeteriaName][MenuType]['menu'] = getMealInfo.text.replace('\n', '|')
                except :
                    pass
        except :
            pass
    return menuInfoDict

# 데일리 메뉴 정보 가져오는 함수
def getDailyMenu() :
    dailyMenuInfoDict = {}
    for mealSchedule in range(1, 4) :
        getMealSchedule = dr.find_element_by_css_selector('#P005 > div > div > div > div > ol > li > header > div.nb-right.nb-t-right > ol > li:nth-child('+ str(mealSchedule) +')')
        dailyMenuInfoDict[mealSchedule-1] = {}
        getMealSchedule.click()
        time.sleep(0.5)
        dailyMenuInfoDict[mealSchedule-1] = getMenuInfo()
    return dailyMenuInfoDict

# 위클리 메뉴 정보 가져오는 함수
def getWeekOfMealMenu() :
    weeklyMenuDict = {}
    weeklyIndex = 7
    for campus in range(1, 3):
        weeklyMenuDict[campus-1] = {}
        for day in range(weeklyIndex) :
            getCampus = dr.find_element_by_css_selector('#P005 > div > div > div > div > header > div > ol > li:nth-child(' + str(campus) + ') > span')
            getCampus.click() #setCampus 메소드
            time.sleep(0.5)
            getDay = dr.find_element_by_css_selector('#P005 > div > div > div > div > ol > li > header > div.nb-left > div > p')
            weeklyMenuDict[campus-1][getDay.text] = getDailyMenu()
            time.sleep(0.3)
            setNextDay = dr.find_element_by_css_selector('#P005 > div > div > div > div > ol > li > header > div.nb-left > div > a.nb-p-time-select-next').click()
            setNextDay
        for day in range(weeklyIndex):
            setPrevDay = dr.find_element_by_css_selector('#P005 > div > div > div > div > ol > li > header > div.nb-left > div > a.nb-p-time-select-prev').click()
            setPrevDay
    jsonParser(weeklyMenuDict)

if __name__ == "__main__":
    getWeekOfMealMenu()
