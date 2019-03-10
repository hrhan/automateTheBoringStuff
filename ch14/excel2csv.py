import csv, openpyxl, os, argparse
from sys import exit

parser = argparse.ArgumentParser()
parser.add_argument('directory', help = 'the directory containing the excel files to convert to csv')
args = parser.parse_args()

if not os.path.exists(args.directory):
	print('Unable to find {}. Exiting the program..')
	exit()
	
for file in os.listdir(args.directory):
	filename, ext = os.path.splitext(file)	
	if ext != '.xlsx':
		continue
	
	print("Converting {} to csv...".format(file))
	wb = openpyxl.load_workbook(file)	
	for sheetname in wb.sheetnames:
		sheet = wb.get_sheet_by_name(sheetname)
		if sheet.dimensions == 'A1:A1':
			continue
	
		outputFilename = '{}_{}.csv'.format(filename, sheetname)
		outputFile = open(os.path.join(args.directory, outputFilename), 'w')
		outputWriter = csv.writer(outputFile)
		
		for val in sheet.values:
			outputWriter.writerow(list(val))
		outputFile.close()
		print("Successfully converted {}_{} to csv".format(file, sheetname))

print("Finished converting all files in {} to csv".format(os.path.abspath(args.directory)))
