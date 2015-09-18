import socket # Allows connection to IRC server
import sys # Allows exit
import string # Allows to check for nonprintable characters
from urllib2 import urlopen # Allows for web info commands
import locale # Allows internationalization support
locale.setlocale(locale.LC_ALL, 'usa') # Sets default locale to USA

'''
Connection details - Edit here
'''

debug = False # For debug mode
nick = 'KuhnerdmBot' # Define nick on IRC
pw = '12345luggagecombo' # Define pass on IRC
network = 'irc.freenode.net' # Define IRC network
port = 6667 # Define IRC server port
chan = '#bitcoin' # Define default channel
usernick = 'kuhnerdm' # Define user's nick on IRC

'''
send_to_channel(message):
Used any time a post is made to an IRC channel
Posts a message "message" to the IRC channel in IRC protocol
'''

def send_to_channel(message):
	irc.send('PRIVMSG ' + chan + ' :' + message + '\r\n')

'''
populate_echoes():
Used at launch and when a new echo is added or changed
Reads the attached KuhnerdmBotEchoes.txt file and returns a dictionary of echoes.
The key is the command in the syntax ",command".
The value is a list containing the response and user in the syntax [response, user].
'''

def populate_echoes():
	global echoes
	echoes = {}
	with open('KuhnerdmBotEchoes.txt', 'r') as echoes_file:
		num_lines = sum(1 for line in echoes_file)
	with open('KuhnerdmBotEchoes.txt', 'r') as echoes_file:
		for x in range(num_lines / 3):
			echo_command = ',' + echoes_file.readline().replace('Command: ', '').replace('\r', '').replace('\n', '').replace(',\xef\xbb\xbf', '')
			echo_response = echoes_file.readline().replace('Response: ', '').replace('\r', '').replace('\n', '')
			echo_nick = echoes_file.readline().replace('User: ', '').replace('\r', '').replace('\n', '')
			echoes[echo_command] = [echo_response, echo_nick]
	return echoes
	
'''
add_echo(args):
Used when a new echo is added
Adds an echo to the KuhnerdmBotEchoes.txt file, given the arguments of the command calling ,echo add
'''

def add_echo(args):
	global echoes
	echo_command_lower = args.lower()
	echo_command = echo_command_lower.split(' ')[1]
	echo_response = ''
	echo_response_list = args.split(' ')[2:len(args)]
	if not echo_response_list:
		return 3
	for x in echo_response_list:
		echo_response += x.rstrip('\r\n')
		echo_response += ' '
	with open('KuhnerdmBotEchoes.txt', 'r+') as echoes_file:
		if (',' + echo_command) in echoes:
			return 1
		elif echo_command in reserved_commands:
			return 2
		else:
			num_lines = sum(1 for line in echoes_file)
			for line in (echoes_file):
				pass
			echoes_file.write('Command: ' + echo_command + '\n')
			echoes_file.write('Response: ' + echo_response.rstrip(' ') + '\n')
			echoes_file.write('User: ' + nick + '\n')
			
			'''Debug'''
			
			print "Echo added:"
			print "Command: " + echo_command
			print "Response: " + echo_response
			print "User: " + nick
			return 0
			
	echoes = populate_echoes()

'''
delete_echo(command):
Used when an echo is deleted
Deletes an echo from the KuhnerdmBotEchoes.txt file, given the command of the echo to be deleted
'''

def delete_echo(command):
	global echoes
	with open('KuhnerdmBotEchoes.txt', 'r') as echoes_file:
		echoes_file_lines = echoes_file.readlines()
	with open('KuhnerdmBotEchoes.txt', 'r') as echoes_file:
		num_lines = sum(1 for line in echoes_file)
	with open('KuhnerdmBotEchoes.txt', 'w') as echoes_file:
		for i in range(num_lines):
			if len(echoes_file_lines) - 1 >= i:
				if echoes_file_lines[i] == 'Command: ' + command + '\n':
					del echoes_file_lines[i]
					del echoes_file_lines[i]
					del echoes_file_lines[i]
		for line in echoes_file_lines:
			echoes_file.write(line)
	send_to_channel('Echo deleted.')
	echoes = populate_echoes()

