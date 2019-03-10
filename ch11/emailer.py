#! python3

from selenium import webdriver
import time, argparse

parser = argparse.ArgumentParser()
parser.add_argument('account')
parser.add_argument('password')
parser.add_argument('recipient')
parser.add_argument('--s', '-subject', nargs = '*', default = '')
parser.add_argument('--c', '-content', nargs = '*', default = '')
args = parser.parse_args()

browser = webdriver.Firefox()
browser.get('http://gmail.com')

input = browser.find_element_by_name('identifier')
input.send_keys(args.account)
button = browser.find_element_by_id('identifierNext')
button.click()
time.sleep(1)

input = browser.find_element_by_name('password')
input.send_keys(args.password)
button = browser.find_element_by_id('passwordNext')
button.click()

button = browser.find_element_by_class_name('z0')
button.click()
time.sleep(5)

input = browser.find_element_by_name('to')
input.send_keys(args.recipient)
input = browser.find_element_by_name('subjectbox')
input.send_keys(' '.join(args.s))
input = browser.find_element_by_xpath('//div[contains(@aria-label, "Message Body")]')
input.send_keys(' '.join(args.c))

button = browser.find_element_by_xpath('//div[contains(@aria-label, "Send")]')
button.click()