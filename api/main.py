#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
sys.path.insert(0, 'libs')
import webapp2
from bs4 import BeautifulSoup, UnicodeDammit
import urllib2,re, datetime, cgi
from webapp2_extras import json


def getTodaysMenu(location):
    
    #Generate Regular Expression for Today
    today = datetime.date.today()
    regex = re.compile(str(today.year) + ".*?" + str(today.month) + ".*?" + str(today.day));

    #Get HTML
    if location == "ulsan":
        baseURL = 'http://massmail.sk.com/menu/print.aspx?rcode=no2'
    else:
        baseURL = 'http://massmail.sk.com/menu/print.aspx?rcode=no1'

    html = urllib2.urlopen(baseURL).read()

    #Parse HTML using BeautifulSoup
    html = BeautifulSoup(html)

    #Find Today's row
    cell = html.find(text=regex)

    today_row = cell.parent.parent
    cells = today_row.find_all("td")

    b_menu_str = ""
    l_menu_str = ""
    d_menu_str = ""

    #Get Breakfast
    breakfast =  cells[0]
    b_menus = breakfast.find_all("li")
    for item in b_menus:
        b_menu_str += item.get_text() + "</br>"

    #Get Lunch
    lunch =  cells[1]
    l_menus = lunch.find_all("li")
    for item in l_menus:
        l_menu_str += item.get_text() + "</br>"

    #Get Dinner
    dinner = cells[2]
    d_menus = dinner.find_all("li")
    for item in d_menus:
        d_menu_str += item.get_text() + "</br>"

    #Generate JSON
    json_str = "{'date' : '%s','breakfast' : '%s','lunch': '%s','dinner': '%s'}" % (today, b_menu_str, l_menu_str, d_menu_str,)

    return json_str


class HQMenuHandler(webapp2.RequestHandler):
    def get(self):
        self.response.content_type = "application/json"
        self.response.write(self.request.get("callback") + "("+getTodaysMenu("hq") + ");")

class UlsanMenuHandler(webapp2.RequestHandler):
    def get(self):
        self.response.content_type = "application/json"
        self.response.write(self.request.get("callback") + "("+getTodaysMenu("ulsan") + ");")

app = webapp2.WSGIApplication([
    ('/', HQMenuHandler),
    ('/hq', HQMenuHandler),
    ('/ulsan', UlsanMenuHandler)
], debug=True)
