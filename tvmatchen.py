# -*- coding: utf-8 -*-
import urllib2
import datetime
import hashlib
import pymongo
from pymongo import MongoClient
from bs4 import BeautifulSoup

def tvmatchen(DEBUG = False, DATABASE = False):
    #DEBUG = False
    req = urllib2.Request("http://www.tvmatchen.nu/")
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
            channels = []
            game = []

            tmp_teams = upcoming_game.text.encode('utf-8').split("\xe2\x80\x93")
            game.append(tmp_teams[0].strip()) #add team 1
            if(DEBUG): print game[0]
            game.append(tmp_teams[1].strip()) #add team 2
            if(DEBUG): print game[1]
            game.append(upcoming_game.parent.parent.find("time").text.encode('utf8'))
            if(DEBUG): print game[2]
            date = upcoming_game.parent.parent.parent.parent.find("h2", {"class" : "day-title"}).text + " " + upcoming_game.parent.parent.parent.parent.find("span", {"class" : "date-month"}).text
            game.append(date.encode('utf8')) #append date, eg lördag 29 juli
            if(DEBUG): print game[3]
            tmp_channels = upcoming_game.parent.find("div", {"class" : "channels"}).find_all("a", {"class" : "channel"})
            for channel in tmp_channels:
                channels.append(channel["title"].encode('utf8'))
            game.append(channels)
            if(DEBUG): print game[4]
            if(DEBUG): print "\n"
            games.append(game)

    if(DEBUG):
        if games:
            for game in games:
                print game
                #print  game[2] + ": " + game[0] + " - " + game[1] + "\n" + game[3] + "\n"


    if games and DATABASE:
        client = MongoClient('localhost', 27017)
        db = client['upcoming']
        collection = db['football']

        for game in games:
            m = hashlib.md5()
            m.update("".join(str(element) for element in game))
            post = {"type": "football",
                    "team1"     : game[0],
                    "team2"     : game[1],
                    "time"      : game[2],
                    "date"      : game[3],
                    "channels"  : game[4],
                    "_id"       : m.hexdigest()}

            if(DEBUG):
                print "inserted into database:"
                print post
            try:
                collection.insert(post) #insert_one ?
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
