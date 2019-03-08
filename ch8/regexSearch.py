import re, argparse, os, sys

parser = argparse.ArgumentParser()
parser.add_argument('directory', help = 'the directory to search')
parser.add_argument('pattern', help = 'the regex pattern to search for')
args = parser.parse_args()

if not os.path.exists(args.directory):
	print('invalid directory given. Exiting program...')
	sys.exit()

files = os.listdir(args.directory)
inputReg = re.compile(args.pattern)

for file in files:
	if os.path.splitext(file)[1] != '.txt':
		continue
	
	found = False
	fileLoc = os.path.join(args.directory, file)
	with open(fileLoc) as text:
		for linenum, line in enumerate(text):
			match = inputReg.search(line)
			if match:
				if not found:
					print('in {}:'.format(file))
					found = True
				print('  line {}: {}'.format(linenum, line.strip()))