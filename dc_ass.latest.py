"""
DontCamp.com Administrative Support System v. 1.3
written by: butter@dontcamp.com
Revision: $Revision: 1.30 $

Changelog:
	1.1.2:
		* changed the ass class layout significantly to make better use of
		  a branched object structure
		* broke logic into more functions to make extensions both easier to write
		  and more powerful
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
    the "level" option. The level option dictates what a user's minimum level
	must be in order to execute the command in question. The admin option is
	optional and defaults to whatever the adminLevel var is set to.

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
        level = 0

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
	
	victimID - a list of all integers of the victim IDs found via the
		parameter for this the command executed
		
	victimTracker - a dictionary of all the people currently being tracked
		by dc_ass (in other words, people that have had kick points issued
		against	them). This is a multidemensional dictionary where the top
		level key is the player_id / slot number and value is another
		dictionary where the key is the keyhash of the issuer of the points and
		the value is a dictionary with the self explainitory keys: points and
		reason.
	
	issuer - an object representing the issuer of the person that executed
		the current command. The typical properties you'll see for this object
		are index and keyhash

	command - an object containing various properties for the command being
		issued. Commmand properties are: string, arguments, type, length,
		reason, function, level, rconString, extension

	config - this is the INI config file object for dc_ass
		
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

class container:
	pass

class ass:
	# some init vars
	victimTracker = {}
	adminLevel = 10
	defaultLevel = 2
	kickThreshold = 10

	"""
		getPlayerList(): returns a dictionary of players currently playing
		where the key is their player player_id/index and the value is list
		containing their playername, IP, outbound port, and CD-key hash.
		Thanks to Woody for doing all the hard work on this one.
	"""
	def getPlayerList(self):
		decho('dc_ass: entering getPlayerList() method', 5)
		rawData = host.rcon_invoke( 'admin.listplayers' )
		# this pattern is for line 0 of the output for each player
		# pattern1 = re.compile(r'''^Id:\ +(\d+)\ -\ (\S+)\ is\ remote\ ip:\ (\d+\.\d+\.\d+\.\d+):(\d+)''', re.VERBOSE)
		pattern1 = re.compile(r'''^Id:\ +(\d+)\ -\ (.*?)\ is\ remote\ ip:\ (\d+\.\d+\.\d+\.\d+):(\d+)''', re.VERBOSE)
		# this pattern is for line 1 of the output for each player
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
		
		decho( 'dc_ass: exiting getPlayerList() method', 5 )
		return players


	def getMapList(self):
		rawData = host.rcon_invoke( 'maplist.list' )
		pattern = re.compile('(\d+): "(\S*?)" (\S*) (\d+)')
		# init the mapList
		mapList = {}

		for line in rawData.split("\n"):
			matches = pattern.findall(line)
			if len(matches) != 0:
				mapID = int(matches[0][0])
				mapList[mapID] = {'name':matches[0][1], 'gpm':matches[0][2], 'size':matches[0][3]}
					
		return mapList

	
	"""
		getKeyhashFromIndex(): find the keyhash of the user at index
		returns a 32-digit hex string that is the user's keyhash at index
		returns False on failure
	"""
	def getKeyhashFromIndex(self, index):
		decho( 'dc_ass: entering getKeyhashFromIndex() method', 5 )
		# make False the default return value
		returnValue = False
		# get a list of players connected right now
		players = self.getPlayerList()

		# is our index in this list of players?
		if players.has_key(index):
			# grab their keyhash
			returnValue = players[index][3]
			
		decho( 'dc_ass: exiting getKeyhashFromIndex() method', 5 )
		return returnValue


	"""
		getLevelFromIndex(): finds the admin level of the user at index
		returns a 2 element tuple with the admin level and keyhash of the user at index
		returns false on failure
	"""
	def getLevelFromIndex(self, index):
		decho( 'dc_ass: entering getLevelFromIndex() method', 5 )
		# make False the default return value
		returnValue = False

		# grab their keyhash
		keyhash = self.getKeyhashFromIndex(index)
		if keyhash:
			decho( 'dc_ass: Attempting to authenticate keyhash: %s' % keyhash, 5 )
			# just in case there is no pbpower.dat file
			try:
				# loop through each line looking for their keyhash
				for line in open('admin/standard_admin/power.dat', 'r'):
					if keyhash == line.split(' ')[1].strip():
						# assign their level
						userLevel = int(line.split(' ')[0].strip())
						decho( 'dc_ass: %s is level %d in power.dat!' % (keyhash, userLevel), 5 )
						break
			except IOError:
				decho( 'dc_ass: unable to open pb/pbpower.dat file', 5 )
				userLevel = None

			returnValue = (userLevel, keyhash)

		decho( 'dc_ass: exiting getLevelFromIndex() method', 5 )
		return returnValue

	"""
		getVictimIDs(): finds all victims from the in-game chat command parameter
		returns true on success and false on failure (the failure case is not being able to determine with certainly which victims the command is for)
		assigns list self.victimID
	"""
	def getVictimIDs(self, string):
		decho( 'dc_ass: entering getVictimIDs() method', 5 )
		# init/destory the old victim list
		self.victimID = []
		# default value for result
		result = False 
		decho( 'dc_ass: Attempting to find victim ID...', 5 )
		
		# if the string is the player number
		if string[0:1] == '.':
			id = int(string[1:])
	
			for p in bf2.playerManager.getPlayers():
				if p.index == id:
					self.victimID = [id]
					decho( 'dc_ass: string was an int, and id = %d' % self.victimID[0], 5 )
					result = True	
					break

			if not result:
				decho( 'dc_ass: (ERROR) no player found with ID: %d' % id, 1 )
			
		# if the string is a wildcard / clantag
		elif string[0:1] == '@':
			decho( 'dc_ass: finding ALL matching players with string...', 5 )
			decho( 'dc_ass: string was NOT an int', 5 )

			# for all players connected...
			for p in bf2.playerManager.getPlayers():
				decho( 'dc_ass: checking player: %s' % p.getName(), 5 )
				# if we find a name that losely matches...
				if p.getName().lower().find( string[1:].lower() ) != -1:
					decho( 'dc_ass: %s losely matches %s' % ( string[1:], p.getName() ), 5 )
					self.victimID.append(p.index)
					result = True

			if result:
				decho( 'dc_ass: Victim ID(s) found @ %r' % self.victimID, 5 )
			else:
				decho( 'dc_ass: (ERROR) no players found with %s in their name' % string[1:], 1 )
		
		# if the string is a team number
		elif string[0:1] == '%':
			decho( 'dc_ass: finding ALL matching players on team %s' % string[1:], 5 )
			
			# for all players connected...
			for p in bf2.playerManager.getPlayers():
				decho( 'dc_ass: checking player: %s' % p.getName(), 5 )
				# if we find a player on the team supplied
				decho( 'dc_ass: %s is on team %d' % ( p.getName(), p.getTeam() ), 5 )
				if p.getTeam() == int(string[1:]):
					self.victimID.append(p.index)
					result = True				

			if result:
				decho( 'dc_ass: Victim ID(s) found @ %r' % self.victimID, 5 )
			else:
				decho( 'dc_ass: (ERROR) there seems to be no one on team %s' % string[1:], 1 )
					
		# if the string is a playername or partial playername
		else:
			# set a centinal value for id so we know if we've found anyone yet
			id = -1
			decho( 'dc_ass: string was NOT an int', 5)
			# for all players connected...
			for p in bf2.playerManager.getPlayers():
				decho( 'dc_ass: checking player: %s' % p.getName(), 5 )
				# if we find a name that loosely matches...
				if p.getName().lower().find( string.lower() ) != -1:
					decho( 'dc_ass: %s loosely matches %s' % ( string, p.getName() ), 5 )
					# if this is the first victim we've found...
					if id == -1:
						decho( 'dc_ass: found %s in %s' % ( string, p.getName() ), 5)
						id = [int(p.index)]
						result = True
					# if we've gotten another possible match...
					else:
						result = False
						break

			if id != -1:
				if result:
					self.victimID = id
					decho( 'dc_ass: Victim ID found @ %d' % self.victimID[0], 5 )
				else:
					decho( 'dc_ass: %s is ambiguous.' % string, 1 )
			else:
				decho( "dc_ass: (ERROR) no players were found against: '%s'" % string, 1 )

		decho( 'dc_ass: exiting getVictimIDs() method', 5 )
		return result


	"""
	def writeLogFile(self, victimID, admin_id, type, reason, length):
		v = bf2.PlayerManager.Player(victimID)
		a = bf2.PlayerManager.Player(admin_id)
		decho("\"%s\",%s,%d,%s,%d,%s,%s,%d,%s\n" % (v.getName(), v.getAddress(), v.getProfileId(), a.getName(), int(time.time()), bf2.gameLogic.getMapName(), type, reason, length * 60), 5)

		fo = open('admin/standard_admin/adminlog.csv', 'a')
		# v.name, v.ip, v.profileId, a.name, timestamp, map, type, length, reason
		fo.write("\"%s\",%s,%d,%s,%d,%s,%s,%d,%s\n" % (v.getName(), v.getAddress(), v.getProfileId(), a.getName(), int(time.time()), bf2.gameLogic.getMapName(), type, reason, length * 60))
		fo.close()
	"""


	"""
		stripPrefix(): removes context prefixes from a chati lines and returns the trimmed chat line
	"""
	def stripPrefix(self, text):
		decho('dc_ass: entering stripPrefix() method', 5)
		text = text.replace( 'HUD_TEXT_CHAT_TEAM', '' )
		text = text.replace( 'HUD_TEXT_CHAT_SQUAD', '' )
		text = text.replace( 'HUD_CHAT_DEADPREFIX', '' )
		text = text.replace( "*\xA71DEAD\xA70*", '' )

		decho('dc_ass: exiting stripPrefix() method', 5)
		# in later versions of BF2 we sometimes saw extra white space in the
		# chat text
		return text.strip()

	"""
		splitArguments(): splits a string into separate arguments
		returns a list of all space, double quote, or single quote string
	"""
	def splitArguments(self, string):
		# init the return list
		returnValue = []

		# string can == None if there are no arguments
		if string != None:
			# init the iterator
			i = 0
			# grab the length of the arguments string
			length = len(string)

			while i < length:
				# handle strings inside ""
				if string[i] == '"':
					# advance the iter past the "
					i += 1
					# find the next "
					nextMark = string[i:].find('"')
					# if we didn't find another " grab the rest of the string
					if nextMark == -1:
						returnValue.append(string[i:])
						break
					else:
						# grab the string inside the ""
						returnValue.append(string[i:i + nextMark])
						# advance the iter past the second "
						i = i + nextMark + 1
				# handle strings inside ''
				elif string[i] == "'":
					i += 1
					nextMark = string[i:].find("'")
					if nextMark == -1:
						returnValue.append(string[i:])
						break
					else:
						returnValue.append(string[i:i + nextMark])
						i = i + nextMark + 1
				# handle other space separated strings
				else:
					nextMark = string[i:].find(' ')
					if nextMark == -1:
						returnValue.append(string[i:])
						i = length
					else:
						returnValue.append(string[i:i + nextMark])
						i = i + nextMark + 1

		return returnValue


	"""
		addPoints(): adds points to the tracker from the issuer to the players @ self.victimID
		returns true if points were added and false if not
	"""
	def addPoints(self):
		decho( 'dc_ass: entering addPoints() method', 5 )
		# set the default returnValue
		returnValue = False

		# add entries in the victimTracker foreach victim
		for vID in self.victimID:
			# check to see if we're already tracking the joker
			if self.victimTracker.has_key(vID):
				decho( 'dc_ass: already tracking %d' % vID, 5 )
				# check to see if this admin has already applied their level to the victim
				if not self.victimTracker[vID].has_key(self.issuer.keyhash):
					if self.manageTracker(vID, self.issuer.keyhash, self.issuer.level, self.command.reason):
						decho( 'dc_ass: applied %d points from %s to player %d' % (self.issuer.level, self.issuer.keyhash, vID), 5 )
						returnValue = True
				# this elif was really added to deal with an extension used at DontCamp.com but it makes sense to have anyway
				# this elif allows an admin to apply their kick points even if they have already
				elif self.issuer.level == self.adminLevel:
					if self.manageTracker(vID, self.issuer.keyhash, self.issuer.level, self.command.reason):
						returnValue = True
				else:
					decho( 'dc_ass: %s has already applied their points to %s' % (bf2.PlayerManager.Player(self.issuer.index).getName(), bf2.PlayerManager.Player(vID).getName()), 1 )
			elif self.manageTracker(vID, self.issuer.keyhash, self.issuer.level, self.command.reason):
					decho( 'dc_ass: applied %d points from %s to player %d' % (self.issuer.level, self.issuer.keyhash, vID), 5 )
					returnValue = True

		decho( 'dc_ass: exiting addPoints() method', 5 )
		return returnValue

	"""
		manageTracker(): changes/adds/removes points given by 'keyhash' to 'victimID' via 'delta' and 'reason'
		returns true is any points were successfully applied
		returns false if no points were applied
	"""
	def manageTracker(self, victimID, keyhash, delta, reason):
		decho( 'dc_ass: entering manageTracker() method', 5)
		returnValue = True
		# if they're not already being tracked...
		if not self.victimTracker.has_key(victimID):
			self.victimTracker[victimID] = {}
			decho( 'dc_ass: now tracking player: %d' % victimID, 5 )

		# has this keyhash already applied their points?
		if self.victimTracker[victimID].has_key(keyhash):
			# apply the delta
			self.victimTracker[victimID][keyhash]['points'] += delta
			# if the resulting delta totally removes this keyhash points then delete the keyhash from their tracker
			if self.victimTracker[victimID][keyhash]['points'] <= 0:
				del(self.victimTracker[victimID][keyhash])
		# if this keyhash HAS NOT already applied their points, only if the delta is > 0 should we even touch the tracker
		elif delta > 0:
			self.victimTracker[victimID][keyhash] = {'points': delta, 'reason': reason}
		else:
			decho( 'dc_ass: no action taken where issuer points <= 0', 2)
			returnValue = False

		decho( 'dc_ass: exiting manageTracker() method', 5)
		return returnValue
		

	"""
		getPointsFromIndex(): returns total accumlative points against player at index
		returns 0 if player at index is not being tracked
	"""
	def getPointsFromIndex(self, index):
		decho( 'dc_ass: entering getPointsFromIndex() method', 5 )
		# set default returnValue
		returnValue = 0

		# is this player index being tracked?
		if self.victimTracker.has_key(index):
			# init value for totalPoints
			totalPoints = 0

			for unusedKey, record in admin.victimTracker[index].iteritems():
				totalPoints += record['points']

			returnValue = totalPoints

		decho( 'dc_ass: exiting getPointsFromIndex() method', 5 )
		return returnValue


	"""
		checkPoints(): checks to see if anyone being tracked has acculated enough points to be kicked
		returns nothing! You son of a bitch!
	"""
	def checkPoints(self):
		decho('dc_ass: entering checkPoints() method', 5)
		for index, tracking in self.victimTracker.iteritems():
			# reset totalPoints for this victim (as we loop through them)
			# this variable hold the accumlative value of all points so far applied to a player
			totalPoints = self.getPointsFromIndex(index)

			# if we see any of our victims here lets print to the screen that they have new and shiny points
			if index in self.victimID:
				decho( 'dc_ass: %s now has %d of %d kick points' % (bf2.PlayerManager.Player(index).getName(), totalPoints, self.kickThreshold), 1 )

			if totalPoints >= self.kickThreshold:
				# issue the kick command
				decho( "dc_ass: Kicking player '%s' (%d) %s" % (bf2.PlayerManager.Player(index).getName(), index, self.command.reason), 1 ) 
				# need to change this to show them ALL the reasons they were kicked
				unused = host.rcon_invoke('pb_sv_kick %d %d %s' % (index + 1, self.command.length, self.command.reason) )

		decho('dc_ass: exiting checkPoints() method', 5)
	

	"""
		processPoints(): this function simply executes checkPoints() conditionally on executing addPoints()
		this can simplify extension code as before you must have called both addPoints and checkPoints you
		can now call only processPoints()
		returns nothing
	"""
	def processPoints(self):
		decho( 'dc_ass: entering processPoints() method', 5 )
		if self.addPoints():
			self.checkPoints()

		decho( 'dc_ass: exiting processPoints() method', 5 )


	"""
		prepExec(): returns true on success and false on failure
		finds the issuer's admin level and keyhash and ensures that the issuer has rights
		to execute the command being atempted
	"""
	def prepExec(self):
		decho( 'dc_ass: entering prepExec() method', 5 )
		# set default returnValue
		returnValue = False

		# find the issuer's level and keyhash
		levelAndKeyhash = self.getLevelFromIndex(self.issuer.index)
		if levelAndKeyhash:
			# assign the level and keyhash as properties to the issuer object
			# see if we need to assign the default level for this user
			if levelAndKeyhash[0] == None:
				self.issuer.level = self.defaultLevel
			else:
				self.issuer.level = levelAndKeyhash[0]

			self.issuer.keyhash = levelAndKeyhash[1]

			# is the issuer allowed to run this command?
			if self.issuer.level >= self.command.level:
				returnValue = True
			else:
				decho ( 'dc_ass: %s is not authorized for the requested action' % bf2.PlayerManager.Player(self.issuer.index).getName(), 1 )
		else:
			decho( 'dc_ass: ERROR failed to get keyhash for player: %s' % bf2.PlayerManager.Player(self.issuer.index).getName(), 1 )

		decho( 'dc_ass: exiting prepExec() method', 5 )
		return returnValue


	def execKick(self):
		decho('dc_ass: entering execKick() method', 5)
		if self.prepExec():
			# make a victim list
			if self.getVictimIDs(self.command.arguments):
				self.processPoints()
			else:
				decho( 'dc_ass: Victim ID not findable given the arguments', 2 )

	
	def execBan(self):
		decho( 'dc_ass: entering execBan() method', 5 )
		if self.prepExec():
			# make a victim list
			if self.getVictimIDs(self.command.arguments):
				for vID in self.victimID:
					decho( "dc_ass: Banning player '%s' (%d) %s" % (bf2.PlayerManager.Player(vID).getName(), vID, self.command.reason), 1 ) 
					unused = host.rcon_invoke( 'pb_sv_ban %d %s' % (vID + 1, self.command.reason) )
			else:
				decho( 'dc_ass: Victim ID not findable given the arguments', 2 )


	def execRcon(self):
		decho( 'dc_ass: entering execRcon() method', 5 )
		if self.prepExec():
			decho( 'dc_ass: Running rcon command: %s' % self.command.rconString, 2 )
			
			if self.command.arguments == None:
				unused = host.rcon_invoke( self.command.rconString)
			else:
				unused = host.rcon_invoke( self.command.rconString + ' ' + self.command.arguments )


	def execExtension(self):
		decho( 'dc_ass: entering execExtension() method', 5 )

		if self.prepExec():
			# reload the extensions file
			reload( dc_ass_extensions )
			if self.command.function in dc_ass_extensions.__dict__:
				decho( 'dc_ass: executing %s() extension' % self.command.function, 2 )
				# send the entire ass object to the extensions
				exec( 'dc_ass_extensions.%s(%s)' % (self.command.function, 'self') )
			else:
				decho( 'dc_ass: %s() extension not found.' % self.command.function, 2 )


	def getCommandData(self, command):
		decho( 'dc_ass: entering getCommandData() method', 5 )
		# set a default returnValue
		returnValue = False

		# read in the commands INI file
		try: 
			self.config = ConfigParser.ConfigParser()
			self.config.read('admin/standard_admin/dc_ass_cmds.ini')

			# is this a defined command in the INI file
			if command in self.config.sections():
				decho( 'dc_ass: command: %s found in INI file' % command, 5 )
				# define/declare some vars for this admin event
				# (I really wouldn't need to do this if I know how to check if a var is defined or even exists
				type = None
				# the default length for a kick
				length = 2 
				rconString = None
				# default reason, is no reason at all
				reason = 'No reason given'
				# this makes all commands default to requiring full admin privs
				level = self.adminLevel 
				function = None

				# get all possible options
				# I could add sanity checks in here for poorly formated lines in the INI file
				for option in self.config.options(command):
					if option == 'type':
						type = self.config.get(command, option).strip()
					elif option == 'reason':
						reason = self.config.get(command, option).strip()
					elif option == 'length':
						length = int(self.config.get(command, option))
					elif option == 'command':
						rconString = self.config.get(command, option).strip()
					elif option == 'level':
						level = int(self.config.get(command, option))
					elif option == 'function':
						function = self.config.get(command, option).strip()

				returnValue = (type, reason, length, rconString, level, function)

			else: # end of is command in INI file conditional
				decho( 'dc_ass: (ERROR) %s command not found!' % command, 1 )

		except IOError:
			decho( 'dc_ass: (FATAL ERROR) could not open dc_ass_cmds.ini', 1 )
	
		return returnValue


	def onChatMessage(self, player_id, text, channel, flags):
		decho('dc_ass: entering onChatMessage() method', 5)
		self.issuer = container()
		self.issuer.index = player_id
		# pull the potential prefix off the text line
		self.chatString = self.stripPrefix(text)
		
		# unless the first character is ! don't do anything 
		if self.chatString[0:1] == '!':
			decho( 'dc_ass: the first character of %s was !' % self.chatString, 5 )

			# grab the parts of the chatline I need with a REGEX
			pattern = re.compile(r'!(\w*) ?(.*)')
			matches = pattern.findall(text)
			self.command = container()
			self.command.string = matches[0][0]
			decho( 'dc_ass: command.string = %s' % self.command.string, 5 )  

			# in case the command doesn't require a victim parameter...
			if matches[0][1] != '':
				self.command.arguments = matches[0][1]
				decho( 'dc_ass: arguments = %s' % self.command.arguments, 5 )
			else:
				self.command.arguments = None
				decho( 'dc_ass: no arguments given', 5 )

			commandData = self.getCommandData(self.command.string)
			if commandData:
				self.command.type = commandData[0]
				self.command.reason = commandData[1]
				self.command.length = commandData[2]
				self.command.rconString = commandData[3]
				self.command.level = commandData[4]
				self.command.function = commandData[5]

				# "switch" for the various command types
				if self.command.type == 'kick':
					self.execKick()
				elif self.command.type == 'ban':
					self.execBan()
				elif self.command.type == 'rcon':
					self.execRcon()
				elif self.command.type == 'extension':
					self.execExtension()
				else:
					decho( 'dc_ass: (ERROR) No type value for %s in dc_ass_cmds.ini file!' % self.commandString, 1 )


	def onPlayerDisconnect(self, p):
		decho('dc_ass: entering onPlayerDisconnect() method', 5)
		# if they disconnect, which might have happened if they were kicked, drop them from the tracker, if they're even in it
		if self.victimTracker.has_key(p.index):
			del(self.victimTracker[p.index])
			decho( 'dc_ass: player %d disconnected and no longer tracked' % p.index, 2 )

admin = ass()

def init():
	decho('dc_ass: initializing DontCamp.com Admin Support System', 2)
	host.registerHandler('ChatMessage', admin.onChatMessage, 1)
	host.registerHandler('PlayerDisconnect', admin.onPlayerDisconnect, 1)
	showLevel()
