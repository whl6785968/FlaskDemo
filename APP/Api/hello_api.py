from flask_restful import Resource


class HelloResource(Resource):
    def get(self):
        return {'msg':'hello'}

    def post(self):
        return {'msg':'hi'}