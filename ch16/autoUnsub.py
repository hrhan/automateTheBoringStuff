from pyzmail import PyzMessage
import imapclient, bs4, argparse, webbrowser, logging
from sys import exit

def gmail_imap_login(account, password):
	try:
		imapObj = imapclient.IMAPClient('imap.gmail.com')
		logging.debug('Connected to imap.gmail.com')
		imapObj.login(account, password)
		logging.debug('Successfully logged into the gmail server')
		print('Successfully logged into the gmail server.')
		return imapObj
	except Exception as exception:
		logging.error('{}'.format(exception))
		print('Unable to connect to the gmail server: {}'.format(exception))
		raise	
	
def gmail_select_folder(imapObj, inputFolder, readonly = False):
	selectedFolder = inputFolder

	if inputFolder != 'INBOX':
		folders = [item[2] for item in imapObj.list_folders()]

		for folder in folders:
			if inputFolder in folder:
				selectedFolder = folder
				break
	
	logging.debug('{} folder selected; input folder = {}'.format(selectedFolder, inputFolder))
	imapObj.select_folder(selectedFolder, readonly = readonly)
	print("{} folder selected..".format(selectedFolder))
	
if __name__ == '__main__':	

	parser = argparse.ArgumentParser()
	parser.add_argument('account')
	parser.add_argument('password')
	parser.add_argument('--f', '-folder', default = 'INBOX')
	args = parser.parse_args()

	# this is my workaround for the webbrower issue with wsl
	# try:
		# webbrowser.get()
	# except:
		# firefox_path = '/mnt/c/Program Files/Mozilla FireFox/firefox.exe'
		# webbrowser.register('firefox', None, webbrowser.BackgroundBrowser(firefox_path),1)
	
	logging.basicConfig(filename='autoUnsubLog.txt', level=logging.ERROR, format='%(asctime)s - %(levelname)s - %(message)s')
	logging.debug('Start of the program')
	
	try:
		imapObj = gmail_imap_login(args.account, args.password)
	except Exception as exception:
		print('Exiting program..')
		exit()

	gmail_select_folder(imapObj, args.f, readonly = True)		
	uids = imapObj.gmail_search('unsubscribe')	
	unsubed = []

	for uid in uids:
		logging.debug('Checking email {}'.format(uid))
		rawMsg = imapObj.fetch(uid, ['BODY[]'])
		msg = PyzMessage.factory(rawMsg[uid][b'BODY[]'])
		src = msg.get_address('from')
		
		if src[0] in unsubed:
			logging.debug('{} already in unsubed. Skippting email {}'.format(src[0], uid))
			continue
		
		if msg.html_part:
			soup = bs4.BeautifulSoup(msg.html_part.get_payload().decode('utf-8','ignore'), features='lxml')	
			url = soup.find("a", string = ["Unsubscribe", "unsubscribe", "UNSUBSCRIBE"])
			if url:
				url = url['href']
				print('opening unsubscription page for {}...'.format(src[0].encode('utf-8', 'ignore')))
				webbrowser.open(url)
				logging.debug('{} openned'.format(url))
			unsubed.append(src[0])
		
	imapObj.logout()
	print('Logged out.')
	logging.debug('Logged out')
	logging.debug('End of the program')
	
	
	
