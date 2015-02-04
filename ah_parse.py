import requests
import json
import urllib.request
import smtplib
from email.mime.text import MIMEText

################################################################################
        ##                   ##
        ##   Functions       ##
        ##                   ##
################################################################################

# todo
# make users.txt a json file
# search AH data in one pass
# put items and users in a database


##### Get Auction Data#####
def getAuctionData():
    HOST = "http://us.battle.net/api/wow/auction/data/"
    REALM = "Lightbringer"

    # Get URL of the AH data dump 
    url = HOST + REALM
    resp = requests.get(url)
    data = resp.json()
    url = data['files'][0]['url']
    print(url)
    # Get the AH data dump JSON file
    resp = requests.get(url)
    data = resp.json()
    return data

##### Parse users.txt #####
def parseUsers():
    users = []
    userFile = open('users.txt','r')
    for line in userFile:
        userline = line.split(',')
        userline[-1] = userline[-1].replace('\n','')
        users.append(userline)
    userFile.close()
    print (users)
    return users

#####Change Item ID to Item Name#####
def idToName(itemIDs):
    itemNames = []
    for i in range(len(itemIDs)):
        # should change this to blizzard api call instead
        url = "http://www.wowdb.com/items/" + str(itemIDs[i])
        req = urllib.request.urlopen(url)
        finalurl = req.geturl()
        finalurl = finalurl.replace("http://www.wowdb.com/items/", "")
        finalurl = finalurl.replace(str(itemIDs[i])+"-", "")
        finalurl = finalurl.replace("?cookieTest=1", "")
        finalurl = finalurl.replace("-", " ")
        itemNames.append(finalurl)
    return itemNames

#####Find Items in Auction Data#####
def findItems(itemID, data):
    foundItem = [[] for x in range(len(itemID))] 
    allAuctions = data['auctions']['auctions']
    for j in range(len(itemID)):
        foundItem[j].append(itemID[j])
        for i in allAuctions:
            if i['item'] == int(itemID[j]):
                # convert to gold per item
                foundItem[j].append(i['buyout']/(i['quantity']*10000))
    # Sort so that ID is the first element, then the buyout prices are contained in a second array
    emailBody = ''
    for j in range(len(itemID)):
        foundItem[j] = [str(foundItem[j][0])+" "+itemName[j], sorted(foundItem[j][1:])]
    for j in range(len(foundItem)):
        for i in range(len(foundItem[j])):
            emailBody = emailBody + str(foundItem[j][i]) + " "
        emailBody = emailBody + "\n"
    return emailBody

#####Send Email#####
def sendEmail(foundItem, email):
    msg = MIMEText(foundItem)

    msg['From'] = 'crens.lightbringer.ah.mailer@gmail.com'
    msg['To'] = email

    s = smtplib.SMTP('smtp.gmail.com:587')
    s.starttls()
    s.login('crens.lightbringer.ah.mailer', '#finddatitemdawg')
    s.sendmail(msg['From'], msg['To'], foundItem)
    s.quit()

    
################################################################################
        ##                   ##
        ##   Main Program    ##
        ##                   ##
################################################################################

auctionData = getAuctionData()
# Parse users.txt
# Loop for every user
users = parseUsers()
for user in users:   
    email = user[0]
    itemID = user[1:]
    itemName = idToName(itemID)
    emailBody = findItems(itemID, auctionData)
    sendEmail(emailBody, email)


