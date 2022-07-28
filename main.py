from pypresence import Presence as DiscordRichPresence
from configparser import ConfigParser
import time, os, psutil, requests

keepGoing = True
Connected = False
os.system("")

def Setup():
    # Load config
    config = ConfigParser()
    config.read("settings.ini")

    global secondButton, button1, button2, text, image, sleeping, vr, timee

    #Get all the needed vars
    secondButton = config["BUTTON"]["secondButton"]
    button1 = config["BUTTON1"]
    button2 = config["BUTTON2"]
    text = config["TEXT"]
    image = config["IMAGE"]
    sleeping = config["SLEEPING"]
    vr = config["VR"]
    timee = time.time()
    
def PPrint(status, text): # Easier method for printing out better looking warnings and errors
    if status == 'warn':
        status = '\033[33m [Warn]'
    elif status == 'error':
        status = '\033[31m[Error]'
    elif status == 'fatal':
        status = '\033[31m[Fatal]'
    else:
        status = '\033[35m [Info]'
    
    print("\033[0m\033[1m" + status + f"\033[0m \033[1m{text}")


config = ConfigParser()
config.read("settings.ini")
# Try to read settings.ini, if file isn't there, create template file
myPath = os.path.realpath(__file__)
completeName = os.path.join(myPath[:-8], 'settings.ini') 
os.system(f'cd {myPath[:-8]}')
if not os.path.exists(completeName):
    PPrint('fatal', "Couldn't find 'settings.ini'.")
    PPrint('info', 'Creating file...')
    response = requests.get('https://raw.githubusercontent.com/tacotopasu/Discord-RichPresence/main/settings.ini')
    open("settings.ini", "wb").write(response.content)
    PPrint('info', 'File successfully created.')
    PPrint('info', 'Running setup...')
    myPath = os.path.realpath(__file__)
    completeName = os.path.join(myPath[:-8], 'setup.py') 
    os.system(f'cd {myPath[:-8]}')
    if not os.path.exists(completeName):
        response = requests.get('https://raw.githubusercontent.com/tacotopasu/Discord-RichPresence/main/setup.py')
        open(completeName, "wb").write(response.content)
    os.system(completeName)
    settingsInstalled = True


myPath = os.path.realpath(__file__)
completeName = os.path.join(myPath[:-8], 'setup.py') 
if not os.path.exists(completeName):
    os.system(f'cd {myPath[:-8]}')
    response = requests.get('https://raw.githubusercontent.com/tacotopasu/Discord-RichPresence/main/setup.py')
    open(completeName, "wb").write(response.content)
    os.system(completeName)


try:
    richpresence = config["TEXT"]["rpc"]
except:
    PPrint('fatal', "Couldn't get 'Discord Application ID' from 'settings.ini'.")
    PPrint('info', "Get your Discord Application ID at 'https://discord.com/developers/applications'.")
    input('\nPress Enter to close.')
    exit()
# Try to use RPC's Client ID
try:
    PPrint('info', 'Initializing RPC...')
    rpc = DiscordRichPresence(richpresence, pipe = 0)
except:
    PPrint('fatal', "Couldn't connect using the Discord Application ID that was set in 'settings.ini'.")
    PPrint('info', "This can be caused by a lack of connection to the internet or an invalid Discord Application ID.")
    PPrint('info', "Check your Internet connection and if the error persists run 'setup.py'.")
    PPrint('info', "If you haven't yet, get your Discord Application ID at 'https://discord.com/developers/applications'.")
    input('\nPress Enter to close.')
    exit()



def Logo():
    print("\u001b[35m _____               _        __    ___  ___ \n/__   \__ _  ___ ___( )__    /__\  / _ \/ __\ \n  / /\/ _` |/ __/ _ \/ __|  / \// / /_)/ /  \n / / | (_| | (_| (_) \__ \ / _  \/ ___/ /___ \n \/   \__,_|\___\___/|___/ \/ \_/\/   \____/\033[0m")


def Sleep():
    os.system('cls')
    Logo()
    rpc.update(details= sleeping["details"], state= sleeping["state"], large_image= sleeping["large"], large_text= sleeping["largeText"])
    print('\n')
    PPrint('', 'Currently sleeping...')
    PPrint('', 'Press Enter to wake up.')
    input()
    os.system('cls')
    ConnectRPC(secondButton, "Just woke up...", Connected)

stopStats = 0
def Stats(): # Loops forever, I'll finish later...
    killMe = stopStats
    while killMe == 0:
        cpu_per = round(psutil.cpu_percent(),1) # Get CPU Usage
        # mem = psutil.virtual_memory() # Get Ram Usage
        mem_per = round(psutil.virtual_memory().percent,1) # Get Ram Usage in %
        rpc.update(details= "Taco's PC Status", state="CPU "+str(cpu_per)+"%"+" / RAM "+str(mem_per)+"%")
        killMe = stopStats
        time.sleep(5)
        

