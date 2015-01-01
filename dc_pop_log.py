# DontCamp.com Population Logger
# written by: butter@dontcamp.com
# Revision: $Revision: 1.7 $
#
# This program writes a simple CSV formatted file in a directory under your BF2
# root directory specified by the the 'dir' variable below. A new CSV file will
# be made for each round played. The current CSV file will be called
# population_log.in_progress. The rotated CSV files will have the .in_progress
# extention replaced with a UNIX C timestamp and a .csv.
#
# Each line contains the profile ID, playername IP address, C timestamp, and
# whether the line was written on connect or disconnect. This program has many
# flaws that have yet to be resolved. But it is at least a useful tool for
# gathering profile IDs to use in the DontCamp.com Administrative Support
# System.
#
# To install this, simply drop it into the admin/standard_admin directory of
# your BF2 installation. Edit the admin/standard_admin/__init__.py to include
# these two lines:
#
#     import dc_pop_log
#     dc_pop_log.init()
# 
# Create a directory somewhere under your BF2 root directory and enter the
# relative path from your BF2 root directory to the directory you just created
# in the 'dir' variable below. For example: if your BF2 server is installed in
# /usr/local/bin/bf2 and you want to keep your population logs in
# /usr/local/bin/bf2/dc_pop_logs then the 'dir' variable should equal
# 'dc_pop_logs'.
#
# NOTE: This program requires that dc_debug.py be installed into the
# admin/standard_admin directory as well.
 

import bf2
import host
import time
import os
from bf2 import g_debug
from dc_debug import decho

dir = 'dc_pop_logs'


def init():
	decho('dc_pop_log: initializing DontCamp.com Population Logger', 2)
	host.registerHandler('PlayerConnect', onPlayerConnect, 1)
	host.registerHandler('PlayerDisconnect', onPlayerDisconnect, 1)
	host.registerGameStatusHandler(onStatusChange)
	
def onPlayerConnect(p):
	decho("dc_pop_log: player connected", 5)
	
	id = p.getProfileId()
	name = p.getName()
	ip = p.getAddress()
	timestamp = time.time()
	state = "connected"
	writeLogFile(id, name, ip, timestamp, state)

def onPlayerDisconnect(p):
	decho("dc_pop_log: player disconnected", 5)
	
	id = p.getProfileId()
	name = p.getName()
	ip = p.getAddress()
	timestamp = time.time()
	state = "disconnected"
	writeLogFile(id, name, ip, timestamp, state)

def writeLogFile(id, name, ip, timestamp, state):
	decho( "dc_pop_log: writing that %s %s to population_log.in_progress" % (name, state), 3 )
	
	try:
		fh = open('%s/population_log.in_progress' % dir, 'a')
		fh.write("%d,\"%s\",%s,%d,%s\n" % (id, name, ip, timestamp, state))
		fh.close()
	except:
		decho( 'dc_pop_log: unable to write to %s/population_log.in_progress' % dir, 2 )

def onStatusChange(status):
	decho("dc_pop_log: status handler entered", 5)

	if status == bf2.GameStatus.EndGame:
		decho("dc_pop_log: status == EndGame", 5)
		timestamp = time.time()

		try:
			fh_old = open('%s/population_log.in_progress' % dir, 'r+')
			fh_new = open('%s/population_log.%d.csv' % (dir, timestamp), 'w')

			for line in fh_old:
				fh_new.write(line)

			fh_old.truncate(0)
			fh_old.close()
			fh_new.close()
		except:
			decho( 'dc_pop_log: there was an error trying to "move" the in progress log', 2 )
