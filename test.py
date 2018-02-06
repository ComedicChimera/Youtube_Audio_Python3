from youtube_audio import AudioClient

client = AudioClient()


def execute_command(inp):
    data = inp.split(' ')
    cmd = data[0]
    args = ' '.join(data[1:])
    if cmd == 'play':
        vid_id = client.get_video_id(args)
        vid_data = client.get_video_data(vid_id)
        link = vid_data.getbestaudio().url
        client.play_audio(link)
        print("Now Playing: ", vid_data.title)
    elif cmd == 'pause':
        client.set_pause_state(True)
    elif cmd == 'resume':
        client.set_pause_state(False)
    elif cmd == 'stop':
        client.stop_audio()
    elif cmd == 'volume':
        client.volume(int(args))
    elif cmd == 'get_devices':
        print(client.query_output_devices())
    elif cmd == 'set_device':
        client.audio_out = args

while True:
    inp = input('$ ')
    # try:
    execute_command(inp)
    # except Exception as e:
    # print('Error: %s\n' % e)
    print('\n')
