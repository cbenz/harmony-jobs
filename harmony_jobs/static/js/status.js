
/*jslint nomen: true, unparam: true, regexp: true */
/*global $, window, document */

$(function () {
    'use strict';

    var el = $('#progress');
    var id = el.data('id');

    var progressInterval = setInterval(function() {
        var show = $('#detail').hasClass('in');
        $.ajax({
            url: '/projects/' + id + '/progress',
            data: {show: $('#detail').hasClass('in')}
        }).done(function(data) {
            el.html(data['html']);
            $('#detail').on('show', function() {
                el.find('button').html('<i class="icon icon-minus icon-white"></i> Less detail');
            });
            $('#detail').on('hide', function() {
                el.find('button').html('<i class="icon icon-plus icon-white"></i> More detail');
            });
            if (data['done']) {
                clearInterval(progressInterval);
            }
        });
    }, 2500);
});
