from pandas.core.frame import DataFrame
from django.core.management.base import BaseCommand
from datetime import datetime
from seleniumwire import webdriver
import pandas as pd
import numpy as np
from core import models
import pytz
import time


class Command(BaseCommand):
    help = ""

    def add_arguments(self , parser):
        parser.add_argument('faculty__name', type=str, help='evid')

    def handle(self, *args, **kwargs):
        faculty__name = kwargs['faculty__name']
        # allStudentGroup = models.Student_group.objects.all()
        allStudentGroup = models.Student_group.objects.filter(faculty__name=faculty__name)
        count = len(allStudentGroup)

        for i, group in enumerate(allStudentGroup, 1):
            name = group.name
            faculty = group.faculty

            group = models.Student_group.objects.get(name=name)
            html_string = self.getTimeTableHTML(faculty, name)
            dfTimeTable = self.parseTimeTable(html_string) 
            time.sleep(1)
            self.save(dfTimeTable, group)

            print(f"{i}/{count}", end="\r")
        print(f"done")

    def save(self, dfTimeTable, group):
        timeTableObjects = []
        for i, j in dfTimeTable.to_dict('index').items():
            begin_time, end_time = tuple(map(lambda x: datetime.strptime(x, '%H:%M').time(), i.split(' ')))

            for data, v in j.items():
                if type(v) is not float:
                    timezone = pytz.timezone("Europe/Athens")
                    begin = timezone.localize(datetime.combine(data, begin_time))
                    end = timezone.localize(datetime.combine(data, end_time))

                    timeTableObjects.append(models.TimeTable(
                        group=group,
                        abbreviation=v.split(" ")[0],
                        begin=begin, 
                        end=end
                    ))
        models.TimeTable.objects.bulk_create(timeTableObjects)

    def getTimeTableHTML(self, faculty: str, group: str) -> str:
        driver = self.browserConf()
        driver.get("https://cist.nure.ua/ias/app/tt/f?p=778:2:2588301904455370::NO:::#")

        driver.find_element_by_xpath(f'//*[@id="GROUPS_AJAX"]/table[1]/tbody/tr/td/a[text()="{faculty}"]').click()

        driver.find_element_by_xpath(f'//a[text()="{group}"]').click()
        driver.find_element_by_xpath('//a[text()="Формат HTML"]').click()

        driver.switch_to_window(driver.window_handles[1])
        
        timeTableHTML = driver.find_element_by_xpath('//table[@class="MainTT"]').get_attribute('outerHTML')

        driver.close()

        return timeTableHTML

    def parseTimeTable(self, html: str) -> DataFrame:
        table_MN = pd.read_html(html)

        df = table_MN[0]

        df.columns = df.iloc[0]
        df.drop(index=df.index[0], axis=0, inplace=True)
        
        df["№"] = df["№"].astype('str').replace({'\d+': np.nan}, regex=True).astype('object')
        df["№"].interpolate('pad', inplace = True)

        df.set_index('№', inplace = True)
        df.index.name = None

        df = df.assign(level2=df.groupby(level=0).cumcount()).set_index('level2',append=True)
        
        daysOfWeek = set(df.index.get_level_values(0))

        dfTimeTable = pd.DataFrame()
        for day in daysOfWeek:
            dfDayTimeTable = df.loc[day].copy()
            dfDayTimeTable.columns = dfDayTimeTable.iloc[0]
            dfDayTimeTable.drop(index=dfDayTimeTable.index[0], axis=0, inplace=True)
            dfDayTimeTable.set_index(day, inplace = True)

            dfTimeTable = dfTimeTable.merge(
                dfDayTimeTable, how="outer", left_index=True, right_index=True, sort=True
            )

        dfTimeTable.dropna(how='all', axis=1, inplace=True)

        # sort by columns date
        dfTimeTable.columns =  pd.to_datetime(dfTimeTable.columns)
        dfTimeTable = dfTimeTable.sort_index(axis = 1) 

        return dfTimeTable

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