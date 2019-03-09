import shutil, os, argparse, re
from sys import exit

parser = argparse.ArgumentParser()
parser.add_argument('directory')
parser.add_argument('prefix')
args = parser.parse_args()

if not os.path.exists(args.directory):
	print('Unable to find the given directory. Exiting program..')
	exit()

gapFiles = sorted(list(filter(lambda x: x.startswith(args.prefix), os.listdir(args.directory))))

if not gapFiles:
	print('Files with prefix {} not found. Exiting program...'.format(args.prefix))
	exit()

filenameReg = re.compile(r'{}(\d+)'.format(args.prefix))

prev = 0
for file in gapFiles:
	match = filenameReg.search(file)
	if not match:
		continue
		
	curr = match.group(1)
	if int(curr) - prev > 1:
		newName = '{}{:0{width}}{}'.format(args.prefix, prev, os.path.splitext(file)[1], width = len(curr))
		shutil.move(os.path.join(args.directory, file), os.path.join(args.directory, newName))
		print('renamed {} to {}'.format(file, newName))
	prev += 1