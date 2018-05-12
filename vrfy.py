#!/usr/bin/env python
#Scripts for Checking VRFY from SMTP server
import socket
import getopt
import sys
import re


def usage():
	help = "Options:\n"
	help += "\t-h <host>\t host\n"
	help += "\t-p <port>\t port (Default: 25)\n"
	help += "\t-u <filename>\t users_list_file\n"
	help += "\t-v \t verbose\n"
	return help


def main():
	print "Good Luck!"
	print "Checking VRFY from SMTP server"
	print "@@@@@@@@@@@@@@@@@@@@@@@@@@@"
	print "@       KMN sharing       @"
	print "@@@@@@@@@@@@@@@@@@@@@@@@@@@"
	print "Ref: OpenSecurityResearch "
        try:
                opts, args = getopt.getopt(sys.argv[1:], "h:p:u:v",[])

        except getopt.GetoptError:
                print usage()
                return
        port = 25 
        verbose = host = users_list_file = 0

        for o, a in opts:
                if o == "-h":
                        host = a
                if o == "-p":
                        port = int(a)
                if o == "-u":
                        users_list_file = a
		if o == "-v":
			verbose = 1
        if (host == 0) or (users_list_file == 0):
                print usage()
                return

	print "Your Target IP =",host,"& Port",port
	s = socket.socket()
	s.settimeout(10)
	recv_data = 0
	s.connect((host,port))

	banner = s.recv(512)
	if verbose == 1:
		print "[V] Banner:"
		print banner
	
	file = open(users_list_file,'r')
	count = 1
	for line in file:

		if count % 10 == 0:
			if verbose == 1:
				print "Reconnecting, Be sure your usernames TRUE"
			s.shutdown(2) 
			s.close

			s = socket.socket()
			s.settimeout(10)
			recv_data = 0
			s.connect((host,port))

			banner = s.recv(512)
			if verbose == 1:
				print "[V] Banner:"
				print banner

		user = line.rstrip('\n')

		msg = "VRFY "
		msg += user
		msg += "\n"
		if verbose == 1:
			print "Verification each user in users_list_file"

		error = s.sendall(msg)
		
		if error:
			print "\n[!] Error with user",user,":", error
		else:
			try:
				recv_data = s.recv(512)
			except socket.timeout:
				print "[!] Timeout on user",user,"!"
	
		if recv_data:
#			print recv_data
			if re.match("250",recv_data):
				print "Found User:",user
			if verbose == 1:
				print "User:",user,
				if re.match("550",recv_data):
					print " -> This user does not exit."
				else:
					print " -> User Exits."
					print "You can login with this username ==>", user
				print recv_data	
		else:
			print "\nNo recv_data!"
		count+=1

	file.close()
	s.shutdown(2)
	s.close()

main()