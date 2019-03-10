import requests, bs4, os, argparse
from sys import exit

def requestPage(link):
	try:
		res = requests.get(link)
		res.raise_for_status()
		print('Connected to {}'.format(link))
		return res
	except Exception as e:
		print('Unable to connect to {}'.format(link))
		raise

if __name__ == '__main__':		
	parser = argparse.ArgumentParser()
	parser.add_argument('start')
	args = parser.parse_args()

	try:
		res = requestPage(args.start)
	except:
		print('Exiting program..')
		exit()

	soup = bs4.BeautifulSoup(res.text, features='html.parser')
	links = soup.select('a[href]')

	if links == []:
		print('no links found on the given page.')
	else:	
		for i in range(len(links)):
			link = links[i].get('href')
			
			if 'http' not in link:
				link = os.path.dirname(args.start) + link
				
			try:
				res = requestPage(link)
			except KeyboardInterrupt:
				break
			except:
				continue
				
			# maybe add what actions to perform on each link here
	print('Done.')