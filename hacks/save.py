#!/usr/bin/python
import email
import mailbox
import os
import os.path
import sys

if len(sys.argv) < 4:
	print "%s <{mailbox}> <mime-type> <directory>" % sys.argv[0]
	sys.exit(-1)


fp = file(sys.argv[1], 'rb')
mbox = mailbox.PortableUnixMailbox(fp, email.message_from_file)

try:
	os.mkdir(sys.argv[3])
except:
	pass

for i in mbox:
	print i.is_multipart()
	if i.is_multipart():
		for ii in i.get_payload():
			print ii.get_content_type()
			if ii.get_content_type()[:len(sys.argv[2])] == sys.argv[2]:
				fn = ii.get_filename()
				f = open(os.path.join('%s', '%s') % (sys.argv[3], fn), 'wb')
				f.write(ii.get_payload(decode=True))
				f.close()
				
