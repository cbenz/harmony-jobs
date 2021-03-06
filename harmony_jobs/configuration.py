# -*- coding: utf-8 -*-


"""Paste INI configuration"""


import logging
import os
import urlparse

from biryani1 import strings
from biryani1.baseconv import (check, cleanup_line, default, function, guess_bool, input_to_int, noop, not_none, pipe,
        struct)


def load_configuration(global_conf, app_conf):
    """Build the application configuration dict."""
    app_dir = os.path.dirname(os.path.abspath(__file__))
    conf = {}
    conf.update(strings.deep_decode(global_conf))
    conf.update(strings.deep_decode(app_conf))
    conf.update(check(struct(
        {
            'app_conf': default(app_conf),
            'app_dir': default(app_dir),
            'app_name': default('Harmony Jobs'),
            'cache_dir': default(os.path.join(os.path.dirname(app_dir), 'cache')),
            'cdn.url': default('http://localhost:7000'),
            'custom_templates_dir': default(None),
            'database.host_name': default('localhost'),
            'database.name': default('harmony'),
            'database.port': pipe(input_to_int, default(27017)),
            'debug': pipe(guess_bool, default(False)),
            'global_conf': default(global_conf),
            'harmony_viewer.urls.base': pipe(cleanup_line, not_none),
            'log_level': pipe(
                default('WARNING'),
                function(lambda log_level: getattr(logging, log_level.upper())),
                ),
            'package_name': default('harmony-jobs'),
            'static_files': pipe(guess_bool, default(False)),
            'static_files_dir': default(os.path.join(app_dir, 'static')),
            'webrokeit.database.collections.states': default('states'),
            'webrokeit.database.collections.subscriptions': default('subscriptions'),
            'webrokeit.database.collections.tasks': default('tasks'),
            'webrokeit.database.host_name': default('localhost'),
            'webrokeit.database.name': default('webrokeit'),
            'webrokeit.database.port': pipe(input_to_int, default(27017)),
            'webrokeit.url.base': default('http;//localhost:8765'),
            'webrokeit.url.emit': default('http://localhost:8765/emit'),
        },
        default='drop',
        drop_none_values=False,
    ))(conf))

    # Assets
    conf.update(check(struct(
        {
            'cdn.bootstrap.css': default(
                urlparse.urljoin(conf['cdn.url'], '/bootstrap/2.2.2/css/bootstrap.min.css')
                ),
            'cdn.bootstrap.js': default(urlparse.urljoin(conf['cdn.url'], '/bootstrap/2.2.2/js/bootstrap.js')),
            'cdn.html5shiv.js': default(urlparse.urljoin(conf['cdn.url'], '/html5shiv/html5shiv.js')),
            'cdn.jquery.js': default(urlparse.urljoin(conf['cdn.url'], '/jquery/jquery-1.9.1.min.js')),
            'cdn.plupload.js': default(urlparse.urljoin(conf['cdn.url'], '/plupload/plupload.full.js')),
            'cdn.underscore.js': default(urlparse.urljoin(conf['cdn.url'], '/underscore/underscore.js')),
        },
        default=noop,
    ))(conf))
    return conf
