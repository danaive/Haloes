$(document).ready(function() {
    $('#footer').css('background-color', '#f5f5f5');
    var docHeight = $(window).height();
    var footerHeight = $('#footer').height();
    var footerTop = $('#footer').position().top + footerHeight;
    if (footerTop < docHeight) {
        $('#footer').css('margin-top', (docHeight - footerTop) + 'px');
    }
});
