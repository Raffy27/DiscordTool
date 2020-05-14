import Client
import Exploits
import requests
import traceback
import time
from consolemenu import ConsoleMenu
from consolemenu.items import SubmenuItem, FunctionItem
from threading import Thread

def about():
    print('Who even cares at this point')
    input()

def safe_remove_menu(task_menu):
    time.sleep(1)
    tasks_menu.remove_item(task_menu)

def terminate_task(task, name, task_menu):
    print(f'[{name}]\nTerminating...')
    task.run = False
    task.join()
    print('Done.')
    input()
    Thread(target=safe_remove_menu, args=[task_menu]).start()

def create_task(name, main, *arg):
    print(f'[{name}]')
    args = []
    for a in arg:
        args.append(input(a + ': '))
    
    task = Thread(target=main, args=args)
    task_menu = FunctionItem(name, terminate_task, [task, name], should_exit=True)
    task_menu.args.append(task_menu)
    tasks_menu.append_item(task_menu)
    task.start()
    print('Started successfully.')
    input()

Client.login()

gen_menu = ConsoleMenu('Send messages and files')
gen_menu.append_item(FunctionItem('Send message', Client.send_message))
gen_menu.append_item(FunctionItem('Send file', Client.send_file))
gen_menu.append_item(FunctionItem('Bulk send', input))
gen_menu.append_item(FunctionItem('User info', Client.user_info))
gen_menu.append_item(FunctionItem('Server list', Client.get_servers))
gen_menu.append_item(FunctionItem('Server members', input))
gen_menu.append_item(FunctionItem('Download avatar', Client.download_avatar))

exploit_menu = ConsoleMenu('Exploits and misc features')
exploit_menu.append_item(FunctionItem('Infinite typing', create_task, 
    ['Infinite typing', Exploits.typing, 'Channel ID']
))
exploit_menu.append_item(FunctionItem('Status changer', create_task,
    ['Status changer', Exploits.status_changer]
))
exploit_menu.append_item(FunctionItem('Friend finder', Exploits.friend_list))
exploit_menu.append_item(FunctionItem('IP logger', input))
exploit_menu.append_item(FunctionItem('Crash link', Exploits.crash_link))
exploit_menu.append_item(FunctionItem('Read notification', input))
exploit_menu.append_item(FunctionItem('Local Storage reassembly', Exploits.reassembly))

tasks_menu = ConsoleMenu('Terminate running tasks')

menu = ConsoleMenu('Discord Tool v0.1.2', 'Coded by Raffy')
menu.append_item(FunctionItem('Info', Client.info))
menu.append_item(SubmenuItem('General', gen_menu, menu=menu))
menu.append_item(SubmenuItem('Exploits', exploit_menu, menu=menu))
menu.append_item(SubmenuItem('Tasks', tasks_menu, menu=menu))
menu.append_item(FunctionItem('About', about))
menu.formatter.set_items_bottom_padding(0)
menu.formatter.set_items_top_padding(0)
menu.formatter.set_title_align(align='center')

menu.show()