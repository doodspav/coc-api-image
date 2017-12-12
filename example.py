from main_profile import CoClient,cocapi
client = CoClient("apiKey")

player_hashtag = "#ULP92C2"
file_name = "test" #default is "test"
file_path = "" #default is "/var/www/html/"
#having the file_path be "" saves the image in the same folder as main_profile.py

client.makeProfile(player_hashtag, name=file_name, path=file_path)

print "Created a profile for %s (%s)." % (client.playerName, client.playerTag)
