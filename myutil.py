
from Savoir import Savoir
import random
from flask import Flask, render_template, request

rpcuser = 'multichainrpc'
rpcpasswd = '52TH6uU5onYPrwGoZzMittjoEjg9iZS6rDi8i3aVQjNi'
rpchost = '127.0.0.1'
rpcport = '1234'
chainname = 'chain1'
api = Savoir(rpcuser, rpcpasswd, rpchost, rpcport, chainname)

SYM = '23456789aAbBcCdDeEfFgGhHijJkKmMnNpPqQrRsStTuUvVwWxXyYzZ'
def gen_pwd():
   pwd = ''
   for _ in range(random.randint(4, 6)):
      pwd += random.choice(SYM)
   return pwd

def is_valid_pwd(pwd):
   if pwd.__class__.__name__ == 'str':
      if 4 <= len(pwd) <= 6:
         for c in pwd:
            if c not in SYM:
               return False
         return True
   return False

##################################################

def str_hex(s):
   return s.encode().hex()

def hex_str(h):
   return bytes.fromhex(h).decode()

##################################################

from datetime import *
def create_date(a): # 'dd/mm/yyyy'
   d, m, y = [int(x) for x in a.split('/')]
   return date(y, m, d)

##################################################

import bitcoin
def is_valid_admin_pwd(pwd):
   for j in api.liststreamkeyitems('energy', 'admin'):
      if j['data'] == bitcoin.sha256(pwd):
         return True
   return False

def is_eligible(name):
   for j in api.liststreamkeyitems('energy', 'eligible'):
      if hex_str(j['data']) == name:
         return render_template('eligibleTrue.html')
   return False

def is_registered(name):
   for j in api.liststreamkeyitems('energy', 'registered'):
      if name == j['data']['json']['name']:
         return True
   return False

def is_valid_user_pwd(name, pwd):
   for j in api.liststreamkeyitems('energy', 'registered'):
      json = j['data']['json']
      if (json['name'] == name) and (json['pwd'] == bitcoin.sha256(pwd)):
         return True
   return False
