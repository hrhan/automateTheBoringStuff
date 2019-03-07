#! python3

def printTable(table):
	for col in range(len(table[0])):
		colMax = max([len(row[col]) for row in table])
		
		for row in table:
			row[col] = '{:>{width}}'.format(row[col], width = colMax)
			
	for row in table:
		print(' '.join(row))

if __name__ == '__main__':		
	tableData = [['apples', 'oranges', 'cherries', 'banana'],
				 ['Alice', 'Bob', 'Carol', 'David'],
				 ['dogs', 'cats', 'moose', 'goose']]
			
	printTable(tableData)