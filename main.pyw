from configparser import ConfigParser # Used to get configs
from pypresence import Presence as DiscordRichPresence # Used for Discord RPC
import time, os, PIL.Image, pystray, threading # Used for system tray and more


config = ConfigParser() # Loading config
config.read("settings.ini")
firstButton = config["BUTTON"]["firstButton"]
secondButton = config["BUTTON"]["secondButton"] # Setting all vars for easier access later.
button1 = config["BUTTON1"]                     # This can definitely be done better, but for now I'll go with this for simplicity.
button2 = config["BUTTON2"]
text = config["PRESENCE"]
image = config["IMAGE"]
defaultArgs = [text["details"], text["state"], image["largeImage"], text["imageText"], '', image["smallImage"], text["smallText"]]
rpc = DiscordRichPresence(config["PRESENCE"]["rpc"], pipe = 0)
rpc.connect()



def UpdateRPC(data):
    details = data[0]
    state = data[1]
    largeImage = data[2]
    largeImageTex = data[3]
    smallImage = data[5]
    smallImageTex = data[6]

    if firstButton == 'True' and secondButton == 'True':
        buttons = [{"label": button1["label"], "url": button1["url"]}, {"label": button2["label"], "url": button2["url"]}]
    elif firstButton == 'True' and secondButton == 'False':
        buttons = [{"label": button1["label"], "url": button1["url"]}]
    else:
        buttons = []
        rpc.update(details = details, state = state, large_image = largeImage, large_text = largeImageTex,
                   small_image = smallImage, small_text = smallImageTex)
    
    if buttons != []:
        rpc.update(details = details, state = state, large_image = largeImage, large_text = largeImageTex,
                   small_image = smallImage, small_text = smallImageTex, buttons = buttons)


# System Tray Section Start
try:
    trayIcon = PIL.Image.open('icon.jpg')
except:
    print("Error occured! Can't get icon!")

def on_clicked(icon, item):
    if str(item) == "Exit":
        icon.stop()
        os._exit(0)
icon = pystray.Icon("Taco's RPC", trayIcon, menu = pystray.Menu(
    pystray.MenuItem("Taco's RPC", on_clicked, enabled = False),
    pystray.MenuItem("Exit", on_clicked)))
def Tray():
    icon.run()
threading.Thread(target = Tray).start()
# System Tray Section End

print("Creating RPC.")
UpdateRPC(defaultArgs) # Create RPC with the default set arguments.
print("RPC Created.")

while True:
    time.sleep(5)
    new_config = ConfigParser()
    new_config.read("settings.ini")
    if new_config != config:
        firstButton = new_config["BUTTON"]["firstButton"]
        secondButton = new_config["BUTTON"]["secondButton"]
        button1 = new_config["BUTTON1"]
        button2 = new_config["BUTTON2"]
        text = new_config["PRESENCE"]
        image = new_config["IMAGE"]
        args = [text["details"], text["state"], image["largeImage"], text["imageText"], '', image["smallImage"], text["smallText"]]
        UpdateRPC(args)
