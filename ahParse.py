import pymysql
import urllib.request
import smtplib
from requests import get
from time import sleep
from email.mime.text import MIMEText
# For printing output with special characters in it
import sys
import codecs
if sys.stdout.encoding != 'cp850':
  sys.stdout = codecs.getwriter('cp850')(sys.stdout.buffer, 'strict')
if sys.stderr.encoding != 'cp850':
  sys.stderr = codecs.getwriter('cp850')(sys.stderr.buffer, 'strict')
  
################################################################################                  
# Functions  

# Extract all orders for locale from database
def getOrders(c, locale):
    c.execute("SELECT * FROM realms WHERE locale='"+locale+"'")
    data = c.fetchall()
    orders = {}
    for i in data:
        orders[i['realm']] = []
        c.execute("SELECT email, locale, itemID, operator, price FROM orders WHERE realm='"+i['realm']+"' AND locale='na'")
        d = c.fetchall()
        orders[i['realm']].append(d)
    return orders
# Get auction data from blizzard for realm in locale
def getAuctionData(locale, realm):
    url = "http://" + locale + ".battle.net/api/wow/auction/data/" + realm
    resp = get(url)
    data = resp.json()
    url = data['files'][0]['url']

    resp = get(url)
    data = resp.json()
    return data
# Find all instances of itemIDs in the auction data
def findItems(itemID, data):
    fItems = {}
    for i in itemID:
        fItems[i] = [] 
    allAuctions = data['auctions']['auctions']
    for i in allAuctions:
        if i['item'] in itemID:
            fItems[i['item']].append([i['buyout']/(i['quantity']*10000),i['buyout']/10000,i['quantity']])     
    return fItems
# Send email, also include item names    
def sendeMail(data, to, server):
    msg = {}
    msg['Message'] = 'Item name | ItemID\n[Price per item, Buyout price, Quantity]\n\n'
    for i in data:
        # Maybe also include a link to the item later
        url = "http://us.battle.net/api/wow/item/" + str(i)
        resp = get(url)
        itemName = resp.json()
        print(i)
        msg['Message'] = msg['Message'] + itemName['name'] + " | " + str(i) + "\n" + str(data[i]) + "\n\n"
        
    msg['Subject'] = 'Items found!'
    msg['From'] = 'crens.lightbringer.ah.mailer@gmail.com'
    msg['To'] = to
    message = 'Subject: %s\n%s' % (msg['Subject'], msg['Message'])
    
    server.sendmail(msg['From'], msg['To'], message)
   
################################################################################                  
# Main program

while True:
    # Need to change to json file
    f = open('logins').read().splitlines() 
    mailUser = f[0]
    mailPW = f[1]
    dbUser = f[2]
    dbPW = f[3]
    # Mail server log in
    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.ehlo()
    server.starttls()
    server.login(mailUser, mailPW)
    # DB connection log in
    connection = pymysql.connect(host='192.168.1.73', port=3306, user=dbUser, passwd=dbPW, db='auction_parser_dev')
    c = connection.cursor(pymysql.cursors.DictCursor)
    # Just get North American orders for now (blizzard uses us instead of na)
    naOrders = getOrders(c, 'na')
    for i in naOrders:
        aData = getAuctionData('us', i)
        c.execute("SELECT DISTINCT itemID FROM orders WHERE realm='"+i+"' AND locale='na'")
        uItems = c.fetchall()
        uItems2 = []
        for j in uItems:
            uItems2.append(j['itemID'])
        fItems = findItems(uItems2, aData)
        userData =  naOrders[i][0]
        naUsers = {}
        # Prep dictionary for users
        for j in userData:
            naUsers[j['email']] = []
        # email: {[itemID, operator, price], [itemID, operator, price], ...}    
        for j in userData:
            naUsers[j['email']].append([j['itemID'], j['operator'], j['price']])
        # For every user in naUsers
        # where the user is email: {[itemID, operator, price], [itemID, operator, price], ...}                   
        for j in naUsers:
            emailItems = {}
            # For each item that user wants            
            for k in naUsers[j]:
                emailItems[k[0]] = []
                # Check if it's in the found items
                for l in fItems[k[0]]:
                    # If found and price is low enough append the price tuple                    
                    if int(l[0]) <= int(k[2]):
                        emailItems[k[0]].append(l)
            # For each user, email to inform found items            
            for k in emailItems:
                # But only if there are found items
                if bool(emailItems[k]):
                    sendeMail(emailItems, mailUser, server)                                     
        sys.stdout.flush()   
    sleep(30*60)
