import json
import time
import requests
import toml

class BlacklistDrrr(object):
	"""sistema de Blacklist"""
	def __init__(self):
		self.config = toml.load('config.toml')
		self.session = requests.session()
		self.cookie = self.config['Botconfig']['cookie']
		self.load_cookie()

	def loadAdm(self, tripcode):
		admins = self.config['Tripcodes']
		for trip in admins:
			token = self.config['Tripcodes'][trip]
			if token == tripcode:
				return True
		return False

	def load_cookie(self):
		f = open(self.cookie, 'r')
		self.session.cookies.update(eval(f.read()))
		f.close()

	def martelo(self,idUser):
		ban_body = {'report_and_ban_user': idUser}
		kc = self.session.post('https://drrr.com/room/?ajax=1', ban_body)
		kc.close()

	def returnIduser(self, idUser):
		try:
			rooms = self.session.get("https://drrr.com/json.php?update=")
			user = []
			if rooms.status_code == 200:
				rooms_data = json.loads(rooms.content)
			for rooms in rooms_data['users']:
				user.append(rooms)
			for j in range(len(user)):
				if user[j]['name'] == idUser:
					try:
						return user[j]['tripcode'],user[j]['id']
					except Exception as e:
						return "None",user[j]['id']
		except Exception:
			return "vazio"

	def checkBlackList(self, username, tripcode):
		with open("athus/Database/Blacklist.json", "r",encoding='utf-8') as json_file:
			Blackusers = json.load(json_file)
		for i in range(len(Blackusers)):
			if tripcode == Blackusers[i]['Tripcode']:
				userId = self.returnIduser(username)
				self.martelo(userId)
		for a in range(len(Blackusers)):
			if username in Blackusers[a]['username']:
				userId = self.returnIduser(username)
				self.martelo(userId)

	def byebye(self, message, tripcode):
		""" sistema de blacklist para imposibilitar a entrada de usuario que eu não quero na sala"""
		try:
			check = self.loadAdm(tripcode)
			if check:
				user = message[8:]
				with open("athus/Database/Blacklist.json", "r") as file_object:
					containts = json.load(file_object)
				itens = self.returnIduser(user)
				insert = {"username" : user,"Tripcode" : itens[0]}
				containts.append(insert)

				with open("athus/Database/Blacklist.json", "w") as file_object:
					json.dump(containts, file_object, indent=4)
				try:
					self.martelo(itens[1])
				except Exception:
					pass
		except Exception as e:
			print(e)