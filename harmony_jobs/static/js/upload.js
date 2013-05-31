
/*jslint nomen: true, unparam: true, regexp: true */
/*global $, window, document */

$(function () {
    'use strict';

    var fileslistItemTpl = _.template(
        '<tr id="<%= id %>"> \
           <td><%= name %> (<%= size %>)</td> \
           <td> \
             <div class="progress progress-striped active"> \
               <div class="bar"></div> \
             </div> \
           </td> \
         </tr>'
    );
    var fileslistErrorTpl = _.template(
        '<tr> \
           <td><%= name %> (<%= size %>)</td> \
           <td><span class="label label-important">Erreur: <%= code %></span> <%= message %></td> \
         </tr>'
    );

    var uploader = new plupload.Uploader({
	runtimes : 'html5,gears,flash,silverlight,browserplus',
	browse_button : 'pickfile',
	container : 'container-upload',
        multi_selection : false,
	max_file_size : '100mb',
	url : '/projects/upload',
	flash_swf_url : '/js/plupload/js/plupload.flash.swf',
	silverlight_xap_url : '/js/plupload/js/plupload.silverlight.xap',
	filters : [
	    {title : "Zip files", extensions : "zip"}
	]
    });

    var init = function() {
        // init buttons
        $('#pickfile').show();
        $('#uploadfile').hide();
	$('#cancelupload').hide();
	$('#removefile').hide();
        $('#create').hide();

        // init files list
        $('#fileslist tbody').empty();
        $('#fileslist').hide();
    };

    uploader.bind('Init', function(up, params) {
        init();
    });

    $('#uploadfile').click(function(e) {
	e.preventDefault();
	uploader.start();
    });
    $('#cancelupload').click(function(e) {
	e.preventDefault();
        var id = $('#fileslist tbody tr').attr('id');

        uploader.stop();
        uploader.removeFile(uploader.getFile(id));
        init();
    });
    $('#removefile').click(function(e) {
	e.preventDefault();
        var id = $('#fileslist tbody tr').data('id');

        $.ajax({
            url: "/projects/remove",
            data: {id: id}
        });
        init();
    });

    uploader.init();

    uploader.bind('FilesAdded', function(up, files) {
        // a file has been selected
	$.each(files, function(i, file) {
            $('#fileslist tbody').append(
                fileslistItemTpl({
                    id: file.id,
                    name: file.name,
                    size: plupload.formatSize(file.size)
                })
            );
	});

        // hide 'select' button, show 'upload' and 'cancel' button
        $('#pickfile').hide();
        $('#uploadfile').show();
	$('#cancelupload').show();

        $('#fileslist').show();

        // Reposition Flash/Silverlight
	up.refresh();
    });

    uploader.bind('UploadFile', function(up, file) {
        // file upload starts
        // hide 'upload' button
        $('#uploadfile').hide();
    });

    uploader.bind('UploadProgress', function(up, file) {
        $('#' + file.id + ' .bar').css('width', file.percent + '%');
    });

    uploader.bind('FileUploaded', function(up, file, response) {
        // file upload ends
        var resp = JSON.parse(response.response);
        var file_info = resp.files[0];

        // hide 'cancel' button and show 'remove' button
	$('#cancelupload').hide();
	$('#removefile').show();

        $('#' + file.id).data('id', file_info.id);
	$('#' + file.id + ' .bar').css('width', '100%');

        $('#fileslist tbody tr td:last').html('<span class="label label-success">Upload success</span> 100%');
        $('#create').show().attr('href', '/projects/' + file_info.slug);
    });

    uploader.bind('Error', function(up, err) {
        // file upload fails
        $('#fileslist tbody').empty();

        $('#fileslist').append(
            fileslistErrorTpl({
                code: err.code,
                message: err.message,
                size: err.file ? plupload.formatSize(err.file.size) : '',
                name: err.file ? err.file.name : ''
            })
        );

        // Reposition Flash/Silverlight
	up.refresh();
    });

});
