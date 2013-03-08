## -*- coding: utf-8 -*-


<%inherit file="/site.mako"/>


<%block name="css">
</%block>


<%block name="scripts">
</%block>


<%block name="container_content">

  <div class="hero-unit">
    <h1>${ctx.conf['app_name']} <small>Easter-eggs</small></h1>
    <p class="muted">Support technique : <a href="mailto:support@easter-eggs.com">support@easter-eggs.com</a></p>
  </div>
  <div class="row-fluid">
    <div class="span4">
      <h4>Simple et rapide</h4>
      <p>Créer votre projet en quelque que minutes un téléversant simplement un fichier</p>
    </div>
    <div class="span4">
      <h4>Comparer votre SIG avec OpenStreetMap</h4>
      <p>
        glop
      </p>
    </div>
    <div class="span4">
      <h4>Reconsilier les données</h4>
      <p>pas glop</p>
    </div>
  </div>

  <table id="jobs" class="table table-bordered table-striped">
    <thead>
      <tr>
        <th>Derniers projets</th>
      </tr>
    </thead>
    <tbody>
% for job in jobs:
      <tr>
        <td>
          Étape 1 / 10
          <div class="progress progress-striped">
            <div class="bar" style="width:10%"></div>
          </div>
        </td>
      </tr>
% endfor
    </tbody>
  </table>

</%block>
