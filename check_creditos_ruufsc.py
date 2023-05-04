# -*- coding: utf-8 -*-
"""
MONITORAMENTO DE CRÉDITOS DO RESTAURANTE UNIVERSITÁRIO
UNIVERSIDADE FEDERAL DE SANTA CATARINA

Criado em 01 de maio de 2023

Autor: Micael Fernando Broggio

Descrição:
Este bot faz envio via email dos créditos contidos nas contas dos alunos ou servidores 
que fazem uso do restaurante universitário (RU) da Universidade Federal de Santa
Catarina aos destinatários pré selecionados.

atualizaçoes:
-> Nenhuma

python 3.9.16
selenium 4.8.0
chrome webdriver 112.0.5615.138

_______________________________________________________________________________
"""

#imports
import time
import smtplib
from selenium import webdriver
from selenium.webdriver.common.by import By
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

#FUNCOES_______________________________________________________________________

def send_message(mensagem,assunto,smtp,cabecalho):
    #inseri assunto ao cabecalho
    cabecalho['assunto'] = assunto
    
    #criar a mensagem do e-mail
    msg = MIMEMultipart('alternative')
    msg['From'] = cabecalho['de']
    msg['To'] = ', '.join(cabecalho['para'])
    msg['Subject'] = cabecalho['assunto']
    
    texto = MIMEText(mensagem, 'plain')
    msg.attach(texto)
    
    #envia o e-mail
    with smtplib.SMTP(smtp['server'], smtp['port']) as server:
        server.starttls()
        server.login(smtp['user'], smtp['password'])
        server.sendmail(cabecalho['de'], cabecalho['para'], msg.as_string())
#______________________________________________________________________________

#CONFIGURACAO EMAIL------------------------------------------------------------
#configurar os parâmetros do servidor SMTP
smtp = {'server':'smtp.gmail.com',
        'port':587,
        'user':'EMAIL REMETENTE',
        'password':'SENHA REMETENTE'}
#------------------------------------------------------------------------------

#abre o navegador
driver = webdriver.Chrome()
driver = webdriver.Chrome(executable_path = "chromedriver.exe")

#usuarios ru UFSC (necessita de configuracao para cada usuario)
usersUFSC        = ['10101010','10101011'] #matriculas
senhasUFSC       = ['123456789','123456789'] #senhas

#iteracao de n vezes seguindo a quantidade de usuarios adicionadas no passo acima
for i in range(0,len(usersUFSC)):
   
    #abre a pagina da loja streamelements
    driver.get('https://sistemas.ufsc.br/login?service=https%3A%2F%2Fsgpru.sistemas.ufsc.br%2Fj_spring_cas_security_check')
    time.sleep(5) #espera de 5 segundos
   
    #realiza o login na pagina
    userUFSC = str(usersUFSC[i])
    senhaUFSC = str(senhasUFSC[i])
    driver.find_element(By.NAME, "username").send_keys(userUFSC)
    driver.find_element(By.NAME, "password").send_keys(senhaUFSC)
    driver.find_element(By.NAME, "submit").click()
    
    #coleta as informacoes de usuario e creditos
    pessoa = driver.find_element(By.CLASS_NAME, "noPrint").get_attribute("innerText")
    pessoa = pessoa[0:pessoa.find("|")-1]
    saldo = driver.find_element(By.CLASS_NAME, "ui-datatable-footer").get_attribute("innerText")
    
    #cria mensagem a ser enviada por email
    mensagem = "SALDO RU UFSC\n" + pessoa + "\n" + saldo #cria mensagem
    
    # Configurar o cabeçalho do e-mail
    primeiro_nome = pessoa.split()
    primeiro_nome = primeiro_nome[0]
    assunto = 'RU ' + primeiro_nome + '> '+ saldo
    cabecalho = {'de':smtp['user'],
                 'para':['xxxxx@xxxxx.com'],
                 'assunto':assunto}
    
    #envio de email
    send_message(mensagem,assunto,smtp,cabecalho)
    
    #sai da conta atual para realizar o login para a próxima conta    
    driver.find_element(By.XPATH, '//*[@id="j_idt17"]/table/tbody/tr/td/a[2]').click()

#fecha o navegador utilizado
driver.close()