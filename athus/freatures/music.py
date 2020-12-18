import requests
import time
import json
import re
import os
from random import randint
import threading
import youtube_dl
import sys
import toml
from requests_toolbelt import MultipartEncoder, MultipartEncoderMonitor


class Uploader:
    def __init(self, filename, file_host_url):
        self.filename = filename
        self.file_host_url = file_host_url

    def _multipart_post(self, data):
        encoder = MultipartEncoder(fields=data)
        monitor = MultipartEncoderMonitor(encoder)
        r = requests.post(self.file_host_url,
                          data=monitor,
                          headers={'Content-Type': monitor.content_type})
        return r

class FileioUploader(Uploader):
    def __init__(self, filename):
        self.filename = filename
        self.file_host_url = "https://file.io"

    def execute(self):
        file = open('./cache/music/{}'.format(self.filename), 'rb')
        try:
            data = {'file': (file.name, file, self._mimetype())}
            response = self._multipart_post(data)
        finally:
            file.close()

        return response.json()['link']


class CatboxUploader(Uploader):
    def __init__(self, filename):
        self.filename = filename
        self.file_host_url = "https://litterbox.catbox.moe/resources/internals/api.php"

    def execute(self):
        file = open('./cache/music/{}'.format(self.filename), 'rb')
        try:
        	#rash: f30cb59306e2d72a0e958cbec
            data = {
                'reqtype': 'fileupload',
                'time': '72h',
                'fileToUpload': (file.name, file)
            }
            response = self._multipart_post(data)
        finally:
            file.close()

        return response.text


