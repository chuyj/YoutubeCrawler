#!/usr/bin/env python
# -*- coding: utf-8 -*-
#file: hw1-2.py
import urllib
import argparse
import requests
from bs4 import BeautifulSoup
parser = argparse.ArgumentParser(description='YouTube Search Crawler', prog = 'YouTube Search Crawler')
parser.add_argument('-n', default = 5, type = int, help = 'number of search result. default is 5')
parser.add_argument('-p', default = 1, type = int, help = 'page that you parse')
parser.add_argument('keyword', nargs = '*')
args = parser.parse_args()
if not args.keyword: parser.error('Must Specify Keyword')
query = '+'.join([urllib.quote_plus(keyword) for keyword in args.keyword])
youtubeurl = 'https://www.youtube.com/results?search_query={}&sp=EgIQAQ%253D%253D&page={}'
requests.packages.urllib3.disable_warnings()
while args.n > 0 :	
	result = requests.get(youtubeurl.format(query, args.p), verify = False)
	soup = BeautifulSoup(result.content, 'html.parser')
	objects = soup.find_all('div', {'class' : 'yt-lockup-content'})
	if args.n >= 20: count = 20
	else: count = args.n
	for i in range(0,count):
		title = objects[i].h3.a.text
		discrip = objects[i].find('div', {'class': 'yt-lockup-description yt-ui-ellipsis yt-ui-ellipsis-2'.split()})
		likepage_url = 'https://www.youtube.com{}'.format(objects[i].h3.a.get('href'))
		likepage = requests.get(likepage_url, verify = False)
		like_soup = BeautifulSoup(likepage.content, 'html.parser')
		like = like_soup.find_all('button', {'class': 'yt-uix-button yt-uix-button-size-default yt-uix-button-opacity yt-uix-button-has-icon no-icon-markup like-button-renderer-like-button like-button-renderer-like-button-unclicked yt-uix-clickcard-target   yt-uix-tooltip'})
		dislike = like_soup.find_all('button', {'class': 'yt-uix-button yt-uix-button-size-default yt-uix-button-opacity yt-uix-button-has-icon no-icon-markup like-button-renderer-dislike-button like-button-renderer-dislike-button-unclicked yt-uix-clickcard-target   yt-uix-tooltip'})
		urlfit = requests.get('https://developer.url.fit/api/shorten?long_url=' + urllib.quote_plus(likepage_url), verify = False).json()['url']
		print title + ' (https://url.fit/' + urlfit + ')'
		if (discrip):
			print discrip.text
		if (len(like) != 0):
			print 'Like: ' + like[0].text + ', Dislike: ' + dislike[0].text;
		print ''
	args.p, args.n = args.p + 1, args.n - 20
