import pymysql

connection = pymysql.connect(host='192.168.1.73', port=3306, user='pythonuser', passwd='pypyaccessingtehdb', db='pylearn')

#curs = connection.cursor()

#curs.execute("CREATE TABLE items (id int not null primary key auto_increment, item int);")

c = connection.cursor(pymysql.cursors.DictCursor)

c.execute("SELECT * FROM orders")

#print(c.description)
orders = {}
orders = c.fetchall()
olist = {}
found = 0
for i in orders:
        #print(i)
        if i['email'] in olist:
            olist[i['email']].append(i['item'])
        else:
            olist[i['email']] = [i['item']]
uItems = []
for x in olist:
        uItems += olist[x]
print(set(uItems))
print(olist)    

c.close()
connection.commit()
connection.close()
