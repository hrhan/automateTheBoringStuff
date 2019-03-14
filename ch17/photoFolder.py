#! python3

import os, argparse
from PIL import Image

extensions = ['.png', '.jpg']

def is_photo(file):
	if os.path.splitext(file)[1].lower() not in extensions:
		return False
	try:
		im = Image.open(file)
		width, height = im.size	
		if width > 500 and height > 500:
			return True
		else:
			return False
	except Exception as e:
		print('Error opening {}: {}'.format(file, e))
		return False

def is_photo_folder(dir, files):
	files = [os.path.join(dir, file) for file in files]
	photofiles = list(filter(is_photo, files))
	if len(files) > 2*len(photofiles):
		return False
	else:
		return True
		
if __name__ == '__main__':
	parser = argparse.ArgumentParser()
	parser.add_argument('--d', '-directory', default = 'C:\\')
	args = parser.parse_args()
	
	print('Scanning {}...'.format(args.d))
	photoFolders = []	
	for dir, subdirs, files in os.walk(args.d):
		if is_photo_folder(dir, files):
			photoFolders.append(dir)
			
	print('{} photo folders found:'.format(len(photoFolders)))	
	for photoFolder in photoFolders:
		print('  {}'.format(photoFolder))
	