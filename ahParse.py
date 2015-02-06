# split order data into realms
# split realm data into orders per user
# for each realm
    # get realm auction dump from blizzard
    # find unique items in realm orders
    # find all instances of unique items from realm orders in auction data
    # for each user on realm
        # find matching orders
        # create and send email with items that match conditions

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
