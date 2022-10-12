
from flask import Flask, render_template, request
from myutil import *

app = Flask(__name__)

@app.route('/Preparae')
def Preparae():
    return render_template('Preparae.html')

import csv, bitcoin
@app.route('/prepare', methods=['POST'])
def perpare():
   # verify admin password
   adminpwd = request.form['pwd']
   if not is_valid_pwd(adminpwd):
      return render_template('test.html')
   
   # create 'energy' stream
   r = api.create('stream', 'energy', True)
   try:
      if r['error']:
         return { 'result': 'error', 'msg': r['error']['message'] }
   except:
      api.subscribe('energy')

   # publish admin pwd to 'energy'
   api.publish('energy', 'admin', bitcoin.sha256(adminpwd))

   # read users list and publish.
   try:
      c = 0
      with open('data/users.csv') as f:
         for r in csv.DictReader(f):
            api.publish('energy', 'eligible', str_hex(r['name']))
            c += 1
##            print(r['name'])
      return { 'result': 'success', 'msg': 'There are %d users.' % c }
   except:
      return { 'result': 'error', 'msg': 'Error reading user file.' }

@app.route('/verifyadminpwd', methods=['POST'])
def verify_admin_pwd():
    pwd = request.form['pwd']
    return { 'result': is_valid_admin_pwd(pwd) }

@app.route('/verifyeligible', methods=['POST'])
def verify_eligible():
    name = request.form['name']
    return { 'result': is_eligible(name) }

@app.route('/verifyregistered', methods=['POST'])
def verify_registered():
    name = request.form['name']
    return { 'result': is_registered(name) }
    
#########################################################

@app.route('/registeruser', methods=['POST'])
def register_user():
   name = request.form['name']
   if not is_eligible(name):
      return render_template('test.html')

   if is_registered(name):
      return render_template('test2.html')

   pwd = gen_pwd()
   json = {'name': name, 'pwd': bitcoin.sha256(pwd)}
   api.publish('energy', 'registered', {'json': json})
   return '{"result": "success", "name": %s, "pwd": %s}' % (name, pwd)

@app.route('/verifyuserpwd', methods=['POST'])
def verify_user_pwd():
    name = request.form['name']
    pwd = request.form['pwd']
    return { 'result': is_valid_user_pwd(name, pwd) }

#########################################################

@app.route('/sendconsumtx', methods=['POST'])
def send_consum_tx():
    try:
        date = request.form['date']
        cons = request.form['cons']
        pwd = request.form['pwd']
        etype = request.form['etype']
        amount = request.form['amount']
    except:
        return {'result': 'error', 'msg': 'Invalid parameter' }
    if (not is_registered(cons)) or (not is_valid_user_pwd(cons, pwd)):
        return {'result': 'error', 'msg': 'Invalid consumer' }
    txid = api.publish('energy', 'consum', {'json': \
        {'date': date, 'cons': cons, 'etype': etype, 'amount': amount}})
    return {'result': 'success', 'txid': txid }

@app.route('/sendtransfertx', methods=['POST'])
def send_transfer_tx():
    try:
        date = request.form['date']
        trans = request.form['trans']
        pwd = request.form['pwd']
        target = request.form['target']
        amount = request.form['amount']
    except:
        return {'result': 'error', 'msg': 'Invalid parameter' }
    if (not is_registered(trans)) or (not is_valid_user_pwd(trans, pwd)):
        return {'result': 'error', 'msg': 'Invalid consumer' }
    txid = api.publish('energy', 'transfer', {'json': \
        {'date': date, 'trans': trans, 'target': target, 'amount': amount}})
    return {'result': 'success', 'txid': txid }

@app.route('/querycons', methods=['POST'])
def query_cons(): # By date or etype
    try:
        date = request.form.get('date')
        etype = request.form.get('etype')
        a = []
        for j in api.liststreamkeyitems('energy', 'consum'):
           s = j['data']['json']
           if (etype == None  and date == s['date']) or \
              (date == None  and etype == s['etype']) or \
              (date == s['date']  and etype == s['etype']):
               a.append(str(s))
    except:
        return {'result': 'error', 'msg': 'Invalid parameter' }
    return {'result': 'success', 'value': str(a)}

@app.route('/querytrans', methods=['POST'])
def query_trans(): # By date or etype
    try:
        date = request.form.get('date')
        etype = request.form.get('etype')
        a = []
        for j in api.liststreamkeyitems('energy', 'transfer'):
           s = j['data']['json']
           if (etype == None  and date == s['date']) or \
              (date == None  and etype == s['etype']) or \
              (date == s['date']  and etype == s['etype']):
               a.append(str(s))
    except:
        return {'result': 'error', 'msg': 'Invalid parameter' }
    return {'result': 'success', 'value': str(a)}

@app.route('/querybyconsumer', methods=['POST'])
def query_by_consumer():
    try:
        cons = request.form['cons']
        pwd = request.form['pwd']
        date = request.form.get('date')
        etype = request.form.get('etype')
        if not is_valid_user_pwd(cons, pwd):
            return {'result': 'error', 'msg': 'Invalid consumer' }
        a = []
        for j in api.liststreamkeyitems('energy', 'consum'):
           s = j['data']['json']  # dict
           if (etype == None  and date == None and cons == s['cons']) or \
              (etype == None  and date == s['date'] and cons == s['cons']) or \
              (date == None  and etype == s['etype'] and cons == s['cons']) or \
              (etype == s['etype']  and date == s['date'] and cons == s['cons']):
               a.append(str(s))
    except:
        return {'result': 'error', 'msg': 'Invalid parameter' }
    return {'result': 'success', 'value': str(a)}  


@app.route('/queryduration', methods=['POST'])
def query_duration():
    try:
        cons = request.form['cons']
        pwd = request.form['pwd']
        date1 = request.form['date1']
        date2 = request.form['date2']
        etype = request.form.get('etype')
        print(date1, date2, etype)
        if not is_valid_user_pwd(cons, pwd):
            return {'result': 'error', 'msg': 'Invalid consumer.' }
        d1 = create_date(date1)
        d2 = create_date(date2)
        print(d1, d2)
        if d1 >= d2:
            return { 'result': 'error', 'msg': 'Invalid duration.' }
    except:
        return {'result': 'error', 'msg': 'Invalid parameter' }
    print('Ok')
    a = []
    for j in api.liststreamkeyitems('energy', 'consum'):
       s = j['data']['json']
       dx = create_date(s['date'])
       if d1 <= dx <= d2:
           if (etype == None and cons == s['cons']) or \
              (etype == s['etype'] and cons == s['cons']):
               a.append(str(s))
    return {'result': 'success', 'value': str(a)} 

#----------------------------------------------------------------

@app.route('/SendConsumTx',methods=['GET','POST'])
def index1():
    return render_template("Send Consum Tx.html")

@app.route('/SendTransferTx',methods=['get','post'])
def index2():
    return render_template("Send Transfer Tx.html")

@app.route('/RegisterUser',methods=['get','post'])
def index3():
    return render_template("Register User.html")

@app.route('/',methods=['get','post'])
def index4():
    return render_template("dashboard.html")

@app.route('/transaction',methods=['get','post'])
def index5():
    return render_template("transaction.html")

@app.route('/customer',methods=['get','post'])
def index6():
    return render_template("customer.html")


#---------------------------------------

if __name__ == '__main__':
    app.run(port=8080, debug=True)


