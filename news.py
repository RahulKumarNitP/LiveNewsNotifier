import requests
import time
import notify2
import xml.etree.ElementTree as ET
RSS_FEED_URL = "http://www.hindustantimes.com/rss/topnews/rssfeed.xml"
def loadRSS():
	resp = requests.get(RSS_FEED_URL)
	return resp.content

def parseXML(rss):
	root = ET.fromstring(rss)
	newsitems = []
	for item in root.findall('./channel/item'):
		news = {}
		for child in item:
			if child.tag == '{http://search.yahoo.com/mrss/}content':
				news['media'] = child.attrib['url']
			else:
				news[child.tag] = child.text.encode('utf8')
		newsitems.append(news)
	return newsitems

def topStories():
	rss = loadRSS()
	newsitems = parseXML(rss)
	return newsitems

ICON_PATH = "/home/rahul/Desktop/projects/text-editor.png"
newsitems = topStories()
notify2.init("News Notifier")
n = notify2.Notification(None, icon = ICON_PATH)
n.set_urgency(notify2.URGENCY_NORMAL)
n.set_timeout(10000)
for newsitem in newsitems:
	n.update(newsitem['title'], newsitem['description'])
	n.show()
	time.sleep(15)
