from flask_restful import Resource


class Handler(Resource):
    def get(self):
        return {"message": "this is the default plugin create some more complex plugins"}
