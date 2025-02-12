from telethon.tl.types import Channel, Chat

keywords = ('кинолог', 'собака', 'зоопсихолог')
result_channel_ID = -1001624784833  # TODO


async def set_chats(client) -> list:
    print('Set of chats starting...')
    dict_for_chat = {}
    counter = 1
    async for dialog in client.iter_dialogs():
        dict_for_chat[counter] = dialog.entity
        counter += 1

    dict_for_print = {}
    for k, dialog in dict_for_chat.items():
        if isinstance(dialog, Channel) or isinstance(dialog, Chat):
            dict_for_print[k] = dialog.title
    print('dict for print chats', dict_for_print)

    print('Your chats are listed here.')

    keys_list = list(map(int, input('Enter the chat numbers separated by a space -').split()))
    print('Chats are being monitored', keys_list, '\n', 'Waiting for messages')

    id_list = []
    for number_chat in keys_list:
        find_id = dict_for_chat[number_chat].id
        id_list.append(find_id)
    print(id_list)

    return id_list
