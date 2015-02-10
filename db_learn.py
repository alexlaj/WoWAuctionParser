import pymysql
import requests
import json
import urllib.request
import smtplib
import time
from email.mime.text import MIMEText

connection = pymysql.connect(host='192.168.1.73', port=3306, user='pythonuser', passwd='pypyaccessingtehdb', db='auction_parser_dev')

#curs = connection.cursor()

#curs.execute("CREATE TABLE items (id int not null primary key auto_increment, item int);")


#   locale{ realm{ email{ orders: [] } } }

c = connection.cursor(pymysql.cursors.DictCursor)

data = {118874: [[60000.0, 60000.0, 1], [70000.0, 70000.0, 1]], 118892: [[40309.6457, 40309.6457, 1], [35000.0, 35000.0, 1]], 32837: [], 32838: []}
'''
msg = {}
msg['Message'] = 'Item name | ItemID\n[Price per item, Buyout price, Quantity]\n\n'

for i in data:
    url = "http://www.wowdb.com/items/" + str(i)
    req = urllib.request.urlopen(url)
    finalurl = req.geturl()
    finalurl = finalurl.replace("http://www.wowdb.com/items/", "")
    finalurl = finalurl.replace(str(i)+"-", "")
    finalurl = finalurl.replace("?cookieTest=1", "")
    finalurl = finalurl.replace("-", " ")
    msg['Message'] = msg['Message'] + finalurl + " | " + str(i) + "\n" + str(data[i]) + "\n\n"
    
msg['Subject'] = 'Items found!'
msg['From'] = 'crens.lightbringer.ah.mailer@gmail.com'
msg['To'] = 'alexlajwow@gmail.com'
message = 'Subject: %s\n%s' % (msg['Subject'], msg['Message'])
server = smtplib.SMTP("smtp.gmail.com", 587)
server.ehlo()
server.starttls()
server.login(msg['From'], '#finddatitemdawg')
server.sendmail(msg['From'], msg['To'], message)
'''
while True:
    print (data)
    time.sleep(2)
c.close()
connection.commit()
connection.close()
