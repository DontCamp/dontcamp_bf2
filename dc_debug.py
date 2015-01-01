"""
DontCamp.com Common Debugging Function
written by: butter@dontcamp.com
Revision: $Revision: 1.11 $

Purpose:
    To provide a central way for all DontCamp BF2 python code to output
    debugging and informational text.

Setup: (defaults should work well)

	1. Create a admin/standard_admin/dc_debug.level file and put the debug
	   level you want in the first character of the first line of said file.
	   Valid levels are 1-5.
    2. Set log_to_file to either False or True if you want a seperate dc_debug
       log file for all DontCamp BF2 python code debug output.
    3. Set log_filename to whatever filename and path you like (relative to
       your BF2 home directory). This is only necessary if log_to_file is set
       to True.
    4. Set log_to_stdout to either True or False if you want dc_debug to send
       out its output to the python stdout interface. This is useful if you
       are using BF2CC and want dc_debug's output in the pythonlog.txt file.
"""

import host
import time

try:
	debug_level_fh = open('admin/standard_admin/dc_debug.level', 'r')
	debug_level = int(debug_level_fh.read(1))
	debug_level_fh.close()
	
except:
	debug_level = 5

log_to_file = True
log_filename = 'dc_debug.log'
log_to_stdout = False

def decho(msg, level = 1):
	# 1 = info w/ in-game feedback
	# 2 = info
	# 5 = debug

	if debug_level > 0 and debug_level >= level:
		string = time.strftime('%Y-%m-%d %H:%M:%S') + ' - ' + msg
		
		if log_to_stdout:
			print string
			
		if log_to_file:
			fh = open(log_filename, 'a')
			fh.write(string + '\n')
			fh.close()
				
		if level == 1:
			host.rcon_invoke('game.sayall "%s"' % msg)

def showLevel():
	decho('dc_debug: The current debug level is %d' % debug_level, 2)
