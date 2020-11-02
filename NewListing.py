import requests
import bot
import pandas as pd
import time
from bs4 import BeautifulSoup
import re

def get_request(url):
	response=""
	try:
		response = requests.get("https://www.binance.com"+url).text
	except Exception as e:
		print('Error Details : {}'.format(e))
	return response

def get_soup(data):
	soup =""
	try: 
		soup = BeautifulSoup(data,'html.parser')
	except Exception as e:
		print('Error details : {}'.format(e))
	return soup

def send_userMessage(coin,date,title):
	message = "Title : {} , Coin Pair : {} , Date : {}".format(title,coin,date)
	last_msg= bot.retrieve_LastMessage()
	Userid=last_msg['message']['from']['id']
	bot.bot_send_message(message, Userid)


def find_date_time(text,remove=None):
	if text is not None:
		strDate = re.search(r'(\d{4}(\/\d{2}){2}.+UTC\))', text)
		coin = re.findall (r'([A-Z]{2,6}\/[a-zA-Z]{2,6})', text)
	return strDate.group(),coin


while True:
	listingData = get_request("/en/support/announcement/c-48")
	soup = get_soup(listingData)
	allLists = soup.find_all('a',class_='css-1neg3js')
	link_df = pd.read_csv("HrefLinks.csv")
	if allLists is not None:
		for listdata in allLists:
			data=None
			title=listdata.text
			link= str(listdata['href'])
			if link not in list(link_df['Links']):
				add_data = pd.DataFrame({'Links' : [link]})
				add_data.to_csv('HrefLinks.csv' , mode='a',header=False ,index = False)
				listDetails = get_request(link)
				if "binance will list" in listdata.text.lower():
					soup = get_soup(listDetails)
					data = str(soup.find('article',class_='css-1ii68zy'))
				elif "binance lists" in listdata.text.lower():
					soup = get_soup(listDetails)
					data = soup.find_all("div",class_='css-3fpgoh')[1].text
				elif "Notice of Removal" in listdata.text:
					soup = get_soup(listDetails)
					data = str(soup.find('article',class_='css-1ii68zy'))
					removeBool = True
				else:
					pass
				if data is not None:
					date,coin = find_date_time(data)
					send_userMessage(" ".join(coin),date,title)
				
	time.sleep(30)