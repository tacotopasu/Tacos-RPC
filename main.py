from pypresence import Presence
import time

rpc = Presence("924811628145434674")
rpc.connect()
rpc.update(state= "My socials!", details= "Check them down below!", large_image= "komidoodle", large_text="This text appears when you hover the large image.", start=time.time(), buttons=[{"label": "My Website", "url": "http://pan0rama.systems"},{"label": "My Github", "url": "https://github.com/Pan0ramaa"}])
input("Press any key to end the program.")