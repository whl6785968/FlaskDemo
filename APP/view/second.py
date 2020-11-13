from flask import Blueprint

second = Blueprint('second',__name__)

@second.route("/second/")
def say():
    return 'im second'