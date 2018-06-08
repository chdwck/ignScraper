import urllib2
import os
from bs4 import BeautifulSoup
from database import DBController
from datetime import datetime
import gevent.monkey
gevent.monkey.patch_all()

# ********** PlatformSlug Format *********
# ps4, xbox-one, ps3, pc
# xbox-360, wii, wii-u, 3ds,
# new-nintendo-3ds, nds, nintendo-switch
# vita, psp, iphone, ipad, xbox, gb, gba,
# n64, mac, gcn, dc, ps, ps2, nng
# *****************************************


class IgnScraper:
    def __init__(self, platformSlug):
        self.root_url = 'http://www.ign.com/reviews/games?platformSlug='+ platformSlug +'&startIndex='
        self.urlList = []
        self.reviewList = []
        self.dbc = DBController(platformSlug)

    def getReviewUrls(self, sIdx):
        page = urllib2.urlopen(self.root_url + `sIdx`)
        soup = BeautifulSoup(page, 'html.parser')
        items = soup.findAll('div', {'class': 'item-title'})
        for child in items:
            self.urlList.append(child.findChild('a').get('href'))

    def asyncGetPages(self):
        gevent.wait([gevent.spawn(self.getReviewUrls,i) for i in xrange(0, 1000, 25)])
        self.reviewList = list(set(self.urlList))

    def tryToGet(self, soup, nodeType, selectType, selectName, childType='None'):
        div = soup.find(nodeType, { selectType: selectName })
        if div == None:
            return 'None was found'
        if childType == 'None':
            return div.text
        else:
            return div.findChild(childType).text

    def getBasicInfo(self, url):
        try:
            page = urllib2.urlopen(url)
            soup = BeautifulSoup(page, 'html.parser')
            blurb = self.tryToGet(soup, 'div', 'class', 'blurb')
            scoreText = self.tryToGet(soup, 'div', 'class', 'score-text')
            score = self.tryToGet(soup, 'span', 'class', 'score', 'span')
            name = self.tryToGet(soup, 'h1', 'class', 'article-headline', 'span')

            self.dbc.addGame(
                title=name.strip(),
                rating=float(score.strip()),
                description=blurb.strip(),
                oneword=scoreText.strip(),
                console=1,
                url=url.strip()
            )
            print "Name: " + name.strip()
            print "Score: " + score.strip() + " - " + scoreText.strip()
            print "Desc: " + blurb.strip()
            print "Url: " + url.strip()
            print "================================================="
        except:
            print "Cant open url: " + url

    def run(self):
        self.asyncGetPages()
        for url in self.reviewList:
            self.getBasicInfo(url)


scrape = IgnScraper('ps4')
scrape.run()
scrape.dbc.close()
