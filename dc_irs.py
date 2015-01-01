import bf2
import host
import re
from dc_debug import decho

# for the time command
import time


def init():
	decho('dc_irs: initializing DontCamp.com In-game Report System', 2)
	host.registerHandler('ChatMessage', onChatMessage, 1)
	
def onChatMessage(player_id, text, channel, flags):
	
	# pull the potential prefix off the text line
	text = text.replace("HUD_TEXT_CHAT_TEAM", "")
	text = text.replace("HUD_TEXT_CHAT_SQUAD", "")
	text = text.replace("*\xA71DEAD\xA70*", "")
	
	# unless the first character is ! don't do anything 
	if text[0:1] == "!":
		decho("dc_irs: the first character of %s was !" % text, 5)

		# grab the parts of the chatline I need with a REGEX
		pattern = re.compile(r'!(\w*) ?(.*)')
		matches = pattern.findall(text)
		command = matches[0][0]
		decho("dc_irs: command = %s" % command, 5)  

		# grab a parameter, if any
		if matches[0][1] != "":
			parameter = matches[0][1]
			decho("dc_irs: parameter = %s" % parameter, 5)
		else:
			parameter = None
			decho("dc_irs: no parameter given", 5)

		if command == "nextmap":
			decho('The next map is %s' % host.rcon_invoke('maplist.list').splitlines()[int(host.rcon_invoke('admin.nextLevel').strip())].split()[1].strip('"').replace('_', ' ').title(), 1)
		elif command == "time":
			decho('The time is: %s' % time.strftime('%H:%M %p %Z'), 1)
		else:
			decho('ERROR: invalid command', 1)
