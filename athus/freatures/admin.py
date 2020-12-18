import requests
import time
import json
import re,os
import threading
import toml


class admininstrator(object):
    def __init__(self):
        self.config = toml.load('config.toml')
        self.session = requests.session()
        self.host = 'https://drrr.com/room/?ajax=1'
        self.admin_list = 'ATHUSo12kM.'
        self.nameBot = self.config['Botconfig']['name']
        self.admin = ''
        self.banido = ''
        self.listBanidos = {}
        self.listBanidos2 = []
        self.comand = ''
        self.valid = []
        self.idplayers = []
        self.autoban = True
        self.spam = {"admin_list": False,"admin": False}
        self.ban = True
        self.load_cookie()

    def load_cookie(self):
        f = open(self.config['Botconfig']['cookie'], 'r')
        self.session.cookies.update(eval(f.read()))
        f.close()


    def loadAdm(self, tripcode):
        admins = self.config['Tripcodes']
        for trip in admins:
            token = self.config['Tripcodes'][trip]
            if token == tripcode:
                return True
        return False

    def unban(self,idUser):
        kick_body = {
            'unban': idUser
        }
        kc = self.session.post('https://drrr.com/room/?ajax=1', kick_body)
        kc.close()

    def share_music(self, url, name=''):
        share_music_body = {
            'music': 'music',
            'name': name,
            'url': url
        }
        p = self.session.post(
            url=self.host, data=share_music_body)
        p.close()

    def unbanDic(self, name, iduser):
        if name in self.listBanidos:
            pass
        else:
            self.listBanidos2.append(name)
            self.listBanidos[name] = iduser
    
    def clearlist(self):
        self.listBanidos = {}
        self.listBanidos2 = []
        self.post(message="/mc Lista limpa")

    def listban(self):
        admin = ""
        for i in range(len(self.listBanidos2)):
            admin += '|@{}|\n'.format(self.listBanidos2[i])
        self.post(message="Lista de Banidos:\n {}".format(admin))


    def avoid_spam(self, com):
        time.sleep(5)
        self.spam[com] = False

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
                    return user[j]['id']
        except Exception:
            return "vazio"

    def post(self, message, url='', to=''):
        post_body = {
            'message': message,
            'url': url,
            'to': to
        }
        p = self.session.post(
            url=self.host, data=post_body)
        p.close()


    def unbanOfficial(self, message, tripcode):
        valid = self.loadAdm(tripcode)
        try:
            if valid == True:
                message = message[7:]
                if message in self.listBanidos:
                    self.unban(self.listBanidos[message])
                else:
                    self.post(message="/mc usuario Não foi banido")
        except Exception:
            pass

    def setRomm_Description(self, message, tripcode):
        valid = self.loadAdm(tripcode)
        try:
            if valid == True:
                message = message[11:]
                room_description_body = {'room_description': 'night {}'.format(message)}
                rd = self.session.post(self.host, room_description_body)
                rd.close()
        except Exception:
            pass

    def setRomm_name(self, message, tripcode):
        valid = self.loadAdm(tripcode)
        try:
            if valid == True:
                message = message[11:]
                room_name_body = {
                'room_name': message
                }
                rn = self.session.post(self.host, room_name_body)
                rn.close()
        except Exception:
            pass

    def leave_room(self):
        leave_body = {
            'leave': 'leave'
        }
        lr = self.session.post(self.host, leave_body)
        lr.close()


    def new_host(self, new_host_id):
        new_host_body = {
            'new_host': new_host_id
        }
        nh = self.session.post(self.host, new_host_body)
        nh.close()

    def kick_room(self,name):
        kick_body = {
            'kick': name
        }
        kc = self.session.post('https://drrr.com/room/?ajax=1', kick_body)
        kc.close()

    def groom(self, new_host_id, tripcode):
        valid = self.loadAdm(tripcode)
        print(valid)
        try:
            if valid == True:
                new_host_body = {
                    'new_host': new_host_id
                }
                nh = self.session.post(self.host, new_host_body)
                nh.close()
            return True
        except Exception as e:
            print(e)
        
    def admin_kick(self, message, name_sender, tripcode, id_sender):
        valid = self.loadAdm(tripcode)
        try:
            if valid == True:
                if re.findall('/kick', message):
                    message = message[6:]
                    if message == 'Athus':
                        return
                    rooms = self.session.get(
                        "https://drrr.com/json.php?update=")
                    user = []
                    id_user = []

                    if rooms.status_code == 200:
                        rooms_data = json.loads(rooms.content)
                    for rooms in rooms_data['users']:
                        user.append(rooms)
                    for j in range(len(user)):
                        if user[j]['name'] in message:
                            kick_body = {'kick': user[j]['id']}
                            kc = self.session.post(
                                self.host, kick_body)
                            kc.close()
                            self.admin = name_sender
                            self.banido = message
                            self.comand = 'Kikado'
                            break
        except Exception:
            pass


    def admin_ban(self, message, name_sender, tripcode, id_sender):
        self.ban = True
        valid = self.loadAdm(tripcode)
        try:
            if valid == True:
                if re.findall('/ban', message):
                    message = message[5:]
                    if message == 'Athus':
                        return
                    rooms = self.session.get(
                        "https://drrr.com/json.php?update=")
                    user = []
                    if rooms.status_code == 200:
                        rooms_data = json.loads(rooms.content)
                    for rooms in rooms_data['users']:
                        user.append(rooms)
                    for j in range(len(user)):
                        if user[j]['name'] in message:
                            try:
                                admcheck = self.loadAdm(user[j]['tripcode'])
                                if admcheck == True:
                                    self.ban = False
                                    self.post(message='Para de ser babacão', to=id_sender)
                            except Exception:
                                pass
                            #report_and_ban_user
                            if self.ban == True:
                                #song = "https://files.catbox.moe/hewoyb.mp3"
                                #self.share_music(url=song, name='Ban:{}'.format(user[j]['name']))
                                ban_body = {'report_and_ban_user': user[j]['id']}
                                kc = self.session.post(
                                    self.host, ban_body)
                                kc.close()
                                self.admin = name_sender
                                self.banido = message
                                self.comand = 'Banido'
                                logs = open('./cache/log.txt', 'a')
                                log = 'ADM:{}\nBanido:{}\n==============\n'.format(self.admin,self.banido,)
                                logs.write(log)
                                logs.close()
                                self.unbanDic(user[j]['name'],user[j]['id'])
                                break
        except Exception:
            pass

    def listcommands(self):
        commandName = 'admin'
        if self.spam[commandName] == False:
            self.post(message="|==ADMIN==|\n|/set|\n|/kick name|\n|/ban name|\n|/room_name Name_room|\n|/room_info Description|\n|/host|\n|/log|\n|/enable|\n|/block|")
            self.spam[commandName] = True
            self.avoid_spam(commandName)

    def log(self):
        self.post(message='Logs:\n|ADM:{}|\n|{}:{}|'.format(self.admin, self.comand,  self.banido))
    

    # def adminList(self):
    #     commandName = 'admin_list'
    #     if self.spam[commandName] == False:
    #         with open('athus/Database/adm.json','r',encoding='utf-8') as json_file:
    #             admin = json.load(json_file)    
    #         adminlist = ""
    #         for i in range(len(admin)):
    #             adminlist += '|@{}|\n'.format(admin[i]['username'])
    #         self.post(
    #                 message="{}".format(adminlist))
    #         self.spam[commandName] = True
    #         self.avoid_spam(commandName)

    def showBl(self):
        commandName = 'admin_list'
        if self.spam[commandName] == False:
            with open("athus/Database/Blacklist.json", "r",encoding='utf-8') as json_file:
                Blackusers = json.load(json_file)
            admin = ""
            for i in range(len(Blackusers)):
                admin += '|@{}#{}|\n'.format(Blackusers[i]['username'],Blackusers[i]['Tripcode'])
            self.post(message={admin})
            self.spam[commandName] = True
            self.avoid_spam(commandName)

#anti-kick
    def loop_msg(self):
        while True:
            time.sleep(120)
            usuario = self.returnIduser(self.nameBot)
            if usuario == "vazio":
                break
            self.post(message="...", to=usuario)


    def thanos(self, tripcode, name_sender):
        if tripcode == "TqOzGmy5V.":
            gif = "https://media1.tenor.com/images/f1b55c5a0fc1f760ce2b0b5c5d495470/tenor.gif?itemid=14599588"
            song = "https://files.catbox.moe/hewoyb.mp3"
            self.share_music(url=song, name='Kick ALL ON')
            self.post(message='.', url=gif)
            try:
                rooms = self.session.get("https://drrr.com/json.php?update=")
                user = []
                if rooms.status_code == 200:
                    rooms_data = json.loads(rooms.content)
                for rooms in rooms_data['users']:
                    user.append(rooms)
                for j in range(len(user)):
                    if user[j]['name'] == 'Athus':
                        pass
                    elif user[j]['name'] == name_sender:
                        pass
                    else:
                        time.sleep(1)
                        kick_body = {'kick': user[j]['id']}
                        kc = self.session.post('https://drrr.com/room/?ajax=1', kick_body)
                        kc.close()
            except Exception as e:
                pass