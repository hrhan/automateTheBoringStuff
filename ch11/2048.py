#! python3

from selenium import webdriver
from selenium.webdriver.common.keys import Keys

browser = webdriver.Firefox()
browser.get('https://gabrielecirulli.github.io/2048/')

htmlElem = browser.find_element_by_tag_name('html')
status = browser.find_element_by_class_name('game-message').text

while u'Game over!' not in status:	
	htmlElem.send_keys(Keys.UP)
	htmlElem.send_keys(Keys.RIGHT)
	htmlElem.send_keys(Keys.DOWN)
	htmlElem.send_keys(Keys.LEFT)
	status = browser.find_element_by_class_name('game-message').text

score = browser.find_element_by_class_name('score-container').text	
print('Final score = {}'.format(score))