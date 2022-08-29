from configparser import ConfigParser # Used to get configs
from ctypes import Structure, windll, c_uint, sizeof, byref # Used to detect idle time (all of this, I know right!)
from pypresence import Presence as DiscordRichPresence # Used for Discord RPC
import psutil, time, os, PIL.Image, pystray, threading # Used for time.sleep() and more


os.system("") # Prepare color codes. We have to do this due to some weird cmd glitch...
class LASTINPUTINFO(Structure): # Used in IdleDuration().
    _fields_ = [
        ('cbSize', c_uint),
        ('dwTime', c_uint),
    ]

config = ConfigParser() # Loading config
config.read("settings.ini")
secondButton = config["BUTTON"]["secondButton"] # Setting all vars for easier access later.
button1 = config["BUTTON1"]                     # This can definetily be done better, but for now I'll go with this for simplicity.
button2 = config["BUTTON2"]
text = config["TEXT"]
image = config["IMAGE"]
sleeping = config["SLEEPING"]
games = config["GAMES"]["games"].split(',')
gameName = config["GAMES"]["gameName"].split(',')
gameIcon = config["GAMES"]["icons"].split(',')
defaultArgs = [text["details"], text["state"], image["largeImage"], text["imageText"], '', image["smallImage"], text["smallText"]] # Default arguments used in RPC.
rpc = DiscordRichPresence(config["TEXT"]["rpc"], pipe = 0)
rpc.connect()

def IdleDuration(): # Get how long (seconds) the user has been AFK for.
    lastInputInfo = LASTINPUTINFO()
    lastInputInfo.cbSize = sizeof(lastInputInfo)
    windll.user32.GetLastInputInfo(byref(lastInputInfo))
    millis = windll.kernel32.GetTickCount() - lastInputInfo.dwTime
    return int(millis // 1000.0)

def PPrint(status, text): # Easier method for printing out better looking warnings and errors.
    if status == 'warn':
        status = '\033[33m[Warn] '
    elif status == 'error':
        status = '\033[31m[Error]'
    elif status == 'fatal':
        status = '\033[31m[Fatal]'
    else:
        status = '\033[35m[Info] '
    
    print("\033[0m\033[1m" + status + f"\033[0m \033[1m{text}")

def GamesOn(): # Get list with all games currently on.
    global gamesOn
    gamesOn = []
    for x in games:
            if(x in (i.name() for i in psutil.process_iter())):
                gamesOn.append(x)
    return gamesOn

def IsGameOn(game): # Check the arg's (game) state.
    if(game in (i.name() for i in psutil.process_iter())):
        return True
    else:
        return False

def UpdateRPC(data): # Update RPC in a way simpler way!
    details = data[0]
    state = data[1]
    largeImage = data[2]
    largeImageTex = data[3]
    startedAt = data[4]
    smallImage = data[5]
    smallImageTex = data[6]

    if secondButton == '1':
        buttons = [{"label": button1["label"], "url": button1["url"]}, {"label": button2["label"], "url": button2["url"]}]
    else:
        buttons = [{"label": button1["label"], "url": button1["url"]}]

    if startedAt == '1':
        rpc.update(details = details, state = state, large_image = largeImage, large_text = largeImageTex, start = time.time(),
                    small_image = smallImage, small_text = smallImageTex, buttons = buttons)
    else:
        rpc.update(details = details, state = state, large_image = largeImage, large_text = largeImageTex,
                    small_image = smallImage, small_text = smallImageTex, buttons = buttons)


# System Tray Section
trayIcon = PIL.Image.open('icon.jpg')
def on_clicked(icon, item):
    if str(item) == "Exit":
        icon.stop()
        os._exit(0)
icon = pystray.Icon("Taco's RPC", trayIcon, menu = pystray.Menu(
    pystray.MenuItem("Taco's RPC", on_clicked, enabled= False),
    pystray.MenuItem("Exit", on_clicked)))
def Tray():
    icon.run()
threading.Thread(target = Tray).start()
# System Tray Section End

print("Creating RPC.")
UpdateRPC(defaultArgs) # Create RPC with the default set arguments.
print("RPC Created.")
gamesAlreadyOn = ['placeholder!']
lastGame = ''

print("Starting while loop(?)")
while True:
    print("While loop running")
    GamesOn()
    if gamesAlreadyOn != gamesOn and gamesOn != [] and lastGame not in gamesOn: # If the games on haven't changed AND if the current games list isn't empty AND last game is not currently open:
        gamesAlreadyOn = gamesOn
        args = [text["details"], gameName[games.index(gamesOn[0])], gameIcon[games.index(gamesOn[0])], text["imageText"], '1', image["smallImage"], text["smallText"]]
        UpdateRPC(args)
        lastGame = gamesOn[0]

    if gamesOn == []: # If no game is currently on:
        UpdateRPC(defaultArgs)

    time.sleep(5)
