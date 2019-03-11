import requests, schedule, argparse
from twilio.rest import Client
from sys import exit

# you should replace these with your own info
APIKey = 'your API key'
ACC_SID = 'your account SID'
AUTH_TOKEN = 'your authorization token'
SOURCE = 'your twilio phone number'
DESTINATION = 'your actual phone number'

def get_weather(city, country):
	url = 'http://api.openweathermap.org/data/2.5/forecast?q={},{}&APPID={}'.format(city, country, APIKey)
	res = requests.get(url)
	try:
		res.raise_for_status()
	except Exception as exception:
		print('Error: {}'.format(exception))
		raise
	return res.json()['list'][0]['weather'][0]['main']

def send_msg(src, dest):
	client = Client(ACC_SID, AUTH_TOKEN)
	message = client.messages.create(body = 'you should take your umbrella today.', from_ = src, to = dest)
	update = client.messages.get(message.sid).fetch()
	while update.status == u'queued':
		update = client.messages.get(message.sid).fetch()
	print('notification has been {}!'.format(update.status))

def umbrella_reminder(city, country, src, dest):
	print('Checking today\'s weather in {}, {}..'.format(city, country))
	todayWeather = get_weather(city, country)
	print('Today we have {}'.format(todayWeather))
	if todayWeather in ['Rain', 'Snow']:
		print('Sending notification to {}...'.format(todayWeather, dest))
		send_msg(src, dest)
	
if __name__ == '__main__':
	parser = argparse.ArgumentParser()
	parser.add_argument('city')
	parser.add_argument('country')
	args = parser.parse_args()
	
	# uncomment the following line to test umbrella_reminder now
	# umbrella_reminder(args.city, args.country, SOURCE, DESTINATION)
	
	schedule.every().day.at("7:00").do(umbrella_reminder, args.city, args.country, SOURCE, DESTINATION)
	
	while True:
		try:
			schedule.run_pending()
		except Exception as exception:
			print('{}. Exiting program..'.format(exception))
			exit()
	
