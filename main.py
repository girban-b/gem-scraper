from module import Parser, Downloader
import payloads
import time
import json

gemload = Downloader()
gem = Parser()
gem.newflag = input("Sort by newest-first?(y/n)").lower()
if gem.newflag == 'y':
    gemload.payload = payloads.boq_newest_first
    gem.newflag = True
    with open('lastrecord.json', 'r') as json_file:
        lastorder = json.load(json_file)
        gem.lastid = lastorder['ID']
elif gem.newflag == 'n':
    gemload.payload = payloads.boq_oldest_first
else:
    raise ValueError('Invalid input: Only "y"/"n" allowed')
    exit()
gemload.csrf = gemload.getcsrf()

bidlist = gemload.getbiddata()['response']['response']['docs']
gem.parselist(bidlist)
pages = gemload.getbiddata()['response']['response']['response']/10
k=2

while k<=pages:
    gemload.payload = {'page':{k}}.update(gemload.payload)
    bidlist = gemload.getbiddata()['response']['response']['docs']
    gem.parselist(bidlist)
    time.sleep(0.4)
    k += 1
    if (gemload.getbiddata()['response']['response']['response']/10)>pages:
        pages = gemload.getbiddata()['response']['response']['response']/10

with open('output.json', 'w') as json_file:
    json.dump(gem.orderlist, json_file)

with open('lastrecord.json', 'w') as json_file:
    json.dump(gem.orderlist[-1], json_file)