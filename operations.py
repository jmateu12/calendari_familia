#! usr/bin/env python
#! -*- coding: utf-8 -*-

import yaml
import datetime
from jinja2 import Template
from pprint import pprint

def get_people_birth_and_saint():
    
    with open("aniversaris.yml") as aniversaris_file:
            data = yaml.load(aniversaris_file)
    
    return data

def make_births_and_saints_calendar(data, year):
    birth = {}
    saint = {}
    # Two dictionaries are created. For each date where there is a birth / saint
    # the dictionary in question will have a key (datetime.date(Year/month/day))
    # with a name of a person assigned as an item.
    
    for person in data:

        person_birth = datetime.datetime.strptime(data[person]["Aniversari"],"%Y/%m/%d").date().replace(year=year)
        person_saint = datetime.datetime.strptime(data[person]["Sant"],"%m/%d").date().replace(year = year)

        if person_birth not in birth:
            birth[person_birth] = []
        birth[person_birth].append([person, datetime.datetime.strptime(data[person]["Aniversari"], "%Y/%m/%d").date()])

        if person_saint not in saint:
            saint[person_saint] = []
        saint[person_saint].append(person)
    

    # We create all the days of a particular year.
    calendar = []
    d1 = datetime.date(year, 1, 1) #Starting day
    d2 = datetime.date(year, 12, 31) #Last day
    
    delta = d2 - d1

    for day_number in range(delta.days + 1):
        date = (d1 + datetime.timedelta(days = day_number))
       
        calendar_date = {"day": [date, date.weekday()], "births":[], "saints":[]}
        if date in birth:
            for person in birth[date]:
                
                age = year - birth[date][birth[date].index(person)][1].year
                calendar_date["births"].append([person, age])
        if date in saint:
            for person in saint[date]:
                calendar_date["saints"].append(person)
        
        calendar.append(calendar_date)
    
    return calendar

def print_calendar(calendar):
    
    with open ("calendar.jinja2", "r") as calendar_tpl:
        t = Template(calendar_tpl.read())
    
    with open("calendar.html", "w") as result:
        result.write(t.render(calendar=calendar))

if __name__ == "__main__":

    data = get_people_birth_and_saint()

    calendar = make_births_and_saints_calendar(data, 2017)

    print_calendar(calendar)
