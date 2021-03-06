from flask import Blueprint, render_template
from evea.db import mongo
from flask_restful import Api, Resource, fields, marshal_with, reqparse, marshal
from collections import Counter, defaultdict

import os
import re
import sys

anno = Blueprint("anno", __name__)
api = Api(anno)


class ncrnaAnno(Resource):
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument("ncrna", type=str)
        args = parser.parse_args()
        print(args["ncrna"])
        mcur = mongo.db.ncrna_anno.find_one({"GeneSymbol": args["ncrna"]}, {"_id": 0})
        return mcur


api.add_resource(ncrnaAnno, "/")


class OneSymbolAnno(Resource):
    def get(self, rna):
        mcur = mongo.db.ncrna_anno.find_one({"GeneSymbol": rna}, {"_id": 0})
        return mcur


api.add_resource(OneSymbolAnno, "/one/<string:rna>")

