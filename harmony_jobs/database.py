# -*- coding: utf-8 -*-


"""Database loading function."""


import pymongo

from . import model


def ensure_indexes(ctx):
    ctx.db.projects.ensure_index([('upload_at', pymongo.ASCENDING)])
    ctx.db.projects.ensure_index([('slug', pymongo.ASCENDING)], unique=True)


def load_database(ctx):
    connection = pymongo.Connection(host=ctx.conf['database.host_name'], port=ctx.conf['database.port'])
    db = connection[ctx.conf['database.name']]
    model.Wrapper.db = db
    return db


def load_database_webrokeit(ctx):
    connection = pymongo.Connection(
        host=ctx.conf['webrokeit.database.host_name'], port=ctx.conf['webrokeit.database.port'])
    db = connection[ctx.conf['webrokeit.database.name']]
    return db
