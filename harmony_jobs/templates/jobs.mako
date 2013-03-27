## -*- coding: utf-8 -*-


<%inherit file="/site.mako"/>


<%block name="css">
</%block>


<%block name="scripts">
</%block>


<%block name="container_content">

    <h1>Projet SIG</h1>
    <hr>
    <h3>Fichier ${project.filename}</h3>

    <table id="jobs" class="table table-bordered">
      <thead>
        <tr>
          <th>État</th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <td>
            Étape 1 / 10
            <div class="progress progress-striped active">
               <div class="bar" style="width:10%"></div>
             </div>
          </td>
        </tr>
      </tbody>
    </table>

    <a class="btn btn-danger" href="/projects/remove?id=${project._id}">
      <i class="icon-trash icon-white"></i> Supprimer le projet
    </a>

</%block>
