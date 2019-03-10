import PyPDF2, os, argparse
from sys import exit

parser = argparse.ArgumentParser()
parser.add_argument('file', help = 'the encrypted pdf file')
parser.add_argument('dictionary', help = 'the list of possible passwords')
args =  parser.parse_args()
	
if not os.path.exists(args.file):
	print('Unable to find {}. Exiting the program..'.format(args.file))
	exit()

if not os.path.exists(args.dictionary):
	print('Unable to find {}. Exiting the program..'.format(args.dictionary))
	exit()

print('Attempting to decrypt {}..'.format(args.file))

with open(args.file, 'rb') as pdfFileObj:
	pdfReader = PyPDF2.PdfFileReader(pdfFileObj)

	if not pdfReader.isEncrypted:
		print("{} is not encrypted".format(args.file))
		pdfFlieObj.close()
		exit()
	
	match = None
	with open(args.dictionary) as passwords:
		for password in passwords:
			if pdfReader.decrypt(password.strip()):
				match = password.strip()
				break
	if match:
		print('SUCCESS: {} decrypted with password = {}'.format(args.file, match))
	else:
		print('FAILURE: correct password for {} not found'.format(args.file))


		