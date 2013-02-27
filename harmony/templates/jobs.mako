## -*- coding: utf-8 -*-


<%inherit file="/site.mako"/>


<%block name="css">
</%block>


<%block name="scripts">
</%block>


<%block name="container_content">

    <h1>Projet SIG</h1>
    <hr>
    <h3>Fichier ${job.filename}</h3>

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

    
</%block>
