from urllib.request import urlopen
from bs4 import BeautifulSoup
import re
import sqlite3
from random import randrange

def get_links(keyword, articleURL):
    db = sqlite3.connect("scrapecrawl.db")
    html = urlopen(articleURL)
    bsobj = BeautifulSoup(html, "lxml")
    if bsobj.find(text=re.compile(keyword)):
        try:
            com = "INSERT into Link(Url) VALUES ('{}')".format(articleURL)
            db.execute(com)
            db.commit()
            db.close()
        except sqlite3.IntegrityError:
            pass
    return bsobj.findAll("h4", {"class":"related-story-headline embed-headline"})

def initiation():
    url = "http://www.straitstimes.com/tech/safeentry-applications-surge-ahead-of-reopening-of-businesses"
    keyword = "Covid-19"
    links = get_links(keyword, url)
    for link in links:
        temp = get_links(keyword, link.next_element.attrs["href"])
        for more_link in temp:
            if more_link not in links:
                links.append(more_link)
        print(link.next_element.attrs["href"])

def delete():
    db = sqlite3.connect("scrapecrawl.db")
    com = "DELETE FROM Link"
    db.execute(com)
    db.commit()
    db.close

delete()
#initiation()


