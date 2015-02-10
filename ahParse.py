import pymysql
import requests
# For printing output with special characters in it
import sys
import codecs
if sys.stdout.encoding != 'cp850':
  sys.stdout = codecs.getwriter('cp850')(sys.stdout.buffer, 'strict')
if sys.stderr.encoding != 'cp850':
  sys.stderr = codecs.getwriter('cp850')(sys.stderr.buffer, 'strict')
  
# Extract all orders for locale from database
def getOrders(c, locale):
    c.execute("SELECT * FROM realms WHERE locale='"+locale+"'")
    data = c.fetchall()
    orders = []
    for i in data:
        c.execute("SELECT email, locale, itemID, operator, price FROM orders WHERE realm='"+i['realm']+"' AND locale='na'")
        d = c.fetchall()
        orders.append([i['realm'],d])
    return orders
# Get auction data from blizzard for realm in locale
def getAuctionData(locale, realm):
    url = "http://" + locale + ".battle.net/api/wow/auction/data/" + realm
    resp = requests.get(url)
    data = resp.json()
    url = data['files'][0]['url']

    resp = requests.get(url)
    data = resp.json()
    return data
# Find all instances of itemIDs in the auction data
def findItems(itemID, data):
    fItems = [[] for x in range(len(itemID))] 
    allAuctions = data['auctions']['auctions']
    for j in range(len(itemID)):
        for i in allAuctions:
            if i['item'] == int(itemID[j]):
                fItems[j].append(itemID[j])
                # convert to gold per item
                fItems[j].append([i['buyout']/(i['quantity']*10000),i['buyout']/10000,i['quantity']])
    fItems = filter(None, fItems)            
    for i in fItems:
        print(i)
        print()
    cItems = []
    for i in fItems:
        cItems.append([fItems[i][0], sorted(fItems[i][1:], key=lambda x:x[0])])           
    return cItems
    
# Main program
connection = pymysql.connect(host='192.168.1.73', port=3306, user='pythonuser', passwd='pypyaccessingtehdb', db='auction_parser_dev')
c = connection.cursor(pymysql.cursors.DictCursor)

naOrders = getOrders(c, 'na')
for i in naOrders:
    aData = getAuctionData('us', i[0])
    c.execute("SELECT DISTINCT itemID FROM orders WHERE realm='"+i[0]+"' AND locale='na'")
    uItems = c.fetchall()
    uItems2 = []
    for j in uItems:
        uItems2.append(j['itemID'])
    fItems = findItems(uItems2, aData)

    for i in fItems:
        print(i)
        print()
    print(fItems)

