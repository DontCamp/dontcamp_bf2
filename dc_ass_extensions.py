import bf2
import host
import time
import new # for kickstick
import re
from dc_debug import decho
  

def sayNextMap(unused=None):
	#It works. We'll just leave it at that.
	decho( 'The next map is %s' % (host.rcon_invoke('maplist.list').splitlines()[int(host.rcon_invoke('admin.nextLevel').strip())].split()[1].strip('"').replace('_', ' ').title()), 1 )


def getMyKeyhash(admin):
	decho( 'dc_ass: %s, your keyhash is %s' % (bf2.PlayerManager.Player(admin.issuer.index).getName(), admin.issuer.keyhash), 1 )


def privGetMyKeyhash(admin):
	host.rcon_feedback( admin.issuer.index, '%s, your keyhash is %s' % (bf2.PlayerManager.Player(admin.issuer.index).getName(), admin.issuer.keyhash) )
	decho( 'dc_ass: %s, check your console for your keyhash' % bf2.PlayerManager.Player(admin.issuer.index).getName(), 1 )


def getStatus(admin):
	# if the issuer is an admin
	decho('dc_ass: debug 1', 5)
	if admin.issuer.level == admin.adminLevel:
		decho('dc_ass: debug 2', 5)
		# if no argument was given just print the status of the issuer
		if admin.command.arguments == None:
			decho('dc_ass: debug 3', 5)
			decho( "dc_ass: %s has %d of %d kick points" % (bf2.PlayerManager.Player(admin.issuer.index).getName(), admin.getPointsFromIndex(admin.issuer.index), admin.kickThreshold), 1 )
		# get victimIDs
		elif admin.getVictimIDs(admin.command.arguments):
			decho('dc_ass: debug 4', 5)
			for vID in admin.victimID:
				decho('dc_ass: debug 5', 5)
				decho( 'dc_ass: %s has %d of %d kick points' % (bf2.PlayerManager.Player(vID).getName(), admin.getPointsFromIndex(vID), admin.kickThreshold), 1 )
	# if the issuer is NOT an admin
	else:
		decho('dc_ass: debug 7', 5)
		decho( 'dc_ass: %s has %d of %d kick points' % (bf2.PlayerManager.Player(admin.issuer.index).getName(), admin.getPointsFromIndex(admin.issuer.index), admin.kickThreshold), 1 )


def clearPoints(admin):
	admin.getVictimIDs(admin.command.arguments)
	for vId in admin.victimID:
		
		if admin.victimTracker.has_key(vId):
			admin.victimTracker.pop(vId)

		# I figure I can say their all cleared even if we're not tracking them... yet
		decho( "dc_ass: Points for %s have been cleared" % bf2.PlayerManager.Player(vId).getName(), 1 )

def adminKickVote(admin):
	admin.getVictimIDs(admin.command.arguments)	
	if admin.issuer.level == admin.adminLevel:
		admin.issuer.level = 4

	admin.processPoints()


def forgiveTK(admin):
	#Have a victim?
	if admin.getVictimIDs(admin.command.arguments):
		#Is the victim in victimTracker?
		if admin.victimTracker.has_key(admin.victimID[0]):
			#If so, is the issuer's keyhash in the victim's tracker?
			if admin.victimTracker[admin.victimID[0]].has_key(admin.issuer.keyhash):
				#If the reason in the tracker is the same reason we're looking for, adjust points
				if admin.command.reason == admin.victimTracker[admin.victimID[0]][admin.issuer.keyhash]['reason']:
					#Adjust points, check them, and escape from the function.
					if admin.manageTracker(admin.victimID[0], admin.issuer.keyhash, -2, admin.command.reason):
						decho('ftk 6', 5)
						admin.checkPoints()
						return

	#If any preceding step failed, we have no TK to forgive.
	decho('dc_ass: No teamkills to forgive for '+bf2.PlayerManager.Player(admin.victimID[0]).getName(), 1)
		
