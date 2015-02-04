


# what do i want this program to do
# i want to load the orders table into a dictionary
# i want to search the ah json for all the unique items in orders
    # and put those in a list
# i want to look through unique auctions and pull out those that match criteria
# i want to match those auctions up to their email addresses
# i want to email those auctions to those users

def getOrders(conn):
    c = conn.cursor(pymysql.cursors.DictCursor)
    
    c.execute("SELECT * FROM orders")

    orders = c.fetchall()
    olist = {}
    found = 0
    for i in orders:
        if i['email'] in olist:
            olist[i['email']].append(i['item'])
        else:
            olist[i['email']] = [i['item']]
          
    c.close()
    return olist

def getUniqueItems(orders):
    uItems = []
    for x in orders:
        uItems += orders[x]
    return (set(items))

def getAuctionData():
    HOST = "http://us.battle.net/api/wow/auction/data/"
    REALM = "Lightbringer"

    url = HOST + REALM
    resp = requests.get(url)
    data = resp.json()
    url = data['files'][0]['url']

    resp = requests.get(url)
    data = resp.json()
    return data
