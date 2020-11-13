import json

from flask import Blueprint

from APP.ext import db
from APP.models import User

blue = Blueprint('blue',__name__)
@blue.route("/say/")
def say_hi():
    return 'first'

@blue.route('/create_db/')
def create_db():
    db.create_all()
    return '创建成功'

@blue.route('/add_user/')
def add_user():
    user = User()
    user.id = 1
    user.name = 'Tom'

    db.session.add(user)
    db.session.commit()
    return '创建成功'

@blue.route('/drop_all/')
def dropall():
    db.drop_all()
    return '删除成功'

@blue.route('/rjson/<string:sentence>')
def rjson(sentence):
    s = ['张三', '年龄', '姓名']
    t = {}
    t['data'] = s
    t = json.dumps(t, ensure_ascii=False)
    return t

@blue.route('/tstPython/<string:sentence>')
def getSentence(sentence):
    return sentence