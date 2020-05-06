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

def get_avatar(id, avatar):
    r = requests.get(f'https://cdn.discordapp.com/avatars/{id}/{avatar}.png?size=64')
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
    r = requests.post(f'https://discordapp.com/api/v6/channels/{ch_id}/messages',
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

def user_info():
    user_id = input('User ID: ')
    r = requests.get(f'https://discordapp.com/api/v6/users/{user_id}/profile', headers={'authorization': Me.token})
    if not r.status_code == 200:
        print('Failed to get user info.')
        input()
        return
    t = json.loads(r.text)
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


def typing(ch_id):
    task = threading.currentThread()
    while getattr(task, 'run', True):
        requests.post(f'https://discordapp.com/api/v6/channels/{ch_id}/typing', headers={'authorization': Me.token})
        time.sleep(10)