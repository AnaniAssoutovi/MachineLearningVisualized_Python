# -*- coding: utf-8 -*-
"""
@author: Anani Assoutovi
Created on Mon Oct 15 08:56:11 2018
Email: anania101@gmail.com
"""

import os, re, platform as pf, socket as sc, datetime
from subprocess import call

def find_ip(ipAddToCheck):
	cmd = 'ipconfig'
	output = os.popen(cmd).read()
	matchOne = re.findall('.* ({0}).*'.format(ipAddToCheck), output)
	matOne = ['{0}'.format(ipAddToCheck)]
	if matchOne == matOne:
		print(output)
	else:
		raise Exception('Expected the matches to be similar but they are Not')
		
def get_OS():
	print('Your Operating System is {0}'.format(os.name))
	
def get_OS_Platform():
	#print('Your Operating Platform is {0}'.format(pf.system()))
	return pf.system()
	
def get_OS_Platform_Release():
	print('Your Operating Platform Release is {0}'.format(pf.release()))
	
get_OS()
print('Your Operating Platform is {0}'.format(get_OS_Platform()))
get_OS_Platform_Release()

def clear_Terminal(osSys):
	# By my assumption, if OS is not equal to Windows, it should be Unix/Linux compatible to perfomr 'clear'
	if osSys != 'Windows':
		call('clear', shell =True)
	elif osSys == 'Windows':
		call('cls', shell =True)

clear_Terminal(get_OS_Platform())

def perform_Shell_Command(command):
	output = os.popen(command).read()
	#print('Here is the output after running \'{0}\''.format(command))
	#print(output)
	return output

if get_OS_Platform() == 'Windows':
	#perform_Shell_Command('/flushdns')
	print()
elif 'macOS' in get_OS_Platform():
	#perform_Shell_Command('sudo killall -HUP mDNSResponder;echo macOS DNS Cache Reset')
	print()

def get_Hostname():
	#print('Host Name is: {0}'.format(sc.gethostbyname(sc.gethostname())))
	return sc.gethostbyname(sc.gethostname())

find_ip(get_Hostname())

def get_List_Of_IPv4():
	#print('Host Name is: {0}'.format(sc.gethostbyname_ex(sc.gethostname())[-1]))
	return sc.gethostbyname_ex(sc.gethostname())[-1]

get_List_Of_IPv4()

for p in range(len(get_List_Of_IPv4())):
	for i in get_List_Of_IPv4():
		if get_OS_Platform() == 'Windows':
			print("{0} at index {1}".format(get_List_Of_IPv4()[p], p))
			break

def get_Socket_IPv6():
	return sc.socket(sc.AF_INET, sc.SOCK_DGRAM)

#print('Socket is: {0}'.format(get_Socket_IPv6()))
	
if get_OS_Platform() == 'Windows':
	print(perform_Shell_Command('netstat -aon'))

if get_OS_Platform() == 'Windows':
	print(perform_Shell_Command('tasklist -v'))

if get_OS_Platform() == 'Windows':
	print(perform_Shell_Command('nslookup myip.opendns.com. resolver1.opendns.com'))

def create_and_write_to_file(fileName, extension, command):
	f = open("{0}{1}".format(fileName,extension), "w+")
	f.write(perform_Shell_Command(command))
	f.close()

create_and_write_to_file(str(datetime.datetime.now()).replace(':','_').split('.',1)[0],".txt",'tasklist -v')
create_and_write_to_file(str(datetime.datetime.now()).replace(':','_').split('.',1)[0],".txt",'netstat -aon')
create_and_write_to_file(str(datetime.datetime.now()).replace(':','_').split('.',1)[0],".pdf",'tasklist -v')
create_and_write_to_file(str(datetime.datetime.now()).replace(':','_').split('.',1)[0],".csv",'tasklist -v')

#print(strftime("%Y-%m-%d %H:%M:%S", gmtime()))
#print(datetime.datetime.now())
#output= str(datetime.datetime.now())
#print(output.split('.',1))[0]


perform_Shell_Command('net1 COMPUTER')
perform_Shell_Command('net1 STATISTICS')
perform_Shell_Command('net1 USER')
perform_Shell_Command('net1 USE')
perform_Shell_Command('net1 SHARE')















