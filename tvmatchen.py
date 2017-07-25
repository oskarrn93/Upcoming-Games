# -*- coding: utf-8 -*-
import urllib2
import time
import datetime
import hashlib
import pymongo
from pymongo import MongoClient
from bs4 import BeautifulSoup


def get_date(soup):
    tmp = soup.parent.parent["data-hash"] + " " + soup.find("time").text.encode('utf8')
    return time.mktime(time.strptime(tmp, "%Y-%m-%d %H:%M"))

def get_channels(soup):
    channels = []
    tmp_channels = soup.find("div", {"class" : "channels"}).find_all("a", {"class" : "channel"})
    for channel in tmp_channels:
        channels.append(channel["title"].encode('utf8'))
    return channels

def tvmatchen(DEBUG = False, DATABASE = False):
    #DEBUG = False
    req = urllib2.Request("http://www.tvmatchen.nu/fotboll/")
    req.add_header('User-Agent', 'Mozilla/5.0')

    response = urllib2.urlopen(req)
    the_page = response.read()
    soup = BeautifulSoup(the_page, "html5lib")

    TEAMS_TO_SEARCH_FOR = ["Real Madrid", "Malmö FF"]

    #To select all the span tags
    soup.find_all("ul", {"id" : "matches"})

    soup.find_all("div", {"class" : "details"})
    upcoming_games = soup.find_all("h3")

    games = []

    for upcoming_game in upcoming_games:
        if any(x in upcoming_game.text.encode('utf-8') for x in TEAMS_TO_SEARCH_FOR):
            #reset variables
            game = []

            tmp_teams = upcoming_game.text.encode('utf-8').split("\xe2\x80\x93")
            game.append(tmp_teams[0].strip()) #add team 1
            if(DEBUG): print game[0]
            game.append(tmp_teams[1].strip()) #add team 2
            if(DEBUG): print game[1]
            date = get_date(upcoming_game.parent.parent)
            game.append(date)
            if(DEBUG): print game[2]
            channels = get_channels(upcoming_game.parent);
            game.append(channels)
            if(DEBUG):
                print game[3]
                print "\n"
            games.append(game)

    """if(DEBUG):
        if games:
            for game in games:
                print game
                #print  game[2] + ": " + game[0] + " - " + game[1] + "\n" + game[3] + "\n"
"""

    if games and DATABASE:
        client = MongoClient('localhost', 27017)
        db = client['upcoming']
        collection = db['football']

        for game in games:
            m = hashlib.md5()
            #print "".join(str(element) for element in game)
            m.update(" ".join(str(element) for element in game))
            post = {"type": "football",
                    "team1"     : game[0],
                    "team2"     : game[1],
                    "date"      : game[2],
                    "channels"  : game[3],
                    "_id"       : m.hexdigest()
                    }

            if(DEBUG):
                print "inserted into database:"
                print post
            try:
                collection.insert_one(post) #insert_one ?
            except:
                if(DEBUG): print "already existing in db"

def remove_all_database():
    client = MongoClient('localhost', 27017)
    db = client['upcoming']
    db.football.remove({})

def show_all_database():
    client = MongoClient('localhost', 27017)
    db = client['upcoming']
    cursor = db.football.find()
    for document in cursor:
        print(document)


if __name__ == "__main__":
    tvmatchen(True, True)
    #remove_all_database()
    show_all_database()
