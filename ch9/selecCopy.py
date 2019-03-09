#! python3

import argparse, os
from shutil import copy
from sys import exit

parser = argparse.ArgumentParser()
parser.add_argument('src', help = 'the source directory to copy files from')
parser.add_argument('dst', help = 'the  directory where the files will be copied to')
parser.add_argument('format', nargs = '+', help = 'extension(s) of the files to copy')
args = parser.parse_args()


if not os.path.exists(args.src):
	print('unable to find the given folder {}'.format(args.src))
	exit()

os.makedirs(args.dst, exist_ok = True)

for dir, subdir, files in os.walk(args.src):
	if os.path.abspath(args.dst) == os.path.abspath(dir):
		continue
		
	print('Searching in {}..'.format(dir))	
	for file in files:
		if os.path.splitext(file)[1] in args.format:
			copy(os.path.join(dir, file), args.dst)
			print('Copied {} to {}'.format(file, args.dst))