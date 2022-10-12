import requests as rq
from myutil import *

john_pwd = 'BeuJ'
jack_pwd = 'qW2B'
joe_pwd = 'MRxN'

##a = [{'date': '01/01/2022', 'cons': 'john', 'pwd': john_pwd, 'etype': 'A', 'amount': 100},
##     {'date': '01/01/2022', 'cons': 'john', 'pwd': john_pwd, 'etype': 'B', 'amount': 200},
##     {'date': '02/01/2022', 'cons': 'john', 'pwd': john_pwd, 'etype': 'A', 'amount': 300},
##     {'date': '02/01/2022', 'cons': 'john', 'pwd': john_pwd, 'etype': 'B', 'amount': 400},
##     {'date': '04/01/2022', 'cons': 'john', 'pwd': john_pwd, 'etype': 'B', 'amount': 500},
##     {'date': '05/01/2022', 'cons': 'john', 'pwd': john_pwd, 'etype': 'C', 'amount': 600},
##     {'date': '01/01/2022', 'cons': 'jack', 'pwd': jack_pwd, 'etype': 'A', 'amount': 200},
##     {'date': '03/01/2022', 'cons': 'jack', 'pwd': jack_pwd, 'etype': 'A', 'amount': 200},
##     {'date': '02/01/2022', 'cons': 'jack', 'pwd': jack_pwd, 'etype': 'B', 'amount': 200},
##    ]
##def consum():
##    for j in a:
##        print(rq.post('http://127.0.0.1:8080/sendconsumtx', data=j).text)
##consum()

def list_key(key):
   for j in api.liststreamkeyitems('energy', key):
       print(j['data'])
##list_key('consum')
list_key('registered')
##list_key('transfer')

######################################################

import json
def query_cons():
    q = {'date': '10/08/2022' }
    q = {'etype': 'wind' }
    q = {'date': '10/08/2022', 'etype': 'wind' }
    res = json.loads(rq.post('http://127.0.0.1:8080/querycons', data=q).text)
    if res['result'] == 'success':
        for j in json.loads(res['value']):
            print(j)
##query_cons()

def query_by_etype():
    q = {'etype': 'wind' }
    res = json.loads(rq.post('http://127.0.0.1:8080/querybyetype', data=q).text)
    if res['result'] == 'success':
        for j in json.loads(res['value']):
            print(j)
##query_by_etype()

def query_by_consumer(): # The consumer must provide password.
    # By consumer
    # q = {'cons': 'joe', 'pwd': joe_pwd}

    # By consumer and date
    # q = {'date': '10/08/2022', 'cons': 'joe', 'pwd': joe_pwd}

    # By consumer and etype
    # q = {'etype': 'A', 'cons': 'john', 'pwd': john_pwd}

    # By consumer, date and etype
    q = {'date': '01/01/2022', 'etype': 'A', 'cons': 'john', 'pwd': john_pwd}

    res = json.loads(rq.post('http://127.0.0.1:8080/querybyconsumer', data=q).text)
    if res['result'] == 'success':
        for j in json.loads(res['value']):
            print(j)
# query_by_consumer()

def query_duration():
    q = {'date1': '01/01/2022', 'date2': '03/01/2022', 'cons': 'john', 'pwd': john_pwd}
    q = {'date1': '01/01/2022', 'date2': '03/01/2022', 'etype': 'A', 'cons': 'john', 'pwd': john_pwd}
    res = json.loads(rq.post('http://127.0.0.1:8080/queryduration', data=q).text)
    if res['result'] == 'success':
        for j in json.loads(res['value']):
            print(j)
    else:
        print(res['msg'])
##query_duration()
