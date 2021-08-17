from flask_restful import Api

from APP.Api.goods_api import GoodResource
from APP.Api.hello_api import HelloResource
from APP.Api.ner_api import NerResource
from APP.Api.err_check_api import ErrCheckApi
from APP.Api.neo4j_api import Neo4jApi
from APP.Api.qa_api import QAApi

api = Api()
def init_api(app):
    api.init_app(app)

api.add_resource(HelloResource, '/hello/')
api.add_resource(GoodResource,'/good/')
api.add_resource(NerResource,'/ner/')
api.add_resource(ErrCheckApi,'/errCheck/')
api.add_resource(Neo4jApi,'/neo4j/')
api.add_resource(QAApi,'/qa/')