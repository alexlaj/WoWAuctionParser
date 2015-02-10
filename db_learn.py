import pymysql
import requests
import json
import urllib.request
import smtplib
from email.mime.text import MIMEText

connection = pymysql.connect(host='192.168.1.73', port=3306, user='pythonuser', passwd='pypyaccessingtehdb', db='auction_parser_dev')

#curs = connection.cursor()

#curs.execute("CREATE TABLE items (id int not null primary key auto_increment, item int);")


#   locale{ realm{ email{ orders: [] } } }

c = connection.cursor(pymysql.cursors.DictCursor)

data = [[32837, [-1]], [32838, [[-1]]], [118874, [[40000.0, 40000.0, 1]]], [118892, [[21000.0, 21000.0, 1], [34000.0, 34000.0, 1], [36500.0, 36500.0, 1], [36630.0, 36630.0, 1], [38025.0, 38025.0, 1], [39000.0, 39000.0, 1], [40000.0, 40000.0, 1]]]]
msg = {}
msg['Message'] = ''
for i in data:
    url = "http://www.wowdb.com/items/" + str(i[0])
    req = urllib.request.urlopen(url)
    finalurl = req.geturl()
    finalurl = finalurl.replace("http://www.wowdb.com/items/", "")
    finalurl = finalurl.replace(str(i[0])+"-", "")
    finalurl = finalurl.replace("?cookieTest=1", "")
    finalurl = finalurl.replace("-", " ")
    msg['Message'] = msg['Message'] + finalurl + " " + str(i) + "\n"


    
msg['Subject'] = 'Items found!'
msg['From'] = 'crens.lightbringer.ah.mailer@gmail.com'
msg['To'] = 'alexlajwow@gmail.com'

server = smtplib.SMTP("smtp.gmail.com", 587) #or port 465 doesn't seem to work!
server.ehlo()
server.starttls()
server.login(msg['From'], '#finddatitemdawg')
server.sendmail(msg['From'], msg['To'], msg['Message'])

c.close()
connection.commit()
connection.close()
