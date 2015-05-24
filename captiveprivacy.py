#!/usr/bin/env python3
# -*- Mode: Python; coding: utf-8; indent-tabs-mode: t; c-basic-offset: 4; tab-width: 4 -*- 
#
# main.py
# Copyright (C) 2015 somehandsomedevil <somehandsomedevil@openmailbox.org>
# 
# captiveprivacy is free software: you can redistribute it and/or modify it
# under the terms of the GNU General Public License as published by the
# Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# 
# captiveprivacy is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
# See the GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License along
# with this program.  If not, see <http://www.gnu.org/licenses/>.
import os, pwd, grp
import time
import argparse
import random
import http.client
import http.cookies
import urllib.parse
email_name_list = ["john","jackie", "jeff", "joanne"]
email_domain_list = ["gmail.com","yahoo.com","hotmail.com","outlook.com"]
mac_prefix_list = ["28:37:37", "28:37:37", "28:37:37"]
arguments = argparse.ArgumentParser(description = "Utility for privately connecting to captive portals")
arguments.add_argument('--email', default="false", dest='mac', help='Use this email(Default is to generate one at random)')
arguments.add_argument('--mac', default="false", dest='mac', help='Use this MAC address(Default is to generate one at random')
arguments.add_argument('--zip', default="false", dest='mac', help='Use this ZIP code(Default is to generate one at random')
parsed = arguments.parse_args()
def drop_privileges():
	uid_name='nobody'
	id_name='nogroup'
	if os.getuid() != 0:
		return "nothing to do"
	running_uid = pwd.getpwnam(uid_name).pw_uid
	running_gid = grp.getgrnam(gid_name).gr_gid
	try:
		os.setgroups([])
		os.setgid(running_gid)
	except(os.error, e):
		return e
	try:
		os.setuid(running_uid)
	except(os.error, e):
		return e
	old_umask = os.umask("077")
	return "root dropped"
def generateEmail():
	emailarg = parsed.email
	if(emailarg =="false"):
		email_name = email_name_list[random.randint(0, len(email_name_list)-1)]
		email_domain = email_domain_list[random.randint(0, len(email_domain_list)-1)]
		return email_name + "@" + email_domain
	else:
		return parsed.email
def generateMAC():
	mac_prefix = mac_prefix_list[random.randint(0, len(mac_prefix_list)-1)]
	mac_suffix = ":" + hex(random.randint(0,255)) + ":" + hex(random.randint(0,255)) + ":" + hex(random.randint(0,255))
	return mac_prefix + mac_suffix.replace ("0x","")
def generateZIP():
	ziparg = parsed.zip
	if(ziparg == "false"):
		return str(random.randint(0,9)) + str(random.randint(0,9)) + str(random.randint(0,9)) + str(random.randint(0,9)) + str(random.randint(0,9))
	else:
		return ziparg
def getInterface():
	return "wlan0"
def changeMac():
	macarg = parsed.mac
	if(macarg == "false"):
		gMac = generateMAC()
	else:
		gMac = macarg
	command = "ifconfig " + getInterface() + " hw ether " + gMac
	try:
		os.system("sudo " + command)
		data = "succeeded MAC change: " + gMac
	except(os.error, e):
		data = e
	return data	
def connectFi():
	try:
		conn = http.client.HTTPSConnection("https://xfinity.nnu.com/xfinitywifi/main", 443)
		params = urllib.parse.urlencode({'@spn_postal': generateZIP(), '@spn_email': generateEmail(), '@spn_terms': 'checked'})
		headers = {"Content-type": "application/x-www-form-urlencoded","Accept": "text/plain"}
		conn.request("POST","",params,headers)
		response = conn.getresponse()
		data = conn.read()
		conn.close()
	except:
		e = sys.exc_info()[0]
		data = e
	return data
ticks = 0
def runD():
	t = ticks
	if(t<600):
		time.sleep(1)
		t += 1
		return t
	return 0
changeMac()
connectFi()
while(True):
	ticks = runD()
	while(ticks==0):
		changeMac()
		connectFi()