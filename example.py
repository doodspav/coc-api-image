from main_profile import cocapi

client = cocapi()

player_hashtag = "#ULP92C2"
file_name = "test" #default is "test"
file_path = "" #default is "/var/www/html/"
#having the file_path be "" saves the image in the same folder as main_profile.py

response = client.makeProfile(player_hashtag, name=file_name, path=file_path)
if response == 200:
  print "Created a profile for %s (%s)." % (client.playerName, client.playerTag)
else:
  print response, client.statusReasons[response]
