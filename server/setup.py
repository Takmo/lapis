# See LICENSE file in top directory.

from auth import connect_sqlite, create_user, initialize_sqlite
from azure import azure_login, azure_create_server
import json

print "lapis - Minecraft + Azure = Wonders"
print "First, you'll need to link your Azure account."
azure_login()

print "Cool! Now, pick a name for your service."

name = raw_input("Name: ")

print "Awesome! Let's set you up with a username and password."

username = raw_input("User: ")
password = raw_input("Pass: ")

initialize_sqlite()
c = connect_sqlite()
create_user(c, username, password)

config = {}
config["name"] = name
config["online"] = True

with open("server.json", "w") as cfg:
    json.dump(config, cfg)

print "Now that we're finished with that, give us some time to spin up your server."
print "Fair warning, this is gonna take a while. Feel free to sing a song or five."

azure_create_server(name)

