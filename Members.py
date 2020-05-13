from selenium import webdriver
from time import sleep
import json

driver = webdriver.Edge('res\\msedgedriver.exe')
driver.get('http://discord.com/login')

print('Login to continue')

while not driver.current_url == 'https://discord.com/channels/@me':
    sleep(1)

print('Login successful')

sleep(7)

with open('res\\GetMembers.js', 'r') as f:
    uscan = f.read()
driver.execute_script(uscan)
done = False
while not done:
    print('Not done')
    done = driver.execute_script('return done;')
    sleep(1)
tmp = driver.execute_script('return JSON.stringify(users);')
driver.close()
with open('Testers.json', 'w') as f:
    f.write(tmp)
print('Done!')