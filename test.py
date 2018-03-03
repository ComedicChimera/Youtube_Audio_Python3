from youtube_audio import AudioClient

client = AudioClient()


class Player:
    def __init__(self):
        self.queue = []
        self.state = client.audio_out
        self.playing = False

    def play(self, name):
        self.queue.append(name)
        if len(self.queue) == 1 and not self.playing:
            self.send_audio()
        else:
            print(name, 'added to queue.')

    def skip(self):
        self.stop()
        if len(self.queue) > 0:
            self.send_audio()

    def send_audio(self):
        vid_id = client.get_video_id(self.queue.pop(0))
        vid_data = client.get_video_data(vid_id)
        link = vid_data.getbestaudio().url
        client.play_audio(link)
        print('Now Playing:', vid_data.title)
        self.playing = True

    @staticmethod
    def pause():
        client.set_pause_state(True)

    @staticmethod
    def resume():
        client.set_pause_state(False)

    def stop(self):
        self.playing = False
        client.stop_audio()

    @staticmethod
    def set_audio_out(state):
        client.set_audio_out(state)

player = Player()


def execute_command(inp):
    data = inp.split(' ')
    cmd = data[0]
    args = ' '.join(data[1:])
    if cmd == 'play':
        player.play(args)
    elif cmd == 'continue':
        if len(player.queue) > 0 and not player.playing:
            player.send_audio()
    elif cmd == 'pause':
        player.pause()
    elif cmd == 'resume':
        player.resume()
    elif cmd == 'stop':
        player.stop()
    elif cmd == 'volume':
        client.volume(int(args))
    elif cmd == 'get_devices':
        print(client.query_output_devices())
    elif cmd == 'set_device':
        player.set_audio_out(args)
    elif cmd == 'skip':
        player.skip()

while True:
    inp = input('$ ')
    # try:
    execute_command(inp)
    # except Exception as e:
    # print('Error: %s\n' % e)
    print('\n')
