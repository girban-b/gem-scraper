# This file is for functions related to downloading
import requests
import time
import json

class Downloader():
    def __init__(self,renewal_interval=1140):
        self.renewal_interval = renewal_interval
        self.last_created = time.time()
        self.session = requests.Session()
        self.csrf = None
        self.payload = None

    def getcsrf(self):
        gemsite = self.session.get('https://bidplus.gem.gov.in/all-bids')
        gemsite.raise_for_status()
        gemcookies = gemsite.cookies
        self.csrf = gemcookies.get('csrf_gem_cookie')
        
    def getbiddata(self):
        if time.time() - self.last_created > self.renewal_interval:
            self.renewsession()
            self.getcsrf()
        data = self.session.post('https://bidplus.gem.gov.in/all-bids-data', data = {'payload':json.dumps(self.payload), 'csrf_bd_gem_nk': self.csrf})
        data.raise_for_status()
        return data.json()
    
    def renewsession(self):      
        self.session.close()
        self.session = requests.Session()
        self.last_created = time.time()

class Parser():
    def __init__(self):
        self.orderlist = []
        self.newflag = False # to indicate is sorting is being done by newest-first
        self.lastid = None # to store the id of the latest record of previous session

    def parselist(self, bidlist):
        for bid in bidlist:
            order = {}
            if self.newflag and self.lastid == bid['b_id']:
                break
            order = {
                'ID' : bid['b_id'],
                'Bid Number' : bid['b_bid_number'],
                'Name' : bid['bd_category_name'],
                'Category Name' : bid['bbt_title'],
                'Start Date' : bid['final_start_date_sort'],
                'End Date' : bid['final_start_date_sort'],
                'Department' : bid['ba_official_details_deptName']
            }
            self.orderlist.append(order)
        