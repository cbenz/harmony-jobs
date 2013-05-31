## -*- coding: utf-8 -*-


<%inherit file="/site.mako"/>


<%block name="css">
</%block>


<%block name="scripts">
</%block>


<%block name="container_content">

  <div class="hero-unit">
    <h1>${ctx.conf['app_name']} <small>Easter-eggs</small></h1>
    <p class="muted">Technical support: <a href="mailto:support@easter-eggs.com">support@easter-eggs.com</a></p>
  </div>
  <div class="row-fluid">
    <div class="span4">
      <h4>Fast and Easy</h4>
      <p>Create your project in a few minutes simply by uploading a file</p>
    </div>
    <div class="span4">
      <h4>Compare your GIS with OpenStreetMap</h4>
      <p>
        glop
      </p>
    </div>
    <div class="span4">
      <h4>Reconcile your data</h4>
      <p>pas glop</p>
    </div>
  </div>

  <table id="projects" class="table table-bordered table-striped">
    <thead>
      <tr>
        <th>Last projects</th>
      </tr>
    </thead>
    <tbody>
% for project in projects:
    % if project.status == 'COMPLETE':
      <tr>
        <td><a href="/projects/${project.slug}">${project.slug}</a></td>
      </tr>
    % endif
% endfor
    </tbody>
  </table>

</%block>
