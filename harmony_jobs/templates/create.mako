## -*- coding: utf-8 -*-


<%inherit file="/site.mako"/>


<%block name="css">
</%block>


<%block name="scripts">
    <!-- Third party script for BrowserPlus runtime (Google Gears included in Gears runtime now) -->
    <script type="text/javascript" src="http://bp.yahooapis.com/2.4.21/browserplus-min.js"></script>
    <script type="text/javascript" src="${ctx.conf['cdn.plupload.js']}"></script>

    <script src="/js/upload.js"></script>
</%block>


<%block name="container_content">

    <h1>Create a project</h1>
    <hr>
    <h3>Upload your GIS file</h3>

    <div id="container-upload" class="well">

      <a class="btn btn-primary" id="pickfile" href="#">
        <i class="icon-plus icon-white"></i> Select a file
      </a>

      <a class="btn btn-primary" id="uploadfile" style="display: none" href="#">
        <i class="icon-arrow-up icon-white"></i> Start upload
      </a>

      <a class="btn btn-warning" id="cancelupload" style="display: none" href="#">
        <i class="icon-remove icon-white"></i> Cancel
      </a>

      <a class="btn btn-primary" id="create" style="display: none" href="">
        <i class="icon-play icon-white"></i> Create the project
      </a>

      <a class="btn btn-danger" id="removefile" style="display: none" href="#">
        <i class="icon-trash icon-white"></i> Delete the file
      </a>

      <table id="fileslist" class="table table-bordered" style="display: none">
        <thead>
          <tr>
            <th>File</th>
            <th>Status</th>
          </tr>
        </thead>
        <tbody></tbody>
      </table>

      <hr>
      <p>File must be an archive (compressed or not) of files in <strong><a href="http://fr.wikipedia.org/wiki/Shapefile">Shapefile</a></strong> format.</p>

    </div>
    
</%block>
