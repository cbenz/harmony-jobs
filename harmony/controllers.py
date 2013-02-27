# -*- coding: utf-8 -*-


import bson
import formencode
import simplejson as json
import os
from webob.dec import wsgify

from . import conv, router, templates, wsgi_helpers
from .model import Jobs


@wsgify
def create(req):
    return templates.render(
        req.ctx,
        '/create.mako',
    )


@wsgify
def jobs(req):
    slug = req.urlvars.get('slug')

    # FIXME: should be done one time, when project is created
    job = Jobs.find_one({'slug': slug})
    job.status = True
    job.step = 0
    job.save()

    return templates.render(
        req.ctx,
        '/jobs.mako',
        job = job
    )


@wsgify
def upload(req):
    result = []
    if req.POST:
        print req.POST
        files = req.POST['file']
        validator = formencode.validators.FieldStorageUploadConverter(not_empty=True)
        try:
            fs = validator.to_python(files)
        except formencode.api.Invalid, e:
            print e
        else:
            job = Jobs()
            job.filename = fs.filename
            job.status = False
            job_id = job.save(safe=True)

            # FIXME: check if upload folder exists
            f = open(os.path.join(req.ctx.conf['cache_dir'], 'upload', str(job_id)), 'w+')
            f.write(fs.file.read())
            f.close()

            result = [dict(
                id = str(job_id),
                name = job.filename,
                slug = job.slug,
                size = len(fs.file.read()),
                )]
        
    return wsgi_helpers.respond_json(req.ctx, {'files': result})


@wsgify
def remove(req):
    obj_id = req.GET['id']

    path = os.path.join(req.ctx.conf['cache_dir'], 'upload', obj_id)
    os.remove(path)

    job = Jobs.find_one({'_id': bson.objectid.ObjectId(obj_id)})
    if job.status:
        # if status is True, remove request comes from jobs page
        # a redirect to homepage is needed
        job.delete()
        return wsgi_helpers.redirect(req.ctx, location='/')
    else:
        # if status is False, project is not yet created
        # remove request comes from create page
        job.delete()


@wsgify
def index(req):
    jobs = Jobs.find()
    return templates.render(
        req.ctx,
        '/index.mako',
        jobs = jobs,
    )


def make_router():
    """Return a WSGI application that dispatches requests to controllers """
    return router.make_router(
        ('GET', '^/?$', index),
        ('GET', '^/projects/(?P<slug>.+)/jobs', jobs),
        ('GET', '^/projects/create', create),
        ('GET', '^/projects/remove/?$', remove),
        ('POST', '^/projects/upload', upload),
    )
