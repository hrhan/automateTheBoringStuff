#! python3

import pyautogui, time

while True:
	try:
		pyautogui.moveRel(-1, 0)
		time.sleep(10)
	except KeyboardInterrupt:
		print('Exiting lookingBusy.py...')