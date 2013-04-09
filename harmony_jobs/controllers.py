# -*- coding: utf-8 -*-


import babel.dates
import bson
import datetime
import formencode
import logging
import os
import simplejson as json
import urllib, urllib2
import urlparse
from pytz import timezone
from webob.dec import wsgify

from . import conv, router, templates, wsgi_helpers
from .model import Projects


log = logging.getLogger(os.path.basename(__file__))


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
def status(req):
    slug = req.urlvars.get('slug')

    project = Projects.find_one({'slug': slug})
    if not project.status:
        # should be done one time, when project is created
        project.status = 'PENDING'
        project.save()

        # Emit the shapefile:ready event
        event_parameters = {
            'file_path': os.path.join(req.ctx.conf['cache_dir'], 'upload', project.filename),
            'project_id': project.slug,
            }
        emit_url_data = {
            'event_name': 'shapefile:archive:ready',
            'event_parameters': json.dumps(event_parameters),
            }
        urllib2.urlopen(req.ctx.conf['webrokeit.urls.emit'], urllib.urlencode(emit_url_data))
        log.debug(u'Event "shapefile:archive:ready" emitted with parameters: {0}.'.format(event_parameters))

    return templates.render(
        req.ctx,
        '/status.mako',
        project = project
    )


@wsgify
def progress(req):
    slug = req.urlvars.get('slug')
    show, error = conv.guess_bool(req.GET.get('show', 'false'))

    project = Projects.find_one({'slug': slug})

    tasks_collection = req.ctx.db_webrokeit[req.ctx.conf['webrokeit.database.collections.tasks']]
    counters = {}
    for status in tasks_collection.distinct('status'):
        counters[status] = tasks_collection.find(
            {'event_parameters.project_id': project.slug, 'status': status}).count()

    tasks = tasks_collection.find({'event_parameters.project_id': project.slug}).sort([('date', -1)])

    if counters.get('COMPLETE', 0) == tasks.count():
        project.status = 'COMPLETE'
        project.save()
    elif counters.get('ERROR', 0) > 0:
        project.status = 'ERROR'
        project.save()
    elif counters.get('RUNNING', 0) > 0:
        project.status = 'RUNNING'
        project.save()

    html = templates.render_def(
        req.ctx,
        '/status.mako',
        'progress',
        counters = counters,
        project = project,
        show = show,
        tasks = tasks_collection.find({'event_parameters.project_id': project.slug}).sort([('date', -1)])
    )

    return wsgi_helpers.respond_json(req.ctx, {'html': html, 'done': counters.get('PENDING', 0) == 0})


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
            project.filename = fs.filename # temporary filename used to compute slug, will be changed below
            project_id = project.save(safe=True)

            upload_dir = os.path.join(req.ctx.conf['cache_dir'], 'upload')
            if (not os.path.exists(upload_dir)):
                os.mkdir(upload_dir)

            # concat mongodb _id and uploaded file's name to compute a new unique filename
            filename = '%s-%s' % (project_id, fs.filename)
            f = open(os.path.join(upload_dir, filename), 'w+')
            f.write(fs.file.read())
            f.close()

            # update filename
            project.filename = filename
            project.save(safe=True)

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
    project = Projects.find_one({'_id': bson.objectid.ObjectId(obj_id)})

    path = os.path.join(req.ctx.conf['cache_dir'], 'upload', project.filename)
    os.remove(path)

    if project.status is not None:
        # if status is not None, remove request comes from projects page
        # a redirect to homepage is needed
        project.delete()
        return wsgi_helpers.redirect(req.ctx, location='/')
    else:
        # if status is None, project is not yet created
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
        ('GET', '^/projects/(?P<slug>.+)/status', status),
        ('GET', '^/projects/(?P<slug>.+)/progress', progress),
        ('GET', '^/projects/create', create),
        ('GET', '^/projects/feed', feed),
        ('GET', '^/projects/remove/?$', remove),
        ('POST', '^/projects/upload', upload),
    )
