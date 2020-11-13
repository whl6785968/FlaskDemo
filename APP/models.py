from APP.ext import db

class User(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(16))

class Student(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(16))

class RespBean:
    def __init__(self,status_code,msg,data):
        self.status_code = status_code
        self.msg = msg
        self.data = data

    def ok(self,msg,data):
        return RespBean(200,msg,data)

    def ok(self,msg):
        return RespBean(200,msg,None)

    def error(self,msg):
        return RespBean(500,msg,None)

class Result:
    def __init__(self,result):
        self.result = result
