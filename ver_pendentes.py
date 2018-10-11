import os
import platform
import shutil
import datetime
import unidecode
from time import localtime, sleep, strftime, time
from splinter import Browser
import winsound
from bs4 import BeautifulSoup

pendentes = 'C:/Documents and Settings/pressione ENTER/Meus documentos/Downloads/'
antigos = 'C:/Documents and Settings/pressione ENTER/Meus documentos/Downloads_antigos/'
cancelados = 'C:/Documents and Settings/pressione ENTER/Meus documentos/Downloads_cancelados/'
        
print('Abrindo Google Chrome...')
executable_path = 'C:/Plotagem/webdriver/win_7/chromedriver.exe' if platform.uname()[2] == '7' else 'C:/Plotagem/webdriver/win_xp/chromedriver.exe'
browser = Browser('chrome', executable_path = executable_path)
print('Acessando a página de login...')
browser.visit('https://ucsvirtual.ucs.br/impressoes/plotista/login')
print('Efetuando login...')
sleep(0.1)
browser.fill('username', 'ucscampus8')
browser.fill('password', 'Pzt2Ytn236!')
browser.find_by_name('login_copista').click()
print('Acessando página de pendentes...')

tempo = 120

while True:
                
    # Limpa tela.
    os.system('cls')


    # Caso algum protocolo tenha sido cancelado, procurar pelo arquivo na pasta Downloads e mover ele para Downloads_cancelados.
    browser.visit('https://ucsvirtual.ucs.br/impressoes/plotista/cancelados')
    browser.find_by_xpath('//*[@id="conteudo"]/form/fieldset/input').click()

    if browser.is_element_present_by_xpath('//*[@id="conteudo"]/div[2]/div[3]/div[2]/img'):
        soup = BeautifulSoup(browser.html, 'html.parser')
        plots = soup.find_all('div', attrs={'class': 'titulo'})
        deletar = []
        for plot in plots:
            plot = str(plot.text.strip())
            plot = plot[36:].replace(' - ', '-').replace(' ', '-').replace('(', '').replace(')','').replace('.pdf', '').replace('.', '')
            deletar.append(plot.lower())

        for _, _, arquivos in os.walk(pendentes):
            for arquivo in arquivos:
                for plot in deletar:             
                    if os.path.isfile(pendentes + arquivo) and (arquivo == plot + '.pdf'):                            
                        try:
                            shutil.move(pendentes + arquivo, cancelados + arquivo)
                        except:
                            print('Não foi possivel mover arquivo {} para pasta plotagens canceladas.\n'.format(arquivo))


    # Os arquivos que estão por mais de 30 min na pasta Downloads serão movidos para a pasta Downloads_antigos.
    data_atual = datetime.datetime.today()
    for _, _, arquivos in os.walk(pendentes):
        for arquivo in arquivos:
            if os.path.isfile(pendentes + arquivo):
                data_arquivo = datetime.datetime.fromtimestamp(os.path.getctime(pendentes + arquivo))
                if (data_atual - data_arquivo).seconds > 1800:
                    try:
                        shutil.move(pendentes + arquivo, antigos + arquivo)
                    except:
                        print('Não foi possivel mover arquivo {} para pasta de arquivos antigos.\n'.format(arquivo))


    browser.visit('https://ucsvirtual.ucs.br/impressoes/plotista/pendentes')

    # Testa para ver se o navegador ainda está na url de plotagens pendentes, se não estiver acessa novamente.
    if 'pendentes' in browser.url:
        browser.reload()
    else:
        browser.visit('https://ucsvirtual.ucs.br/impressoes/plotista/login')
        browser.fill('username', 'ucscampus8')
        browser.fill('password', 'Pzt2Ytn236!')
        browser.find_by_name('login_copista').click()
        sleep(1)
        browser.visit('https://ucsvirtual.ucs.br/impressoes/plotista/pendentes')
    sleep(1)

    # Se essa frase não for encontrada no código da página quer dizer que tem plotagem pendente.
    if 'Nenhum protocolo encontrado.' not in browser.html:

        print('Plotagem pendente:\t{}\n'.format(strftime('%H:%M:%S', localtime())))

        # Procura pela listagem de plotagens pendentes, mostra elas na tela e salva uma lista com essas informações.
        soup = BeautifulSoup(browser.html, 'html.parser')
        plots = soup.find_all('div', attrs={'class': 'titulo'})

        protocolos = []        
        for i, plot in enumerate(plots):
            if i > 0:
                plot = str(plot.text.strip())
                data = datetime.datetime.strptime(plot[:16].strip(), '%d/%m/%Y %H:%M')                
                protocolo = int(plot[21:31])
                arquivo = plot[36:].replace(' - ', '-').replace(' ', '-').replace('(', '').replace(')','').replace('.pdf', '').replace('.', '')
                plotagem = {'data': data, 'protocolo':str(protocolo), 'arquivo':arquivo}
                protocolos.append(plotagem)

        protocolos = sorted(protocolos, key=lambda k:k['data'])
        for protocolo in protocolos:
            print(protocolo['data'], protocolo['arquivo'])
            
        # Procura por arquivos que já estão na pasta pendentes
        arquivos_pendentes = []
        for _, _, arquivos in os.walk(pendentes):
            for arquivo in arquivos:
                if os.path.isfile(pendentes + arquivo):
                    arquivos_pendentes.append(str(arquivo).lower())

        # Se o arquivo da listagem de plotagem não estiver entre os pendentes ainda, vai baixar ele.        
        for protocolo in protocolos:            
            numero = protocolo['protocolo']
            nome = protocolo['arquivo'].lower() + '.pdf'
            nome = unidecode.unidecode(nome)          
            if nome not in arquivos_pendentes:
                browser.visit('https://ucsvirtual.ucs.br/impressoes/plotista/{}'.format(numero))
                if 'Atenção! O total do documento excede a cota restante.' not in browser.html:
                    browser.visit('https://ucsvirtual.ucs.br/impressoes/plotista/{}/download/{}'.format(numero, nome))
        browser.visit('https://ucsvirtual.ucs.br/impressoes/plotista/pendentes')
        
        # Toca o alarme avisando que tem plotagem pendente.
        winsound.PlaySound('C:/Plotagem/ver_pendentes/plotagem_pendente.wav', winsound.SND_FILENAME)
        
        # Limita o tempo de espera para atualizar a página. Dessa forma o tempo vai chegar no máximo em 8 min.
        if tempo < (8*60):
            tempo *= 2
            
        print('\nPróxima verificação:\t{}'.format(strftime('%H:%M:%S', localtime(time()+tempo))))
    else:

        # Se não for identificada alguma plotagen pendente o tempo volta a ser 2 min
        tempo = 120     
        print('Nenhuma plotagem pendente:\t{}\nPróxima verificação:\t\t{}'.format(strftime('%H:%M:%S', localtime()), strftime('%H:%M:%S', localtime(time()+tempo))))       
    sleep(tempo)

browser.quit()
print('Encerrado.')
