import imapclient, schedule, argparse, logging
from pyzmail import PyzMessage
from autoUnsub import gmail_imap_login, gmail_select_folder
from sys import exit

class DoNotContinue(Exception): 
	pass

def add_label(imapObj, uid, label):
	imapObj.add_gmail_labels(uid, label)
	logging.debug('Error label added to email {}'.format(uid))
	
def execute_email_content(imapObj, uid, passphrase, _continue):
	rawMsg = imapObj.fetch(uid, ['BODY[]'])
	msg = PyzMessage.factory(rawMsg[uid][b'BODY[]'])	
	lines = msg.text_part.get_payload().decode('utf-8','ignore').split()
	
	# check the first line in the email for passphrase
	if passphrase:	
		logging.debug('passphrase = {}'.format(passphrase))
		found = lines.pop(0)
		if found != passphrase:
			logging.error('Incorrect passphrase provided for uid {}: {}'.format(uid, found))
			print('incorrect passphrase provided for email {}.'.format(uid))
			return	# move onto the next email

	for num, line in enumerate(lines):
		try:
			exec(line)
		except:
			logging.error('Error: unable to execute line {}:{}'.format(num, line))
			print('Error: unable to execute line {}. Aborting email {}...'.format(num, uid))
			add_label(imapObj, uid, 'Error')
			if _continue:
				logging.error('Continue flag set. Continuing program..')
				print('Continue flag set. Continuing program..')
				return	# move onto the next email
			else:
				logging.error('Continue flag not set. Stop processing emails..')
				print('Continue flag not set. Stop processing emails..')
				raise DoNotContinue

def check_and_execute(account, password, folder, passphrase, _continue):
	try:
		imapObj = gmail_imap_login(account, password)
		gmail_select_folder(imapObj, folder)
		uids = imapObj.gmail_search('from:{} AND is:unread'.format(account))
		for uid in uids:
			logging.debug('Processing email {}'.format(uid))
			print('Processing email {}..'.format(uid))
			execute_email_content(imapObj, uid, passphrase, _continue)	
	except:
		raise
		
	imapObj.logout()
	logging.debug('Logged out.')
	print('Logged out.')
	

if __name__ == '__main__':

	parser = argparse.ArgumentParser()
	parser.add_argument('account')
	parser.add_argument('password')
	parser.add_argument('--f', '-folder', default = 'INBOX')
	parser.add_argument('--p', '-passphrase', default = None, help = 'use this option if you want this program to check for passphrase before processing emails')
	parser.add_argument('--c', '-continue', action = 'store_true', help = 'use this option if you want to continue processing emails after encountering errors')
	args = parser.parse_args()
	
	logging.basicConfig(filename='emailControllerLog.txt', level=logging.ERROR, format='%(asctime)s - %(levelname)s - %(message)s')
	logging.debug('Start of the program')
	
	# uncomment the following the line to use check_and_execute now
	# try:
		# check_and_execute(args.account, args.password, args.f, args.p, args.c)
	# except:
		# print('error')
	
	schedule.every(15).minutes.do(check_and_execute, args.account, args.password, args.f, args.p, args.c)
	
	while True:
		try:
			schedule.run_pending()
		except Exception as exception:
			print('{}. Exiting program..'.format(exception))
			exit()
			
	logging.debug('End of the program')