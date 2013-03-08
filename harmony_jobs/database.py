# -*- coding: utf-8 -*-


"""Database loading function."""


import pymongo
import suq.monpyjama


def ensure_indexes(ctx):
    ctx.db.harmony.ensure_index([('upload_at', pymongo.ASCENDING)])
    ctx.db.harmony.ensure_index([('slug', pymongo.ASCENDING)], unique=True)


def load_database(ctx):
    connection = pymongo.Connection(host=ctx.conf['database.host_name'], port=ctx.conf['database.port'])
    db = connection[ctx.conf['database.name']]
    suq.monpyjama.Wrapper.db = db
    return db
