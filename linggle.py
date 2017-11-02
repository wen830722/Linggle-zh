#!/usr/bin/env python
# -*- coding: utf-8 -*-
import psycopg2
from collections import Counter
from lingglecmd import expand_query


SELECT_CMD = "SELECT results FROM cna WHERE query=%s;"


class Linggle:
    def __init__(self, dbname='linggle', host='localhost', user='linggle', password='linggle', port=5432):
        self.connstr = "dbname='{dbname}' user='{user}' password='{password}' host='{host}' port='{port}'".format(
            dbname=dbname, host=host, user=user, password=password, port=port)
        self.conn = psycopg2.connect(self.connstr)

    def __del__(self):
        self.close()

    def __getitem__(self, querystr):
        return self.query(querystr)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.close()

    def close(self):
        if not self.conn.closed:
            self.conn.close()

    def query(self, querystr, topn=50):
        print(querystr)
        # expand query description and then gather results
        with self.conn.cursor() as cursor:
            result = Counter()
            for query_unit in expand_query(querystr):
                cursor.execute(SELECT_CMD, [query_unit])
                res = cursor.fetchone()
                if res:
                    for row in res:
                        for ngram, count in res[0]:
                            result[ngram] = count
            return result.most_common(topn)