class musicSistem(object):
    def __init__(self):
        self.config = toml.load('config.toml')
        self.session = requests.session()
        self.spam = {"next": False, "skip": False, "pause": False,"music": False,"post_music": False}
        self.music_info = []
        self.host = 'https://drrr.com/room/?ajax=1'
        self.paylist_cont = 0
        self.paylist_duration = []
        self.paylist = []
        self.paylist_title = []
        self.listUrl = []
        self.countMusic = 0
        self.pause = True
        self.nextCont = 0
        self.playStatus = False
        self.blockMusic = True
        self.name = 'music_1.mp3'
        self.durationMusic = 600
        self.load_cookie()

    def load_cookie(self):
        f = open(self.config['Botconfig']['cookie'], 'r')
        self.session.cookies.update(eval(f.read()))
        f.close()


    def blockMusicCommand(self):
        self.blockMusic = False

    def AnableMusicCommand(self):
        self.blockMusic = True

    def avoid_spam(self, com):
        time.sleep(5)
        self.spam[com] = False

    def default(self):
        self.durationMusic = 600

    def livre(self):
        self.durationMusic = 10800

    def post(self, message, url='', to=''):
        post_body = {
            'message': message,
            'url': url,
            'to': to
        }
        p = self.session.post(
            url=self.host, data=post_body)
        p.close()


    def share_music(self, url, name=''):
        share_music_body = {
            'music': 'music',
            'name': name,
            'url': url
        }
        p = self.session.post(
            url=self.host, data=share_music_body)
        p.close()

    def thPlay(self):
        t_start = threading.Thread(target=self.play)
        t_start.start()

    def play(self):
        if self.playStatus == False:
            self.playStatus = True
            self.pause = False
            while True:
                try:
                    if self.pause == False:
                        self.share_music(
                            url=self.paylist[self.paylist_cont], name=self.paylist_title[self.paylist_cont])
                        self.paylist_cont += 1
                        loop = self.paylist_cont - 1
                        for i in range(0, self.paylist_duration[loop]):
                            if self.pause == True:
                                return
                            time.sleep(1)
                    else:
                        return
                except Exception as e:
                    self.post(message="/me Playlist Vazia")
                    self.playStatus = False
                    return
        else:
            self.post(message="/me:Musica em andamento")

    def pause_playlist(self):
        commandName = 'pause'
        if self.spam[commandName] == False:
            self.spam[commandName] = True
            self.pause = True
            self.playStatus = False
            self.post(message="/me Playlist Pausada")
            time.sleep(10)
            self.avoid_spam(commandName)

    def skip_playlist(self):
        commandName = 'skip'
        if self.spam[commandName] == False:
            self.spam[commandName] = True
            self.pause = True
            self.playStatus = False
            self.post(message="/me Musica Pulada")
            #tempo para  não bugar o tempo de cada musica
            time.sleep(2)
            t_skip = threading.Thread(target=self.play)
            t_skip.start()
            self.avoid_spam(commandName)

    def next(self):
        commandName = 'next'
        if self.spam[commandName] == False:
            self.spam[commandName] = True
            self.playStatus = False
            try:
                self.post(
                    message="/me Proxima Musica: {} ".format(self.paylist_title[self.paylist_cont]))
            except Exception:
                self.post(message="/me Playlist Vazia")
            time.sleep(10)
            self.avoid_spam(commandName)

    def rebotPlaylist(self):
        self.post(
            message="/me Restart Playlist Total de Musicas: {}".format(len(self.paylist)))
        self.paylist_cont = 0
        self.pause = True
        self.playStatus = False
        time.sleep(1)
        t_skip = threading.Thread(target=self.play)
        t_skip.start()

    def skipPlaylist(self):
        self.post(message="/me Playlist Skip: {} music".format(len(self.paylist)))
        self.paylist_cont =  len(self.paylist)
        self.pause = True
        self.playStatus = False
        time.sleep(1)
        t_skip = threading.Thread(target=self.play)
        t_skip.start()


    def replayPlaylist(self):
        self.post(message="/me ▷Replay▷")
        self.paylist_cont =  len(self.paylist) - 2
        self.pause = True
        self.playStatus = False
        time.sleep(1)
        t_skip = threading.Thread(target=self.play)
        t_skip.start()

    def downloadMusic(self):
        while True:
            if self.spam["music"] == False:
                try:
                    url = self.listUrl[self.countMusic]
                    #print(url)
                    #self.post(message=f"▷Carregando Sua Musica.▷", to=user)
                    t_start = threading.Thread(target=self.playlist, args=(url,))
                    t_start.start()
                    self.countMusic += 1
                except Exception:
                    pass

    def musicList(self, message, name_sender, id_sender):
        link = message[4:].replace(" ", "")
        self.listUrl.append(link)
        self.post(message=f"/me @{name_sender} ▷Carregando...▷")


    def playlist(self, message):
        commandName = 'music'
        uploader_classes = {
        "catbox": CatboxUploader,
        "fileio": FileioUploader}
        if self.spam[commandName] == False:
            if self.blockMusic == True:

                def upload(self, host, name):
                    uploader_class = uploader_classes[host]
                    uploader_instance = uploader_class(name)
                    #print(name)
                    result = uploader_instance.execute()

                    self.paylist.append(result)
                    self.paylist_duration.append(self.music_info['duration'])
                    self.paylist_title.append(self.music_info['title'])
                    os.remove("./cache/music/music_1.mp3")

                def sand_music(self, message):
                    try:
                        link = "https://www.youtube.com/watch?v={}".format(
                            message)
                        ydl_consult = {
                            'quiet': True,
                            'skip_download': True,
                        }
                        with youtube_dl.YoutubeDL(ydl_consult) as ydl:
                            info = ydl.extract_info(link)
                            if info['duration'] > self.durationMusic:
                                self.post(
                                    message="/me Musica cancelada devido a sua duração.!")
                                self.avoid_spam(commandName)
                                return
                    except Exception:
                        self.post(message="/me [Error 404 Not Found]")
                        self.avoid_spam(commandName)
                        return
                    try:
                        #print(message)
                        title = 'music_1'
                        extp = '.webm'
                        ydl_opts = {
                            'format': 'bestaudio/best',
                            'outtmpl': './cache/music/{}{}'.format(title, extp),
                            'postprocessors': [{
                                       'key': 'FFmpegExtractAudio',
                                       'preferredcodec': 'mp3',
                                       'preferredquality': '192',
                                   }],
                        }
                        #self.post(message="/me ▷Carregando musica▷")
                        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                            # link = "https://www.youtube.com/watch?v={}".format(message)
                            filenames = ([link])
                            ydl.download(filenames)
                            self.music_info = info
                        upload(self,host = 'catbox', name = '{}'.format(self.name))
                        self.avoid_spam(commandName)
                        self.post(message=f"/me [add] {self.music_info['title']}")
                    except Exception:
                        self.post(message="/me Erro Link Invalido")
                        self.avoid_spam(commandName)
                self.spam[commandName] = True
                sand_music(self, message=message)
            else:
                self.spam[commandName] = True
                self.post(message='/me Comando Bloqueado')
                self.avoid_spam(commandName)



    def music_help(self, message, name_sender):
        commandName = 'post_music'
        if self.spam[commandName] == False:
            ajuda_musica = "https://i.imgur.com/hmmERQi.png"
            self.post(message="Como usar musica.",
                      url='{}'.format(ajuda_musica))  # deixa a sala
            self.spam[commandName] = True
            time.sleep(30)
            self.avoid_spam(commandName)
