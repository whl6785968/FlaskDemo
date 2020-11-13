from flask_restful import Resource, fields, reqparse, marshal
from APP.models import Result, RespBean
from gcforest.gcforest import GCForest
import pickle
import numpy as np

result_fields = {
    "result": fields.String
}

resp_bean_fields = {
    "status_code": fields.Integer,
    "msg": fields.String,
    "data": fields.Nested(result_fields)
}

parser = reqparse.RequestParser()
parser.add_argument("data",type=str,required=True,help="please input data")

class ErrCheckApi(Resource):
    def get(self):
        args = parser.parse_args()
        data = args.get("data")

        arr = data.split(",")
        for i in range(len(arr)):
            arr[i] = float(arr[i])

        arr = np.array(arr,dtype=float).reshape(1,-1)
        with open(r"E:\PycharmProjects\smallFlaskDemo\APP\Api\gcModel\gc_model.pkl","rb") as f:
            gc = pickle.load(f)

        f.close()

        result = gc.predict(arr)

        r = Result(result[0])
        resp_bean = RespBean(200, 'success', r)

        return marshal(resp_bean, resp_bean_fields)


