def comma_code(list):
	if len(list) < 2:
		return ''.join(list)
		
	string = ', '.join(list[:-1]) + ' and ' + list[-1]
	return string

if __name__ == '__main__':
	spam = ['apples', 'bananas', 'tofu', 'cats']
	print(comma_code(spam))