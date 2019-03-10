#! python3

import requests, bs4, sys, re, shelve, os, schedule, time
from sys import exit
	
SHELVE_FILE = 'sd_data'

def get_comic_num(text):	
	comicNumber = re.search(r'https://xkcd.com/(\d+)/', text)	
	if comicNumber:
		return int(comicNumber.group(1))
	else:
		return None		

def read_and_update_shelve_file(latest):
	shelveFile = shelve.open(SHELVE_FILE)
	last_downloaded = shelveFile.setdefault('last_downloaded', 1)
	shelveFile['last_downloaded'] = latest
	shelveFile.close()	
	return last_downloaded
		
def download_update(res):
	soup = bs4.BeautifulSoup(res.text, "html.parser")
	latest = get_comic_num(soup.get_text())	
	if not latest:
		print('Error: unable to find comic number')
		return

	last_downloaded = read_and_update_shelve_file(latest)	
	if last_downloaded != latest:
		comicElem = soup.select('#comic img')
		if not comicElem:
			print('Error: unable to find comic')
			return
			
		comicSrc = 'http:{}'.format(comicElem[0].get('src'))
		print('Found update. Downloading comic #{}..'.format(latest))
		res = requests.get(comicSrc)
		try:
			res.raise_for_status()
		except:
			print('Error: unable to download comic #{}'.format(latest))
			return
		
		with open('{}.jpg'.format(os.path.join('xkcd', str(latest))), 'wb') as imageFile:
			for chunk in res.iter_content(100000):
				imageFile.write(chunk)									
		print('Completed downloading comic #{}'.format(latest))		
	else:
		print('No updates found')
		
def get_update(url):
	res = requests.get(url)
	try:
		res.raise_for_status()
	except:
		print('Error: unable to connect to {}'.format(url))
		return		
	download_update(res)
	
if __name__ == "__main__":
	os.makedirs('xkcd', exist_ok = True)		
	url = 'http://xkcd.com'
	schedule.every().day.do(get_update, url)
	
	while True:
		try:
			schedule.run_pending()
		except Exception as exception:
			print('{}. Exiting program..'.format(exception))
			sys.exit()

