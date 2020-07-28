# (c) Aaron Brady 2004

import PIL.Image as Image
import PIL.ImageFont as ImageFont
import PIL.ImageDraw as ImageDraw
import sys

def do_image(fn, out_fn=None, width=100):
	if not out_fn:
		out_fn = fn + ".thumb.png"

	WANTED_BOX=width * 1.00

	#fon = ImageFont.truetype(r'04b_24__.ttf', 8)

	src = Image.open(fn)
	src.load()
	iwid, ihei = src.size

	if iwid > ihei:
		scale = WANTED_BOX / iwid
	else:
		scale = WANTED_BOX / ihei

	src = src.resize((iwid*scale, ihei*scale), Image.BICUBIC)
	# pos, is where the image is pasted
	if 1 == 1: # have image border hug the image
		wid, hei = src.size
		pos = (10, 10)
	if 1 == 0: # have image border constant
		wid, hei = (int(WANTED_BOX), int(WANTED_BOX))
		if iwid > ihei:
			pos = (10, 10 + ((hei - (ihei*scale)) / 2))
		else:
			pos = (10 + ((wid - (iwid*scale)) / 2), 10)

	fram = Image.open('photo-frame.bmp')
	fram.load()

	im = Image.new('RGB', (26+wid, 26+hei), '#ffffff')

	tl = fram.crop( (0, 0, 10, 10) )
	tr = fram.crop( (10, 0, 36, 10) )
	bl = fram.crop( (0, 10, 10, 36) )
	br = fram.crop( (10, 10, 36, 26) )

	t = fram.crop( (9, 0, 10, 10) )
	l = fram.crop( (0, 9, 10, 10) )
	b = fram.crop( (9, 10, 10, 36) )
	r = fram.crop( (10, 9, 26, 10) )

	im.paste(tl, (0, 0))
	im.paste(tr, (10+wid, 0))
	im.paste(bl, (0, 10+hei))
	im.paste(br, (10+wid, 10+hei))
	for i in range(hei):
		im.paste(l, (0, i+10))
		im.paste(r, (10+wid, i+10))
	for i in range(wid):
		im.paste(t, (i+10, 0))
		im.paste(b, (i+10, 10+hei))
	im.paste(src, pos)

	#draw = ImageDraw.Draw(im)
	#draw.text((10,hei+10), u'(c) 2004 Aaron Brady', font=fon, fill='#dddddd')

	f = open(out_fn, 'wb')
	im.save(f, "PNG")

if __name__ == '__main__':
	import os
	import os.path
	if len(sys.argv) > 1:
		D = sys.argv[1]
	else:
		D = '.'
	for item in os.listdir(D):
		if item.lower().endswith("jpg"):
			do_image(os.path.join(D, item))
			print '<a href="%s"><img src="%s"/></a>' % (item, item + ".thumb.png")
	
