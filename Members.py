from selenium import webdriver
from time import sleep
import json
import Client

t = Client.get_servers_raw()
if t == None:
    print('Failed to get the list of servers')
    raise SystemExit
if len(t) == 0:
    print('The list of servers is empty')
    raise SystemExit
print(f'Added {len(t)} servers to the queue')

with open('res\\GetMembers.js', 'r') as f:
    uscan = f.read()
users = set()
total_expected = 0
total = 0
driver = webdriver.Edge('res\\msedgedriver.exe')
driver.get('https://discord.com/login')

print('Login to continue')
while not driver.current_url == 'https://discord.com/channels/@me':
    sleep(1)
print('Login successful!')

for srv in t:

    print(f'Processing [{srv["id"]}] {srv["name"]}')
    count = Client.get_member_count(srv['id'])
    print(f'Expected member count:', count)
    total_expected += count

    driver.get('https://discord.com/channels/' + srv['id'])

    wait = True
    while wait:
        sleep(0.5)
        wait = False
        try:
            driver.find_element_by_xpath('//div[@aria-label="Members"]')
        except:
            wait = True
    sleep(0.5)

    driver.execute_script(uscan)
    done = False
    while not done:
        done = driver.execute_script('return done;')
        sleep(1)
    tmp = json.loads(driver.execute_script('return JSON.stringify(users);'))
    total += len(tmp)
    users = users.union(tmp)
    print(f'Discovered {len(tmp)} members ~{len(tmp)*100//count}%.\n')

driver.close()
with open('Users.json', 'w') as f:
    json.dump(list(users), f)
print(f'Exported {total} users as Users.json')
print(f'Final discovery rate: ~{total*100//total_expected}%')