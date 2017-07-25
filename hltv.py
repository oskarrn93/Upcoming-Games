import urllib2
import datetime
import pymongo
import hashlib
from pymongo import MongoClient
from bs4 import BeautifulSoup
"""
client = MongoClient('localhost', 27017)
db = client['upcoming']
#db.cs.remove({})
cursor = db.cs.find()
for document in cursor:
    print(document)

"""
def hltv(DEBUG = False, DATABASE = False):
    #DEBUG = True
    req = urllib2.Request("http://www.hltv.org/matches")
    req.add_header('User-Agent', 'Mozilla/5.0')

    response = urllib2.urlopen(req)
    the_page = response.read()
    soup = BeautifulSoup(the_page, "html5lib")

    #TEAM_TO_SEARCH_FOR = "fnatic".lower()
    TEAMS_TO_SEARCH_FOR = ["fnatic", "NiP"]

    soup.find_all("a", {"class" : "upcoming-match"})
    upcoming_games_team = soup.find_all("div", {"class" : "team"})

    games = []

    for upcoming_game in upcoming_games_team:
        #if TEAM_TO_SEARCH_FOR in (tmp_game.lower() for tmp_game in upcoming_game):
        if any(x in upcoming_game.text for x in TEAMS_TO_SEARCH_FOR ):
            #reset variable
            game = []
            #print upcoming_game
            #game.append(TEAM_TO_SEARCH_FOR)
            #print upcoming_game.parent.parent.parent.find_all("div", {"class" : "team"})
            for tmp_other_team in upcoming_game.parent.parent.parent.find_all("div", {"class" : "team"}):
                #print tmp_other_team.text
                #if TEAM_TO_SEARCH_FOR not in str(tmp_other_team).lower():
                if any(x in tmp_other_team.text for x in TEAMS_TO_SEARCH_FOR ):
                    #print tmp_other_team.text
                    game.append(tmp_other_team.text)
                else:
                    game.append(tmp_other_team.text)

            timestamp = upcoming_game.parent.parent.parent.find("div", {"class" : "time"})["data-unix"]
            #game.append(datetime.datetime.fromtimestamp(int(timestamp)/1000).strftime('%Y-%m-%d %H:%M:%S'))
            game.append(timestamp)
            game.append("https://www.hltv.org" + upcoming_game.parent.parent.parent.parent.parent.parent["href"])

            games.append(game)

    if(DEBUG):
        if games:
            for game in games:
                print  game[2] + ": " + game[0] + " - " + game[1] + "\n" + game[3] + "\n"

    if games and DATABASE:
        client = MongoClient('localhost', 27017)
        db = client['upcoming']
        collection = db['cs']

        for game in games:
            m = hashlib.md5()
            m.update("".join(str(element) for element in game))
            post = {"type"  : "cs",
                    "team1" : game[0],
                    "team2" : game[1],
                    "date"  : game[2],
                    "url"   : game[3],
                    "_id"   : m.hexdigest()}
            if(DEBUG):
                print "inserted into database:"
                print post
            try:
                collection.insert_one(post) #insert_one ?
            except:
                if(DEBUG): print "already existing in db"
    else:
        if(DEBUG): print "no games found"

def remove_all_database():
    client = MongoClient('localhost', 27017)
    db = client['upcoming']
    db.cs.remove({})

def show_all_database():
    client = MongoClient('localhost', 27017)
    db = client['upcoming']
    cursor = db.cs.find()
    for document in cursor:
        print(document)

if __name__ == "__main__":
   hltv(True, False)
   #remove_all_database()
