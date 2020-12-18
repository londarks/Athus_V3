import json
import time
import requests
import toml
import threading
from modules import commands
from freatures import blacklist
import threading
#from freatures. impor 


class Room(object):
	"""docstring for Room"""
	def __init__(self):
		self.config = toml.load('config.toml')
		self.cookie = self.config['Botconfig']['cookie']
		self.nameBot = self.config['Botconfig']['name']
		self.Blacklist = blacklist.BlacklistDrrr()
		self.session = requests.session()
		self.commands = commands.BotCommands()

	def load_cookie(self,file_name):
		f = open(file_name, 'r')
		self.session.cookies.update(eval(f.read()))
		f.close()

	def room_enter(self, url_room):
		#load cookie
		self.load_cookie(self.cookie)
		#enter room
		send = self.session.get(url_room,headers={'User-Agent': 'Bot'})
		send.close()
		self.room()

	def room(self):
		#inicializando bot
		self.load_cookie(self.cookie)
		endpoint  = self.session.get("https://drrr.com/json.php?").json()
		#print(endpoint)
		#condição para  ver se esta na sala ou não
		checkUpdate = endpoint['update']
		#print(checkUpdate)
		#ligando o loop de msg
		t_normal = threading.Thread(target=self.commands.loop)
		t_normal.start()
		while True:
			resp  = self.session.get("https://drrr.com/json.php?").json()
			#print(resp)
			if checkUpdate != resp['update']:
				try:
					url_room_update = "https://drrr.com/json.php?update={}".format(resp['update'])
					msgApi = self.session.get(url_room_update).json()
					if msgApi['talks'][0]['type'] == 'join':
						name_sender = msgApi['talks'][0]['user']['name']
						try:
							tripcode = msgApi['talks'][0]['from']['tripcode']
						except Exception:
							tripcode = None
							self.Blacklist.checkBlackList(name_sender, tripcode)
						#manda menssagem de boas vindas
					#pegando dados dos usuarios que estao conversando
					name_sender = msgApi['talks'][0]['from']['name']
					id_sender  = msgApi['talks'][0]['from']['id']
					message = msgApi['talks'][0]['message']
					try:
						tripcode = msgApi['talks'][0]['from']['tripcode']
					except Exception:
						tripcode = None
					#auto ban de floods
						# self.flood.insetValue(name_sender)
					if '/'  in message:
						if name_sender == self.nameBot:
							continue
						t_normal = threading.Thread(target=self.commands.Search, args=(message, id_sender, name_sender, tripcode))
						t_normal.start()
							#self.commands.handle_message(message=message, id_sender=id_sender, name_sender=name_sender, tripcode=tripcode)
					checkUpdate = resp['update']
				except Exception as e:
					pass
					#print(e)