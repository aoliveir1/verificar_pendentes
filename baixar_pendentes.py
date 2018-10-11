import os
import time

protocolos = []
with open('protocolos.txt') as p:
    for protocolo in p:
        protocolos.append(protocolo.strip())

arquivos = []
for _, _, arquivo in os.walk('Downloads'):
    arquivos.append(str(arquivo).lower())

baixar = []
print('\n')
for protocolo in protocolos:
    nome = str(protocolo[11:].strip().lower())
    protocolo = str(protocolo[:10].strip())
    if nome in arquivos[0]:
        pass
    else:
        print(nome)
        baixar.append('https://{}/download/{}'.format(protocolo, nome))

tempo = len(baixar) * 10

if len(baixar) > 0:
    import platform
    from splinter import Browser
            
    print('\nBaixando {} arquivo{}'.format(len(protocolos), 's.' if len(protocolos) > 1 else '.'))

    executable_path = 'C:\\webdriver\\win_7\\chromedriver.exe' if platform.uname()[2] == '7' else 'C:\\webdriver\\win_xp\\chromedriver.exe'
    browser = Browser('chrome', executable_path = executable_path)
    browser.visit('login')
    time.sleep(0.5)
    browser.fill('username', 'my_username')
    browser.fill('password', 'my_password')    
    browser.find_by_name('login').click()
    time.sleep(0.5)

    for b in baixar:
        browser.visit(b)
        
    time.sleep(tempo)
    browser.quit()

with open('protocolos.txt', 'w') as p:
    p.write('')
    p.close()
