#! python3
 
import os, PyPDF2, argparse
from sys import exit

parser = argparse.ArgumentParser()
parser.add_argument('directory')
parser.add_argument('mode', choices = ['en', 'de'])
parser.add_argument('password')
args = parser.parse_args()

if not os.path.exists(args.directory):
	print('Unable to find {}. Exiting the program..'.format(args.directory))
	exit()

if args.mode == 'en':
	for dir, subdirs, files in os.walk(args.directory):
		for file in files:
			filename, ext = os.path.splitext(file)
			if ext == '.pdf':
				with open(os.path.join(dir, file), 'rb') as pdfFile:
					pdfReader = PyPDF2.PdfFileReader(pdfFile)
					
					if pdfReader.isEncrypted:
						continue
					
					print('Encrypting {}..'.format(file))
					pdfWriter = PyPDF2.PdfFileWriter()						
					pdfWriter.appendPagesFromReader(pdfReader)
					pdfWriter.encrypt(args.password)
					
					encryptedFilename = filename + '_encrypted' + ext
					encryptedFile = open(os.path.join(dir, encryptedFilename), 'wb')
					pdfWriter.write(encryptedFile)
					encryptedFile.close()
					
					test = open(os.path.join(dir, encryptedFilename), 'rb')
					testPdfReader = PyPDF2.PdfFileReader(test)
					if testPdfReader.isEncrypted:
						print ('{} encrypted successfully'.format(file))
					test.close()

elif args.mode == 'de':
	for dir, subdirs, files in os.walk(args.directory):
		for file in files:
			filename, ext = os.path.splitext(file)
			if ext == '.pdf':
				with open(os.path.join(dir, file), 'rb') as pdfFile:
					pdfReader = PyPDF2.PdfFileReader(pdfFile)
					
					if not pdfReader.isEncrypted:
						continue
					
					print('Decrypting {}..'.format(file))
					pdfReader.decrypt(args.password)				
					try:
						pdfReader.getPage(0)
					except:
						print('Failed to decrypt {}. Moving on to the next file..'.format(file))
						continue
									
					pdfWriter = PyPDF2.PdfFileWriter()				
					pdfWriter.appendPagesFromReader(pdfReader)
					
					pdfFilename = filename + '_decrypted' + ext
					pdfFile = open(os.path.join(dir, pdfFilename), 'wb')
					pdfWriter.write(pdfFile)
					print('{} decrypted successfully'.format(file))
					pdfFile.close()