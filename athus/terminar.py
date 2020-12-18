    # def block (self, message, name_sender, tripcode, id_sender):
    #     message = message[7:]
    #     for i in range(len(self.admin_list)):
    #         if tripcode == self.admin_list[i]:
    #             if 'gif' in message:
    #                 t_gif = threading.Thread(
    #                     target=self.social.blockGifCommand)
    #                 t_gif.start()
    #             elif 'music' in message:
    #                 t_music = threading.Thread(
    #                     target=self.music.blockMusicCommand)
    #                 t_music.start()
    #             elif 'ship' in message:
    #                 t_ship = threading.Thread(
    #                     target=self.social.blockShipCommand)
    #                 t_ship.start()

    # def anable (self, message, name_sender, tripcode, id_sender):
    #     message = message[8:]
    #     for i in range(len(self.admin_list)):
    #         if tripcode == self.admin_list[i]:
    #             if 'gif' in message:
    #                 t_gif = threading.Thread(
    #                     target=self.social.AnableGifCommand)
    #                 t_gif.start()
    #             elif 'music' in message:
    #                 t_music = threading.Thread(
    #                     target=self.music.AnableMusicCommand)
    #                 t_music.start()
    #             elif 'ship' in message:
    #                 t_ship = threading.Thread(
    #                     target=self.social.AnableShipCommand)
    #                 t_ship.start()


    #https://github.com/jonathanong/heroku-buildpack-ffmpeg-latest.git