from flask import Blueprint, render_template
from evea.db import mongo
from flask_restplus import fields, Api, Resource

sample = Blueprint('sample', __name__)

api = Api(sample)

model = api.model('Model', {
    'GEO_project_id': fields.String,
    'SRA_project_id': fields.String
})


@api.route('/', methods=['GET'])
class FuzzyFoo(Resource):
    # @api.marshal_with(model)
    @api.marshal_with(model)
    def get(self):
        cur = mongo.db.sample_info.find().limit(5)
        a = list(cur)
        return a