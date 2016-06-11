import discord
import asyncio
import inspect
import traceback
import random
import configparser

from os import listdir

client = discord.Client()
parser = configparser.ConfigParser()
parser.read('credentials.ini')
token = parser['Login']['Token']
ownerID = parser['Permissions']['Owner ID']
prefixString = parser['Options']['Prefix String']
voiceDict = {}

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
                "catnap" : "Owner use only! Puts me to bed."}
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
    
        
    async def cmd_sound(self, channel, author, message):
        soundFiles = listdir('Sounds')
        soundFile = ""
        vChan = author.voice_channel
        if vChan == None:
            await self.send_message(channel, "You must be in a voice nyannel to use this nyammand!")
            return
        if not vChan.permissions_for(vChan.server.me).speak:
            await self.send_message(channel, "Unyable to speak in your channel.")
            return
        messageArray = message.content.split()
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
        soundFile = 'Sounds/' + soundFile
        index = voiceDict.get(str(vChan.id))
        if index != None:
            await self.send_message(channel, 'I can only play one sound nyat a time!')
            return

        voiceDict[str(vChan.id)] = (await self.join_voice_channel(vChan), None)
        """
        async def afterFunc(vChan):
            await voiceDict[str(vChan.id)][0].disconnect()
            voiceDict[str(vChan.id)] = None
            return
         """
        voiceDict[str(vChan.id)] = (voiceDict[str(vChan.id)][0], voiceDict[str(vChan.id)][0].create_ffmpeg_player(soundFile)) # after = afterFunc(vChan)))
        voiceDict[str(vChan.id)][1].start()
        
        while not voiceDict[str(vChan.id)][1].is_done():
            await asyncio.sleep(1)
        await voiceDict[str(vChan.id)][0].disconnect() 
        voiceDict[str(vChan.id)] = None
        
        return    
    

 
    async def on_message(self, message):

        if message.content.startswith(prefixString):
    
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
                    
                    await command(**commandArgs)
                except:
                    traceback.print_exc()
    
        return
        
    async def on_ready(self):
        print("Connected!")
        await self.change_status(discord.Game(name="Type " + prefixString + "help for a list of commands!"))
            
NyaBot().run(token)