def getCommands(admin):
	output = "kick commands:\n"

	for cmd in admin.config.sections():
		if admin.config.get(cmd, 'type').strip() == 'kick':
			output += "%s - %s" % (cmd, admin.config.get(cmd, 'reason').strip()) + "\n"

	output += "\nban commands:\n"
	for cmd in admin.config.sections():
		if admin.config.get(cmd, 'type').strip() == 'ban':
			output += "%s - %s" % (cmd, admin.config.get(cmd, 'reason').strip()) + "\n"

	output += "\nrcon commands:\n"
	for cmd in admin.config.sections():
		if admin.config.get(cmd, 'type').strip() == 'rcon':
			output += "%s" % cmd + "\n"

	output += "\nextensions:\n"
	for cmd in admin.config.sections():
		if admin.config.get(cmd, 'type').strip() == 'extension':
			output += "%s" % cmd + "\n"

	host.rcon_feedback( admin.issuer.index, output )


def customKick(admin):
	slicePoint = admin.command.arguments.find(' ')
	if slicePoint == -1:
		decho( 'dc_ass: 2 arguments are required for this command', 1 )
	else:
		argVictim = admin.command.arguments[:slicePoint]
		admin.command.reason = admin.command.arguments[slicePoint + 1:]

		if admin.getVictimIDs(argVictim):
			admin.processPoints()


def switchTeam(admin):
	admin.getVictimIDs(admin.command.arguments)

	for vID in admin.victimID:
		decho('debug 1', 5)
		p = bf2.PlayerManager.Player(vID)
		# if they were not in a vehicle
		if killPlayerAtIndex(vID):
			decho( '%s is on team %d' % ( p.getName(), p.getTeam() ), 5 )

			if p.getTeam() == 1:
				p.setTeam(2)
				decho( 'dc_ass: switched %s to team 2' % p.getName(), 1)
			else: 
				p.setTeam(1)
				decho( 'dc_ass: switched %s to team 1' % p.getName(), 1)
		else:
			decho( 'dc_ass: unable to switch teams for %s' % p.getName(), 1 )


def tacticalSwitchTeam(admin):
	splitArgs = admin.splitArguments(admin.command.arguments)
	splitArgsLen = len(splitArgs)
	if splitArgsLen == 1:
		roundNum = int(splitArgs[0])
		if roundNum == 1:
			host.rcon_invoke('admin.restartmap');
			host.rcon_invoke('sv.startDelay 900');
		elif roundNum == 2:
			host.rcon_invoke('admin.restartmap');
			host.rcon_invoke('sv.startDelay 300');
			admin.command.arguments = '@'
			switchTeam(admin)
		elif roundNum == 3:
			host.rcon_invoke('admin.restartmap');
			host.rcon_invoke('sv.startDelay 600');
		elif roundNum == 4:
			host.rcon_invoke('admin.restartmap');
			host.rcon_invoke('sv.startDelay 300');
			admin.command.arguments = '@'
			switchTeam(admin)
		else:
			decho('dc_ass: Argument must be a valid tactical round number', 1)
		
	else:
		decho('dc_ass: Number of arguments for !tst is 1', 1)
			

def kill(admin):
	argReason = None
	argSpawnTime = None
	argVictim = None

	splitArgs = admin.splitArguments(admin.command.arguments)
	splitArgsLen = len(splitArgs)

	if splitArgsLen > 2:
		argReason = splitArgs[2]
	if splitArgsLen > 1:
		argSpawnTime = int(splitArgs[1])
	if splitArgsLen > 0:
		argVictim = splitArgs[0]

	admin.getVictimIDs(argVictim)
	for vID in admin.victimID:
		
		if not killPlayerAtIndex(vID):
			decho( 'dc_ass: unable to kill %s' % bf2.PlayerManager.Player(vID).getName(), 1 )
		else:
			if argSpawnTime != None:
				bf2.PlayerManager.Player(vID).setTimeToSpawn(argSpawnTime)

			if argReason != None:
				decho( 'dc_ass: %s was killed \'%s\'' % ( bf2.PlayerManager.Player(vID).getName(), argReason ), 1 )
			else:
				decho( 'dc_ass: %s was killed via admin system' % bf2.PlayerManager.Player(vID).getName(), 1 )


