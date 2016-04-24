import discord
import asyncio
import inspect
import traceback
import random

client = discord.Client()
userEmail = 'username'
userPass = 'password'
nyavySeals = 'What the nya did you just nyaing nyay about me, you little nya? Ill have you meow I nyaduated top of my class in the Nyavy Seals, and Ive been involved in numerous secret raids on Nyal-Quaeda, and I have over 300 confirmed nyas. I am trained in chitoge warfare and Im the top cat-nipper in the entire US nyarmed forces. You are nyathing to me but just another mouse. I will wipe you nya fuck out with precision the likes of which has never been seen before on this Earth, meowk my nyaing words. You think you can get away with saying nyat shit to me over the Internet? Think again, nyaer. As we speak I am contacting my secret network of cats across the USA and your IP is being traced right nyau so you better prepare for the storm, meowggot.The storm that wipes out the pathetic little thing you call your life. Youre nyaing dead, kid. I can be anywhere, anytime, and I can nya you in over seven hundred ways, and thats just with my bare paws. Nyat only am I extensively trained in unyarmed combat, but I have access to the entire nyarsenal of the Unnyaited States Meowrine Corps and I will use it to its full extent to wipe your miserable nya off the face of the continent, you little nya. If only you could have known what unholy retribution your little clever comment was about to bring nyaown upon you, maybe you would have held your nyaing tongue. But you couldnt, you didnt, and now youre paying the price, you godnyamn idiot. I will shit fury all over you and you will drown in it. Youre nyaing dead, kiddo.'
class NyaBot(discord.Client):
    """
    async def on_ready():
        print('Logged in as: \n' + client.user.name + client.user.id + '--------')
    """  
    async def nya(self, message):
        nyaSet = {nyavySeals, 'Nya!', 'Nya?', 'Nyamamugi nyamagome nyamatamago!', 'Nyanyame nyanyajuu nyanyado no nyarabi de nyakunyaku inyanyaku nyanyahan nyanyadai nyannyaku nyarabete nyaganyagame!',
                  'Meow'}
        await self.send_message(message.channel, random.choice(list(nyaSet)))
        return
    
    async def catnap(self, channel):
        await self.send_message(channel, 'Goodnyaight, everybody!')
        await self.logout()
        return
        
    
 
    async def on_message(self, message):

        if message.content.startswith('^'):
    
            command = getattr(self, (message.content.split()[0])[1:], None)
        
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
            
NyaBot().run(userEmail, userPass)