# irc-bot
IRC bot written in Python

This repo contains the code for an IRC bot to be run through the command line. It functions by creating a simple socket connection, *not* using Python's IRC library.

#Setup

* In KuhnerdmBot.py, under "Connection Details - Edit here", change the following fields:

    debug    - Change to "true" to use the debug channel instead of the channel specified in "chan"
    nick     - The IRC nick of the bot
    pw       - The IRC pass of the bot
    network  - The IRC server to connect to
    port     - The port of the IRC server to connect to
    chan     - The channel of the IRC server to connect to
    usernick - The IRC nick of the user running the bot (i.e. your nick)

* Run KuhnerdmBot.py from the command line in the irc-bot directory

#Functions

**Receiving Messages** - irc-bot works by repeatedly calling "recv" on the socket connection and storing the raw input in "data." It then parses the data into several useful fields:

    message     - String containing data minus miscellaneous server info
    nick        - String containing the nick of the user who sent "message"
    destination - String containing the receiving channel
    function    - String containing first word in the message
    args        - String containing all arguments in "message" (i.e. words after "function")
    arg         - List containing all arguments *including* "function" (i.e. arg[0] = function; arg[1] = first arg)

**Sending Messages** - irc-bot posts to the IRC channel by sending the server a message in IRC protocol. The process is simplified by the use of "send_to_channel", which takes a string and posts it to the channel. irc-bot also responds to pings in a similar manner, but the process is automated.

**Responding to Commands** - irc-bot responds to commands by comparing "function" against the list of pre-established custom echoes (explained in "Custom Echoes"), and several base commands. For example, when function is equal to ',fud', the bot responds by sending the message 'PANIC PANIC PANIC PANIC PANIC PANIC PANIC PANIC!!!!!'

**Custom Echoes** - irc-bot contains the functionality to let users of the IRC room make simple custom echo commands for the bot. This allows users to:

* Store and retrieve links to websites for easy reference to new users
* Store and retrieve tutorial text for instructional purposes
* Store quotes from users for user entertainment
* etc.

This works by storing three attributes in the text file KuhnerdmBotEchoes.txt:

* Command  - The command to be called (must be following a comma, e.g. ',test')
* Response - The text to send to the server after Command is called
* User     - The nick of the user who established the echo

The format for adding echoes is:

    ,echo add [command] [response]

The format for deleting echoes is:

    ,echo delete [command]

Note: ',echo delete' only works if "nick" (in KuhnerdmBot.py) is equal to "User" (in KuhnerdmBotEchoes.txt). ',echo add' only works if the echo doesn't already exist and is not found in the list of reserved words (e.g. A user cannot create ',fud' because it is in the list of reserved words, and that same user cannot create ',test' because it is already in KuhnerdmBotEchoes.txt). At this point, irc-bot cannot change a pre-existing echo's response, but this can be accomplished by deleting and re-adding the echo.

**Speaking for Bot Owner** - irc-bot allows the bot owner (i.e. the user with the nick specified in "usernick") to "speak" through the bot. This is done by PM-ing the bot the following:

    ,say [message]

This can create some fun meta-moments.
