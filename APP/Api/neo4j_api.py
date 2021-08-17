from flask_restful import Resource, fields, reqparse, marshal
from APP.models import Result, RespBean
from py2neo import Graph

result_fields = {
    "result": fields.String
}

resp_bean_fields = {
    "status_code": fields.Integer,
    "msg": fields.String,
    "data": fields.Nested(result_fields)
}

class Neo4jApi(Resource):
    def get(self):
        graph = Graph('bolt://localhost:7687')
        res = graph.run("match (n{sid:'4014'})-[r:`流入`]-(m)  where m.status = 1 and n.excessed = m.excessed  return n,r,m").data()

        r = Result(res)
        resp_bean = RespBean(200,'success',r)
        return marshal(resp_bean,resp_bean_fields)

