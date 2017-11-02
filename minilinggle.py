#!/usr/bin/env python
# -*- coding: utf-8 -*-
from flask import Flask, jsonify, request

from linggle import Linggle
from operator import itemgetter
import os
import logging


app = Flask(__name__)
settings = {
    'dbname': os.environ['dbname'],
    'host': os.environ['host'],
    'user': os.environ['user'],
    'password': os.environ['password'],
    'port': int(os.environ['port'])
}
miniLinggle = Linggle(**settings)


@app.route("/", methods=['GET'])
def index():
    search = request.args.get('search', '')
    if search:
        return linggleit(search)
    return "mini linggle api: \/?=<query>"


@app.route("/<query>")
def linggle(query):
    print(request.full_path)
    try:
        return linggleit(query)
    except:
        miniLinggle.shutdown()
        miniLinggle = Linggle()
        return jsonify({"message": "Some problems occurred, please try again later"}, code=500)


def linggleit(query):
    def to_linggle_format(ngram, count):
        return {
            'count': int(count),
            'phrase': ngram,
            'count_str': '{0:,}'.format(count),
            'percent': '{0}%'.format(round(count / total, 1))
        }
    result = miniLinggle[query]

    if not result:
        return jsonify([])

    total = sum(map(itemgetter(1), result)) / 100
    result = [to_linggle_format(ngram, count) for ngram, count in result]
    return jsonify(result)


if __name__ == "__main__":
    app.run()
