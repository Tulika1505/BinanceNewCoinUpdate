import requests
import bot
import pandas as pd
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

def send_userMessage(message):
	last_msg= bot.retrieve_LastMessage()
	Userid=last_msg['message']['from']['id']
	bot.bot_send_message(message, Userid)


def check_csv(coin,date,title,removeCsv=None):
	if len(coin) != 0 :
		new_df= pd.read_csv("New-CoinPair.csv")
		remove_df = pd.read_csv("Remove-CoinPair.csv")
		coin = " ".join(coin)
		message = "Title : {} , Coin Pair : {} , Date : {}".format(title,coin,date)
		if removeCsv is not None:
			#check remove coin pair csv
			if coin not in list(remove_df['CoinPair']):
				#send msg to bot and add to remove csv
				send_userMessage(message)
				add_data = pd.DataFrame({'CoinPair' : [coin], 'Date' : [date]})
				add_data.to_csv('Remove-CoinPair.csv' , mode='a',header=False ,index = False)

		else:
			#check add coin pair csv 
			if coin not in list(new_df['CoinPair']):
				#send msg to bot and add to csv
				send_userMessage(message)
				add_data = pd.DataFrame({'CoinPair' : [coin], 'Date' : [date]})
				add_data.to_csv('New-CoinPair.csv' , mode='a',header=False ,index = False)

def find_date_time(text,remove=None):
	if text is not None:
		strDate = re.search(r'(\d{4}(\/\d{2}){2}.+UTC\))', text)
		coin = re.findall (r'([A-Z]{2,6}\/[a-zA-Z]{2,6})', text)
	return strDate.group(),coin


while True:
	listingData = get_request("/en/support/announcement/c-48")
	soup = get_soup(listingData)
	allLists = soup.find_all('a',class_='css-1neg3js')

	if allLists is not None:
		for listdata in allLists:
			title=listdata.text
			if "binance will list" in listdata.text.lower():
				listDetails = get_request(listdata['href'])
				soup = get_soup(listDetails)
				data = str(soup.find('article',class_='css-1ii68zy'))
				date,coin = find_date_time(data)
				check_csv(coin,date,title)
				print(coin,date)
			elif "binance lists" in listdata.text.lower():
				listDetails = get_request(listdata['href'])
				soup = get_soup(listDetails)
				data = soup.find_all("div",class_='css-3fpgoh')[1].text
				date,coin = find_date_time(data)
				check_csv(coin,date,title)
				print(coin,date)
			elif "Notice of Removal" in listdata.text:
				listDetails=get_request(listdata['href'])
				soup = get_soup(listDetails)
				data = str(soup.find('article',class_='css-1ii68zy'))
				date,coin = find_date_time(data)
				check_csv(coin,date,title,"remove")
				print(coin,date)
				break
			else:
				pass