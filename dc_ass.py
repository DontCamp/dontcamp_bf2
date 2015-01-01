"""
DontCamp.com Administrative Support System v. 1.2.1
written by: butter@dontcamp.com

Changelog:
	1.2 beta:
		* added support for multiple arguments in a chat command
		* no longer spews so much to the screen when someone is kicked
	1.1.1 beta:
		* playernames with prefixs can now issue commands
	1.1 beta:
		* added userlevels via a kick points system a la PB power users
		* added general public vote kicking
		* using keyhash rather than PB GUID for auth
		* moved to more OO codebase
		* extensions can now act on anything in the dc_ass object

Acknowledgements:
    Thanks to dst@dontcamp.com for significant coding contributions.
    Thanks to superwabbit@dontcamp.com for his conceptual contributions.
    Thanks to my brother for helping me with fundamental coding concepts.
    Thanks to the guy that was willing to sell me a T40 ThinkPad on eBay for
        that insanely low price!
    Dear God, thanks be to O'Reilly!
    And a REALLY BIG thanks to Kevin Lockitt of blackbagops.com. This software
        is clearly a big stinkin' rip off of BFSM, a program that did as much
        as anything to make DontCamp.com the successful gaming community that
        it is.

Purpose:
    To provide an in-game chat based admin system similar to Kevin Lockitt's
    Battlefield Server Manager while also providing a kick vote system
	similar to PunkBuster's Poweruser system.

Requirements:
    1. dc_debug.py - a common debugging function for all DontCamp.com BF2
       python level tools
    2. dc_ass_extensions.py - this file is currently required to exist but
       can be empty. See dc_ass_extensions Instructions.
    3. dc_ass_cmds.ini - the configuration file for all in-game admin commands
    4. power.dat - a list of your admins' power levels and keyhashs

Known issues:
    1. writeToLogfile() is not currently tested or up-to-date and is therefore
		disabled.
    2. In general be very careful what you code in an extension. The BF2
       server may lag or crash when running poorly written extensions.
    3. dc_ass currently requires punkbuster to be enabled.
    4. There is almost no sanity checking for poorly configured INI files.
    5. Non permanent bans are not maintained between server restarts.

Setup:
    1. Drop dc_ass.py and dc_debug.py into the admin/standard_admin directory
       of your BF2 installation.
    2. Edit admin/standard_admin/__init__.py file to include these lines:

           import dc_ass
           dc_ass.init()

    3. Create an empty dc_ass_extensions.py file or populate it as per the
       dc_ass_extensions instructions below.
    4. Create a power.dat file as per the instructions below.
    5. Create / edit a dc_ass_cmds.ini file as per the instructions below.

power.dat Instructions:
	This file is simply a space delimited file with two values on each line
	that must exist in the admin/standard_admin directory. The first value is
	the power level assignment and the second value is the keyhash.

	Currently dc_ass is lacking some flexibily in that 10 kick points always
	causes a player to be kicked. Keep that in mind when assigning power
	levels.	The power level must be a positive integer but can otherwise be
	whatever you like.

	The keyhash for a user is a 32 digit hexidecimal number that be found when
	executing admin.listplayers in the console. I have written a dc_ass
	extensions that prints the keyhash for a user while in-game and I will like
	make that extensions available in the future. Please note that BF2
	keyhashes are NOT the same thing as PB GUID's.

    An example power.dat file:

	10 352a507c78da1dea6dd42a5867d3c2cc
	4 2365c8ef755723efc10b425fffb65ebe

	This examples shows that the player with the keyhash:
	352a507c78da1dea6dd42a5867d3c2cc can apply 10 kick points to each player
	and that the player with the keyhash: 2365c8ef755723efc10b425fffb65ebe can
	apply 4 kick points to each player.
	
	Since 10 kick points kicks a user, we can assume that any admin with a
	kick power of 10 is a full admin and therefore they can run "admin"
	commands. See the section on the dc_ass_cmds.ini file for more info.
	
dc_ass_cmds.ini Instructions:
    This file follows standard INI file formatting. Each section name is the
    name of a command that can be run from in-game text chat. Each section
    must have a "type" option. Supported types are:
        kick - a simple kick
        ban - a permanent ban (or possibly temporary)
        rcon - user defined rcon command execution
        extension - user defined python function execution

    Depending on the type, different options are required. Each type supports
    the "admin" option. When admin = 1, the user must have a kick power of 10
    to execute that command. When admin = 0, any user on your BF2 server is
	allowed to execute that command. The admin option is optional and defaults
	to 1.

    (* = required)
    Type: kick
    Options:
        *reason = (a non-delimited string contained the reason for this kick)
        length = (an integer representing how many minutes before the
            the offender will be allowed back into the game. If this option is
            missing, the default value will be 2.)
    Type: ban
    Options:
        *reason = (same as above)
        length = (same as above) (see known issue #5)

    Type: rcon
    Options:         
        *command = (a non-delimited string contained the rcon command you want
            to issue)

    Type: extension
    Options:
        *function = (the name of the function in dc_ass_extensions.py you want
            this command to run WITHOUT any (). See dc_ass_extensions
             Instructions.)

    An example dc_ass_cmds.ini file might look like this:

        [kfms]
        type = kick
        reason = for firing from a vehicle in/into an uncapturable spawn
        length = 5

        [brsc]
        type = ban
        reason = for a racist or slanderous comment

        [restart]
        type = rcon
        command = admin.restartmap

        [slap]
        type = extension
        function = slapPlayer

        [nextmap]
        type = extension
        function = sayNextMap
        admin = 0

    NOTE: Changes made to the dc_ass_cmds.ini file are in effect immediately
    and do not require a server restart.

dc_ass_extensions.py Instructions:
    The extensions provide a means to do more complex actions that cannot be
    achieved through a simple rcon command. This file works similarly to other
    python files inside the BF2 environment. It's simply a list of functions
    as well as the proper imports to provide the facility the functions
    require.

    NOTE: Each function that is run as an extension must accept one and only
    one parameter. That parameter will be the dc_ass admin object most noteably
	containing these properties:
	
	victim_id - a list of all integers of the victim IDs found via the
		parameter for this the command executed
		
	victim_tracker - a dictionary of all the people currently being tracked
		by dc_ass (in other words, people that have had kick points issued
		against	them). This is a multidemensional dictionary where the top
		level key is the player_id / slot number and value is another
		dictionary where the key is the keyhash of the issuer of the points and
		the value is the number of points issued by said issuer.
	
	issuer - an integer representing the player_id of the person that executed
		the current command.
		
    keyhash - a string that is the hexidecimal keyhash of the person that
		executed the current command.

	See http://dontcamp.com/code/ for an example dc_ass_extenions.py file.

    Note: Changes made to the dc_ass_extensions.py file are in effect
        immediately and do not require a server restart.

How to use all this once you've got it setup:
    All commands are issued with in-game chat, NOT console commands. To my
    knowledge, these commands should work in any chat mode. Each command MUST
    be prefixed with an ! and optionally suffixed with a space followed by a 
    case insensitive playername, partial playername, or a . followed by a
    player number. Additionally, you may prefex an @ in front of a case
    insensitive string to execute an action against all players containing
    that string in their playername. You may also use a % followed by a team
    number to execute a command against an entire team.

    Using our previous example INI file and given that the server has two
    players on it: Butter (in slot 0) and MuttDog (in slot 1) here's how the
    following commands would react...

        !kfms
            [ Whenever no parameter for a victim is given, dc_ass will
              assume the player ID of the admin issuing the command. In this
              case the admin will be kicked for 5 minutes for firing into
              a main spawn. ]

        !kfms .0
            [ This will kick Butter for 5 minutes for firing into a main spawn
              because butter is player number 0 / in slot 0. ]

        !kfms butter
            [ This will also kick Butter because butter matches Butter in our
              case insensitive string comparison. ]

        !kfms ter
            [ This will also kick Butter because ter is a string match in
              Butter's name and ONLY in Butter's name. ]

        !kfms utt
            [ This will kick no one but print a global message in green at the
              top left of the screen that utt is ambiguous. ]

        !kfms dst
            [ This will kick no one and print a global message saying "Could
              not find ID for dst". ]

        !kfms @t
            [ This will kick both dst and butter as they both have a t in their
              their playername. ]

        !kfms @T
            [ This will still kick both dst and butter because our text search
              is case insensitive. ]

        !kfms %2
            [ This will kick everyone on team 2. ]
"""


