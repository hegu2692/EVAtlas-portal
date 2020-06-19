from flask import Blueprint, render_template
from evea.db import mongo
from flask_restful import Api, Resource, fields, marshal_with, reqparse, marshal
from collections import Counter, defaultdict

import os
import re
import sys

stat = Blueprint('stat', __name__)
api = Api(stat)

category_stat_field = {
    'category_stat':
    fields.Nested({
        'sample_n':
        fields.Integer,
        'category_type':
        fields.Nested({
            'ex_type': fields.String,
            'source': fields.String,
        }),
    }),
    'category_n':
    fields.Integer,
    'ex_type_lst':
    fields.List(
        fields.Nested({
            'sample_n': fields.Integer,
            'ex_type': fields.String,
        })),
    'source_type_lst':
    fields.List(
        fields.Nested({
            'sample_n': fields.Integer,
            'source_type': fields.String,
        })),
}


class CategoryStat(Resource):
    @marshal_with(category_stat_field)
    def get(self):
        sample_category = {}
        category_stat_oj = mongo.db.sample_info.aggregate([{
            "$group": {
                "_id": {
                    "ex_type": "$ex_type",
                    "source": "$source"
                },
                "sample_n": {
                    "$sum": 1
                }
            }
        }, {
            "$project": {
                "_id": 0,
                "category_type": "$_id",
                "sample_n": 1
            }
        }])
        category_stat_lst = list(category_stat_oj)
        category_n = len(category_stat_lst)
        ex_type_oj = mongo.db.sample_info.aggregate([{
            "$group": {
                "_id": "$ex_type",
                "sample_n": {
                    "$sum": 1
                }
            }
        }, {
            "$project": {
                "_id": 0,
                "ex_type": "$_id",
                "sample_n": 1
            }
        }])
        ex_type_lst = list(ex_type_oj)
        source_type_oj = mongo.db.sample_info.aggregate([{
            "$group": {
                "_id": "$source",
                "sample_n": {
                    "$sum": 1
                }
            }
        }, {
            "$project": {
                "_id": 0,
                "source_type": "$_id",
                "sample_n": 1
            }
        }])
        source_type_lst = list(source_type_oj)
        return {
            'category_n': category_n,
            'category_stat': category_stat_lst,
            'ex_type_lst': ex_type_lst,
            'source_type_lst': source_type_lst
        }
api.add_resource(CategoryStat, '/category')

exp_stat_field = {
    "exp_level": fields.List(fields.Nested({
        "exp_flag": fields.String,
        "count": fields.Integer,
    })),
    "count": fields.Integer,
    "ncRNA": fields.String,
}

ncRNA_stat_field_lst = {
    "exp_stat_lst" : fields.List(fields.Nested(exp_stat_field))
}

class SamplesExpStat(Resource):
    @marshal_with(ncRNA_stat_field_lst)
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('querys', type=str)
        parser.add_argument('ncRNA_type', type=str)
        parser.add_argument('query_type', type=str)
        args = parser.parse_args()
        query_type = args['query_type']
        ncRNA_lst = ['miRNA', 'rRNA', 'tRNA', 'piRNA', 'snoRNA', 'snRNA', 'pRNA', 'scRNA']
        if args['ncRNA_type']:
            ncRNA_lst = args['ncRNA_type'].strip().split(',')
        query_lst = args['querys'].strip().split(',')
        if query_type != "sample":
            samples_lst = list(mongo.db.sample_info.find({query_type: {"$in":query_lst}}, {"srr_id": 1, "_id": 0}))
            query_lst = [ z['srr_id'] for z in samples_lst ]
        exp_stat_oj = mongo.db.sample_exp.aggregate([{"$match": {"srr_id": {"$in":query_lst}}}, {"$unwind":"$ncrna_exp"}, {"$match":{"ncrna_exp.ncrna": {"$in":ncRNA_lst}}}, {"$project": {"_id":0, "ncrna_exp":1, "exp_flag":{"$cond":{"if":{ "$gte": [ "$ncrna_exp.RPM", 10000 ] }, "then": "10000", "else": {"$cond":{"if":{ "$gte": [ "$ncrna_exp.RPM", 1000 ] }, "then": "1000", "else": {"$cond":{"if":{ "$gte": [ "$ncrna_exp.RPM", 100 ] }, "then": "100", "else": {"$cond":{"if":{ "$gte": [ "$ncrna_exp.RPM", 10 ] }, "then": "10", "else": {"$cond":{"if":{ "$gte": [ "$ncrna_exp.RPM", 1 ] }, "then": "1", "else": '0'} }}}}}}}}}}}, {"$group": {"_id":{"ncrna":"$ncrna_exp.ncrna", "exp_flag":"$exp_flag"}, "total":{"$sum":1}}},{"$group": {"_id":"$_id.ncrna", "exp_level":{"$push":{"exp_flag":"$_id.exp_flag", "count":"$total"}}, "count":{"$sum":"$total"}}},{"$project": {"_id":0, "ncRNA":"$_id", "exp_level":1, "count":1}}])
        exp_stat_lst = list(exp_stat_oj)
        return {"exp_stat_lst": exp_stat_lst}
api.add_resource(SamplesExpStat, '/samplesexp')




