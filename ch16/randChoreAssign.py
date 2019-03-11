import random, shelve, smtplib, os, schedule, argparse
from sys import exit

SHELVE_FILE = 'choreAssignHistory'

def string_to_list(string):
	return list(set([item.strip() for item in string.split(',')]))

def was_prev_chore(email, chore):
	with shelve.open(SHELVE_FILE) as history:
		if email not in history.keys():
			return False
		else:
			return history[email] == chore

def update_shelve(email, chore):
	with shelve.open(SHELVE_FILE) as history:
		history[email] = chore

def assign_chores(emails, chores):
	assignedChores = {}
	choreCopy = list(chores)
	for email in emails:
		if not choreCopy:
			chore = None
		else:
			chore = random.choice(choreCopy)
			while was_prev_chore(email, chore):
				chore = random.choice(choreCopy)
		assignedChores[email] = chore
		update_shelve(email, chore)
		choreCopy.remove(chore)
	return assignedChores

def gmail_smtp_login(account, password):
	try:
		smtpObj = smtplib.SMTP('smtp.gmail.com', 587)
		smtpObj.ehlo()
		smtpObj.starttls()
		print('Connection to the server established.')		
		smtpObj.login(account, password)
		print('Successfully logged into the server.')
		return smtpObj
	except Exception as exception:
		print('Error occurred while trying to log into gmail: {}'.format(exception))
		raise
	
def send_chores(account, password, assignedChores):
	try:
		smtpObj = gmail_smtp_login(account, password)
	except:
		raise
	
	for email, chore in assignedChores.items():
		try:
			smtpObj.sendmail(account, email, 'Your new chore for the week is {}'.format(chore))
			print('Assigned chore sent to {}!'.format(email))
		except Exception as exception:
			print('Failed to send email to {}: {}'.format(email, exception))
	print('Finished sending new chores. Logging off from the server...')
	smtpObj.quit()
	
def assign_and_send(account, password, emails, chores):
		assignedChores = assign_chores(emails, chores)
		send_chores(account, password, assignedChores)
		
if __name__ == '__main__':
	parser = argparse.ArgumentParser()
	parser.add_argument('account')
	parser.add_argument('password')
	parser.add_argument('file')
	args = parser.parse_args()
	
	if not os.path.exists(args.file):
		print('Unable to find {}'.format(args.file))
		exit()

	with open(args.file) as listFile:
		line = listFile.readline()
		while line.strip().startswith('#'):
			line = listFile.readline()
		emails = string_to_list(line)
		chores = string_to_list(listFile.readline())
	
	# Uncomment the following line to test assign_and_send now
	# assign_and_send(args.account, args.password, emails, chores)
	
	schedule.every().week.do(assign_and_send, args.account, args.password, emails, chores)
	
	while True:
		try:
			schedule.run_pending()
		except Exception as exception:
			print('Exiting program..')
			exit()