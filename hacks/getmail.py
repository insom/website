#!/usr/bin/python
from poplib import *
import time
import re
import sys

class null_file:
	def write(self,x):
		pass
	def close(self):
		pass

# account = (server, username, password, function)
def check(accounts, out=null_file()):
	for account in accounts:
		print >>out, "Checking", account[0]
		con = POP3(account[0])
		con.user(account[1])
		con.pass_(account[2])
		stat = con.stat()
		list_ = con.list()
		print >>out, stat[0], "messages."
		for msg in list_[1]:
			id, size = msg.split(" ")
			print >>out, "Message %s, %s bytes." % (id, size)
			body_ = con.retr(id)
			body = "\n".join(body_[1])
			del body_
			if type(account[3]) == type(''):
				f = open(account[3], 'ab')
			else:
				f = account[3](account, body)
			f.write("From test@test.domain %s\n" % time.asctime())
			f.write(body)
			f.write('\n')
			f.close()
			con.dele(id)
		con.quit()

if __name__ == '__main__':
	def f_oc(account, body):
		if re.search("^To:.*crestnorth.com", body, re.M):
			f = open("cn", "ab") # append, binary
		else:
			f = open("cs", "ab")
		return f

	default_accounts = [
	('mail.crestsource.com', 'username', 'password', f_oc), 
	('mail.insom.me.uk', 'username', 'password', 'mailbox'), 
	]
	check(default_accounts, sys.stdout)
