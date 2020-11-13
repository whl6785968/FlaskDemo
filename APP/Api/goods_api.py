from flask_restful import Resource, fields, reqparse, marshal

from APP.models import Result, RespBean

result_fields = {
    "result": fields.String
}

resp_bean_fields = {
    "status_code": fields.Integer,
    "msg": fields.String,
    "data": fields.Nested(result_fields)
}

parser = reqparse.RequestParser()
parser.add_argument("sentence",type=str,required=True,help="please input a sentence")

class GoodResource(Resource):
    def get(self):
        args = parser.parse_args()
        sentence = args.get('sentence')

        result = Result(sentence)
        resp_bean = RespBean(200,'success',result)
        return marshal(resp_bean,resp_bean_fields)

