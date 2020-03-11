#!/usr/bin/env python3


# get data from form
# work on data?
# get from bd
# send to email

# import constants

import cgi # для получения данных из формы
import html # для экранирования html-символов, для безопасности

# import sqlite3

# import smtplib # Импортируем библиотеку по работе с SMTP

    # Добавляем необходимые подклассы - MIME-типы
# from email.mime.multipart import MIMEMultipart      # Многокомпонентный объект
# from email.mime.text import MIMEText                # Текст/HTML
# from email.mime.image import MIMEImage              # Изображения

def data_as_json(): # for testing
    values = {
        'checkbox-love': 'true',
        'checkbox-money': 'false',
        'checkbox-family': 'false',
        'checkbox-business': 'true',
        'checkbox-luck': 'false',
        'checkbox-power': 'false',
        'checkbox-wiseness': 'false',
        'checkbox-smartness': 'true',
        'checkbox-kindness': 'false',
        'checkbox-intuition': 'false',
        'name': 'имя юзера на китайском',
        'email': 'sdfdf@dfgsd.cn',
        'sex': 'withoutsex'
        }


    sign_dict = []

    for key in values:
        if key == 'sex': babysex = values[key]
        if key == 'name': usr_name =  values[key]
        if key == 'email': usr_email =  values[key]

        if key in [ 
        'checkbox-love',
        'checkbox-money',
        'checkbox-family',
        'checkbox-business',
        'checkbox-luck',
        'checkbox-power',
        'checkbox-wiseness',
        'checkbox-smartness',
        'checkbox-kindness',
        'checkbox-intuition',
        ] and values[key] == 'true': 
            sign_dict.append(key)


    return(babysex, usr_name, usr_email, sign_dict)



def get_data_from_form():
    # ?values={'checkbox-intuition':'false','name':'имя','email':'sdfdf@dfgsd.cn','sex':'boy'}


    form = cgi.FieldStorage()

    sign_dict = []

    for key in form:
        if key == 'sex': babysex = html.escape(form.getvalue(key))
        if key == 'name': usr_name = html.escape(form.getvalue(key))
        if key == 'email': usr_email = html.escape(form.getvalue(key))


        if key in [ 
        'checkbox-love',
        'checkbox-money',
        'checkbox-family',
        'checkbox-business',
        'checkbox-luck',
        'checkbox-power',
        'checkbox-wiseness',
        'checkbox-smartness',
        'checkbox-kindness',
        'checkbox-intuition',
        ]: 
            sign_dict.append(key)


    if babysex and usr_email and len(sign_dict) > 0 and usr_name:
        # sign_dict.sort()
        return(babysex, usr_name, usr_email, sign_dict)
    else:
        print('no full data got from form')
        exit()

def get_data_from_db(babysex, sign_dict):
    # DB_HOST = constants.db_host
    # DB_USER = constants.db_user
    # DB_PASSWORD = constants.db_password
    # DB_NAME = constants.db_name

    # names4email = 'usr_name'
    # email4email = 'usr_email'


    str_signs = ''.join(sign_dict)


    if babysex == 'boy' or babysex == 'girl':
        sqlselect = "SELECT name, signs FROM "+babysex+"names WHERE signs = " + str_signs
    else:
        print('no full data got from form')
        exit()


     
    connect = sqlite3.connect('/home/dipp/names_db.db')
     
    with connect:
        cursor = connect.cursor()  
        cursor.execute(sqlselect)  

        resp = cursor.fetchall() # or use fetchone()


        return (resp)


def send_to_email(usr_name, usr_email, resp):
    # EMAIL_HOST = constants.email_host
    # SUBJECT = constants.email_subject
    # FROM = constants.email_from


    addr_from = "375411664dip@gmail.com"                 # Адресат
    addr_to   = usr_email # "adast-remont@yandex.ru"                    # Получатель
    password  = "dypgikooajmbjlmp"   

    msg = MIMEMultipart()                               # Создаем сообщение
    msg['From']    = addr_from                          # Адресат
    msg['To']      = addr_to                            # Получатель
    msg['Subject'] = 'Тема сообщения'                   # Тема сообщения

    body = "for " + usr_name + ": " + str(resp)

    msg.attach(MIMEText(body, 'plain'))                 # Добавляем в сообщение текст

    server = smtplib.SMTP('smtp.gmail.com', 587)        # Создаем объект SMTP 587 or 465
    server.set_debuglevel(True)                         # Включаем режим отладки - если отчет не нужен, строку можно закомментировать
    server.starttls()                                   # Начинаем шифрованный обмен по TLS
    server.login(addr_from, password)                   # Получаем доступ
    server.send_message(msg)                            # Отправляем сообщение
    server.quit()                                       # Выходим



def main():

    babysex, usr_name, usr_email, sign_dict = data_as_json()
    # babysex, usr_name, usr_email, sign_dict = get_data_from_form()
    
    # resp = get_data_from_db(babysex, sign_dict)

    print("Content-type: text/html\n")
    print("""<!DOCTYPE HTML>
            <html>
            <head>
                <meta charset="utf-8">
                <title>данные для тестирования</title>
            </head>
            <body>""")
    print('данные для тестирования:<br>')

    # print('<br>user name: ', usr_name, '<br>email: ', usr_email, '<br>data from DB: ', resp)
    print('<br>user name: ', usr_name, '<br>email: ', usr_email, '<br>sex of baby got from form: ', babysex)
    print('<br>you requested signs: ')
    print(*sign_dict, sep=', ')
    print('<br>email sent to ', usr_email, 'look in SPAM too')

    print("""</body>
            </html>""")


    # send_to_email(usr_name, usr_email, resp)



if __name__ == '__main__':  
    
    main()
