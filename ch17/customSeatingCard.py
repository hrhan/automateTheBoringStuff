#! usr/bin/python3

from PIL import Image, ImageDraw, ImageFont
import argparse, os

PIXEL_PER_INCH = 72
WIDTH = 5
HEIGHT = 4
OUTLINE = 20
FONTS_FOLDER = '/mnt/c/Windows/Fonts'

def resize_logo(image, logo, proportion):
	width, height = image.size
	logoWidth, logoHeight = logo.size
	
	logoHeight = int((width*proportion)/logoWidth*logoHeight)
	logoWidth = int(width*proportion)
	logo = logo.resize((logoWidth, logoHeight))
	return logo

if __name__ == '__main__':
	parser = argparse.ArgumentParser()
	parser.add_argument('guestList')
	parser.add_argument('--f', '-font', nargs='+', default='arial.ttf')
	parser.add_argument('--s', '-size', type=int, default=50)
	parser.add_argument('--l', '-logo')
	args = parser.parse_args()

	os.makedirs('seatingCards', exist_ok=True)	
		
	with open(args.guestList) as guestList:
		for guest in guestList:
			name = guest.strip()
			
			card = Image.new('RGBA', (WIDTH*PIXEL_PER_INCH, HEIGHT*PIXEL_PER_INCH), 'white')
			cWidth, cHeight = card.size
			
			draw = ImageDraw.Draw(card)		
			draw.rectangle((OUTLINE, OUTLINE, cWidth-OUTLINE, cHeight-OUTLINE), outline='black')
		
			if args.l:
				try:
					im = Image.open(args.l)
				except:
					print('Error opening {}'.format(args.l))
					break
				im = resize_logo(card, im, 0.3)
				iWidth, iHeight = im.size
				card.paste(im, (cWidth-iWidth, cHeight-iHeight), im)		
		
			try:
				font = ImageFont.truetype(os.path.join(FONTS_FOLDER, ' '.join(args.f)), size=args.s)
			except:
				font = ImageFont.truetype(os.path.join(FONTS_FOLDER, 'arial.ttf'), size=args.s)			
			fWidth, fHeight = draw.textsize(name, font=font)
			draw.text(((cWidth-fWidth)/2, (cHeight-fHeight)/2), name, fill = 'black', font = font)		
			
			print('Seating card for {} created and saved to {}'.format(name, os.path.abspath('seatingCards')))
			card.save(os.path.join('seatingCards', name + '.png'))
			
		