import re, argparse

def re_strip(string, char = "\s"):
	stripReg = re.compile(r'^[{}]*(.*?)[{}]*$'.format(char, char))
	stripped = stripReg.search(string)
	
	if stripped:
		return stripped.group(1)
	else:
		return string

		
if __name__ == '__main__':
	parser = argparse.ArgumentParser()
	parser.add_argument('string', help = 'the string containing the characters to strip')
	parser.add_argument('pattern', nargs = '?', help = 'the characters to strip from the string')
	args = parser.parse_args()
	
	if args.pattern:
		print(re_strip(args.string, args.pattern))
	else:
		print(re_strip(args.string))


