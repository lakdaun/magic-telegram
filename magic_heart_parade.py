import asyncio

from random import choice
from telethon import TelegramClient, events, errors

api_id = 27869659
api_hash = "5a757cf261de7f56fa153283d1ad3a92"

client = TelegramClient("tg-account", api_id , api_hash)

words_for_start = ["magic"]

heart = "🤍"
colored_hearts = ['💗', '💓', '💖', '💘', '❤️', '💞']

love_words = "I love you💓"

number_of_frames = 50

replace_dict = {
    "0": heart,
    "1": choice(colored_hearts)
}

heart_map = '''
00000000000
00111011100
01111111110
01111111110
00111111100
00011111000
00001110000
00000100000
00000000000
'''
lines = heart_map.strip().split('\n')
height = len(lines)

width = len(lines[0])

global_output = ""

delay = 0.01


def frames_gen():
    output = ""
    for char in heart_map:
        if char == "1":
            output += choice(colored_hearts)
        elif char == "0":
            output += heart
        else:
            output += char
    return output


async def magic_parade(event):
    for _ in range(number_of_frames):
        frame = frames_gen()
        await event.edit(frame)
        await asyncio.sleep(delay)


async def build_place(event):
    global global_output
    output = ''
    for _ in range(height):
        output += '\n'
        for _ in range(width):
            output += heart
            await event.edit(output)
            await asyncio.sleep(delay)
    global_output = output


async def processed_heart(event):
    global_output_lines = global_output.strip().split('\n')
    heart_map_lines = heart_map.strip().split('\n')
    for i in range(len(heart_map_lines)):
        if heart_map_lines[i].count('1') > 0:
            global_output_lines[i] = heart_map_lines[i].translate(str.maketrans(replace_dict))
        try:
            await event.edit('\n'.join(global_output_lines))
            await asyncio.sleep(delay * 10)
        except errors.MessageNotModifiedError:
            pass


async def process_love_words(event):
    words = love_words.split(" ")
    output = ""
    for word in words:
        output += word + " "
        await event.edit(output)
        await asyncio.sleep(delay * 5)


@client.on(events.NewMessage(outgoing=True))
async def start(event):
    if event.message.message in words_for_start:
        await build_place(event)
        await processed_heart(event)
        await magic_parade(event)
        await process_love_words(event)


if __name__ == "__main__":
    client.start()
    client.run_until_disconnected()
