import zmq
from profile_image import player
import random

context = zmq.Context()
socket = context.socket(zmq.REP)
socket.bind("tcp://*:5555")

api_key = "api_key"
client = player(api_key)

while True:
	player_tag = socket.recv()
	file_name = str(random.randint(10000,99999))
	response = client.main_full_profile(player_tag, name=file_name)
	if response == 200:
		socket.send(b"%s.jpg" % file_name)
	else:
		socket.send(b"Error: %s" % client.status_reasons[response])
