from freatures import admin
from freatures import autoban
from freatures import music
from freatures import social
from freatures import translation
from freatures import blacklist
import threading
import toml
import requests

class BotCommands(object):
    """Commands for bot"""
    def __init__(self):
        self.session = requests.session()
        self.config = toml.load('config.toml')
        self.social = social.Fun()
        self.music = music.musicSistem()
        self.configAdmn = admin.admininstrator()
        self.flood = autoban.AutomaticBan()
        self.trans = translation.Translation()
        self.Blacklist = blacklist.BlacklistDrrr()

    def loop(self):
        t_loop = threading.Thread(target=self.configAdmn.loop_msg)
        t_loop.start()
        t_loop = threading.Thread(target=self.music.downloadMusic)
        t_loop.start()


    def Search(self, message, id_sender, name_sender, tripcode):
        switcher = {
        self.config['commands']['command'][0]:self.help,
        self.config['commands']['command'][1]:self.commandsAdmins,
        self.config['commands']['command'][2]:self.play,
        self.config['commands']['command'][3]:self.pause,
        self.config['commands']['command'][4]:self.skip,
        self.config['commands']['command'][5]:self.queue,
        self.config['commands']['command'][6]:self.list_ban,
        self.config['commands']['command'][7]:self.clearBan,
        self.config['commands']['command'][8]:self.help_music,
        self.config['commands']['command'][9]:self.log,
        self.config['commands']['command'][10]:self.stop_trans,
        self.config['commands']['command'][11]:self.thanos,
        self.config['commands']['command'][12]:self.sera,
        self.config['commands']['command'][13]:self.report,
        self.config['commands']['command'][14]:self.trans,
        self.config['commands']['command'][15]:self.gif,
        self.config['commands']['command'][16]:self.add,
        self.config['commands']['command'][17]:self.t,
        self.config['commands']['command'][18]:self.set,
        self.config['commands']['command'][19]:self.kick,
        self.config['commands']['command'][20]:self.ban,
        self.config['commands']['command'][21]:self.unban,
        self.config['commands']['command'][22]:self.block,
        self.config['commands']['command'][23]:self.enable,
        self.config['commands']['command'][24]:self.room_name,
        self.config['commands']['command'][25]:self.room_info,
        self.config['commands']['command'][26]:self.exit,
        self.config['commands']['command'][27]:self.host,
        self.config['commands']['command'][28]:self.replay,
        self.config['commands']['command'][29]:self.troll_mode,
        self.config['commands']['command'][30]:self.default_mode,
        self.config['commands']['command'][31]:self.default,
        self.config['commands']['command'][32]:self.free,
        self.config['commands']['command'][33]:self.say,
        self.config['commands']['command'][34]:self.send,
        self.config['commands']['command'][35]:self.blacklist,
        self.config['commands']['command'][36]:self.dollar,
        self.config['commands']['command'][37]:self.rewind,
        self.config['commands']['command'][38]:self.replay2
        }

        for msg in switcher:
            if msg in message:
                #print('entrei', msg)
                set_function = switcher.get(msg)
                #print(set_function)
                t_search = threading.Thread(target=set_function, args=(message, id_sender, name_sender, tripcode))
                t_search.start()

    def help(self, message, id_sender, name_sender, tripcode):
        t_help = threading.Thread(target=self.social.help, args=(message, name_sender))
        t_help.start()

    def commandsAdmins(self, message, id_sender, name_sender, tripcode):
        t_admin = threading.Thread(target=self.configAdmn.listcommands)
        t_admin.start()

    def blacklist(self, message, id_sender, name_sender, tripcode):
        t_blacklist = threading.Thread(target=self.configAdmn.showBl)
        t_blacklist.start()

    # def admin_list(self, message, id_sender, name_sender, tripcode):
    #     t_listAdmin = threading.Thread(target=self.configAdmn.adminList)
    #     t_listAdmin.start()

    def play(self, message, id_sender, name_sender, tripcode):
        t_play = threading.Thread(target=self.music.thPlay)
        t_play.start()

    def pause(self, message, id_sender, name_sender, tripcode):
        t_pause = threading.Thread(target=self.music.pause_playlist)
        t_pause.start()

    def skip(self, message, id_sender, name_sender, tripcode):
        t_skip = threading.Thread(target=self.music.skip_playlist)
        t_skip.start()

    def queue(self, message, id_sender, name_sender, tripcode):
        t_next = threading.Thread(target=self.music.next)
        t_next.start()

    def list_ban(self, message, id_sender, name_sender, tripcode):
        t_listban = threading.Thread(target=self.configAdmn.listban)
        t_listban.start()

    def clearBan(self, message, id_sender, name_sender, tripcode):
        #arrumar
        t_listban = threading.Thread(target=self.configAdmn.clearlist)
        t_listban.start()

    def help_music(self, message, id_sender, name_sender, tripcode):
        t_music_help = threading.Thread(target=self.music.music_help, args=(message, name_sender))
        t_music_help.start()

    def log (self, message, id_sender, name_sender, tripcode):
        t_music_help = threading.Thread(target=self.configAdmn.log)
        t_music_help.start()

    def stop_trans(self, message, id_sender, name_sender, tripcode):
        #arrumar translation real time
        pass

    def thanos(self, message, id_sender, name_sender, tripcode):
        t_thanos = threading.Thread(target=self.configAdmn.thanos, args=(tripcode, name_sender))
        t_thanos.start()

    def sera(self, message, id_sender, name_sender, tripcode):
        t_sera = threading.Thread(target=self.social.ship, args=(message, name_sender))
        t_sera.start()

    def report (self, message, id_sender, name_sender, tripcode):
        t_report = threading.Thread(target=self.Blacklist.byebye, args=(message, tripcode))
        t_report.start()

    def trans(self, message, id_sender, name_sender, tripcode):
        #tradução tempo real
        pass
        # valid = self.loadAdm(tripcode)
        # if valid == True:
        #     #condições
        #     transMessage = re.findall(':.*', message)
        #     username= transMessage[0][2:]
        #     self.usernameTrans = username
        #     self.transBollean = True
        #     t_trans = threading.Thread(
        #         target=self.translation.userTranslation, args=(message, name_sender))
        #     t_trans.start()
        
    def gif(self, message, id_sender, name_sender, tripcode):
        t_ghipy = threading.Thread(target=self.social.ghipy, args=(message, name_sender, id_sender))
        t_ghipy.start()

    def add(self, message, id_sender, name_sender, tripcode):
        t_music = threading.Thread(target=self.music.musicList, args=(message, name_sender, id_sender))
        t_music.start()

    def t(self, message, id_sender, name_sender, tripcode):
        t_translation = threading.Thread(target=self.social.translation, args=(message, name_sender))
        t_translation.start()

    def set(self, message, id_sender, name_sender, tripcode):
        t_floodchat = threading.Thread(target=self.flood.floodchat, args=(message,tripcode))
        t_floodchat.start()

    def kick(self, message, id_sender, name_sender, tripcode):
        t_adm_k = threading.Thread(target=self.configAdmn.admin_kick, args=(message, name_sender, tripcode, id_sender))
        t_adm_k.start()

    def ban(self, message, id_sender, name_sender, tripcode):
        t_ban = threading.Thread(target=self.configAdmn.admin_ban, args=(message, name_sender, tripcode, id_sender))
        t_ban.start()

    def unban(self, message, id_sender, name_sender, tripcode):
        t_ban = threading.Thread(target=self.configAdmn.unbanOfficial, args=(message, tripcode))
        t_ban.start()

    def block(self, message, id_sender, name_sender, tripcode):
        t_bloc = threading.Thread(target=self.block, args=(message, name_sender, tripcode, id_sender))
        t_bloc.start()

    def enable(self, message, id_sender, name_sender, tripcode):
        t_anable = threading.Thread(target=self.anable, args=(message, name_sender, tripcode, id_sender))
        t_anable.start()

    def room_name(self, message, id_sender, name_sender, tripcode):
        t_adm_name = threading.Thread(target=self.configAdmn.setRomm_name, args=(message, tripcode))
        t_adm_name.start()

    def room_info(self, message, id_sender, name_sender, tripcode):
        t_adm_description = threading.Thread(target=self.configAdmn.setRomm_Description, args=(message, tripcode))
        t_adm_description.start()


    def exit (self, message, id_sender, name_sender, tripcode):
        if tripcode == "ATHUSo12kM":
            leave_body = {'leave': 'leave'}
            lr = self.session.post('https://drrr.com/room/?ajax=1', leave_body)
            lr.close()

    def host(self, message, id_sender, name_sender, tripcode):
        t_skip = threading.Thread(target=self.configAdmn.groom, args=(id_sender, tripcode))
        t_skip.start()

    def replay(self, message, id_sender, name_sender, tripcode):
        t_skip = threading.Thread(target=self.music.rebotPlaylist)
        t_skip.start()

    def rewind(self, message, id_sender, name_sender, tripcode):
        t_skip = threading.Thread(target=self.music.skipPlaylist)
        t_skip.start()

    def replay2(self, message, id_sender, name_sender, tripcode):
        t_skip = threading.Thread(target=self.music.replayPlaylist)
        t_skip.start()

    def troll_mode(self, message, id_sender, name_sender, tripcode):
        t_time = threading.Thread(target=self.autoban.troll)
        t_time.start()

    def default_mode(self, message, id_sender, name_sender, tripcode):
        t_time = threading.Thread(target=self.autoban.defaultime)
        t_time.start()

    def default(self, message, id_sender, name_sender, tripcode):
        t_default = threading.Thread(target=self.music.default)
        t_default.start()

    def free(self, message, id_sender, name_sender, tripcode):
        t_free = threading.Thread(target=self.music.livre)
        t_free.start()

    def say(self, message, id_sender, name_sender, tripcode):
        t_mensagemprivate = threading.Thread(target=self.social.mensagemprivate, args=(message, name_sender, id_sender))
        t_mensagemprivate.start()

    def send(self, message, id_sender, name_sender, tripcode):
        t_sendMessage = threading.Thread(target=self.social.privatemenssagem, args=(message, name_sender))
        t_sendMessage.start()

    def dollar(self, message, id_sender, name_sender, tripcode):
        t_sendMessage = threading.Thread(target=self.social.cotacao)
        t_sendMessage.start()