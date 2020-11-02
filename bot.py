import requests
import json
from configparser import ConfigParser
url = "https://api.telegram.org/bot"
def app_config_file(config):
		parser = ConfigParser()
		parser.read(config)
		return parser.get('Credential', 'token')
telegrambot = url + app_config_file('config.ini') 


	
def request_bot(url):
	
	try:
		request = requests.get(url)
		response = request.json()
	except HttpError as http_response:
		print("Error occured : {}".format(http_response))
	except Exception as exp:
		print("Detail of exception : {}".format(exp))
	return response

def bot_info():

	info = request_bot(telegrambot+"/getme")
	return info


def bot_receive_msg():

	resp = request_bot(telegrambot+"/getUpdates?timeout=100")
	return resp

def bot_send_message(message,chat_id):
	url = "{}/sendMessage?timeout=100&chat_id={}&text={}".format(telegrambot,chat_id,message)
	Bot_response = request_bot(url)
	return Bot_response

def retrieve_LastMessage():

	msg = bot_receive_msg()
	if msg is not None:
		list_msgs= msg['result']
		len_list=len(list_msgs)
		last_msg= list_msgs[len_list-1]
		update_id = last_msg['update_id']
		
	return last_msg

