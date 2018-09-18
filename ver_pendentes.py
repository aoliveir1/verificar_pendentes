import os
import platform
from time import localtime, sleep, strftime, time
from splinter import Browser
import winsound
from bs4 import BeautifulSoup

print('Abrindo Google Chrome...')
executable_path = 'C:\\webdriver\\win_7\\chromedriver.exe' if platform.uname()[2] == '7' else 'C:\\webdriver\\win_xp\\chromedriver.exe'
browser = Browser('chrome', executable_path = executable_path)
print('Acessando a página de login...')
browser.visit('https://login')
print('Efetuando login...')
sleep(1)
browser.fill('username', 'my_username')
browser.fill('password', 'my_password')
browser.find_by_name('login').click()

print('Acessando página de pendentes...')
sleep(1)
browser.visit('https://pendentes')

tempo = 120

while True:
    
    os.system('cls')
    
    if 'Resumo dos protocolos impressos' in browser.html:
        browser.reload()
    else:
        browser.visit('https://login')
        browser.fill('username', 'my_username')
        browser.fill('password', 'my_assword')
        browser.find_by_name('login_copista').click()
        sleep(1)
        browser.visit('https://pendentes')
    sleep(1)
    
    if 'Nenhum protocolo encontrado.' not in browser.html:  
        start = time()
        
        if tempo < (15*60):
            tempo *= 2
   
        print('Pendente:\t{}\n'.format(strftime('%H:%M:%S', localtime())))
        
        soup = BeautifulSoup(browser.html, 'html.parser')
        plots = soup.find_all('div', attrs={'class': 'titulo'})

        protocolos = []
        print('  Protocolo      Arquivo')
        for i, plot in enumerate(plots):
            if i > 1:
                plot = str(plot.text.strip())
                protocolo = plot[21:31]
                arquivo = plot[36:]
                plotagem = {'protocolo':protocolo, 'arquivo':arquivo.replace(' ', '-')}
                protocolos.append(plotagem['protocolo'] + ' ' + plotagem['arquivo'] + '\n')
                print(i, plot[21:])                

        with open('C:\\protocolos.txt', 'w') as txt:
            for protocolo in protocolos:                
                txt.write(protocolo)
            txt.close
            
        os.system('baixar_pendentes.py')
        winsound.PlaySound('pendente.wav', winsound.SND_FILENAME)
        end = time()
        elapsed = end - start        
        print('\nPróxima verificação:\t{}'.format(strftime('%H:%M:%S', localtime(time()+tempo-elapsed))))
    else:
        tempo = 120            
        print('Nenhum pendente:\t{}\nPróxima verificação:\t\t{}'.format(strftime('%H:%M:%S', localtime()), strftime('%H:%M:%S', localtime(time()+tempo))))
    sleep(tempo)

browser.quit()
print('Encerrado.')
