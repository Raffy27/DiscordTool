import requests
import json
import consolemenu
import io
import threading
import time
import traceback
from img2ascii import img2ascii
from PIL import Image

class MainUser:
    def __init__(self, obj, token):
        self.id = obj['id']
        self.user = obj['username']
        self.avatar = obj['avatar']
        self.num = obj['discriminator']
        self.email = obj['email']
        self.verified = obj['verified']
        self.phone = obj['phone']
        self.token = token

Me = None

def login():
    token = input('Token = ')
    r = requests.get('https://discord.com/api/v6/users/@me', headers={'authorization': token})
    if not r.status_code == 200:
        print('Login failed.')
        exit()
    global Me
    Me = MainUser(json.loads(r.text), token)

def get_avatar(id, avatar, size = '64'):
    r = requests.get(f'https://cdn.discordapp.com/avatars/{id}/{avatar}.png?size=' + size)
    if r.status_code == 200:
        return r.content
    return ''

def info():
    img_content = get_avatar(Me.id, Me.avatar)
    if img_content == '':
        print('[No Avatar]')
    else:
        img = Image.open(io.BytesIO(img_content))
        img2ascii.print_img(img, (32,32), 'o', 1, True)
    print(f'\nUsername: {Me.user}#{Me.num}')
    print(f'User ID: {Me.id}')
    print(f'Email: {Me.email}')
    print(f'Phone: {Me.phone}')
    print(f'Verified: {Me.verified}')
    input()

def send_raw_message(ch_id, msg, fpath = ''):
    data = {
        'content': msg,
        'tts': 'false'
    }
    files = {}
    if not fpath == '':
        files['file'] = (fpath.split('\\')[-1], open(fpath, 'rb').read())
    r = requests.post(f'https://discord.com/api/v6/channels/{ch_id}/messages',
        headers={'authorization': Me.token},
        data=data, files=files
    )
    return r
    
def send_message():
    ch_id = input('Channel ID: ')
    msg = input('Message: ')
    r = send_raw_message(ch_id, msg)
    if r.status_code == 200:
        print('Message sent!')
    else:
        print('Failed to send message:', r.status_code)
    input()

def send_file():
    ch_id = input('Channel ID: ')
    msg = input('Message: ')
    f = input('File path: ')
    r = send_raw_message(ch_id, msg, f)
    if r.status_code == 200:
        print('Message sent!')
    else:
        print('Failed to send message:', r.status_code)
    input()

def user_info_raw(user_id, retry = True):
    r = requests.get(f'https://discord.com/api/v6/users/{user_id}/profile', headers={'authorization': Me.token})
    if not r.status_code == 200:
        if retry:
            if r.status_code == 429:
                lim = json.loads(r.text)
                time.sleep(lim['retry_after'] / 1000)
                return user_info_raw(user_id, True)
        return None
    return json.loads(r.text)

def mutual_friends_raw(user_id):
    r = requests.get(f'https://discord.com/api/v6/users/{user_id}/relationships', headers={'authorization': Me.token})
    if not r.status_code == 200:
        return None
    return json.loads(r.text)

def user_info():
    user_id = input('User ID: ')
    t = user_info_raw(user_id)
    print(t)
    if t == None:
        print('Failed to get user info.')
        input()
        return
    nitro = not t['premium_since'] == None
    t = t['user']
    img_content = get_avatar(t['id'], t['avatar'])
    if img_content == '':
        print('[No Avatar]')
    else:
        img = Image.open(io.BytesIO(img_content))
        img2ascii.print_img(img, (32,32), 'o', 1, True)
    print(f'\nUsername: {t["username"]}#{t["discriminator"]}')
    print(f'User ID: {t["id"]}')
    print(f'Nitro: {nitro}')
    input()

def download_avatar():
    user_id = input('User ID: ')
    t = user_info_raw(user_id)
    if t == None:
        print('Failed to get user info.')
        input()
        return
    t = t['user']
    img_content = get_avatar(t['id'], t['avatar'], '512')
    if img_content == '':
        print('[No Avatar]')
    else:
        img = Image.open(io.BytesIO(img_content))
        img.save(user_id + '.png', 'png')
        print('Avatar saved!')
    input()

def get_member_count(srv_id):
    r = requests.get(f'https://discord.com/api/v6/guilds/{srv_id}?with_counts=true', headers={'authorization': Me.token})
    if not r.status_code == 200:
        return -1
    return json.loads(r.text)['approximate_member_count']

def get_servers_raw():
    r = requests.get(f'https://discord.com/api/v6/users/@me/guilds', headers={'authorization': Me.token})
    if not r.status_code == 200:
        return None
    return json.loads(r.text)

def get_servers():
    t = get_servers_raw()
    if t == None:
        print('Filed to get the list of servers')
        input()
        return
    for srv in t:
        print(f'[{srv["id"]}] {srv["name"]}')
    input()

def create_list():
    import Members
    input()

def bulk_send():
    ch_id = input('Channel ID: ')
    msg = input('Message: ')
    count = int(input('Count: '))
    print('Sending messages...')
    for i in range(count):
        sent = False
        while not sent:
            r = send_raw_message(ch_id, msg)
            if not r.status_code == 200:
                if r.status_code == 429:
                    lim = json.loads(r.text)
                    time.sleep(lim['retry_after'] / 1000)
                else:
                    print('Unknown response encountered:', r.status_code)
                    input()
                    return
            else:
                sent = True
        print(f'\tSent {i+1}/{count} -> ~{((i+1)*100/count):.2f}%', end='\r')
    print('\nDone')
    input()
