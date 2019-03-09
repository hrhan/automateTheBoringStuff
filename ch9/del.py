import os, argparse
from sys import exit
from send2trash import send2trash

UNITS = {'KB': 2**10, 'MB': 2**20, 'GB': 2**30, 'TB': 2**40}

parser = argparse.ArgumentParser()
parser.add_argument('directory')
parser.add_argument('size', type=int)
parser.add_argument('unit', choices = ['KB', 'MB', 'GB', 'TB'])
args = parser.parse_args()

if not os.path.exists(args.directory):
	print('Unable to find the specified directory. Exiting program..')
	exit()
	
sizeThres = args.size * UNITS[args.unit]
print('Searching for files larger than {} {}..'.format(args.size, args.unit))

foundFiles = []
for curr, subdirs, files in os.walk(args.directory):
	for file in files:
		if os.path.getsize(file) >= sizeThres:
			fileLoc = os.path.abspath(os.path.join(curr, file))
			foundFiles.append(fileLoc)
			
print('Files found:')
for idx, file in enumerate(foundFiles):
	print('{}: {}'.format(idx, file))
			
selected = input('Select files to delete (enter \'all\' to delete all listed files):\n')

if selected == 'all':
	for file in foundFiles:
		send2trash(file)
		print('{} deleted'.format(file))
else:
	selected = selected.split()
	for idx in selected:
		try:
			file = foundFiles[int(idx)]
			send2trash(file)
			print('{} deleted'.format(file))
		except:
			pass