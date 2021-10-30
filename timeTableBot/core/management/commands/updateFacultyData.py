import os
import sys
from pandas.core.frame import DataFrame
from django.core.management.base import BaseCommand
from datetime import datetime
from seleniumwire import webdriver
import pandas as pd
import numpy as np
from core import models
from bs4 import BeautifulSoup


class Command(BaseCommand):
    help = ""

    def handle(self, *args, **kwargs):
        AllFaculty = self.parseAllFaculty()
        models.Faculty.objects.all().delete()
        for name, data in AllFaculty.items():
            try:
                self.save(name, data)
            except Exception as e:
                print(e)
        
    def save(self, name, data):
        faculty_name = name
        Faculty = models.Faculty.objects.create(name=faculty_name)

        groupObjects = list()
        for course in data:
            for direction, group in data[course].items():
                groupObjects.extend([models.Student_group(
                    name=g,
                    faculty=Faculty,
                    course=course[0],
                    direction=direction,
                ) for g in group])

        models.Student_group.objects.bulk_create(groupObjects)

    def getFacultyHTML(self, driver, facultyName: str) -> str:
        driver.find_element_by_xpath(f'//*[@id="GROUPS_AJAX"]/table[1]/tbody/tr/td/a[text()="{facultyName}"]').click()
        facultyHTML = driver.find_element_by_xpath('//*[@id="GROUPS_AJAX"]/table[2]').get_attribute('outerHTML')

        return facultyHTML

    def parseFacultyHtml(self, html) -> dict:
        soup = BeautifulSoup(html, 'lxml')
        coursesTable = soup.find_all('td')

        courses = {}
        for course in coursesTable:  
            
            b = course.find_all('b')
            groups = {}

            for el in b:
                groupName = el.text
                groups[groupName] = list()
                while 1:
                    el = el.find_next_sibling()

                    if not el or el.name == 'b':
                        break

                    if el.name == 'a':
                        groups[groupName].append(el.text)

            courseName = course.find('th', class_="t13RegionTitle")
            if not courseName:
                continue
            courses[courseName.text] = groups

        return courses

    def parseAllFaculty(self):
        driver = self.browserConf()
        driver.get("https://cist.nure.ua/ias/app/tt/f?p=778:2:2588301904455370::NO:::#")

        facultyNames = self.getFacultysName(driver)

        data = dict()
        for facultyName in facultyNames:
            html = self.getFacultyHTML(driver, facultyName)
            data[facultyName] =  self.parseFacultyHtml(html)

        driver.quit()

        return data

    def getFacultysName(self, driver) -> list:
        facultysWE = driver.find_elements_by_xpath(f'//*[@id="GROUPS_AJAX"]/table[1]/tbody/tr/td/a')
        facultyList = list()

        for faculty in facultysWE:
            facultyList.append(faculty.text)
        return facultyList

    def  browserConf(self):
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--window-size=1420,1080")
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--disable-dev-shm-usage")

        driver = webdriver.Chrome(
            chrome_options=chrome_options,
            executable_path="/usr/local/bin/chromedriver",
        )

        return driver