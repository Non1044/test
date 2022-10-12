from myutil import *
import bitcoin

def gen_pwd_test():
    for _ in range(10):
        pwd = gen_pwd()
        print(gen_pwd(), is_valid_pwd(pwd), bitcoin.sha256(pwd))
##gen_pwd_test()

def hex_test():
    en = str_hex('john')
    print(en)
    print(hex_str(en))
##hex_test()

def encode_test():
    admin_addr = '1ZAHSRHpJFtXQLLeWw1Z2D1XEQyFuMaRHxXrFN'
    pwd = 'hi234'
    ena = encode(admin_addr, pwd)
    sh_ena = str_hex(ena)
    print(sh_ena)
    hs_ena = hex_str(sh_ena)
    print(decode(hs_ena, pwd))
##encode_test()

#------------------------------------------------------
    
