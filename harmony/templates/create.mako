## -*- coding: utf-8 -*-


<%inherit file="/site.mako"/>


<%block name="css">
</%block>


<%block name="scripts">
    <!-- Third party script for BrowserPlus runtime (Google Gears included in Gears runtime now) -->
    <script type="text/javascript" src="http://bp.yahooapis.com/2.4.21/browserplus-min.js"></script>
    <script type="text/javascript" src="/js/plupload/js/plupload.full.js"></script>

    <script src="/js/app.js"></script>
</%block>


<%block name="container_content">

    <h1>Creation d'un projet</h1>
    <hr>
    <h3>Téléversement d'un fichier SIG</h3>

    <div id="container-upload" class="well">

      <a class="btn btn-primary" id="pickfile" href="#">
        <i class="icon-plus icon-white"></i> Choisir un fichier
      </a>

      <a class="btn btn-primary" id="uploadfile" style="display: none" href="#">
        <i class="icon-arrow-up icon-white"></i> Téléverser le fichier
      </a>

      <a class="btn btn-warning" id="cancelupload" style="display: none" href="#">
        <i class="icon-remove icon-white"></i> Annuler
      </a>

      <a class="btn btn-danger" id="removefile" style="display: none" href="#">
        <i class="icon-trash icon-white"></i> Supprimer le fichier
      </a>

      <a class="btn btn-primary" id="create" style="display: none" href="">
        <i class="icon-play icon-white"></i> Créer le projet
      </a>

      <table id="fileslist" class="table table-bordered" style="display: none">
        <thead>
          <tr>
            <th>Fichier</th>
            <th>État</th>
          </tr>
        </thead>
        <tbody></tbody>
      </table>

      <hr>
      <p>Le fichier doit être une archive (compressée ou non) de fichiers au format <strong><a href="http://fr.wikipedia.org/wiki/Shapefile">Shapefile</a></strong>.</p>

    </div>
    
</%block>