def killPlayerAtIndex(index):
	# we had a dirty function that did this before but the POE2 guy's code was a bit prettier. So, thanks guys!
	# set default returnValue
	p = bf2.PlayerManager.Player(index)
	if p:
		# we'll return true if we found someone at index
		returnValue = True

		# make some vars!
		playerVehicle = p.getVehicle()
		playerDefaultVehicle = p.getDefaultVehicle()
		parent = playerVehicle.getParent()
		parentDefault = playerDefaultVehicle.getParent()


		# if player is not driving a vehicle or on a vehicle's gun
		if playerVehicle == playerDefaultVehicle:
			# player using parachute
			if parentDefault:
				playerDefaultVehicle.setDamage(0.01)
			else:
				playerDefaultVehicle.setDamage(0.0)

		else:
			playerDefaultVehicle.setDamage(0.01)
			playerVehicle.setDamage(0.01)
	else:
		returnValue = False

	return returnValue


def setTickets(admin):
	slicePoint = admin.command.arguments.find(' ')
	if slicePoint == -1:
		arg = int(admin.command.arguments)
		if arg > 999 or arg < 0:
			decho( 'dc_ass: First argument must be a valid team number or a ticket value for both teams.', 1)
			return
		else:
			bf2.gameLogic.setTickets(1, arg)
			bf2.gameLogic.setTickets(2, arg)
	else:
		argTeam = int(admin.command.arguments[:slicePoint])
		argTickets = int(admin.command.arguments[slicePoint + 1:])

		if argTeam != 1 and argTeam != 2:
			decho( 'dc_ass: First argument must be a valid team number or a ticket value for both teams. ', 1)
			return

		if argTickets > 999 or argTickets < 0:
			decho( 'dc_ass: Second argument must be a valid ticket value.', 1)
			return

		bf2.gameLogic.setTickets(argTeam, argTickets)
			
	
def showTime(admin):
	decho( 'The time is %s' % time.strftime('%H:%M:%S'), 1 ) 


def setNextMap(admin):
	# default restltValue
	result = False
	argSize = None
	argGPM = None
	argName = None

	# split our args
	splitArgs = admin.splitArguments(admin.command.arguments)
	splitArgsLen = len(splitArgs)

	# this is for future use, right now we just use the argName
	if splitArgsLen > 2:
		argSize = splitArgs[2]
	if splitArgsLen > 1:
		argGPM = splitArgs[1]
	if splitArgsLen > 0:
		argName = splitArgs[0]

	if argName == None:
		decho( 'dc_ass: (ERROR) at least one argument is required', 1 ) 
	else:
		# set a centinal value for id so we know if we've found a map yet
		id = -1
		mapList = admin.getMapList()
	
		# search our maplist
		for mapID, mapData in mapList.iteritems():
			if mapData['name'].lower().find( argName.lower() ) != -1:
				decho( 'dc_ass: %s loosely matches %s' % ( argName, mapData['name'] ), 5 )
				# if this is the first map we've found...
				if id == -1:
					decho( 'dc_ass: found %s in %s' % ( argName, mapData['name'] ), 5 )
					id = mapID
					result = True
				# if we've gotten another possible match...
				else:
					result = False
					break

		if id != -1:
			if result:
				decho( 'dc_ass: mapID found @ %d' % id, 5 )
				if host.rcon_invoke('admin.nextLevel %d' % id):
					decho( 'dc_ass: nextmap will be %s' % mapList[id]['name'], 1 )
				else:
					decho( 'dc_ass: (ERROR) failed to set nextmap', 1 )
			else:
				decho( 'dc_ass: %s is ambiguous.' % argName, 1 )
		else:
			decho( 'dc_ass: no maps can be matched to %s' % argName, 1 )

def showMapList(admin):
	mapList = admin.getMapList()
	output = "current maplist:\n"
	for mapID, mapData in mapList.iteritems():
		output += mapData['name'] + ' ' + mapData['gpm'] + ' ' + mapData['size'] + "\n"

	host.rcon_feedback( admin.issuer.index, output )
