#! python3

import pyautogui
from pywinauto import findwindows, Application
from sys import exit
from time import sleep

pyautogui.FAILSAFE = True

try:
	app = Application().connect(handle=findwindows.find_windows(title='Skype')[0])
except:
	print('Skype is not running. Exiting..')
	exit()

print('Send to...')
sendTo = input().split(",")
print('Message:')
msg = input()
	
skype = app['Skype']
skypeLoc = skype.rectangle()
searchBarLoc = (skypeLoc.left + 50, skypeLoc.top + 150)
addButtonLoc = (skypeLoc.right - 70, skypeLoc.top + 130)

skype.set_focus()
pyautogui.click(*searchBarLoc)
sleep(0.25)
first = sendTo.pop(0).strip()
pyautogui.typewrite(first, 0.1)
sleep(1)
pyautogui.doubleClick(skypeLoc.left + 100, skypeLoc.top + 490)

if sendTo:
	sleep(0.25)
	pyautogui.click(*addButtonLoc)

	for person in sendTo:		
		sleep(0.5)
		pyautogui.typewrite(person.strip(), 0.1)
		sleep(0.5)
		pyautogui.click(skypeLoc.right/2, skypeLoc.top + 450)
		sleep(0.5)
		pyautogui.click(skypeLoc.right/2, skypeLoc.top + 230)
		pyautogui.typewrite('\b'*len(person))

	doneButton = (int(skypeLoc.right/2 + skypeLoc.left + 250), skypeLoc.top + 140)
	pyautogui.click(*doneButton)
	
sleep(5)
pyautogui.typewrite(msg + '\n', 0.1)
print('send notification to {} people'.format(len(sendTo) + 1))
	
	

	