# Connect RPC Function 
def ConnectRPC(buttonState, game, con):
    modes = ['ramen', 'sleep', 'stats']
    Setup()
    if not con:
        try:
            rpc.connect()
            PPrint('info', 'RPC Connected.')
            time.sleep(1)
        except:
            PPrint('fatal', "Couldn't connect RPC. Check if the Application ID is correct (Located in settings.ini).")
            PPrint('', 'Press Enter to close.')
            input()
            exit()
    if game == "": # Default State ('game' var is empty)
        statee = text["state"]
        if buttonState == "False":            
            rpc.update(details= text["details"], state= statee, large_image= image["largeImage"],
            large_text=text["imageText"], start= timee, small_image = image["smallImage"], small_text = text["smallText"],
            buttons=[{"label": button1["label"], "url": button1["url"]}])
        elif buttonState == "True":
            rpc.update(details= text["details"], state= statee, large_image= image["largeImage"],
            large_text=text["imageText"], start= timee, small_image = image["smallImage"], small_text = text["smallText"],
            buttons=[{"label": button1["label"], "url": button1["url"]},
                     {"label": button2["label"], "url": button2["url"]}])
    else:
        if game.lower() not in modes:
            statee = game
            if buttonState == "False":          
                rpc.update(details= text["details"], state= statee, large_image= image["largeImage"],
                           large_text=text["imageText"], start= timee, small_image = image["smallImage"], small_text = text["smallText"],
                           buttons=[{"label": button1["label"], "url": button1["url"]}])
            elif buttonState == "True":
                rpc.update(details= text["details"], state= statee, large_image= image["largeImage"],
                           large_text=text["imageText"], start= timee, small_image = image["smallImage"], small_text = text["smallText"],
                           buttons=[{"label": button1["label"], "url": button1["url"]},
                                    {"label": button2["label"], "url": button2["url"]}])           
   

    # Ramen Cafe
    if game.lower() == "ramen":          
        rpc.update(details= "Ramen Cafe", state= "Discord Server", large_image= "ramen",
            large_text= "Ramen Cafe - Discord Server",
            buttons=[{"label": "Join now!", "url": "https://discord.st/ramen"}])

    # Sleeping
    if game.lower() == "sleep":           
        Sleep()

    
    # PC Status
    #if game.lower() == "stats":
    #    warning = False
    #    if(not warning):
    #        PPrint('info', "This is a new feature, and since bugs are expected feel free to report any errors to 'https://github.com/tacotopasu/Discord-RichPresence/issues'.")
    #        warning = True
    #    Stats()
    #    # Bad method but works fine for now
    #    PPrint('', 'Press Enter to stop stats.')
    #    input()
    #    global stopStats
    #    stopStats = 1
    #    ConnectRPC(secondButton, "", Connected)



Setup()
ConnectRPC(secondButton, "", Connected)
Connected = True

vrMode = False
while True:
    if keepGoing:
        os.system('cls')
        Logo()
        choice = input("\n\nWhat game are you playing right now? (Press Enter to close.)\n> ")
        if choice == "":
            PPrint('', 'Are you sure you want to exit? Press Enter to confirm (Type anything to cancel).')
            exitt = input()
            if exitt == '': exit()
        if choice.lower() == 'vr':
            vrMode = True
            keepGoing = False
        else:
            ConnectRPC(secondButton, choice, Connected)
    if vrMode:
        buttonState = secondButton
        os.system('cls')
        PPrint('', 'What game are you playing right now? (Press Enter to leave VR Mode.)')
        choice = input('> ')
        if choice != "":
            statee = choice
            if buttonState == "False":          
                rpc.update(details= vr["details"], state= statee, large_image= vr["largeImage"],
                        large_text=vr["imageText"], start= timee, small_image = vr["smallImage"], small_text = vr["smallText"],
                        buttons=[{"label": button1["label"], "url": button1["url"]}])
            elif buttonState == "True":
                rpc.update(details= vr["details"], state= statee, large_image= vr["largeImage"],
                        large_text= vr["imageText"], start= timee, small_image = vr["smallImage"], small_text = vr["smallText"],
                        buttons=[{"label": button1["label"], "url": button1["url"]},
                                {"label": button2["label"], "url": button2["url"]}])
        else:
            keepGoing = True
            vrMode = False
            time.sleep(1)
            ConnectRPC(secondButton, "", Connected)

