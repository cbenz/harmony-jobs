## -*- coding: utf-8 -*-


<%inherit file="/site.mako"/>


<%block name="css">
</%block>


<%block name="scripts">
    <script src="/js/status.js"></script>
</%block>


<%block name="container_content">

    <header>
      <div class="pull-right">
        <a class="btn btn-small btn-danger" href="/projects/remove?id=${project._id}">
          <i class="icon-trash icon-white"></i> Delete project
        </a>
      </div>
      <h1>GIS Project</h1>
    </header>

    <hr>
    <h3>File ${project.filename}</h3>

    <div id="progress" data-id="${project.slug}">
    </div>
</%block>


<%block name="progress">
    % if project.status == 'COMPLETE':
Completed <a href="#">View</a>
    % else:
<%
if counters.get('ERROR'):
    progress_bar_class = ' progress-danger'
elif counters.get('PENDING') or counters.get('RUNNING'):
    progress_bar_class = ' progress-info'
else:
    progress_bar_class = ' progress-success'
width = float(counters.get('COMPLETE', 0) + counters.get('ERROR', 0)) / tasks.count()
%>\
    Step ${counters.get('COMPLETE', 0) + counters.get('ERROR', 0)} / ${tasks.count()}
    <div class="progress${progress_bar_class} progress-striped">
      <div class="bar" style="width:${width * 100}%"></div>
    </div>
    <div class="pull-right">
      <button class="btn btn-primary" data-toggle="collapse" data-target="#detail">
        <i class="icon icon-${u'minus' if show else u'plus'} icon-white"></i> ${u'Less' if show else u'More'} detail
      </button>
    </div>
    <div id="detail" class="collapse${u' in' if show else u''}">
            % for task in tasks:
<%
if task['status'] == 'ERROR':
    alert_class = ' alert-error'
elif task['status'] == 'COMPLETE':
    alert_class = ' alert-success'
elif task['status'] == 'RUNNING':
    alert_class = ' alert-info'
else:
    alert_class = ''
%>\
        <div class="alert${alert_class}">
            <strong>${task['status']}</strong>
                % for key in ('event_name', 'function_name',):
            ${key} : ${task[key]}
                % endfor
        </div>
            % endfor
    </div>
    % endif
</%block>
