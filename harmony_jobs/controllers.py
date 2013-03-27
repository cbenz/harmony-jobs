# -*- coding: utf-8 -*-


import babel.dates
import bson
import datetime
import formencode
import os
import simplejson as json
import urlparse
from pytz import timezone
from webob.dec import wsgify

from . import conv, router, templates, wsgi_helpers
from .model import Projects


@wsgify
def create(req):
    return templates.render(
        req.ctx,
        '/create.mako',
    )


@wsgify
def feed(req):
    projects = Projects.find()
    entries = []
    for project in projects:
        entry = project.to_bson()
        entry['link'] = urlparse.urljoin(req.application_url, '%s/view' % project.slug)
        entry['upload_at_formated'] = babel.dates.format_datetime(
            project.upload_at, 'yyyy-MM-ddTHH:mm:ssZ', tzinfo = timezone('Europe/Paris'), locale = 'fr_FR')
        entries.append(entry)
    return templates.render(
        req.ctx,
        '/feed.mako',
        entries = entries,
        feed_url = 'http://localhost',
        feed_updated = babel.dates.format_datetime(
            datetime.datetime.utcnow(), 'yyyy-MM-ddTHH:mm:ssZ', tzinfo = timezone('Europe/Paris'), locale = 'fr_FR')
    )


@wsgify
def jobs(req):
    slug = req.urlvars.get('slug')

    # FIXME: should be done one time, when project is created
    project = Projects.find_one({'slug': slug})
    project.status = True
    project.step = 0
    project.save()

    return templates.render(
        req.ctx,
        '/jobs.mako',
        project = project
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
            project = Projects()
            project.filename = fs.filename
            project.status = False
            project_id = project.save(safe=True)

            # FIXME: check if upload folder exists
            f = open(os.path.join(req.ctx.conf['cache_dir'], 'upload', str(project_id)), 'w+')
            f.write(fs.file.read())
            f.close()

            result = [dict(
                id = str(project_id),
                name = project.filename,
                slug = project.slug,
                size = len(fs.file.read()),
                )]
        
    return wsgi_helpers.respond_json(req.ctx, {'files': result})


@wsgify
def remove(req):
    obj_id = req.GET['id']

    path = os.path.join(req.ctx.conf['cache_dir'], 'upload', obj_id)
    os.remove(path)

    project = Projects.find_one({'_id': bson.objectid.ObjectId(obj_id)})
    if project.status:
        # if status is True, remove request comes from projects page
        # a redirect to homepage is needed
        project.delete()
        return wsgi_helpers.redirect(req.ctx, location='/')
    else:
        # if status is False, project is not yet created
        # remove request comes from create page
        project.delete()


@wsgify
def index(req):
    projects = Projects.find()
    return templates.render(
        req.ctx,
        '/index.mako',
        projects = projects,
    )


def make_router():
    """Return a WSGI application that dispatches requests to controllers """
    return router.make_router(
        ('GET', '^/?$', index),
        ('GET', '^/projects/(?P<slug>.+)/jobs', jobs),
        ('GET', '^/projects/create', create),
        ('GET', '^/projects/feed', feed),
        ('GET', '^/projects/remove/?$', remove),
        ('POST', '^/projects/upload', upload),
    )
