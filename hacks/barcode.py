#
# The smarts of this are taken from SDLcam's barcode interpretation.
# Major kudos & whuffie to Raphael Assenat of http://sdlcam.raphnet.net/
#
# (c) Aaron Brady 2004
#
import PIL.Image as Image
import PIL.ImageFont as ImageFont
import PIL.ImageDraw as ImageDraw
import sys
import math

# UPCA
codes = [
	( 3, 2, 1, 1 ),
	( 2, 2, 2, 1 ),
	( 2, 1, 2, 2 ),
	( 1, 4, 1, 1 ),
	( 1, 1, 3, 2 ),
	( 1, 2, 3, 1 ),
	( 1, 1, 1, 4 ),
	( 1, 3, 1, 2 ),
	( 1, 2, 1, 3 ),
	( 3, 1, 1, 2 ),
]

#
# Why not math.floor? Well, I was trying out different values when trying to
# get it to work with the scans & photos that I had. Some tweaking of these
# values compensated for the coversion to 1-bit and the various contrast
# settings of my equipment.
#

def floor(amnt):
	if amnt > 3.5:
		return 4
	elif amnt > 2.15:
		return 3
	elif amnt > 1.5:
		return 2
	elif amnt > 0.5:
		return 1
	else:
		return 0

def get_lengths(row):
	counts = []
	amnt = 0
	a = row[0]
	for col in row:
		if not col == a:
			counts.append(amnt)
			amnt = 0
		amnt = amnt + 1
		a = col
	return counts

#
# XXX: ChangeMe
#

def print_barcode(fn='barcode.bmp'):
	src = Image.open(fn)
	src.load()
	width = src.size[0]
	height = src.size[1]
	data = list(src.getdata())
	idx = width * ((height / 8) * 3)
	row = data[idx:(idx+width)]

	lens = get_lengths(row)[1:]

	avg1 = float(reduce(lambda x, y: x+y, lens[0:3])) / 3.0

	amounts = map(lambda x: int(floor(x / avg1)), lens)
	amounts = amounts[3:]

	num = 0
	code = []
	while len(amounts) > 3:
		num = num + 1
		if num == 7:
			amounts = amounts[5:]
			continue
		frun = amounts[:4]
		amounts = amounts[4:]
		print frun,
		try:
			f = tuple(frun)
			x = codes.index(f)
			print x
			code.append(x)
		except:
			try:
				frun.reverse()
				f = tuple(frun)
				x = codes.index(f)
				print x
				code.append(x)
			except:
				code.append('X')
	print ''.join([str(x) for x in code])
	try:
		import niamh
		try:
			print "Checksum:", niamh.checkModTen(code) and "Passed" or "Failed"
		except:
			print "Checksum: Failed"
	except:
		print "Checksum: niamh.py not found"

if __name__ == '__main__':
	print_barcode()
