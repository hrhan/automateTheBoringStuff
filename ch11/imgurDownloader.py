#! python3

import requests, bs4, os, argparse

parser = argparse.ArgumentParser()
parser.add_argument('keyword', nargs = '+', help = 'the keyword to search for')
parser.add_argument('--n', '-number', type = int, default = 5, help = 'the number of images you want to download. Set to 5 by default')
args = parser.parse_args()

dlFolder = 'downloaded_images'
os.makedirs(dlFolder, exist_ok = True)

res = requests.get('https://imgur.com/search?q=' + ' '.join(args.keyword))
soup = bs4.BeautifulSoup(res.text, features='html.parser')
images = soup.select('.image-list-link')
numImages = args.n

if images == []:
	print('No images found. Exiting the program..')
else:
	curr = 0
	print('Started downloading {} {} images..'.format(numImages, ' '.join(args.keyword)))
	while curr < numImages and images:
		try:
			imageUrl = 'https://imgur.com' + images.pop(0).get('href')
			res = requests.get(imageUrl)
			res.raise_for_status()
			
			soup = bs4.BeautifulSoup(res.text, features='html.parser')
			image = soup.select('link[rel=image_src]')
			if image:											# if the image is in jpg format
				imageUrl = image[0].get('href')
			else:												# else the image is in a different format..
				image = soup.select('meta[itemprop=embedURL]')	# check if we can find the source of the image in gif format
				if not image:									
					continue									# uh oh, it's not in gif either! Skip this image..
				imageUrl = image[0].get('content').rstrip('v')			
				
			res = requests.get(imageUrl)
			try:
				res.raise_for_status()
			except:
				continue
				
			imageFile = open(os.path.join(dlFolder, os.path.basename(imageUrl)), 'wb')
			for chunk in res.iter_content(100000):
				imageFile.write(chunk)
			imageFile.close()				
			curr += 1
			
		except KeyboardInterrupt:
			break
		except:
			continue
	
	print('Downloaded {} images to the {} folder'.format(curr, dlFolder))