'''
getdogeminedinfo():
Used in ,dogemined command
Returns a list containing the total number of Dogecoins mined and the percentage of initial Dogecoins
'''

def getdogeminedinfo(): # Used in ,dogemined command
	totaldogemined = float(urlopen('https://dogechain.info/chain/Dogecoin/q/totalbc').read())
	percentinitialdoge = totaldogemined / 100000000000 * 100
	return [totaldogemined, percentinitialdoge]
	
'''
getdogemarketcapinto():
Used in ,dogemarketcap command
Returns the Dogecoin market cap
'''
	
def getdogemarketcapinfo(): # Used in ,dogemarketcap command
	dogecoinpage = urlopen('http://coinmarketcap.com/currencies/dogecoin/')
	page_source = dogecoinpage.read()
	marketcapsection = page_source.find('</tr>')
	marketcapbeginning = page_source.find('$', marketcapsection)
	marketcapend = page_source.find('</small>', marketcapbeginning)
	dogemarketcap = page_source[marketcapbeginning:marketcapend].strip('$').strip(' ').replace(',', '')
	return dogemarketcap


'''Set up echoes file'''

reserved_commands =['echo', 'say', 'help', 'window', 'fud', 'pi', 'ping', 'pong', 'dogemined', 'dogemarketcap']
echoes = {}
echoes = populate_echoes()
print echoes # Debug

'''Set up debug mode'''

if debug == True:
	chan = '#KuhnerdmBotTesting'

'''Connect'''

irc = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # Define IRC socket
irc.connect((network,port)) # Connect to the server

'''Set up receive buffer and send user info and such'''

irc.recv (4096) # Setting up the Buffer
irc.send('NICK ' + nick + '\r\n') # Send nick to the server
irc.send('USER kuhnerdm kuhnerdm kuhnerdm :kuhnerdm IRC\r\n') # Send user info to the server
irc.send('JOIN ' + chan + '\r\n') # Join chan
irc.send('PRIVMSG ' + 'NickServ' + ' :IDENTIFY ' + nick + ' ' + pw + '\r\n') # Identify
send_to_channel(nick + ' is IN THE BUILDING!') # Send joining message

'''Start main loop and create receive buffer'''

