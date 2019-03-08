import argparse, re
from os.path import exists
from sys import exit

wordRegex = re.compile(r'(NOUN|ADJECTIVE|ADVERB|VERB)')	

parser = argparse.ArgumentParser()
parser.add_argument('file')
args = parser.parse_args()

if not exists(args.file):
	print('Unable to find {}. Exiting the program..'.format(args.file))
	exit()
	
with open(args.file) as story:
	text = story.read()
	match = wordRegex.search(text)
	
	while match:		
		word = input('Enter a(n) {}:'.format(match.group(1)))
		text = wordRegex.sub(word, text, 1)
		match = wordRegex.search(text)
	
	print(text)