import re, argparse

def strong_password(password):
	pwRegex = re.compile(r'(?=.*[a-z])(?=.*[A-Z])(?=.*[0-9]).{8,}')
	match = pwRegex.search(password)
	if match:
		return True
	else:
		return False

if __name__ == '__main__':
	parser = argparse.ArgumentParser()
	parser.add_argument('password')
	args = parser.parse_args()
	
	print("Password Strength: ", end = "")
	if strong_password(args.password):
		print("STRONG")
	else:
		print("WEAK")