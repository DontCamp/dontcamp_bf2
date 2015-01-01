#Insert the line "import dc_query" at the top of you __init__.py file
#in your BF2's admin/standard_admin directory, then use the bf2_rcon_class
#DC_query extension to utilize this file's functionality

import bf2
import host
import new, default
from bf2.stats.constants import *

def registerRConCommand(command, function): 
	# Put the function into a new instancemethod object bound to the AdminServer
	newMethod = new.instancemethod(function, default.server, default.AdminServer)
	
	# Create a new class attribute in AdminServer that's wired to our function
	setattr(default.AdminServer, command, newMethod)
	
	# Add the new command into the rcon dispatch table, pointing to our function
	default.server.rcon_cmds[command] = newMethod
	
def getPlayerList(self, ctx, cmd):
	output = ('player_id\tname\tteam\tsquad\tsquadleader\tcommander\tip\t'
	'connected\tvalid\tremote\tai\tping\talive\tmandown\tprofile_id\t'
	'flagholder\tsuicide\tspawngroup\ttimetospawn\tscore_kills\tscore_deaths\t'
	'score_tks\tscore_suicides\tscore_score\tscore_heals\tscore_ammos\t'
	'score_repairs\tscore_damageassists\tscore_passengerassists\t'
	'score_driverassists\tscore_targetassists\tscore_revives\t'
	'score_teamdamage\tscore_teamvehicledamage\tscore_cpcaptures\t'
	'score_cpdefends\tscore_cpassists\tscore_cpneutralizes\t'
	'score_cpneutralizeassets\tscore_skillscore\tscore_rplscore\t'
	'score_cmdscore\tscore_fracscore\trank\tvehicletype\tvehicle\t'
	'kittype\tkit\n')
	
	try:
		for p in bf2.playerManager.getPlayers():
			output += str(p.index)
			output += '\t' + p.getName()
			output += '\t' + str(p.getTeam())
			output += '\t' + str(p.getSquadId())
			output += '\t' + str(p.isSquadLeader())
			output += '\t' + str(p.isCommander())
			output += '\t' + str(p.getAddress())
			output += '\t' + str(p.isConnected())
			output += '\t' + str(p.isValid())
			output += '\t' + str(p.isRemote())
			output += '\t' + str(p.isAIPlayer())
			output += '\t' + str(p.getPing())
			output += '\t' + str(p.isAlive())
			output += '\t' + str(p.isManDown())
			output += '\t' + str(p.getProfileId())
			output += '\t' + str(p.isFlagHolder())
			output += '\t' + str(p.getSuicide())
			output += '\t' + str(p.getSpawnGroup())
			output += '\t' + str(p.getTimeToSpawn())		
			output += '\t' + str(p.score.kills)
			output += '\t' + str(p.score.deaths)
			output += '\t' + str(p.score.TKs)
			output += '\t' + str(p.score.suicides)
			output += '\t' + str(p.score.score)
			output += '\t' + str(p.score.heals)
			output += '\t' + str(p.score.ammos)
			output += '\t' + str(p.score.repairs)
			output += '\t' + str(p.score.damageAssists)
			output += '\t' + str(p.score.passengerAssists)
			output += '\t' + str(p.score.driverAssists)
			output += '\t' + str(p.score.targetAssists)
			output += '\t' + str(p.score.revives)
			output += '\t' + str(p.score.teamDamages)
			output += '\t' + str(p.score.teamVehicleDamages)
			output += '\t' + str(p.score.cpCaptures)
			output += '\t' + str(p.score.cpDefends)
			output += '\t' + str(p.score.cpAssists)
			output += '\t' + str(p.score.cpNeutralizes)
			output += '\t' + str(p.score.cpNeutralizeAssists)
			output += '\t' + str(p.score.skillScore)
			output += '\t' + str(p.score.rplScore)
			output += '\t' + str(p.score.cmdScore)
			output += '\t' + str(p.score.fracScore)
			output += '\t' + str(p.score.rank)

			try:
				output += '\t' + str(getVehicleType(p.getVehicle().templateName))
				output += '\t' + str(p.getVehicle().templateName)
			except:
				output += '\t' + str(VEHICLE_TYPE_UNKNOWN)
				output += '\t' + 'unknown'

			try:
				output += '\t' + str(getKitType(p.getKit().templateName))
				output += '\t' + str(p.getKit().templateName)
			except:
				output += '\t' + str(KIT_TYPE_UNKNOWN)
				output += '\t' + 'unknown'
			output += '\n'
	except:
		output = 'Error retriving player information.'

	ctx.write(output)

def getServerInfo(self, ctx, cmd):
	output = ('servername\tplayers_connected\tplayers_joining\tmod_dir\t'
	'mapname\tnextmap\tteam1_name\tteam2_name\tteam1_tickets\tteam2_tickets\t'
	'team1_defaulttickets\tteam2_defaulttickets\tticketratio\tteamratio\t'
	'numplayers\tmaxplayers\tgamemode\ttimelimit\tscorelimit\t'
	'autobalanceteam\ttkpunishenabled\ttknumpunishtokick\ttkpunishbydefault\t'
	'useglobalrank\tuseglobalunlocks\n')
	
	connected = 0
	joining = 0
	try:
		for p in bf2.playerManager.getPlayers():
			if p.isConnected():
				connected += 1
			else:
				joining += 1
	except:
		pass
			
	numplayers = joining + connected
	try:
		output += host.rcon_invoke('sv.serverName').strip()
		output += '\t' + str(connected)
		output += '\t' + str(joining)
		output += '\t' + str(bf2.gameLogic.getModDir())
		output += '\t' + str(bf2.gameLogic.getMapName().replace('_', ' ').title())
		output += '\t' + str(host.rcon_invoke('maplist.list').splitlines()[int(host.rcon_invoke('admin.nextLevel').strip())].split()[1].strip('"').replace('_', ' ').title())
		output += '\t' + str(bf2.gameLogic.getTeamName(1))
		output += '\t' + str(bf2.gameLogic.getTeamName(2))
		output += '\t' + str(bf2.gameLogic.getTickets(1))
		output += '\t' + str(bf2.gameLogic.getTickets(2))
		output += '\t' + str(bf2.gameLogic.getDefaultTickets(1))
		output += '\t' + str(bf2.gameLogic.getDefaultTickets(2))
		output += '\t' + str(bf2.serverSettings.getTicketRatio())
		output += '\t' + str(bf2.serverSettings.getTeamRatioPercent())
		output += '\t' + str(numplayers)
		output += '\t' + str(bf2.serverSettings.getMaxPlayers())
		output += '\t' + str(bf2.serverSettings.getGameMode())
		output += '\t' + str(bf2.serverSettings.getTimeLimit())
		output += '\t' + str(bf2.serverSettings.getScoreLimit())
		output += '\t' + str(bf2.serverSettings.getAutoBalanceTeam())
		output += '\t' + str(bf2.serverSettings.getTKPunishEnabled())
		output += '\t' + str(bf2.serverSettings.getTKNumPunishToKick())
		output += '\t' + str(bf2.serverSettings.getTKPunishByDefault())
		output += '\t' + str(bf2.serverSettings.getUseGlobalRank())
		output += '\t' + str(bf2.serverSettings.getUseGlobalUnlocks())
		output += '\n'
	except:
		output = 'Error retriving server information.'

	ctx.write(output)

registerRConCommand('dc_pl', getPlayerList)
registerRConCommand('dc_si', getServerInfo)
