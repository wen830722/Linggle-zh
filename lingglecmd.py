#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
from itertools import product
from synonym import Synonym


LONGEST_LEN = 5
SELECT_CMD = "SELECT results FROM cna WHERE query=%s;"
# TODO: pron: Nh
POS_WILDCARD_EN = {'v.': 'V.', 'n.': 'N.', 'adj.': 'A.', 'prep.': 'P.', 'det.': 'DET.', 'conj.': 'C.', 'pron.': 'pron.', 'adv.': 'ADV.'}
posabbr = [ line.strip().split('\t')[0]+'.' for line in open('pos_list.txt') ]
POS_WILDCARD = {pos.lower():pos for pos in posabbr}
POS_WILDCARD.update(POS_WILDCARD_EN)

settings = {
    'dbname': os.environ['dbname'],
    'host': os.environ['host'],
    'user': os.environ['user'],
    'password': os.environ['password'],
    'port': int(os.environ['port'])
}
sym = Synonym(**settings)


def item_to_candidate(item):
    for token in item.split('/'):
        if token.startswith('?'):
            yield ''
            token = token[1:]
        if token.startswith('~'):
            for symword in findsyms(token):
                yield symword
            token = token[1:]
        if token in POS_WILDCARD:
            # print(token, POS_WILDCARD[token])
            token = ' ' + POS_WILDCARD[token] + ' '
        if token == '_':
             yield ' _ '
        # print(token)
        yield token


def gen_candidates(query):
    for item in query.split():
        if item == '*':
            yield [' '+'_ '*n for n in range(LONGEST_LEN)]
        else:
            yield list(item_to_candidate(item))


def candidates_to_cmds(candidates):
    for tokens in product(*candidates):
        tokens = [token for token in tokens if token]
        if len(tokens) > LONGEST_LEN:
            continue
        yield ' '.join(''.join(tokens).strip().split())


def expand_query(query):
    candidates = list(gen_candidates(query.replace('@', '/')))
    return {sqlcmd for sqlcmd in candidates_to_cmds(candidates)}


def findsyms(word):
    result = sym[word[1:]]
    return result

