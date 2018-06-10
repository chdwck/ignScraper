import gevent.monkey
gevent.monkey.patch_all()

import urllib3
import os
from bs4 import BeautifulSoup
from datetime import datetime


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
        self.http = urllib3.PoolManager()

    def urlopen(self, url):
        return self.http.request(
            'GET',
            url,
            headers={
                'Connection': 'keep-alive',
                'Upgrade-Insecure-Requests': 1,
                'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.79 Safari/537.36',
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
                'Accept-Encoding': 'gzip, deflate',
                'Accept-Language': 'en-US,en;q=0.9',
                'Cookie': 'geoCC=US; _USERCOUNTRY6=US; _ga=GA1.2.2099736787.1528238296; _cb_ls=1; _cb=Bh2oMcD-nwLzDe5EC1; _v__chartbeat3=DKHm1HCoBw51JqSRO;' + 
                          ' __gads=ID=9620a1578b77db33:T=1528238296:S=ALNI_MbXerXr9w1_Epu7hNV6fp3kb2bP4g; optimizelyEndUserId=oeu1528238302000r0.38460126887665;' + 
                          ' optimizelySegments=%7B%221360400627%22%3A%22search%22%2C%221371990448%22%3A%22false%22%2C%221373960443%22%3A%22gc%22%2C%221373960444%22%3A%22none%22%7D; ' +
                           'i10cfd=1; _gid=GA1.2.242024738.1528643017; ign_user_frequency={"lastVisit":"2018-06-10T15:03:40.910Z","oldestVisit":"2018-06-05T22:38:21.175Z",'+
                           '"visits":{"118":{"5":2}}}; zdcse_source=direct; _cb_svref=null; newPrivacyPolicy=closed; OX_plg=pm; _chartbeat5=12,634,%2Freviews%2Fgames,'+
                           'http%3A%2F%2Fwww.ign.com%2Farticles%2F2018%2F06%2F06%2Fthe-elder-scrolls-online-summerset-review%3Fwatch,DH5WJMCYKt41NjukDU5-qPDEiwJO,,c,BT5AgADO6_EgCFnDQjCFoXHXmQuPC,ign.com,;'+
                           ' _gat_UA-71985660-1=1; _chartbeat2=.1528238296292.1528668921163.100001.ZdpPR-XNwdU8hfDYEc3AMNm1J.3; muxData=mux_viewer_id=9cbcf46d-12cd-4408-b927-195806cd6818&msn=0.6236762735498729&sid=3df314cb-05b9-4839-96ea-e51d02ffca0c&sst=1528668920631&sex=1528670422342;'+
                           ' optimizelyBuckets=%7B%2210455061499%22%3A%2210453441056%22%2C%2210841591719%22%3A%2210793845212%22%7D; GED_PLAYLIST_ACTIVITY=W3sidSI6Im5xdkoiLCJ0c2wiOjE1Mjg2Njg5MjMsIm52IjowLCJ1cHQiOjE1Mjg2Njg5MTgsImx0IjoxNTI4NjY4OTE4fV0.; optimizelyPendingLogEvents=%5B%5D'
            }
            ).data

    def getReviewUrls(self, sIdx):
        page = self.urlopen(self.root_url + str(sIdx))
        soup = BeautifulSoup(page, 'html.parser')
        items = soup.findAll('div', {'class': 'item-title'})
        for child in items:
            if (child != None):
                self.urlList.append(child.findChild('a').get('href'))

    def asyncGetPages(self):
        gevent.wait([gevent.spawn(self.getReviewUrls,i) for i in range(0, 1000, 25)])
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
            page = self.urlopen(url)
            soup = BeautifulSoup(page, 'html.parser')
            blurb = self.tryToGet(soup, 'div', 'class', 'blurb')
            scoreText = self.tryToGet(soup, 'div', 'class', 'score-text')
            score = self.tryToGet(soup, 'span', 'class', 'score', 'span')
            name = self.tryToGet(soup, 'h1', 'class', 'article-headline', 'span')

            print("Name:", name.strip())
            print("Score:", score.strip(), "-", scoreText.strip())
            print("Desc:", blurb.strip())
            print("Url:", url.strip())
            print("=================================================")
        except:
            print("Cant open url: ", url)

    def run(self):
        self.asyncGetPages()
        for url in self.reviewList:
            self.getBasicInfo(url)


scrape = IgnScraper('ps4')
scrape.run()