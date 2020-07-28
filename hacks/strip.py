#!/usr/bin/python
import email
import mailbox
import os
import sys

if len(sys.argv) < 3:
	print "%s <{mailbox}> <mime-type>" % sys.argv[0]
	sys.exit(-1)

fp = file(sys.argv[1], 'rb')

mbox = mailbox.PortableUnixMailbox(fp, email.message_from_file)

for i in mbox:
		if i.is_multipart():
			l = i.get_payload()
			for ii in l: 
				if ii.get_content_type()[:len(sys.argv[2])] == sys.argv[2]:
					l.remove(ii)
		print i