while True: # Loops until connection breaks
	data = irc.recv (4096) # Make "data" the receive buffer
	print data # For debug purposes
	
	'''Keep from pinging out'''
	
	if data.find('PING') != -1: # If PING is Found in the Data
		irc.send('PONG ' + data.split()[1] + '\r\n') # Send back a PONG

	'''Handle commands'''
		
	if data.find('PRIVMSG') != -1: # If data is not a ping
		message = (' '.join(data.split(' ')[3:]))[1:] # Split misc data from the actual message
		if message.lower().find(chan) == -1 or message.lower().find('KuhnerdmBot') == -1: # If it's not a ping, continue
			nick = data.split('!')[0].replace(':','') # Assigns the sender to "nick"
			destination = ''.join(data.split(' ')[2]) # Assigns the receiving channel to "destination"
			print 'Message is ' + message.rstrip('\r\n') + ' from ' + nick + '\r\n' # For debug
			if message.strip() != '': # If there is not just whitespace in the message
				function = (message.split( )[0]).replace('\r', '').replace('\n', '') # The function is the first thing in the message
				print 'Function is ' + function + ' From ' + nick + '\r\n' # For debug
				arg = message.split(" ") # arg[0] is the command; arg[1] is the first argument
				args = '' # Create the args variable
				for index,item in enumerate(arg) : # For every index and item in arg
					if index > 0 : # If the word is not the command
						'''Add to args'''
						if args == '':
							args = item
						else:
							args += ' ' + item
				
				'''Respond to commands'''
				
				if function.lower() in echoes: # If command is a custom echo
					send_to_channel(echoes[function.lower()][0]) # Prints echo response
				elif function.lower() == ',echo': # If giving an echo-related command
					if all(c in string.printable for c in message) == True:
						if len(arg) == 1 or len(arg) == 2:
							send_to_channel('Syntax error. Proper syntax: ,echo add [command] [response] OR ,echo delete [command]') # Prints bad syntax response
						else:	
							if arg[1].lower() == 'add': # If adding an echo
								if arg[2][0] == ',':
									send_to_channel('Syntax error. Do not place a comma before the command.')
								else:
									echo_add_report = add_echo(args) # Adds echo
									if echo_add_report == 0: # Echo added
										send_to_channel('Echo added.') # Prints echo response	
									elif echo_add_report == 1: # Echo already exists
										send_to_channel('This echo already exists. Please change the echo command.') # Prints echo already exists response
									elif echo_add_report == 2: # Echo reserved
										send_to_channel('This echo is reserved. Please change the echo command.') # Prints echo reserved response
									elif echo_add_report == 3: # Bad syntax
										send_to_channel('Syntax error. Proper syntax: ,echo add [command] [response]' + '\r\n') # Prints bad syntax response
							elif arg[1].lower() == 'delete': # If deleting an echo
								if arg[2][0] == ',':
									send_to_channel('Syntax error. Do not place a comma before the command.')
								elif ',' + arg[2].lower().rstrip('\r\n') not in echoes:
									send_to_channel('Error: This echo does not exist.')
								else:
									echo_command_to_be_deleted = arg[2].rstrip('\r\n').lower()
									if not(echoes[',' + echo_command_to_be_deleted][1] == nick or echoes[',' + echo_command_to_be_deleted][1] == usernick):
										send_to_channel('Error: You do not have permissions to delete this echo.')
									else:
										delete_echo(echo_command_to_be_deleted)
							else:
								send_to_channel('Syntax error. Proper syntax: ,echo add [command] [response]') # Prints bad syntax response
				elif function.lower() == ',say' and nick == usernick and destination == 'KuhnerdmBot': # Command: ,say (PM only; me only)
					send_to_channel(args) # Prints args
				elif function.lower() == ',help': # Command: ,help
					send_to_channel('Hello! I am ' + usernick + '\'s IRC bot! Commands are: ,help / !mobilize / ,window / ,enthusiasmcheck / ,fud / ,dogemined / ,dogemarketcap') # Prints help text
				elif function.lower() == '!mobilize': # Command: !mobilize
					send_to_channel(nick + ' ROLLING OUT!') # Prints mobilize reply
				elif function.lower() == ',exit' and nick == usernick: # Command: ,exit (me only)
					send_to_channel(nick + ' shutting down.') # Prints shutting down text
					sys.exit() #DC
				elif function.lower() == ',window': # Command: ,window
					send_to_channel('Throw it out the window, the window, the second-story window!') # Prints window reply
				elif function.lower() == ',enthusiasmcheck': # Command: ,enthusiasmcheck
					send_to_channel('BOY, AM I ENTHUUUUUUSIASTIC! H-A-P-P-Y! I LOOOOOOOOOVE MY JOB!') # Prints enthusiastic reply
				elif function.lower() == ',fud': # Command: ,fud
					send_to_channel('PANIC PANIC PANIC PANIC PANIC PANIC PANIC PANIC!!!!!') # Prints FUD reply
				elif function.lower() == ',dogemined':
					functionreturnarray = getdogeminedinfo()
					send_to_channel('Total Dogecoins mined = ' + locale.format("%d", int(functionreturnarray[0]), True) + ' (' + str(round(functionreturnarray[1], 2)) + '% of initial DOGEs)')
				elif function.lower() == ',dogemarketcap':
					send_to_channel('Dogecoin market cap = $' + locale.format("%d", int(getdogemarketcapinfo()), True))