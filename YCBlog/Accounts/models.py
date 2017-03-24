from django.db import models
import random
import string
import hashlib
import hmac
import re

# Create your models here.
class Account(models.Model):
    username = models.CharField(max_length=500)
    hash_password = models.CharField(max_length=500)

    @staticmethod
    def hashPassword(username,password):
        salt = ''.join([random.choice(string.ascii_letters) for i in range(10)])
        all_string = username+password+salt
        add_salt = hashlib.sha256(all_string.encode('utf-8')).hexdigest()
        hashcode = "{}|{}".format(add_salt,salt)
        return hashcode

    @staticmethod
    def valid_password(username,password,h):
        hash,salt = h.split('|')
        all_string = username+password+salt
        hashcode = hashlib.sha256(all_string.encode('utf-8')).hexdigest()
        return hashcode == hash

    @staticmethod
    def rot13(text):
        new_text = ""
        for c in text:
            ascii_c = ord(c)
            if ord("a") <= ascii_c <= ord("z"):
                new_text = chr(((ascii_c+13 - ord("a"))%(ord("z")-ord("a")+1))+ord("a"))+new_text
            elif ord("A") <= ascii_c <= ord("Z"):
                new_text = chr(((ascii_c+13 - ord("A"))%(ord("Z")-ord("A")+1))+ord("A"))+new_text               
            else:
                new_text = c + new_text
        return new_text

    @staticmethod
    def hashUsername(username):
        username = str(username)
        addition = "YCCHEN//http://www.ycc.idv.tw"
        new_username = Account.rot13(username)
        return "{}|{}".format(new_username,hmac.new(addition.encode('utf-8'),username.encode('utf-8')).hexdigest())

    @staticmethod
    def checkHashUsername(h):
        if not re.match(r'^[^|]+|[^|]+$', h): return None
        username, hash = h.split("|")
        username = Account.rot13(username)
        if h == Account.hashUsername(username):
            return username
        else:
            return None
