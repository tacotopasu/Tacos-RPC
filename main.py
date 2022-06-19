from pypresence import Presence as DiscordRichPresence
from configparser import ConfigParser
import base64, time, os, requests

keepGoing = True
Connected = False

# Load config
config = ConfigParser()
config.read("settings.ini")

#Get all the needed vars
richpresence = config["TEXT"]["rpc"]
rpc = DiscordRichPresence(richpresence, pipe = 0)
secondButton = config["BUTTON"]["secondButton"]
button1 = config["BUTTON1"]
button2 = config["BUTTON2"]
text = config["TEXT"]
image = config["IMAGE"]
timee = time.time()

# Connect RPC Function 
def ConnectRPC(buttonState, game, con):

    if(not con):
        rpc.connect()
    if(game == ""):
        statee = text["state"]
    else:
        statee = game

    if(buttonState == "False"):            
        rpc.update(details= text["details"], state= statee, large_image= image["largeImage"],
        large_text=text["imageText"], start= timee,
        buttons=[{"label": "Twitch", "url": "https://twitch.tv/avocadoism"}])
    elif(buttonState == "True"):
        rpc.update(details= text["details"], state= statee, large_image= image["largeImage"],
        large_text=text["imageText"], start= timee, small_image = image["smallImage"], small_text = text["smallText"],
        buttons=[{"label": "Twitch", "url": "https://twitch.tv/avocadoism"},
                 {"label": "Steam", "url": "https://steamcommunity.com/id/pan0rama"}])
ConnectRPC(secondButton, "", Connected)
Connected = True


while(keepGoing):
    os.system('cls')
    choice = input("What game are you playing right now? (Press Enter to close.)\n> ")
    if(choice == ""):
        keepGoing = False
        ConnectRPC(secondButton, "", Connected)
   
    elif(choice.lower() == "ramen"):          
        rpc.update(details= "Ramen Cafe", state= "Discord Server", large_image= "ramen",
            large_text= "Ramen Cafe - Discord Server",
            buttons=[{"label": "Join now!", "url": "https://discord.st/ramen"}])
    
    elif(choice.lower() == "sleeping"):           
        rpc.update(details= "I am now sleeping. Feel free to message me", state= "though! I will answer as soon as I wake up", large_image= "astortion")
    
    else:
        ConnectRPC(secondButton, choice, Connected)
