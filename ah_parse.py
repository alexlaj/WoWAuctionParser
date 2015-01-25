import requests
import json
import re
import urllib.request
import smtplib
from email.mime.text import MIMEText

################################################################################
        ##                   ##
        ##   Functions       ##
        ##                   ##
################################################################################

##### Get Auction Data#####
def getAuctionData():
    HOST = "http://us.battle.net/api/wow/auction/data/"
    REALM = "Lightbringer"

    # Get URL of the AH data dump 
    url = HOST + REALM
    resp = requests.get(url)
    data = resp.json()
    url = data['files'][0]['url']

    # Get the AH data dump JSON file
    resp = requests.get(url)
    data = resp.json()
    return data

#####Change Item ID to Item Name#####
def idToName(itemIDs):
    itemNames = []
    for i in range(len(itemIDs)):
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
            if i['item'] == itemID[j]:
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
def sendEmail(foundItem):
    msg = MIMEText(foundItem)

    msg['Subject'] = 'Test message'
    msg['From'] = 'crens.lightbringer.ah.mailer@gmail.com'
    msg['To'] = 'crens.lightbringer.ah.mailer@gmail.com'

    # Send the message via our own SMTP server, but don't include the
    # envelope header.
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

# vvv Change itemIDs here to change what the script looks up vvv
itemID = [118874,118882,118876]
# ^^^ Change itemIDs here to change what the script looks up ^^^
auctionData = getAuctionData()
itemName = idToName(itemID)
emailBody = findItems(itemID, auctionData)
sendEmail(emailBody)


