from profile_image import player

api_key = "Your api key. Check the README.md file to see how to get one."
client = player(api_key)

player_tag = "#ULP92C2"
file_name = "test" #default is "test"
file_path = "" #default is "/var/www/html/"
#having the file_path be "" saves the image in the same folder as profile_image.py

response = client.main_full_profile(player_tag, name=file_name, path=file_path)
if response == 200:
  print "Created a profile for %s (%s)." % (client.playerName, client.playerTag)
else:
  print response, client.status_reasons[response]