import bf2
import host
import re
import ConfigParser
import time
from dc_debug import decho
from dc_debug import showLevel
import dc_ass_extensions

class ass:
	# some init vars
	victim_tracker = {}
	admin_level = 10
	default_weight = 2
	kick_threshold = 10

	"""
		_getPlayerList(): returns a dictionary of players currently playing
		where the key is their player player_id/index and the value is list
		containing their playername, IP, outbound port, and CD-key hash.
		Thanks to Woody for doing all the hard work on this one.
	"""
	def _getPlayerList(self):
		rawData = host.rcon_invoke( 'admin.listplayers' )
		# this patern is for line 0 of the output for each player
		# pattern1 = re.compile(r'''^Id:\ +(\d+)\ -\ (\S+)\ is\ remote\ ip:\ (\d+\.\d+\.\d+\.\d+):(\d+)''', re.VERBOSE)
		pattern1 = re.compile(r'''^Id:\ +(\d+)\ -\ (.*?)\ is\ remote\ ip:\ (\d+\.\d+\.\d+\.\d+):(\d+)''', re.VERBOSE)
		# this patern is for line 1 of the output for each player
		pattern2 = re.compile(r'''(?:.*hash:\ (\w{32}))?''', re.VERBOSE)
		players = {}
		
		i = 0
		for line in rawData.split("\n"):
			# if we're looking at a "line 0"
			if i == 0:
				matches = pattern1.findall(line)
				if len(matches) != 0:
					p_id = int(matches[0][0])
					players[p_id] = []
					players[p_id].append(matches[0][1])
					players[p_id].append(matches[0][2])
					players[p_id].append(matches[0][3])

			# if we're looking at a "line 1"
			elif i == 1:
				matches = pattern2.findall(line)
				players[p_id].append(matches[0])

			# flop the value of the iter
			i ^= 1
		
		return players


	"""
		_getWeight(): finds the admin level of the user at index
		returns true on success, false on failure (the true case being that a user is found at index)
		assigns string self.keyhash as the keyhash of the user at index
		assigns int self.user_weight as the admin level of the user at index
	"""
	def _getWeight(self, index):
		return_value = False
		players = self._getPlayerList()
		self.user_weight = self.default_weight

		if players.has_key(index):
			return_value = True
			self.keyhash = players[index][3]
			# assigns the default weight in case this user is not found in the pbpower.dat file
			decho( "dc_ass: Attempting to authenticate keyhash: %s" % self.keyhash, 5 )

			# just in case there is no pbpower.dat file
			try:
				for line in open('admin/standard_admin/power.dat', 'r'):
					if self.keyhash == line.split(' ')[1].strip():
						self.user_weight = int(line.split(' ')[0].strip())
						decho( "dc_ass: %s is level %d in power.dat!" % (self.keyhash, self.user_weight), 5 )
						break

			except IOError:
				decho( "dc_ass: unable to open pb/pbpower.dat file", 5 )

		return return_value


	"""
		_getVictimId(): finds all victims from the in-game chat command parameter
		returns true on success and false on failure (the failure case is not being able to determine with certainly which victims the command is for)
		assigns list self.victim_id
	"""
	def _getVictimId(self, parameter):
		# returns true/false on success/failure and assigns self.victim_id if possible
		# self.victim_id is a list of all victims found
		# sorry for the silly parameter name, but it does make sense in this case.

		self.victim_id = []
		result = False # default value for result
		decho("dc_ass: Attempting to find victim ID...", 5)
		
		# if the parameter is the player number
		if parameter[0:1] == ".":
			id = int(parameter[1:])
	
			for p in bf2.playerManager.getPlayers():
				if p.index == id:
					self.victim_id = [id]
					decho( "dc_ass: parameter was an int, and id = %d" % self.victim_id[0], 5 )
					result = True	
					break

			if not result:
				decho( "dc_ass: (ERROR) no player found with ID: %d" % id, 1 )
			
		# if the parameter is a wildcard / clantag
		elif parameter[0:1] == "@":
			decho( "dc_ass: finding ALL matching players with parameter...", 5 )
			decho( "dc_ass: parameter was NOT an int", 5 )

			# for all players connected...
			for p in bf2.playerManager.getPlayers():
				decho( "dc_ass: checking player: %s" % p.getName(), 5 )
				# if we find a name that loosely matches...
				if p.getName().lower().find( parameter[1:].lower() ) != -1:
					decho( "dc_ass: %s loosely matches %s" % ( parameter[1:], p.getName() ), 5 )
					self.victim_id.append(p.index)
					result = True

			if result:
				decho( "dc_ass: Victim ID(s) found @ %r" % self.victim_id, 5 )
			else:
				decho( "dc_ass: (ERROR) no players found with %s in their name" % parameter[1:], 1 )
		
		# if the parameter is a team number
		elif parameter[0:1] == "%":
			decho( "dc_ass: finding ALL matching players on team matching paramenter...", 5 )
			
			# for all players connected...
			for p in bf2.playerManager.getPlayers():
				decho( "dc_ass: checking player: %s" % p.getName(), 5 )
				# if we find a player on the team supplied
				if p.getTeam() == int(parameter[1:]):
					decho( "dc_ass: %s is on team %s" % ( p.getName(), p.getTeam() ), 5 )
					self.victim_id.append(p.index)
					result = True				

			if result:
				decho( "dc_ass: Victim ID(s) found @ %r" % self.victim_id, 5 )
			else:
				decho( "dc_ass: (ERROR) there seems to be no one on team %s" % parameter[1:], 1 )
					
		# if the parameter is a playername or partial playername
		else:
			id = -1
			decho("dc_ass: parameter was NOT an int", 5)
			# for all players connected...
			for p in bf2.playerManager.getPlayers():
				decho( "dc_ass: checking player: %s" % p.getName(), 5 )
				# if we find a name that loosely matches...
				if p.getName().lower().find( parameter.lower() ) != -1:
					decho( "dc_ass: %s loosely matches %s" % ( parameter, p.getName() ), 5 )
					# if this is the first victim we've found...
					if id == -1:
						decho("dc_ass: found %s in %s" % ( parameter, p.getName() ), 5)
						id = [int(p.index)]
						result = True
					# if we've gotten another possible match...
					else:
						result = False
						break

			if result:
				self.victim_id = id
				decho( "dc_ass: Victim ID found @ %d" % self.victim_id[0], 5 )
			else:
				decho( "dc_ass: %s is ambiguous." % parameter, 1 )

		return result

	"""
	def writeLogFile(self, victim_id, admin_id, type, reason, length):
		v = bf2.PlayerManager.Player(victim_id)
		a = bf2.PlayerManager.Player(admin_id)
		decho("\"%s\",%s,%d,%s,%d,%s,%s,%d,%s\n" % (v.getName(), v.getAddress(), v.getProfileId(), a.getName(), int(time.time()), bf2.gameLogic.getMapName(), type, reason, length * 60), 5)

		fo = open('admin/standard_admin/adminlog.csv', 'a')
		# v.name, v.ip, v.profileId, a.name, timestamp, map, type, length, reason
		fo.write("\"%s\",%s,%d,%s,%d,%s,%s,%d,%s\n" % (v.getName(), v.getAddress(), v.getProfileId(), a.getName(), int(time.time()), bf2.gameLogic.getMapName(), type, reason, length * 60))
		fo.close()
	"""


	"""
		_stripPrefix(): removes context prefixes from a chati lines and returns the trimmed chat line
	"""
	def _stripPrefix(self, text):
		text = text.replace( "HUD_TEXT_CHAT_TEAM", "" )
		text = text.replace( "HUD_TEXT_CHAT_SQUAD", "" )
		text = text.replace( "HUD_CHAT_DEADPREFIX", "" )
		text = text.replace( "*\xA71DEAD\xA70*", "" )

		return text.strip()


	def addPoints(self):
		# add entries in the victim_tracker foreach victim
		for v_id in self.victim_id:
			# check to see if we're already tracking the joker
			if self.victim_tracker.has_key(v_id):
				decho( "dc_ass: already tracking %d" % v_id, 5 )
				# check to see if this admin has already applied their weight to the victim
				if not self.victim_tracker[v_id].has_key(self.keyhash):
					self.victim_tracker[v_id][self.keyhash] = self.user_weight
					# added this conditional to make it a bit less noisy when someone is just kicked with one action
					if self.user_weight < self.kick_threshold:
						decho( "dc_ass: applied %d points from %s to player %d" % (self.user_weight, self.keyhash, v_id), 5 )
				# this elif was really added to deal with an extension used at DontCamp.com but it makes sense to have anyway
				elif self.user_weight == self.kick_threshold:
					self.victim_tracker[v_id][self.keyhash] = self.user_weight
				else:
					decho( "dc_ass: %s has already applied their points to %s" % (bf2.PlayerManager.Player(self.issuer).getName(), bf2.PlayerManager.Player(v_id).getName()), 1 )
			else:
				self.victim_tracker[v_id] = {}
				decho( "dc_ass: now tracking player: %d" % v_id, 5 )
				self.victim_tracker[v_id][self.keyhash] = self.user_weight
				decho( "dc_ass: applied %d points from %s to player %d" % (self.user_weight, self.keyhash, v_id), 5 )


	def checkPoints(self):
		for index, tracking in self.victim_tracker.iteritems():
			# reset total_points for this victim
			total_points = 0

			# added up all the points being applied to this victim
			for unused_key, points in tracking.iteritems():
				total_points += points	
				
			if index in self.victim_id:
				decho( "dc_ass: %s now has %d of %d kick points" % (bf2.PlayerManager.Player(index).getName(), total_points, self.kick_threshold), 1 )

			if total_points >= self.kick_threshold:
				self.reason += " - see dontcamp.com/forums for discussion"
				# issue the kick command
				decho( "dc_ass: Kicking player '%s' (%d) %s" % (bf2.PlayerManager.Player(index).getName(), index, self.reason), 1 ) 
				unused = host.rcon_invoke('pb_sv_kick %d %d %s' % (index + 1, self.length, self.reason) )

	# it might be helpful to create a new object to pass to extensions that
	# has a reference to the admin object. In that new object, that I hope
	# would only exist during the execution of a command, things like the
	# issuer and keyhash properties could be assigned.
	def onChatMessage(self, player_id, text, channel, flags):
		self.issuer = player_id
		# pull the potential prefix off the text line
		text = self._stripPrefix(text)
		
		# unless the first character is ! don't do anything 
		if text[0:1] == "!":
			decho( "dc_ass: the first character of %s was !" % text, 5 )

			# As BF2 playernames cannot contain spaces except what is printed
			# between the prefix and the name, it is probably safe to assume
			# that we don't need to accept spaces in playernames for this
			# parameter. Therefore, I could use the space as a separator
			# between the victim name and another command parameter, like
			# a custom reason.

			# grab the parts of the chatline I need with a REGEX
			pattern = re.compile(r'!(\w*) ?(\S*) ?(.*)')
			matches = pattern.findall(text)
			command = matches[0][0]
			# set an arguments property for future use or for extensions
			self.arguments = matches[0][2]
			decho( "dc_ass: command = %s" % command, 5 )  

			# in case the command doesn't require a victim parameter...
			if matches[0][1] != "":
				parameter = matches[0][1]
				decho( "dc_ass: parameter = %s" % parameter, 5 )
			else:
				parameter = None
				decho( "dc_ass: no parameter given", 5 )

			try: # read in the commands INI file
				self.config = ConfigParser.ConfigParser()
				self.config.read('admin/standard_admin/dc_ass_cmds.ini')

				# is this a defined command in the INI file
				if command in self.config.sections():
					decho( "dc_ass: Command found in INI file!", 5 )
					# define/declare some vars for this admin event (I really wouldn't need to do this if I know how to check if a var is defined or even exists
					type = ""
					# these values will be members of the object because they may be needed in an extension
					self.length = 2 # the default length for a kick
					self.reason = ""
					admin = 1 # this makes all commands default to requiring admin privs

					# get all possible options
					# I could add sanity checks in here for poorly formated lines in the INI file
					for option in self.config.options(command):
						if option == "type":
							type = self.config.get(command, option).strip()
						elif option == "reason":
							self.reason = self.config.get(command, option).strip()
						elif option == "length":
							self.length = int(self.config.get(command, option))
						elif option == "command":
							rcon_string = self.config.get(command, option).strip()
						elif option == "admin":
							admin = int(self.config.get(command, option))
						elif option == "function":
							function = self.config.get(command, option).strip()

					# make sure we have a type
					if type == "":
						decho( "dc_ass: (ERROR) No type value for %s in dc_ass_cmds.ini file!" % command, 1 )
					
					# good, we're all set
					else:
						decho( "dc_ass: type: %s" % type, 5 )

						# to get their keyhash and admin level
						if self._getWeight(player_id):

							# see if we can/need to get a victim ID to move forward
							if ( parameter != None and self._getVictimId(parameter) ) or parameter == None:

								# for non-perma bans, change type to kick_ban - this will be useful when we start to log this stuff
								if type == "ban" and self.length != "":
									decho( "dc_ass: Length value given for ban. Converting type to kick_ban.", 5 )
									type = "kick_ban"

								# if no parameter was given, make the command reflect on the issuer
								if parameter == None:
									decho( "dc_ass: No parameter given... assigning victim_id to issuer.", 5 )
									self.victim_id = [player_id]

								if ( admin and self.user_weight == self.admin_level ) or not admin:

									# the main switch like section that gets the shit done (if only I had switches)
									# Are reasons optional in these PB kicks/bans? If so, I guess I don't need to worry about sanity checking them

									if type == "kick" or type == "kick_ban":
										self.addPoints()
										self.checkPoints()

									elif type == "ban":
										for v_id in self.victim_id:
											decho( "dc_ass: Banning player '%s' (%d) %s" % (bf2.PlayerManager.Player(v_id).getName(), v_id, self.reason), 1 ) 
											unused = host.rcon_invoke( 'pb_sv_ban %d %s' % (v_id + 1, self.reason) )
			
									elif type == "rcon":
										decho( "dc_ass: Running rcon command: %s" % rcon_string, 2 )
										unused = host.rcon_invoke( rcon_string )
			
									elif type == "extension":
										reload( dc_ass_extensions )
										if function in dc_ass_extensions.__dict__:
											decho( "dc_ass: executing %s() extension" % function, 2 )
											# send the entire object to the extensions
											exec( "dc_ass_extensions.%s(%s)" % (function, "self") )
										else:
											decho( "dc_ass: %s() extension not found." % function, 2 )

									else:
										decho( "dc_ass: No such type: %s" % type, 1 )

								else:
									decho ( "dc_ass: User in slot %d is not authorized for the requested action" % player_id, 1 )

							else:
								decho( "dc_ass: Victim ID not findable given the parameter", 2 )

						else:
							decho( "dc_ass: ERROR failed to get keyhash for player: %d" % player_id, 1 )
								
				else: # end of is command in INI file conditional
					decho( "dc_ass: (ERROR) %s command not found!" % command, 1 )
		
			except IOError:
				print "dc_ass: (FATAL ERROR) could not open one or more required files: (admin_profile_ids.csv | dc_ass_cmds.ini)"

		else: # a debug line just so I can see all the chat if I need to
			decho( "dc_ass: player %d: %s" % (player_id, text), 5 )
			
	def onPlayerDisconnect(self, p):
		# if they disconnect, which might have happened if they were kicked, drop them from the tracker, if they're even in it
		if self.victim_tracker.has_key(p.index):
			del(self.victim_tracker[p.index])
			decho( "dc_ass: player %d disconnected and no longer tracked" % p.index, 2 )

admin = ass()

def init():
	decho('dc_ass: initializing DontCamp.com Admin Support System', 2)
	host.registerHandler('ChatMessage', admin.onChatMessage, 1)
	host.registerHandler('PlayerDisconnect', admin.onPlayerDisconnect, 1)
	showLevel()
