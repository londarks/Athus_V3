import json
import os
import toml
from modules import login, room



class Bot(object):
	"""Drrr bot feito em Python"""
	def __init__(self):
		self.config = toml.load('config.toml')
		self.name = self.config['Botconfig']['name']
		self.icon = self.config['Botconfig']['icon']
		self.roomId = self.config['Botconfig']['room']
		self.cookie = self.config['Botconfig']['cookie']
		self.login = login.Connect(self.name,self.icon)
		self.checkLogin()

	def checkLogin(self):
		if not os.path.isfile(self.cookie):
			self.login.login()
			self.login.save_cookie(self.cookie)

	def start(self):
		run = room.Room()
		run.room_enter(self.roomId)
		

if __name__ == "__main__":
	run = Bot()
	run.start()