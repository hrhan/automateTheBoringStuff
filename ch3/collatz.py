#! /usr/bin/env python3

def collatz(number):
	if number % 2 == 0:
		output = number // 2
	else:
		output = 3 * number + 1
	return output

if __name__ == '__main__':
	while True:
		try:
			userNum = int(input("please enter a number: "))
		except ValueError:
			print("This isn't a number!")
			continue
		
		while userNum != 1:
			print(userNum)
			userNum = collatz(userNum)
		
		print(userNum)
		break
		
