from colorama import Back, Style
from colorama import init as colorama_init
from telethon.tl.types import Channel, Chat

keywords = ('кинолог', 'собака', 'зоопсихолог')
result_channel_ID = -1002444797511


async def set_chats(client) -> list:
    colorama_init()
    print(Back.CYAN + 'Set of chats starting...' + Style.RESET_ALL)
    dict_for_chat = {}
    counter = 1
    async for dialog in client.iter_dialogs():
        dict_for_chat[counter] = dialog.entity
        counter += 1

    dict_for_print = {}
    for k, dialog in dict_for_chat.items():
        if isinstance(dialog, Channel) or isinstance(dialog, Chat):
            dict_for_print[k] = dialog.title
    print(f'{dict_for_print}')

    print(Back.CYAN + 'Your chats are listed here.' + Style.RESET_ALL)

    keys_list = list(map(int, input(Back.CYAN + 'Enter the chat numbers separated by a space -'+ Style.RESET_ALL).split()))

    id_list = []
    for number_chat in keys_list:
        try:
            find_id = dict_for_chat[number_chat].id
            id_list.append(find_id)
        except KeyError:
            print(f'It seems that you entered the wrong channel number: {number_chat}. '
                  'Please check the channel numbers carefully and re-enter them.')
            continue
    return id_list
