from pypresence import Presence as DiscordRichPresence
from configparser import ConfigParser
import time, os

keepGoing = True
Connected = False

# Load config
config = ConfigParser()
config.read("settings.ini")

#Get all the needed vars
richpresence = config["TEXT"]["rpc"]
rpc = DiscordRichPresence(richpresence, pipe = 0)

def Setup():
    # Load config
    config = ConfigParser()
    config.read("settings.ini")

    global secondButton, button1, button2, text, image, sleeping, timee

    #Get all the needed vars
    secondButton = config["BUTTON"]["secondButton"]
    button1 = config["BUTTON1"]
    button2 = config["BUTTON2"]
    text = config["TEXT"]
    image = config["IMAGE"]
    sleeping = config["SLEEPING"]
    timee = time.time()
    

# Connect RPC Function 
def ConnectRPC(buttonState, game, con):

    Setup()
    if(not con):
        rpc.connect()
    if(game == ""):
        statee = text["state"]
    else:
        statee = game

    if(buttonState == "False"):            
        rpc.update(details= text["details"], state= statee, large_image= image["largeImage"],
        large_text=text["imageText"], start= timee, small_image = image["smallImage"], small_text = text["smallText"],
        buttons=[{"label": button1["label"], "url": button1["url"]}])
    elif(buttonState == "True"):
        rpc.update(details= text["details"], state= statee, large_image= image["largeImage"],
        large_text=text["imageText"], start= timee, small_image = image["smallImage"], small_text = text["smallText"],
        buttons=[{"label": button1["label"], "url": button1["url"]},
                 {"label": button2["label"], "url": button2["url"]}])

Setup()
ConnectRPC(secondButton, "", Connected)
Connected = True


def Logo():
    print("\033[35m _____               _        __    ___  ___ \n/__   \__ _  ___ ___( )__    /__\  / _ \/ __\ \n  / /\/ _` |/ __/ _ \/ __|  / \// / /_)/ /  \n / / | (_| | (_| (_) \__ \ / _  \/ ___/ /___ \n \/   \__,_|\___\___/|___/ \/ \_/\/   \____/\033[0m")

while(keepGoing):
    os.system('cls')
    Logo()
    choice = input("\n\n\033[1mWhat game are you playing right now? (Press Enter to close.)\n> ")
    if(choice == ""):
        keepGoing = False
   
# Example usage:
    elif(choice.lower() == "ramen"):          
        rpc.update(details= "Ramen Cafe", state= "Discord Server", large_image= "ramen",
            large_text= "Ramen Cafe - Discord Server",
            buttons=[{"label": "Join now!", "url": "https://discord.st/ramen"}])
    
    elif(choice.lower() == "sleeping" or choice.lower() == "sleep"):           
        rpc.update(details= sleeping["details"], state= sleeping["state"], large_image= sleeping["large"], large_text= sleeping["largeText"])
    
    else:
        ConnectRPC(secondButton, choice, Connected)
