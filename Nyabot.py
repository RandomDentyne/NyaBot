import discord
import asyncio
import inspect
import traceback
import random
import configparser
import pixiv

from asyncio import Event
from os import listdir

client = discord.Client()
parser = configparser.ConfigParser()
parser.read('credentials.ini')
token = parser['Login']['Token']
ownerID = parser['Permissions']['Owner ID']
prefixString = parser['Options']['Prefix String']
pixID = parser['Login']['Pixiv ID']
pixPass = parser['Login']['Pixiv Pass']
voiceDict = {}
flagDict = {}

class NyaBot(discord.Client):
    def __init__(self):
        super(NyaBot, self).__init__()
        discord.opus.load_opus('libs/libopus-0.dll')
        
    helpDict = {"nya" : "Nya!", 
                "help" : "You probably need a different kind of help.", 
                "sound" : ("Usage:\n"
                           "{0}sound -> plays a random sound in the voice channel you're in\n"
                           "{0}sound [sound name] -> plays the sound\n"
                           "{0}sound list -> lists all nyavailable sounds\n"
                           "{0}sound list [filter] -> lists all nyavailable sounds containing the filter").format(prefixString),
                "listnyas" : "Equivalent to {0}sound list \"nya\"",
                "catnap" : "Owner use only! Puts me to bed.",
                "nyapic" : "Pulls a random pic from pixiv",
                "nuzzle" : ("Usage:\n"
                           "{0}nuzzle -> nuzzles you\n"
                           "{0}nuzzle [user] -> nuzzles first user mentioned")}
    queue = []       
    """
    async def on_ready():
        print('Logged in as: \n' + client.user.name + client.user.id + '--------')
    """

    async def cmd_help(self, channel, message):
        msgArray = message.content.split()
        if len(msgArray) > 1:
            usageString = self.helpDict.get(msgArray[1], None)
            if usageString != None:
                await self.send_message(channel, usageString)
            return
        cmdList = []
        for cmd in dir(self):
            if cmd.startswith('cmd_'):
                cmdList.append(cmd.replace('cmd_', '^'))
        printString = 'Here is a list of nyavailable commands:\n' + '\n'.join(cmdList) + '\nType ' + prefixString + 'help [command] for instructions on a specific command.'
                  
        await self.send_message(channel, printString)
        return
        
    async def cmd_nyapic(self, channel):
        pix = pixiv.login(pixID, pixPass)
        nyaList = pix.search("星空凛")
        await self.send_message(channel, "http://www.pixiv.net/member_illust.php?mode=medium&illust_id=" + str(random.choice(nyaList).id))
        
        
    async def cmd_nya(self, message):
        nyavySeals = ('What the nya did you just nyaing nyay about me, you little nya? ' 
              'Ill have you meow I nyaduated top of my class in the Nyavy Seals,' 
              'and Ive been involved in numerous secret raids on Nyal-Quaeda, and '
              'I have over 300 confirmed nyas. I am trained in chitoge warfare and Im'
              ' the top cat-nipper in the entire US nyarmed forces. You are nyathing to me'
              ' but just another mouse. I will wipe you nya fuck out with precision the likes '
              'of which has never been seen before on this Earth, meowk my nyaing words. You '
              'think you can get away with saying nyat shit to me over the Internet? Think again, nyaer. '
              'As we speak I am contacting my secret network of cats across the USA and your IP is being '
              'traced right nyau so you better prepare for the storm, meowggot.The storm that wipes out '
              'the pathetic little thing you call your life. Youre nyaing dead, kid. I can be anywhere, '
              'anytime, and I can nya you in over seven hundred ways, and thats just with my bare paws. '
              'Nyat only am I extensively trained in unyarmed combat, but I have access to the '
              'entire nyarsenal of the Unnyaited States Meowrine Corps and I will use it to its full extent '
              'to wipe your miserable nya off the face of the continent, you little nya. If only you could '
              'have known what unholy retribution your little clever comment was about to bring nyaown upon you, '
              'maybe you would have held your nyaing tongue. But you couldnt, you didnt, and now youre paying the price, '
              'you godnyamn idiot. I will shit fury all over you and you will drown in it. Youre nyaing dead, kiddo.'
              )
        nyaSet = {nyavySeals, 'Nya!', 'Nya-Nyandato?!', 'Nya?', 'Nyamamugi nyamagome nyamatamago!', 
                  'Nyanyame nyanyajuu nyanyado no nyarabi de nyakunyaku inyanyaku nyanyahan nyanyadai nyannyaku nyarabete nyaganyagame!',
                  'Meow', 'Nyanpasu!', 'Nyaow\'s it goin\'?', 'Nyan nyan, nyan nyan, nihao nyan, gorgeous, delicious, deculture!', 'Nyani sore? Imi wakannyai.',
                  'Nyarasho!', 'Nico Nico Nya~', 'Washi washi suru nyan~', 'NYABU ARROW SHOOOOOTO!', 'Nyareka nyasukete!', 'Faito da nya!', 'Nyatashi, nyanbarimasu!',
                  'Nyaruhodo...', 'Nya to the hand, girlfriend.', 'Nyat\'s up?', 'What\'s nyappenin\'?'}
        await self.send_message(message.channel, random.choice(list(nyaSet)))
        return
    
    async def cmd_catnap(self, author, channel):
        if author.id != ownerID:
            await self.send_message(channel, random.choice(list({'You\'re nyat the boss of me!', 'Nyaice try.'})))
            return
        napSet = {'Goodnyaight, everybody!', 'Onyasuminyasai!', 'Peace nyaut!'}
        await self.send_message(channel, random.choice(list(napSet)))
        await self.logout()
        return
        
    async def cmd_listnyas(self, author, channel):
        sounds = [sound[:-4] for sound in listdir('Sounds') if sound.find("nya") != -1]
        printstring = 'There are currently %d nyavailable nyas:\n' % len(sounds)
        printstring = printstring + '\n'.join(sounds)
        await self.send_message(author, printstring)
        await self.send_message(channel, 'I\'ve messaged you with a list of nyavailable nyas!')
        
    async def list_sounds(self, author, channel, message):
        sounds = listdir('Sounds')
        msgArray = message.content.split('"')
        str = "There are currently %d nyavailable sounds:\n"
        filter = ""
        if len(msgArray) > 1:
            filter = msgArray[1]
            str = "%d sounds found:\n" 
        filteredSounds = [sound[:-4] for sound in sounds if sound.find(filter) != -1]
        str = str % len(filteredSounds)
        str = str + '\n'.join(filteredSounds)
        await self.send_message(author, str)
        await self.send_message(channel, 'I\'ve messaged you with a list of nyavailable sounds!')
        return
    
    async def cmd_nuzzle(self, channel, author, mentions):
        nuzzleSet = {'http://www.lolzgif.com/wp-content/uploads/2012/09/cat-nuzzles-dog.gif',
                     'http://i.imgur.com/a6aj1Tk.jpg',
                     'http://distractify-media-prod.cdn.bingo/1492055-980x.jpg',
                     'https://66.media.tumblr.com/22c4fbbc02efbc3ef99f956fca58e7d0/tumblr_nysupfhV0P1ui28jfo1_500.gif'}
        nuzzleGif = random.choice(list(nuzzleSet))
        if(len(mentions) == 0):
            await self.send_message(channel, '*nuzzles ' + author.mention + '*\n' + nuzzleGif)
        else:
            await self.send_message(channel, author.mention + ' nuzzles ' + mentions[0].mention + '\n' + nuzzleGif)
        return

    async def cmd_joinvc(self, message, channel, author):
        vChan = author.voice.voice_channel
        if vChan == None:         # user not in a voice channel
            await self.send_message(channel, "You must be in a voice nyannel to use this nyammand!")
            return
        if not vChan.permissions_for(vChan.server.me).speak:    # no permission to join voice channel
            await self.send_message(channel, "I am nyat allowed to join that voice channel.")
            return
        serv = message.server
        vClient = voiceDict.get(serv.id) 
        if vClient != None and vClient.channel == vChan:     # already in the channel
            await self.send_message(channel, "I'm nyalready in this channel!")
            return
        flag = flagDict.get(serv.id)
        if flag != None and flag:         #check if another voice channel process is already running
            await self.send_message(channel, "One thing nyat a time, please!")
            return
        flagDict[serv.id] = True 
        if vClient != None:
            await vClient.move_to(vChan)
            voiceDict[serv.id]["channel"] = vChan
            flagDict[server.id] = False
            return
        voiceDict[serv.id] = {}
        voiceDict[serv.id]["client"] = await self.join_voice_channel(vChan)
        voiceDict[serv.id]["channel"] = vChan
        flagDict[serv.id] = False
        return

        
                

    
     '''
     Function name: cmd_sound
     Parameters: channel - channel the command was sent in
                 author  - person who sent the command
                 message - message itself
     Description: Plays a sound clip in a voice channel from the Sounds directory.
                  If bot is not in a voice channel, calls joinvc to try to join
                  If bot is already in a voice channel, author must be in the same voice channel
                  Cannot be used while any other sound-related command is being used in the server
     Return: n/a
     '''
                  
    async def cmd_sound(self, channel, author, message):

        soundFiles = listdir('Sounds')
        soundFile = ""
        messageArray = message.content.split()
        serv = message.server

        if len(messageArray) > 1:

            if messageArray[1] == "list":
                await self.list_sounds(author, channel, message)
                return

            soundFile = messageArray[1] + ".mp3"

            if not(soundFile in soundFiles):
                await self.send_message(channel, "Innyalid File.")
                return

        else:
            soundFile = random.choice(soundFiles)


        vChan = author.voice.voice_channel

        if vChan == None:
            await self.send_message(channel, "You must be in a voice nyannel to use this nyammand!")
            return

        if serv.me.voice.voice_channel != None and serv.me.voice.voice_channel != vChan:
            await self.send_message(channel, "Wrong voice channel, buddy! Come join mine!")
            return

        if not vChan.permissions_for(vChan.server.me).speak:
            await self.send_message(channel, "Unyable to speak in your channel.")
            return

        soundFile = 'Sounds/' + soundFile

        if serv.voice_client == None:
           await self.cmd_joinvc(message, channel, author)

        flag = flagDict.get(serv.id) #server-exclusive mutual exclusion flag
        if flag != None and flag:
            await self.send_message(channel, "One thing nyat a time, please!")
            return

        flagDict[serv.id] = True
        voiceDict[serv.id]["player"] = serv.voice_client.create_ffmpeg_player(soundFile)
        """
        async def afterFunc(vChan):
            await voiceDict[str(vChan.id)][0].disconnect()
            voiceDict[str(vChan.id)] = None
            return
        """
        voiceDict[serv.id]["player"].start()
        
        while not voiceDict[serv.id]["player"].is_done():
            await asyncio.sleep(1)
        print("Done!")
        voiceDict[serv.id]["player"] = None
        flagDict[serv.id] = False
        return    

    async def cmd_exitvc(self, channel, server):
        if server.voice_client == None:
            await self.send_message(channel, "Can't leave when I'm not in there in the first place.")
            return
        if flagDict.get(server.id) != None and flagDict[server.id]:
            await self.send_message(channel, "One thing nyat a time, please!")
            return
        flagDict[server.id] = True
        await server.voice_client.disconnect()
        voiceDict[server.id] = None
        flagDict[server.id] = False
        await self.send_message(channel, "Successfully disconnected!")
        return

    
    async def on_message(self, message):

        if message.content.startswith(prefixString) and message.server != None:
    
            command = getattr(self, 'cmd_' + (message.content.split()[0])[len(prefixString):], None)
        
            if command != None:
                try:
                    commandArgs = {}
                    args = inspect.signature(command).parameters.copy()
                    if args.pop('message', None):
                        commandArgs['message'] = message
                        
                    if args.pop('channel', None):
                        commandArgs['channel'] = message.channel
                        
                    if args.pop('author', None):
                        commandArgs['author'] = message.author
                        
                    if args.pop('mentions', None):
                        commandArgs['mentions'] = message.mentions

                    if args.pop('server', None):
                        commandArgs['server'] = message.server
                    
                    await command(**commandArgs)
                except:
                    traceback.print_exc()
    
        return
        
    async def on_ready(self):
        print("Connected!")
        await self.change_status(discord.Game(name="Type " + prefixString + "help for a list of commands!"))
            
NyaBot().run(token)
