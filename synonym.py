#!/usr/bin/env python
# -*- coding: utf-8 -*-
import psycopg2
from collections import Counter


SELECT_SYM_CMD = "SELECT similar_words FROM cna_sim WHERE word=%s;"


class Synonym:
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

    def query(self, querystr):
        print('synonym querystr =', querystr)
        # expand query description and then gather results
        with self.conn.cursor() as cursor:
            result = []
            cursor.execute(SELECT_SYM_CMD, [querystr])
            res = cursor.fetchone()
            if res:
                for similar_word, sim in res[0]:
                    result.append(similar_word)
                return result
        return []